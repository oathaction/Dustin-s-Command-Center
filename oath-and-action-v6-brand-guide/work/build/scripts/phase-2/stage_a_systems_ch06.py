"""Chapter 06 Type: copy, rules and specimens (stage board A, systems designer, November 6, 2026).

Characters per line, word-space widths, the width of a heading in its fallback face and the hang of an opening
quotation mark are measured in Chromium with the Google Fonts files the guide page loads (stage_a_systems_capture.js).
"""
import json
import re
import sys

C = sys.modules['stage_a_systems_core']
B = sys.modules['stage_a_systems_build']

# Sample text for measures (D2-248): real Oath & Action copy whose terms are all plain, the first paragraph of chapter
# 02's writing section (approved on Board 5). It quotes the tagline and W02's rewrite word for word.
SAMPLE = ('Our tagline is “A country that answers to its people.” People can hold an office to account once they know which '
          'office decided. So we name who acts, in words you would use at a kitchen table, as in “A regulator or a board '
          'approves your rate.”')
TAGLINE = 'A country that answers to its people.'
DRAFT_H3 = -0.03      # the H3 tracking in the first build of this guide, before DR-95
V5_TRACK = -0.045     # our fifth edition's tracking at every heading size
HEAD = 'Who decides what happens next?'            # our fifth edition's type chapter, its H2 sample line
PLATE_HEAD = 'Tighten tracking only as headings grow.'   # Rule 06.4's own title, set at the H3 ceiling
BAL = 'What a primary decides, and who may vote in it'   # our fifth edition's balanced-heading sample
COMMIT = 'Clarity is our duty. Action is our promise.'   # locked editorial commitment (Master Brief section 3)
W02 = 'A regulator or a board approves your rate.'       # chapter 02, W02's rewrite of an Atlas V7 everyday answer

STYLES = [
    ('title', 'Title', 'Edition 06'),
    ('section', 'Section', '05 Color'),
    ('h3', 'H3', 'Set text only on color pairs that pass.'),
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


def track(ctx, name):
    return ctx.T.ext(f'oa.type.{name}').get('trackingEm', 0)


def pct(tr):
    """Tracking in em as the guide prints it: −1 percent, +6 percent, 0."""
    if not tr:
        return '0'
    return f'{C.MINUS if tr < 0 else "+"}{abs(tr) * 100:g} percent'


def probes(ctx):
    body = 'font:var(--oa-type-body)'
    ctx.probe('cpl body ideal', 'cpl', text=SAMPLE, css=f'{body};width:var(--oa-layout-measure-body-ideal)')
    ctx.probe('cpl body max', 'cpl', text=SAMPLE, css=f'{body};width:var(--oa-layout-measure-body-max)')
    ctx.probe('cpl long sample ideal', 'cpl', text=long_sample(), css=f'{body};width:var(--oa-layout-measure-body-ideal)')
    ctx.probe('cpl long sample max', 'cpl', text=long_sample(), css=f'{body};width:var(--oa-layout-measure-body-max)')
    ctx.probe('cpl intro max', 'cpl', text=long_sample(), css='font:var(--oa-type-intro);font-size:1.375rem;width:var(--oa-layout-measure-intro-max)')
    ctx.probe('cpl v5 intro 65ch', 'cpl', text=SAMPLE, css='font:var(--oa-type-intro);font-size:1.375rem;width:65ch')
    ctx.probe('width v5 intro 65ch', 'width', text='0', css='font:var(--oa-type-intro);font-size:1.375rem;display:block;width:65ch')
    # Rule 06.4: word spaces and touching letter pairs at the token tracking (DR-95) and at the earlier values
    h3 = track(ctx, 'h3')
    for name, tr in (('h3 0', 0), ('h3 token', h3), ('h3 draft', DRAFT_H3)):
        ctx.probe(f'space {name}', 'space', css=f'font:var(--oa-type-h3);font-size:2rem;letter-spacing:{tr}em')
    for name, tr in (('0', 0), ('token', h3), ('draft', DRAFT_H3)):
        ctx.probe(f'pairs plate {name}', 'pairs', text=PLATE_HEAD, family='Inter Tight', weight=800, size=32, track=tr)
    for name, tr in (('0', 0), ('token', track(ctx, 'title')), ('v5', V5_TRACK)):
        ctx.probe(f'pairs tagline {name}', 'pairs', text=TAGLINE, family='Inter Tight', weight=800, size=110, track=tr)
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
            f'<span class="u">Download the lockmark</span><span class="l">Explainer · Local utilities</span>'
            f'<p class="t">Body text, buttons, labels, captions, tables and chart text</p></div>'
            f'<div><p class="k">Lora Italic 400 · quotation</p><p class="q">“{COMMIT}”</p>'
            f'<p class="t">Only words we quote: pull quotes and quote cards</p></div></div>')
    ctx.spec('s-06-1-correct', html, '06', '06.1',
             f'The three faces at true size. Inter Tight 800 sets the heading {HEAD} Inter sets the sentence {W02}, a button '
             f'labeled Download the lockmark and the kicker Explainer, Local utilities, in capitals. Lora Italic sets our '
             f'editorial commitment, “{COMMIT}”',
             notes='The heading line is our fifth edition’s type sample; the body line is chapter 02’s W02 rewrite.')
    cssf = (f'.d{{margin:0;{ctx.ty("h3")};font-family:var(--oa-font-family-quote);font-style:italic;font-weight:var(--oa-font-weight-regular);text-wrap:balance}}'
            f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}.b{{margin:12px 0 0;{ctx.ty("body")}}}')
    htmlf = (f'<style>{cssf}</style><p class="k">Explainer · Local utilities</p><p class="d">{HEAD}</p>'
             f'<p class="b">{W02}</p>')
    ctx.spec('s-06-1-failure', htmlf, '06', '06.1',
             f'The heading {HEAD} set in Lora Italic above the sentence {W02}, so the heading looks like a quotation.',
             notes='A labeled failure: the face does a job that is not its own.')


def style_spec(ctx, key):
    """Face, weight, web size, line height, tracking and extras for one style, read from tokens.json."""
    T = ctx.T
    node = T.node(f'oa.type.{key}')
    ext = T.ext(f'oa.type.{key}')
    val = node['$value']
    fam = T.value(val['fontFamily'][1:-1])[0] if isinstance(val['fontFamily'], str) else val['fontFamily'][0]
    wt = T.value(val['fontWeight'][1:-1]) if isinstance(val['fontWeight'], str) else val['fontWeight']
    lh = val['lineHeight']
    tr = ext.get('trackingEm', 0)
    lo, hi = ctx.fixed_px(key)
    size = (f'{lo:g} to {hi:g} px ({lo / 16:g} to {hi / 16:g} rem)' if hi != lo else f'{lo:g} px ({lo / 16:g} rem)')
    face = fam + (' Italic' if key == 'quote' else '')
    trk = 'tracking 0' if not tr else f'tracking {C.MINUS if tr < 0 else "+"}{abs(tr) * 100:g}%'
    extra = []
    if ext.get('numeric'):
        extra.append('tabular figures')
    if ext.get('textTransform') == 'uppercase':
        extra.append('capitals')
    return f'{face} {wt} · {size} · line height {lh:g} · {trk}' + (' · ' + ', '.join(extra) if extra else ''), lo, hi


def s_06_2(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    rows = []
    for key, name, sample in STYLES:
        spec, lo, hi = style_spec(ctx, key)
        ctx.fig(f'type scale {key}', spec, 'tokens.json oa.type')
        rows.append(f'<li><p class="nm">{name}<code>{C.css_name("oa.type." + key)}</code></p><p class="sp">{spec}</p>'
                    f'<p class="smp" style="{ctx.ty(key)}">{sample}</p></li>')
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
             'height and tracking, and a sample line in the style. On a phone each sample shows the style’s phone floor, '
             'and on a wider screen its desktop ceiling.', readable=True,
             notes='A readable list (D2-255). Every spec line is read from tokens.json; every sample uses the token’s CSS '
                   'custom properties at a fixed size from D2-254.')

    # the fixed-artboard column (D2-254), as its own readable table
    trs = []
    for key, name, _ in STYLES:
        _, lo, hi = style_spec(ctx, key)
        web = f'{lo:g} to {hi:g} px' if hi != lo else f'{lo:g} px'
        trs.append(f'<tr><th scope="row">{name}</th><td>{web}</td><td>{lo:g} px</td><td>{hi:g} px</td></tr>')
    cssa = (f'table{{width:100%;max-width:40rem;border-collapse:collapse;{ctx.ty("bodySmall")}}}'
            f'th,td{{text-align:left;padding:8px 16px 8px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")};vertical-align:baseline}}'
            f'thead th{{{ctx.ty("label")};border-bottom-color:{v("oa.color.border.strong.onNewsprint")}}}'
            f'tbody th{{{ctx.ty("ui")}}}td{{font-variant-numeric:tabular-nums}}'
            f'@container (max-width:30rem){{thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}'
            f'table,tbody,tr,th,td{{display:block}}tr{{padding:8px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
            f'th,td{{border:0;padding:0}}td::before{{content:attr(data-k) ": ";color:{sec}}}}}.wr{{container-type:inline-size}}')
    heads = ['On a web page', 'Artboards up to 600 px', 'Artboards 1,200 px and up']
    out = []
    for r in trs:
        cells = r.split('<td>')
        out.append(cells[0] + ''.join(f'<td data-k="{heads[i]}">' + c for i, c in enumerate(cells[1:])))
    htmla = (f'<style>{cssa}</style><div class="wr"><table role="table"><thead><tr><th scope="col">Style</th>'
             + ''.join(f'<th scope="col">{h}</th>' for h in heads) + f'</tr></thead><tbody>{"".join(out)}</tbody></table></div>')
    ctx.spec('s-06-artboards', htmla, '06', None,
             'A table of the fourteen styles with three sizes each: on a web page, on an artboard up to 600 px wide and on '
             'an artboard 1,200 px wide or more. ' + '; '.join(
                 f'{name} {style_spec(ctx, key)[1]:g} and {style_spec(ctx, key)[2]:g} px' for key, name, _ in STYLES) + '.',
             readable=True, notes='The fixed-artboard column of Rule 06.2 (D2-254), read from tokens.json and checked '
                                  'against the decision\'s list.')

    # failure: what 200 percent text does to px and rem
    cssf = (f'.pr{{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr))}}'
            f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
            f'.r{{margin:0;font-family:var(--oa-font-family-reading);font-size:2.125rem;line-height:1.6}}'
            f'.p{{margin:0;font-family:var(--oa-font-family-reading);font-size:1.0625rem;line-height:1.6}}')
    htmlf = (f'<style>{cssf}</style><div class="pr"><div><p class="k">Set in rem, at 34 px</p><p class="r">{W02}</p></div>'
             f'<div><p class="k">Set in px, still 17 px</p><p class="p">{W02}</p></div></div>')
    ctx.spec('s-06-2-failure', htmlf, '06', '06.2',
             f'Two columns showing the sentence {W02} as a reader sees it with text set to 200 percent: on the left, set in '
             f'rem, it has grown to 34 px; on the right, set in px, it is still 17 px.', exempt=['scale'],
             notes='A depiction: both columns are drawn at the sizes a 200 percent text setting produces, since the guide '
                   'page itself runs at the reader’s own setting. Exempt from the scale check: 34 px is the body size '
                   'doubled, off the scale on purpose in a labeled failure.')


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
    htmlf = (f'<style>{cssf}</style><div class="v"><div><p class="e">06 / Type</p><p class="n">Kicker: 11 px, Inter 700, '
             f'13 percent tracking</p></div><div><p class="f">OATH &amp; ACTION · Type / 06</p><p class="n">Footer line: 10 px, '
             f'Inter 400</p></div></div>')
    ctx.spec('s-06-3-failure', htmlf, '06', '06.3',
             'A graphic at true size of two labels from our fifth edition: the kicker 06 / Type at 11 px in capitals with '
             'wide tracking, and the footer line Oath & Action, Type / 06 at 10 px.', exempt=['size', 'scale'],
             notes='Sizes and tracking from the V5 text census (eyebrow 11 px, 700, 1.43 px tracking; footer 10 px). A '
                   'historical record in a labeled failure, so its sizes sit off the scale on purpose.')


def s_06_4(ctx):
    v = ctx.v
    sec = v('oa.color.text.secondary.onNewsprint')
    h3 = track(ctx, 'h3')
    out = {}
    for sid, tr, which in (('s-06-4-correct', h3, 'token'), ('s-06-4-failure', DRAFT_H3, 'draft')):
        sp = (ctx.m(f'space h3 {which}') or {}).get('width') or 0
        pr = ctx.m(f'pairs plate {which}') or {'pairs': 0, 'touching': 0, 'which': []}
        out[which] = (sp, pr)
        css = (f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}'
               f'.h{{margin:0;{ctx.ty("h3", "ceil")};letter-spacing:{tr}em;text-wrap:balance}}'
               f'.m{{margin:12px 0 0;{ctx.ty("dataLabel")};color:{sec}}}')
        lab = f'H3 at 32 px, {pct(tr)} tracking'
        meas = f'Word space {sp:.1f} px · {pr["touching"]} of {pr["pairs"]} letter pairs touch'
        html = f'<style>{css}</style><p class="k">{lab}</p><p class="h">{PLATE_HEAD}</p><p class="m">{meas}</p>'
        ctx.spec(sid, html, '06', '06.4',
                 f'The heading {PLATE_HEAD} in Inter Tight 800 at 32 px with {pct(tr).replace(C.MINUS, "minus ")} '
                 f'tracking. A line below it reads: word space {sp:.1f} px, {pr["touching"]} of {pr["pairs"]} letter pairs '
                 f'touch.',
                 notes='Set at 32 px, the H3 ceiling. Word space and touching pairs measured in Chromium with the Google '
                       'Fonts files the page loads, at this tracking.')
    return out


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
             f'right and the true minus sign. {vals}. Source line below.', readable=True,
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
        html = f'<style>{css}</style><p class="k">Explainer · Primaries</p><p class="h">{text}</p>'
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
    ctx.spec('s-06-8-correct', f'<style>{css}</style><p class="k">Body, 17 px, at the body measure</p><p class="b">{SAMPLE}</p>',
             '06', '06.8', f'A paragraph in Inter at 17 px set to the body measure of 33.88 rem: {SAMPLE}',
             notes='The paragraph is the opening of chapter 02’s writing section, whose terms are all plain (D2-248).')
    w = ctx.m('width v5 intro 65ch')
    wpx = round(w['width']) if w else 880
    cssf = (f'.k{{margin:0 0 12px;{ctx.ty("label")};color:{sec}}}'
            f'.b{{margin:0;font:var(--oa-type-intro);font-size:1.375rem;width:65ch;max-width:none}}')
    ctx.spec('s-06-8-failure', f'<style>{cssf}</style><p class="k">Intro, 22 px, at 65ch</p><p class="b">{SAMPLE}</p>',
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
               f'.mh .illus{{margin:0;font-family:var(--oa-font-family-email-sans)}}'
               f'.h{{margin:24px 0 0;font-family:{hfam};font-weight:700;font-size:1.625rem;line-height:1.08}}'
               f'.b{{margin:16px 0 0;font-family:var(--oa-font-family-email-sans);font-size:1.0625rem;line-height:1.6}}'
               f'.q{{margin:24px 0 0;font-family:var(--oa-font-family-email-quote);font-style:italic;font-size:1.5rem;line-height:1.3}}')
        html = (f'<style>{css}</style><div class="em"><div class="mh">'
                f'<img data-inline src="work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg" width="152" height="16" alt="" data-red="signature">'
                f'{B.ILLUS}</div>'
                f'<p class="h">The school board votes on the new bell schedule April 14.</p>'
                f'<p class="b">Sign up with the board clerk by April 10 to speak before the vote.</p>'
                f'<p class="q">“{COMMIT}”</p></div>')
        ctx.spec(sid, html, '06', '06.9',
                 ('An Illustrative email header at 600 px on White, set in the system stack: the wordmark, the headline The '
                  'school board votes on the new bell schedule April 14 in Helvetica or Arial bold at 26 px, a sentence of '
                  'body text, and our editorial commitment in Georgia Italic at 24 px.') if good else
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
        css = (f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{sec}}}.h{{margin:0;{ctx.ty("h3", "ceil")};{fam}text-wrap:balance}}'
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
    p64 = s_06_4(ctx)
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
    li = cpl('cpl long sample ideal')
    lm = cpl('cpl long sample max')
    v5 = cpl('cpl v5 intro 65ch')
    im = cpl('cpl intro max')
    wi = ms(ctx, 'width head inter tight').get('width') or 1
    wa = ms(ctx, 'width head arial').get('width') or 1
    wider = (wa / wi - 1) * 100
    ctx.fig('Arial over Inter Tight width, percent', f'{wider:.1f}', 'rendered width of the heading at 32 px')

    # Rule 06.4: tracking from tokens.json, checked against DR-95, and what it does at each size
    trk = {k: track(ctx, k) for k in ('title', 'section', 'h3', 'h4', 'figure', 'quote', 'label')}
    off = {k: (trk[k], want) for k, want in B.TRACKING_DR95.items() if abs(trk[k] - want) > 1e-9}
    if off:
        msg = f'display tracking in tokens.json is not yet DR-95: {off}'
        if ctx.stage == 'final' and not getattr(ctx, 'allow_old_tracking', False):
            raise ValueError(msg)
        print('warning:', msg)
    sp0 = (ms(ctx, 'space h3 0').get('width') or 0)
    sp_tok, pr_tok = p64['token']
    sp_dr, pr_dr = p64['draft']
    tg = {k: ms(ctx, f'pairs tagline {k}') for k in ('0', 'token', 'v5')}
    tt = {k: ms(ctx, f'pairs titles {k}') for k in ('0', 'token', 'draft')}
    for k, val in (('space h3 0 px', sp0), ('space h3 token px', sp_tok), ('space h3 draft px', sp_dr)):
        ctx.fig(k, f'{val:.2f}', 'width("n n") minus width("nn") in Inter Tight 800 at 32 px, Chromium')
    for k, r in [(f'pairs tagline {k}', tg[k]) for k in tg] + [(f'pairs titles {k}', tt[k]) for k in tt] + \
            [('pairs plate token', pr_tok), ('pairs plate draft', pr_dr)]:
        if r:
            ctx.fig(f'{k}, touching', f'{r.get("touching")} of {r.get("pairs")}: {" ".join(r.get("which", []))}',
                    f'canvas at twice size, Inter Tight 800 at {r.get("size_px")} px, tracking {r.get("track_em")} em, '
                    f'with kerning; a pair touches when no white device pixel separates the two glyphs')
    n_titles = (tt['token'] or {}).get('titles') or 0
    all_r = bool(pr_tok.get('which')) and all('r' in w for w in pr_tok.get('which', []))
    tok_r = tt['token'].get('which', []) if tt['token'] else []
    tok_all_r = bool(tok_r) and all('r' in w for w in tok_r)

    phone = ctx.R.get('cpl span phone 4') or {}
    phone_s = ctx.R.get('cpl span phoneSmall 4') or {}
    ph_lo = round(min(phone_s.get('mean', 0), phone.get('mean', 0)))
    ph_hi = round(max(phone_s.get('mean', 0), phone.get('mean', 0)))
    sec = 'oa.color.text.secondary.onNewsprint'
    ch_n = ctx.ratio('oa.color.text.primary.onNewsprint', 'oa.color.surface.newsprint')
    lab_r = ctx.ratio(sec, 'oa.color.surface.newsprint')
    fonts = ctx.R.get('font check', {})
    fl = {k: ctx.fixed_px(k) for k in B.FLUID}
    floor_list = ', '.join(f'{n} {B.ARTBOARD_FLOOR[k]}' for k, n in (
        ('title', 'title'), ('section', 'section'), ('figure', 'figure'), ('h3', 'H3'), ('h4', 'H4'), ('quote', 'quote'),
        ('intro', 'intro'), ('ask', 'ask'), ('body', 'body'), ('bodySmall', 'body small'), ('ui', 'UI'),
        ('caption', 'caption'), ('label', 'label'), ('dataLabel', 'data label'))) + ' px'
    ceil_list = ', '.join(f'{n} {B.ARTBOARD_CEIL[k]}' for k, n in (
        ('title', 'title'), ('section', 'section'), ('figure', 'figure'), ('h3', 'H3'), ('h4', 'H4'), ('quote', 'quote'),
        ('intro', 'intro'))) + ' px; the rest as on phones'
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
                'id': '06.1', 'title': 'Keep each typeface to its one job.',
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
                        'basis': 'Our locked identity rules; design judgment'},
                'correct': {'specimen': 's-06-1-correct',
                            'caption': 'The three faces at true size, each in its job: a heading in Inter Tight 800, a '
                                       'sentence, a button and a kicker in Inter, and our editorial commitment quoted in Lora '
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
                'id': '06.2', 'title': 'Take every size from the type scale.',
                'rule': ['Set text in the fourteen styles of the scale, with no sizes between them. On a web page, display '
                         'styles grow with the window from 390 to 1440 px wide, and every size is in rem so it follows the '
                         'reader’s text setting. A fixed artboard, such as a card, an email or a social image, takes fixed '
                         'sizes from the same scale: up to 600 px wide, each style’s phone floor, and from 1,200 px wide, its '
                         'desktop ceiling. Print pieces set type in points.'],
                'tokens': [f'oa.type.{k}' for k, _, _ in STYLES],
                'why': {'text': ['WCAG 2.2 success criterion 1.4.4 Resize Text asks that text grow to 200 percent with '
                                 'nothing lost. A size in rem grows with the reader’s text setting, which a size fixed in px '
                                 'ignores. Our fifth edition set every size in px, and when our audit doubled its root text '
                                 'size, no text on the page grew.',
                                 'A card or an email has one width, so the window cannot pick its sizes. Taking them from the '
                                 'scale’s two ends keeps a 480 px card and a 1,200 px social image in the same family as the '
                                 'page around them.'],
                        'basis': 'WCAG 2.2 SC 1.4.4; design judgment'},
                'correct': {'specimen': 's-06-2-correct',
                            'caption': 'The fourteen styles at true size. On a phone each sample shows its phone floor, the '
                                       'size an artboard up to 600 px wide takes, and on a wider screen its desktop ceiling, '
                                       'the size for artboards 1,200 px and wider. On a web page, display styles move between '
                                       'the two as the window grows.'},
                'failure': {'specimen': 's-06-2-failure',
                            'caption': '<strong>Fails 1.4.4.</strong> Two columns as a reader sees them with text set to 200 '
                                       'percent. The column set in rem has grown to 34 px; the column set in px is still 17 px.'},
                'specs': [
                    {'label': 'Text size base', 'value': '16 px, the browser default; every size is a multiple in rem', 'token': None},
                    {'label': 'On a web page', 'value': 'Display sizes grow from 390 px to 1440 px wide', 'token': 'oa.type.title'},
                    {'label': 'Artboards up to 600 px wide', 'value': f'Each style’s phone floor: {floor_list}', 'token': None},
                    {'label': 'Artboards 1,200 px and wider', 'value': f'Each style’s desktop ceiling: {ceil_list}', 'token': None},
                    {'label': 'Artboards between 600 and 1,200 px', 'value': 'Each style’s size from either column', 'token': None},
                    {'label': 'Print', 'value': 'Points, with all text at 10 pt or larger; chapter 25 sets the point scale', 'token': None},
                    {'label': 'Body', 'value': 'Inter 400, 17 px (1.0625 rem), line height 1.6', 'token': 'oa.type.body'},
                ],
                'related': ['07', '19', '25'],
                'builders': ['Set a style with its shorthand and its parts: <code>font: var(--oa-type-body)</code> carries '
                             'face, weight, size and line height, and <code>letter-spacing</code>, '
                             '<code>text-transform</code> and <code>font-variant-numeric</code> each have their own property, '
                             'such as <code>--oa-type-label-letter-spacing</code>. On a fixed artboard, override only the '
                             'size, as in <code>font-size: 1.625rem</code> for an H3 on a 480 px card. Never write a font '
                             'size in px.'],
            },
            {
                'id': '06.3', 'title': 'Set no text on screen below 13 px.',
                'rule': ['The smallest text on screen is 13 px, or 0.8125 rem: labels, tags and data labels. A label in '
                         'capitals at 13 px takes Inter 700 with 6 percent tracking. A specimen that shows a mark or a minimum '
                         'size at true size is a graphic, and its caption says so.'],
                'tokens': ['oa.type.label', 'oa.type.dataLabel', 'oa.type.caption'],
                'why': {'text': ['Our fifth edition set its labels at 10 to 12 px. Our census of its text, which measured '
                                 '2,346 text elements rendered at 1440 px and left out text inside SVG drawings, counted 833 '
                                 'under 13 px. A floor with no screen exceptions keeps kickers, tags and navigation readable '
                                 'without zoom. At 13 px, capitals need less tracking than they did at 10 px, so 6 percent '
                                 'keeps them open without pulling a word apart.'],
                        'basis': 'Design judgment; our measurements of the fifth edition, October 2026'},
                'correct': {'specimen': 's-06-3-correct',
                            'caption': f'Four labels at true size, all at 13 px. The location line is secondary text at '
                                       f'{lab_r} to 1; the column head, tag and data label are primary text at {ch_n} to 1.'},
                'failure': {'specimen': 's-06-3-failure',
                            'caption': '<strong>Fails the 13 px floor.</strong> A graphic at true size of two labels from our '
                                       'fifth edition: the chapter kicker at 11 px with 13 percent tracking, and the footer '
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
                'id': '06.4', 'title': 'Tighten tracking only as headings grow.',
                'rule': [f'Tracking is the space added to or taken from every pair of letters. Display styles take negative '
                         f'tracking that eases as the size drops: {pct(trk["title"])} for titles, {pct(trk["section"])} for '
                         f'sections, {pct(trk["h3"])} for H3 and {pct(trk["h4"])} for H4. Big figures, which are digits, '
                         f'take {pct(trk["figure"])}, and quotes in Lora Italic {pct(trk["quote"])}. Reading styles keep the '
                         f'font’s own spacing, and labels in capitals open to {pct(trk["label"])}.'],
                'tokens': ['oa.type.title', 'oa.type.section', 'oa.type.h3', 'oa.type.h4', 'oa.type.figure', 'oa.type.label'],
                'why': {'text': [f'At display sizes the font’s own spacing leaves gaps a reader sees, and a little negative '
                                 f'tracking closes them. Pulled too far, the letters touch. Our fifth edition used '
                                 f'{pct(V5_TRACK)} at every heading size from 24 to 110 px, and at the cover’s 110 px that '
                                 f'makes {tg["v5"].get("touching", 0)} of our tagline’s {tg["v5"].get("pairs", 0)} letter pairs '
                                 f'touch. At the title’s {pct(trk["title"])}, {C.num(tg["token"].get("touching", 0))} do.',
                                 f'Across the {n_titles} rule titles in chapters 05 to 07, set at the H3 size of 32 px, '
                                 f'{tt["draft"].get("touching", 0)} of {tt["draft"].get("pairs", 0)} letter pairs touch at '
                                 f'{pct(DRAFT_H3)}, the value an early draft of this guide used, and '
                                 f'{tt["token"].get("touching", 0)} at {pct(trk["h3"])}'
                                 + (', each where the arm of an r meets its neighbor.' if tok_all_r else '.')],
                        'basis': 'Our measurements, November 2026; design judgment'},
                'correct': {'specimen': 's-06-4-correct',
                            'caption': f'An H3 at true size, 32 px with {pct(trk["h3"])} tracking. Its word spaces measure '
                                       f'{sp_tok:.1f} px, and {C.num(pr_tok.get("touching", 0))} of its {pr_tok.get("pairs", 0)} '
                                       f'letter pairs touch'
                                       + (', where the arm of an r meets its neighbor.' if all_r else '.')},
                'failure': {'specimen': 's-06-4-failure',
                            'caption': f'<strong>Fails the tracking scale.</strong> The same heading at {pct(DRAFT_H3)}, the '
                                       f'H3 value in an early draft of this guide. {C.num(pr_dr.get("touching", 0)).capitalize()} of its '
                                       f'{pr_dr.get("pairs", 0)} letter pairs touch, and its word spaces shrink to '
                                       f'{sp_dr:.1f} px.'},
                'specs': [
                    {'label': 'Title', 'value': f'{pct(trk["title"])} ({trk["title"]:g} em)'.replace('-', C.MINUS), 'token': 'oa.type.title'},
                    {'label': 'Section', 'value': pct(trk['section']), 'token': 'oa.type.section'},
                    {'label': 'H3', 'value': pct(trk['h3']), 'token': 'oa.type.h3'},
                    {'label': 'H4', 'value': pct(trk['h4']), 'token': 'oa.type.h4'},
                    {'label': 'Big figures', 'value': pct(trk['figure']), 'token': 'oa.type.figure'},
                    {'label': 'Quote', 'value': pct(trk['quote']), 'token': 'oa.type.quote'},
                    {'label': 'Reading styles', 'value': '0, the font’s own spacing', 'token': 'oa.type.body'},
                    {'label': 'Label', 'value': pct(trk['label']), 'token': 'oa.type.label'},
                    {'label': 'Letter pairs that touch, tagline at 110 px', 'value': f'{tg["token"].get("touching", 0)} of {tg["token"].get("pairs", 0)} at {pct(trk["title"])}; {tg["v5"].get("touching", 0)} at {pct(V5_TRACK)}; {tg["0"].get("touching", 0)} at the font’s own spacing', 'token': None},
                    {'label': 'Letter pairs that touch, rule titles at 32 px', 'value': f'{tt["token"].get("touching", 0)} of {tt["token"].get("pairs", 0)} at {pct(trk["h3"])}; {tt["draft"].get("touching", 0)} at {pct(DRAFT_H3)}; {tt["0"].get("touching", 0)} at the font’s own spacing', 'token': None},
                ],
                'related': ['03', '04'],
                'builders': ['Tracking lives in each style’s <code>letter-spacing</code> property, in em, so it scales with '
                             'the size: <code>letter-spacing: var(--oa-type-h3-letter-spacing)</code>. Leave body text at '
                             'the font’s own spacing.'],
            },
            {
                'id': '06.5', 'title': 'Line up figures in tables, and give negatives the true minus sign.',
                'rule': ['Tables, trackers and chart labels set tabular figures, which give every digit the same width so a '
                         'column lines up. A negative number takes the minus sign (−, U+2212), which matches the plus sign’s '
                         'width, and the numbers in one column carry the same number of decimals.'],
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
                'id': '06.6', 'title': 'Balance a heading’s lines, and keep two words or more on its last line.',
                'rule': ['A heading that runs to two or more lines splits into lines of near equal length, and its last line '
                         'holds at least two words. Body text wraps so its last line holds more than one short word.'],
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
                'id': '06.7', 'title': 'Hang opening quotation marks outside the text edge.',
                'rule': ['In a pull quote or a quote card, the opening mark sits in the margin, so the first letter of every '
                         'line starts on the same edge. Use curly quotation marks and apostrophes (“ ” ‘ ’), and keep common '
                         'ligatures on and discretionary ligatures off.'],
                'tokens': ['oa.type.quote'],
                'why': {'text': ['When the mark sits inside the edge, the first line starts a mark’s width to the right of the '
                                 'rest, and the block looks indented by accident. Readers know curly marks from books and '
                                 'newspapers, so a straight mark looks like a typing slip.'],
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
                'id': '06.8', 'title': 'Set body text at 60 to 75 characters a line.',
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
                            'caption': f'The opening of our writing rules in chapter 02, at true size and the body measure, '
                                       f'33.88 rem. Its full lines measure {bi[1]} to {bi[2]} characters. Over {li[3]:,} '
                                       f'characters of chapter 02’s prose at the same width, lines average {li[0]:.0f}, and at '
                                       f'the widest body measure, {lm[0]:.0f}.'},
                'failure': {'specimen': 's-06-8-failure',
                            'caption': f'<strong>Fails the measure.</strong> The same paragraph as our fifth edition set its '
                                       f'intros, at 22 px and 65ch. Its full lines run {v5[1]} to {v5[2]} characters, and the '
                                       f'eye has far to travel back to the start of each.'},
                'specs': [
                    {'label': 'Body measure', 'value': f'33.88 rem, 542 px at 16 px text; lines average {li[0]:.0f} characters', 'token': 'oa.layout.measure.bodyIdeal'},
                    {'label': 'Widest body measure', 'value': f'37.37 rem; lines average {lm[0]:.0f} characters', 'token': 'oa.layout.measure.bodyMax'},
                    {'label': 'Widest intro measure', 'value': f'41.91 rem; at 22 px, lines average {im[0]:.0f} characters', 'token': 'oa.layout.measure.introMax'},
                    {'label': 'Phones', 'value': f'About {ph_lo} to {ph_hi} characters at 360 and 390 px', 'token': 'oa.layout.grid.phone.margin'},
                ],
                'related': ['07', '19'],
                'builders': ['Cap a text block with <code>max-width: var(--oa-layout-measure-body-ideal)</code>. The measure '
                             'is in rem, so a reader who enlarges text keeps the same characters a line.'],
            },
            {
                'id': '06.9', 'title': 'Set email type in the system font stack.',
                'rule': ['Many mail apps ignore web fonts, so email sets headlines and body text in Helvetica, Arial, '
                         'sans-serif, and quotations in Georgia Italic. An email is a fixed artboard 600 px wide, so it takes '
                         'the scale’s phone floor sizes, as Rule 06.2 sets out. Chapter 22 shows the full template.'],
                'tokens': ['oa.font.family.emailSans', 'oa.font.family.emailQuote'],
                'why': {'text': ['A mail app that cannot load a web font falls back to a face of its own choosing, often a '
                                 'serif. The system stack names the fallback in advance, so every reader sees a face we chose. '
                                 'Our fifth edition kept this rule and then set its own email headline in Inter Tight.'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-06-9-correct',
                            'caption': 'An email header at its true width of 600 px on White, set in the system stack: the '
                                       'headline in Helvetica or Arial at 26 px, the H3 floor, and the quote in Georgia Italic '
                                       'at 24 px, the quote floor.'},
                'failure': {'specimen': 's-06-9-failure',
                            'caption': '<strong>Fails the email rule.</strong> The headline set in Inter Tight, as a mail app '
                                       'shows it when the web font does not load: in the app’s default serif.'},
                'specs': [
                    {'label': 'Headlines and body', 'value': 'Helvetica, Arial, sans-serif', 'token': 'oa.font.family.emailSans'},
                    {'label': 'Quotation', 'value': 'Georgia, serif, italic', 'token': 'oa.font.family.emailQuote'},
                    {'label': 'Width', 'value': '600 px', 'token': None},
                    {'label': 'Sizes', 'value': 'The phone floor: headline 26 px, quote 24 px, body 17 px', 'token': 'oa.type.h3'},
                ],
                'related': ['02', '22'],
                'builders': ['Write the stack on every text element of an email, inline, since many mail apps strip a '
                             'style block. The wordmark goes in as an image with its name as alt text.'],
            },
            {
                'id': '06.10', 'title': 'Load the three faces, and let no other face stand in.',
                'rule': ['Pages load Inter Tight, Inter and Lora from their published files, in the weights the scale uses. '
                         'Arial and Georgia appear only as fallbacks inside the font stacks. No other face stands in for '
                         'ours, including Spectral, Source Sans, Public Sans, IBM Plex, Libre Baskerville, Playfair Display, '
                         'Cormorant, Helvetica Neue for display, Times New Roman, Calibri, Roboto, Open Sans and Montserrat.'],
                'tokens': ['oa.font.family.display', 'oa.font.family.reading', 'oa.font.family.quote'],
                'why': {'text': [f'Our locked identity rules say a font substitution is never a finished identity decision. A '
                                 f'fallback’s one job is to keep a page readable when a font fails to load. Measured at 32 '
                                 f'px, the heading here sets {wi:.0f} px wide in Inter Tight and {wa:.0f} px in Arial, '
                                 f'{wider:.1f} percent wider. A page that failed to load Inter Tight can look finished, and '
                                 f'only the letters give it away. The list carries our fifth edition’s never-substitute list '
                                 f'forward.'],
                        'basis': 'Our locked identity rules; design judgment'},
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
        'extras': [
            {'after_rule': '06.2', 'specimen': 's-06-artboards', 'label': 'Sizes for fixed artboards',
             'caption': 'Every style’s size on a web page and on a fixed artboard, such as a card, an email or a social '
                        'image. Between 600 and 1,200 px, take each style’s size from either column. Print pieces set type '
                        'in points, with all text at 10 pt or larger.'},
        ],
        'sources': [src,
                    'W3C, Web Content Accessibility Guidelines (WCAG) 2.2, W3C Recommendation, success criteria 1.4.4 and '
                    '1.4.8, https://www.w3.org/TR/WCAG22/.'],
    }
    for r in ch['rules']:
        r['specs'] = [{k: x for k, x in s.items() if x is not None} for s in r['specs']]
    ctx.fig('fonts loaded in the render', json.dumps(fonts), 'document.fonts.check in Chromium')
    return ch
