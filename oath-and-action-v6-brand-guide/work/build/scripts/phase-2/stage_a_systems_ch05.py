"""Chapter 05 Color: copy, rules and specimens (stage board A, systems designer, November 6, 2026).

Every contrast figure is computed by ctx.ratio() from tokens.json. Color shares of the two phone pages come from a
Chromium render (stage_a_systems_capture.js), classified pixel by pixel against the palette in analyze().
"""
import re
import sys

C = sys.modules['stage_a_systems_core']

WORDMARK16 = 'work/build/assets/identity/wordmark/20261028_Wordmark-16px-Master.svg'
AMP24 = 'work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg'
B = sys.modules['stage_a_systems_build']
SURF = ['newsprint', 'white', 'charcoal', 'prussian']
SNAME = {'newsprint': 'Newsprint', 'white': 'White', 'charcoal': 'Charcoal', 'prussian': 'Prussian'}
ON = {'newsprint': 'onNewsprint', 'white': 'onWhite', 'charcoal': 'onCharcoal', 'prussian': 'onPrussian'}
PAL = ['newsprint', 'charcoal', 'pillarRed', 'prussian', 'stone', 'verdigris', 'white']
PNAME = {'newsprint': 'Newsprint', 'charcoal': 'Charcoal', 'pillarRed': 'Pillar Red', 'prussian': 'Prussian',
         'stone': 'Stone', 'verdigris': 'Verdigris', 'white': 'White'}
SHARE = {'newsprint': (60, 85), 'charcoal': (10, 25), 'pillarRed': (1, 5), 'prussian': (5, 15), 'stone': (5, 15),
         'verdigris': (1, 5), 'white': None}
JOB = {'newsprint': 'The reading surface: the page most of our work sits on, and the ground for charts and the atlas.',
       'charcoal': 'Text and structure on light surfaces, and the dark ground for one panel per section.',
       'pillarRed': 'Signature red in the marks, and one working red in each view.',
       'prussian': 'Depth: panels that hold a tracker, an explainer or a set of figures.',
       'stone': 'Hairlines, structure and the context marks in a chart.',
       'verdigris': 'Success marks and the focus ring on light surfaces.',
       'white': 'A bright surface for specimens and email, and reversed text on Prussian.'}


def P(name):
    return f'oa.color.palette.{name}'


# ------------------------------------------------------------------------------------------------ phone page
PHONE_CSS = """
.ph{width:100%%;overflow:hidden}
.mh{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:56px;padding:0 16px;border-bottom:1px solid var(--rule)}
.mh svg{display:block;flex:none}
.menu{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid var(--edge);%(ui)s}
.bd{padding:24px 16px 8px}
.ey{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0;color:var(--sec);%(label)s}
.ey .illus{margin:0}
.hl{margin:8px 0 0;%(h3)s;text-wrap:balance}
.tx{margin:16px 0 0;%(body)s}
.hg{display:flex;align-items:center;gap:12px;margin:24px 16px;color:var(--hinge)}
.hg i{display:block;flex:1 1 0;height:0;border-top:1px solid currentColor}
.hg svg{display:block;flex:none}
.pn{margin-top:24px;padding:16px 16px 8px;background:var(--panel);color:var(--panel-ink)}
.hg + .pn{margin-top:0}
.pk{margin:0;color:var(--panel-sec);%(label)s}
.st{list-style:none;margin:8px 0 0;padding:0}
.st li{display:grid;grid-template-columns:5.5rem 1fr;gap:12px;padding:5px 0;border-top:1px solid var(--panel-rule);%(bodySmall)s}
.st b{font-weight:600}
.ft{padding:24px 16px 20px}
.ask{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 20px;background:var(--ask);color:var(--ask-ink);box-shadow:var(--ask-edge);%(ask)s}
"""


def phone_vars(ctx, dark=False):
    v = ctx.v
    if not dark:
        # The dates sit on the section's one dark panel, in Charcoal, so the red ask below it never meets Prussian
        return (f'--rule:{v("oa.color.border.hairline.onNewsprint")};--edge:{v("oa.color.border.strong.onNewsprint")};'
                f'--sec:{v("oa.color.text.secondary.onNewsprint")};--hinge:{v("oa.color.identity.hingeDivider.onNewsprint")};'
                f'--panel:{v("oa.color.surface.charcoal")};--panel-ink:{v("oa.color.text.primary.onCharcoal")};'
                f'--panel-sec:{v("oa.color.text.secondary.onCharcoal")};--panel-rule:{v("oa.color.border.hairline.onCharcoal")};'
                f'--ask:{v("oa.component.button.ask.fill.onNewsprint")};--ask-ink:{v("oa.component.button.ask.label.onNewsprint")};'
                f'--ask-edge:inset 0 0 0 1px {v("oa.component.button.ask.keyline.onNewsprint")};'
                f'background:{v("oa.color.surface.newsprint")};color:{v("oa.color.text.primary.onNewsprint")}')
    return (f'--rule:{v("oa.color.border.hairline.onCharcoal")};--edge:{v("oa.color.border.strong.onCharcoal")};'
            f'--sec:{v("oa.color.text.secondary.onCharcoal")};--hinge:{v("oa.color.identity.hingeDivider.onCharcoal")};'
            f'--panel:{v("oa.color.surface.prussian")};--panel-ink:{v("oa.color.text.primary.onPrussian")};'
            f'--panel-sec:{v("oa.color.text.secondary.onPrussian")};--panel-rule:{v("oa.color.border.hairline.onPrussian")};'
            f'--ask:{v("oa.component.button.ask.fill.onPrussian")};--ask-ink:{v("oa.component.button.ask.label.onPrussian")};'
            f'--ask-edge:none;background:{v("oa.color.surface.charcoal")};color:{v("oa.color.text.primary.onCharcoal")}')


def phone_css(ctx):
    return PHONE_CSS % {'ui': ctx.ty('ui'), 'label': ctx.ty('label'), 'h3': ctx.ty('h3', 'floor'), 'body': ctx.ty('body'),
                        'bodySmall': ctx.ty('bodySmall'), 'ask': ctx.ty('ask'), 'caption': ctx.ty('caption')}


def phone(ctx, variant='plain'):
    """The school board page on a 360 px phone. variant: plain, dark, threejobs, error."""
    dark = variant == 'dark'
    head = ('The school board votes on the new bell schedule <span class="date" data-red="working" data-red-job="date">April 14</span>.'
            if variant == 'threejobs' else 'The school board votes on the new bell schedule April 14.')
    extra = ''
    if variant == 'threejobs':
        extra = (f'.date{{color:{ctx.v(P("pillarRed"))}}}'
                 f'.rb{{display:block;width:64px;height:4px;margin:12px 0 0;background:{ctx.v(P("pillarRed"))}}}')
    # The hinge divider as Rule 04.4 sets it: B's 24 px master at 24 px, centered on a 1 px line as wide as the text
    # block, 12 px clear on each side, in the surface's ink (DR-96)
    hinge = ('' if dark else
             f'<div class="hg" aria-hidden="true"><i></i><img data-inline src="{AMP24}" width="21" height="24" alt=""><i></i></div>')
    pn_style = ''
    if dark:
        extra += '.ft{background:var(--panel);color:var(--panel-ink)}'
    ft = ''
    if variant == 'error':
        er = ctx.v('oa.color.state.error.mark.onNewsprint')
        extra += (f'.fld{{margin:0 0 16px}}.fl{{display:block;{ctx.ty("ui")}}}'
                  f'.in{{display:block;height:48px;margin-top:6px;border:1px solid {ctx.v("oa.color.border.strong.onNewsprint")};'
                  f'background:{ctx.v("oa.color.surface.white")};box-shadow:inset 4px 0 0 {er}}}'
                  f'.er{{display:grid;grid-template-columns:20px 1fr;gap:10px;margin-top:8px;padding:12px;'
                  f'background:{ctx.v("oa.color.state.error.band.onNewsprint")};color:{ctx.v("oa.color.state.error.text.onNewsprint")};'
                  f'box-shadow:inset 4px 0 0 {er};{ctx.ty("bodySmall")}}}'
                  f'.er svg{{display:block;margin-top:2px}}.er b{{font-weight:700}}'
                  f'.ask.pri{{background:{ctx.v("oa.component.button.primary.fill.onNewsprint")};'
                  f'color:{ctx.v("oa.component.button.primary.label.onNewsprint")};box-shadow:none}}')
        glyph = (f'<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true">'
                 f'<circle cx="10" cy="10" r="8.5" fill="{er}" stroke="{ctx.v("oa.color.border.strong.onNewsprint")}" stroke-width="1"/>'
                 f'<path d="M6.5 6.5l7 7M13.5 6.5l-7 7" stroke="{ctx.v("oa.color.text.primary.onCharcoal")}" stroke-width="2" stroke-linecap="square"/></svg>')
        ft = ('<div class="fld" data-red="working" data-red-job="error"><span class="fl">Email</span><span class="in"></span>'
              f'<div class="er">{glyph}<span><b>Error:</b> Enter an email address so the clerk can confirm your time to speak.</span></div></div>'
              '<span class="ask pri">Sign up to speak</span>')
    else:
        ft = ('<span class="ask">Sign up to speak</span>' if dark else
              '<span class="ask" data-red="working" data-red-job="ask">Sign up to speak</span>')
    body = (f'<div class="ph" style="{phone_vars(ctx, dark)}">'
            f'<div class="mh"><img data-inline src="{WORDMARK16}" width="152" height="16" alt="" data-red="signature"><span class="menu">Menu</span></div>'
            f'<div class="bd"><p class="ey"><span>Explainer · Local schools</span>{B.ILLUS}</p><p class="hl">{head}</p>'
            + ('<span class="rb" data-red="working" data-red-job="rule under the headline"></span>' if variant == 'threejobs' else '') +
            f'<p class="tx">The proposal moves the high school’s first bell from 7:25 to 8:10 a.m. Anyone may speak for two '
            f'minutes before the vote.</p>'
            f'<p class="tx">Buses would reach each stop about 40 minutes later. The middle and elementary schools keep '
            f'their hours.</p>'
            f'<p class="tx">The agenda and the full proposal are on the district’s website.</p></div>'
            f'{hinge}'
            f'<div class="pn"{pn_style}><p class="pk">What happens next</p><ol class="st">'
            f'<li><b>April 10</b><span>Sign-ups close at 5 p.m.</span></li>'
            f'<li><b>April 14</b><span>Public comment, then the vote</span></li></ol></div>'
            f'<div class="ft">{ft}</div></div>')
    return f'<style>{phone_css(ctx)}{extra}</style>{body}'


def inline_masters(html):
    """For probe pages only: place the identity masters inline, as guide_build.py does."""
    def rep(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag).group(1)
        w = re.search(r'width="([\d.]+)"', tag).group(1)
        h = re.search(r'height="([\d.]+)"', tag).group(1)
        svg = (C.ROOT / src).read_text()
        svg = re.sub(r'<\?xml.*?\?>', '', svg)
        return svg.replace('<svg ', f'<svg width="{w}" height="{h}" aria-hidden="true" ', 1)
    return re.sub(r'<img\b[^>]*data-inline[^>]*>', rep, html)


def probe_pages(ctx, page):
    pages = {}
    for sid, var in (('s-05-1-correct', 'plain'), ('s-05-1-failure', 'dark')):
        html = inline_masters(phone(ctx, var))
        pages[f'phone-{sid}.html'] = page(ctx, f'<div class="cap" style="width:360px">{html}</div>', sid)
        ctx.probe(f'shot {sid}', 'screenshot', page=f'phone-{sid}.html', selector='.cap .ph', file=f'phone-{sid}.png')
    return pages


def analyze(ctx, scratch):
    """Color shares of the two phone pages: each pixel goes to the nearest palette or derived color."""
    from PIL import Image
    cands = {k: ctx.hx(P(k)) for k in PAL}
    cands.update({'deepStone': ctx.hx('oa.color.derived.deepStone'), 'dimNewsprint': ctx.hx('oa.color.derived.dimNewsprint')})
    fold = {'deepStone': 'stone', 'dimNewsprint': 'newsprint'}
    rgbs = {k: C.rgb(h) for k, h in cands.items()}
    for sid in ('s-05-1-correct', 's-05-1-failure'):
        im = Image.open(scratch / f'phone-{sid}.png').convert('RGB')
        counts = {k: 0 for k in PAL}
        hist = im.getcolors(maxcolors=1 << 24)
        total = 0
        for n, px in hist:
            best = min(rgbs, key=lambda k: sum((a - b) ** 2 for a, b in zip(px, rgbs[k])))
            counts[fold.get(best, best)] += n
            total += n
        shares = {k: 100 * v / total for k, v in counts.items()}
        ctx.R[f'share {sid}'] = {'size': list(im.size), 'pixels': total,
                                  'shares': {k: round(v, 2) for k, v in shares.items()}}


def share_txt(ctx, sid, k):
    v = ctx.R[f'share {sid}']['shares'][k]
    return '<1' if 0 < v < 0.5 else f'{round(v):d}'


def share_bar(ctx, sid):
    sh = ctx.R[f'share {sid}']['shares']
    order = [k for k in PAL if sh.get(k, 0) > 0.05]
    segs = ''.join(f'<span class="sg" style="flex:{sh[k]:.2f} 0 0;background:{ctx.v(P(k))}"></span>' for k in order)
    key = ''.join(f'<li><span class="sw" style="background:{ctx.v(P(k))}"></span>{PNAME[k]} <b>{share_txt(ctx, sid, k)}%</b></li>'
                  for k in order)
    css = (f'.sb{{display:flex;height:24px;margin-top:16px;outline:1px solid {ctx.v("oa.color.border.strong.onNewsprint")};outline-offset:0}}'
           f'.sb .sg{{display:block;min-width:2px}}.sb .sg + .sg{{box-shadow:inset 1px 0 0 {ctx.v("oa.color.border.strong.onNewsprint")}}}'
           f'.sk{{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px 16px;{ctx.ty("caption")}}}'
           f'.sk li{{display:inline-flex;align-items:center;gap:6px}}.sk b{{font-weight:600}}'
           f'.sw{{width:12px;height:12px;flex:none;box-shadow:inset 0 0 0 1px {ctx.v("oa.color.border.strong.onNewsprint")}}}')
    return css, f'<div class="sb" aria-hidden="true">{segs}</div><ul class="sk">{key}</ul>'


# ------------------------------------------------------------------------------------------------ specimens
def s_05_1(ctx):
    for sid, var in (('s-05-1-correct', 'plain'), ('s-05-1-failure', 'dark')):
        if ctx.stage == 'final':
            css, bar = share_bar(ctx, sid)
            measured = f'<div class="ms"><p class="mk">Measured shares of this page</p>{bar}</div>'
            css += f'.ms{{padding:16px 0 0}}.mk{{margin:0;{ctx.ty("label")};color:{ctx.v("oa.color.text.secondary.onNewsprint")}}}'
        else:
            css, measured = '', ''
        html = phone(ctx, var).replace('</style>', css + '</style>', 1) + measured
        if var == 'plain':
            sh = ctx.R.get(f'share {sid}', {}).get('shares', {})
            alt = ('An Illustrative phone page at 360 px on Newsprint: the wordmark and a Menu button, the kicker Explainer, '
                   'Local schools, the headline The school board votes on the new bell schedule April 14, three short '
                   'paragraphs, a hinge divider, a Charcoal panel listing what happens next on April 10 and April 14, and '
                   'below it on Newsprint a red Sign up to speak button with a Charcoal edge. Below the page, a bar of its '
                   f'measured color shares: Newsprint {share_txt(ctx, sid, "newsprint") if sh else ""} percent, Charcoal '
                   f'{share_txt(ctx, sid, "charcoal") if sh else ""}, Stone {share_txt(ctx, sid, "stone") if sh else ""} and '
                   f'Pillar Red {share_txt(ctx, sid, "pillarRed") if sh else ""}.')
            ctx.spec(sid, html, '05', '05.1', alt, width=360, illustrative=True,
                     notes='Shares measured from a 1x Chromium render of the page, each pixel assigned to its nearest '
                           'palette color; Deep Stone counts as Stone and Dim Newsprint as Newsprint.')
        else:
            sh = ctx.R.get(f'share {sid}', {}).get('shares', {})
            alt = ('The same Illustrative phone page with a Charcoal masthead and body, a Prussian panel and a Newsprint '
                   'button, so dark surfaces cover most of the screen. Below it, its measured color shares: Newsprint '
                   f'{share_txt(ctx, sid, "newsprint") if sh else ""} percent, Charcoal '
                   f'{share_txt(ctx, sid, "charcoal") if sh else ""} and Prussian {share_txt(ctx, sid, "prussian") if sh else ""}.')
            ctx.spec(sid, html, '05', '05.1', alt, width=360, illustrative=True,
                     notes='A labeled failure: the proportion fails, every text pair still passes.')


def s_05_palette(ctx):
    rows = []
    for k in PAL:
        h = ctx.hx(P(k))
        r, g, b = C.rgb(h)
        share = SHARE[k]
        share_t = f'{share[0]} to {share[1]} percent' if share else 'As specimens and production need'
        edge = ' class="sw edge"' if k in ('white', 'newsprint') else ' class="sw"'
        if k == 'pillarRed':
            edge += ' data-red="swatch"'
        rows.append(f'<li><span{edge} aria-hidden="true" style="background:{ctx.v(P(k))}"></span><span class="tx"><b>{PNAME[k]}</b>'
                    f'<span class="hx">&#35;{h[1:]} · RGB {r} {g} {b}</span><span class="sh">{share_t}</span>'
                    f'<span class="jb">{JOB[k]}</span><code>{C.css_name(P(k))}</code></span></li>')
        ctx.T.used.add(P(k))
    css = (f'.pl{{list-style:none;margin:0;padding:0;display:grid;gap:24px;grid-template-columns:repeat(auto-fill,minmax(min(100%,13rem),1fr))}}'
           f'.pl li{{display:flex;flex-direction:column;gap:12px}}'
           f'.sw{{display:block;height:88px}}.sw.edge{{box-shadow:inset 0 0 0 1px {ctx.v("oa.color.border.hairline.onNewsprint")}}}'
           f'.tx{{display:flex;flex-direction:column;gap:4px}}'
           f'.tx b{{{ctx.ty("h4", "floor")}}}'
           f'.hx{{{ctx.ty("dataLabel")};color:{ctx.v("oa.color.text.secondary.onNewsprint")}}}'
           f'.sh{{{ctx.ty("ui")}}}'
           f'.jb{{{ctx.ty("bodySmall")}}}'
           f'.tx code{{{ctx.ty("caption")};color:{ctx.v("oa.color.text.secondary.onNewsprint")};overflow-wrap:anywhere}}')
    html = f'<style>{css}</style><ul class="pl">{"".join(rows)}</ul>'
    alt = ('The seven colors, each as a swatch with its name, hex value, RGB values, share of a composition and job: '
           + '; '.join(f'{PNAME[k]} {ctx.hx(P(k))}, ' + (f'{SHARE[k][0]} to {SHARE[k][1]} percent' if SHARE[k] else 'as needed')
                       for k in PAL) + '.')
    ctx.spec('s-05-palette', html, '05', None, alt, readable=True,
             notes='Fluid sheet, a readable list (D2-255). Values read from tokens.json; shares are Master Brief and V5 '
                   'ranges.')


def surface_tile(ctx, s, failing=False):
    v = ctx.v
    on = ON[s]
    prim = f'oa.color.text.primary.{on}'
    sec = f'oa.color.text.secondary.{on}'
    rp = ctx.ratio(prim, f'oa.color.surface.{s}')
    rs = ctx.ratio(sec, f'oa.color.surface.{s}')
    job = {'newsprint': 'The page for reading and most of what we publish.',
           'white': 'Specimens and email, where a page needs a bright ground.',
           'charcoal': 'The dark beat: one panel per section at most.',
           'prussian': 'Panels that hold a tracker, an explainer or a set of figures.'}[s]
    return (f'<div class="tl" style="background:{v("oa.color.surface." + s)};color:{v(prim)};--sec:{v(sec)};'
            f'--rule:{v("oa.color.border.hairline." + on)}">'
            f'<p class="sn">{SNAME[s]}</p><p class="sj">{job}</p>'
            f'<p class="ey"><span>Explainer · Local budgets</span>{B.ILLUS}</p><p class="hd">Who sets the library’s hours?</p>'
            f'<p class="bt">The council sets the hours each spring, when it passes the budget. Residents can speak at the '
            f'hearing before the vote.</p>'
            f'<p class="cp">New hours start July 1, with the budget year.</p>'
            f'<p class="rt">Primary text {rp}:1 · secondary text {rs}:1</p></div>'), rp, rs


TILE_CSS = """
.tl{display:flex;flex-direction:column;padding:24px;min-width:0}
.sn{margin:0;%(h4)s}
.sj{margin:4px 0 0;color:var(--sec);%(caption)s}
.ey{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:20px 0 0;padding-top:16px;border-top:1px solid var(--rule);color:var(--sec);%(label)s}
.ey .illus{margin:0}
.hd{margin:8px 0 0;%(h4)s;text-wrap:balance}
.bt{margin:12px 0 0;%(body)s}
.cp{margin:12px 0 0;color:var(--sec);%(caption)s}
.rt{margin:auto 0 0;padding-top:16px;%(dataLabel)s}
"""


def s_05_2(ctx):
    css = TILE_CSS % {'h4': ctx.ty('h4', 'floor'), 'caption': ctx.ty('caption'), 'label': ctx.ty('label'), 'body': ctx.ty('body'),
                      'dataLabel': ctx.ty('dataLabel')}
    tiles, rat = [], {}
    for s in SURF:
        t, rp, rs = surface_tile(ctx, s)
        tiles.append(t)
        rat[s] = (rp, rs)
    html = (f'<style>{css}.gr{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr))}}</style>'
            f'<div class="gr">{"".join(tiles)}</div>')
    alt = ('Four tiles, one per surface, each with the same Illustrative short article: the kicker Explainer, Local '
           'budgets, the headline Who sets the library’s hours?, two sentences of body text, a caption and its measured '
           'ratios. '
           + ' '.join(f'{SNAME[s]}: primary text {rat[s][0]} to 1, secondary text {rat[s][1]} to 1.' for s in SURF))
    ctx.spec('s-05-2-correct', html, '05', '05.2', alt, illustrative=True,
             notes='Fluid grid of four surface tiles. Each tile is its own surface; ratios from tokens.json.')

    # failure: Stone caption and a red link on Newsprint
    stone = ctx.ratio(P('stone'), P('newsprint'), 'contrast Stone on Newsprint')
    red = ctx.ratio(P('pillarRed'), P('newsprint'), 'contrast Pillar Red on Newsprint')
    t, _, _ = surface_tile(ctx, 'newsprint')
    t = t.replace(f'--sec:{ctx.v("oa.color.text.secondary.onNewsprint")}', f'--sec:{ctx.v(P("stone"))}', 1)
    t = t.replace('<p class="cp">New hours start July 1, with the budget year.</p>',
                  '<p class="cp">New hours start July 1, with the budget year.</p><p class="lk"><span data-red="working" data-red-job="link">Read the hearing notice</span></p>')
    t = re.sub(r'<p class="rt">.*?</p>', f'<p class="rt">Caption {stone}:1 · link {red}:1</p>', t)
    html = (f'<style>{css}.lk{{margin:12px 0 0;{ctx.ty("caption")}}}.lk span{{color:{ctx.v(P("pillarRed"))};'
            f'text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.2em}}</style>{t}')
    alt = (f'The Newsprint tile, labeled Illustrative, with its kicker, caption and ratio line in Stone, measured at '
           f'{stone} to 1, and a link, Read the hearing notice, in Pillar Red at 14 px, measured at {red} to 1.')
    ctx.spec('s-05-2-failure', html, '05', '05.2', alt, width=360, illustrative=True, exempt=['contrast'],
             notes='A labeled failure case: its small text fails 4.5 to 1 on purpose.')


ROLES = [
    ('Text, primary', 'oa.color.text.primary', 'text', 'Body text, headings, data values'),
    ('Text, secondary', 'oa.color.text.secondary', 'text', 'Captions, labels, source lines, disabled text'),
    ('Marks a reader needs', 'oa.color.graphic.essential', 'graphic', 'Icons, diagram strokes, the subject of a chart'),
    ('Marks that support', 'oa.color.graphic.subtle', 'graphic', 'Context series, unlit nodes'),
    ('Control edges', 'oa.color.border.strong', 'graphic', 'Inputs, buttons, keylines on red'),
    ('Hairlines', 'oa.color.border.hairline', 'decorative', 'Dividers and table rules'),
    ('Focus ring', 'oa.color.focus.ring', 'graphic', '2 px outline, 2 px gap'),
    ('Signature red', 'oa.color.identity.signature', 'mark', 'The wordmark’s ampersand, the lever'),
    ('Working red', 'oa.color.action.ask.fill', 'mark', 'The one job per view'),
]
NEED = {'text': 4.5, 'graphic': 3.0, 'decorative': None, 'mark': None}


def roles_matrix(ctx):
    v = ctx.v
    head = ''.join(f'<th scope="col" style="background:{v("oa.color.surface." + s)};color:{v("oa.color.text.primary." + ON[s])}">{SNAME[s]}</th>'
                   for s in SURF)
    rows = []
    for name, base, kind, job in ROLES:
        cells = []
        for s in SURF:
            path = f'{base}.{ON[s]}'
            surf = f'oa.color.surface.{s}'
            ink = v(f'oa.color.text.primary.{ON[s]}')
            sec = v(f'oa.color.text.secondary.{ON[s]}')
            bg = v(surf)
            hexv = ctx.hx(path)
            alias = ctx.T.alias(path) or ''
            cname = alias.split('.')[-1]
            cname = {'deepStone': 'Deep Stone', 'dimNewsprint': 'Dim Newsprint', 'pillarRed': 'Pillar Red'}.get(cname, cname[:1].upper() + cname[1:])
            r = ctx.ratio(path, surf)
            if kind == 'text':
                sample = f'<span class="aa" aria-hidden="true" style="color:{v(path)}">Aa</span>'
            elif kind == 'decorative':
                sample = f'<span class="hl" aria-hidden="true" style="border-top-color:{v(path)}"></span>'
            elif base.endswith('focus.ring'):
                sample = f'<span class="fr" aria-hidden="true" style="outline-color:{v(path)}"></span>'
            else:
                edge = ''
                if s == 'newsprint' and hexv == ctx.hx(P('pillarRed')):
                    edge = f';box-shadow:inset 0 0 0 1px {v("oa.color.border.strong.onNewsprint")}'
                sw = ' data-red="swatch"' if hexv == ctx.hx(P('pillarRed')) else ''
                sample = f'<span class="ch"{sw} aria-hidden="true" style="background:{v(path)}{edge}"></span>'
            note = ''
            if base.endswith('ask.fill') and s == 'prussian':
                note = 'Newsprint stands in: red never sits on Prussian'
            elif base.endswith('ask.fill') and s == 'newsprint':
                note = 'Takes a 1 px Charcoal keyline'
            elif base.endswith('signature') and s == 'prussian':
                note = 'White marks on Prussian'
            elif base.endswith('signature') and s == 'newsprint':
                note = 'Logotype only; it does not count'
            elif kind == 'decorative':
                note = 'Decoration; carries no meaning'
            need = NEED[kind]
            verdict = ''
            if need:
                verdict = ' · passes' if C.contrast(hexv, ctx.hx(surf)) >= need else ' · fails'
            cells.append(f'<td style="background:{bg};color:{ink}" data-s="{SNAME[s]}">{sample}'
                         f'<span class="nm">{cname}</span><span class="rr">{r}:1{verdict}</span>'
                         + (f'<span class="nt" style="color:{sec}">{note}</span>' if note else '') + '</td>')
        thr = {'text': 'Needs 4.5 to 1', 'graphic': 'Needs 3 to 1', 'decorative': 'No minimum',
               'mark': 'Governed by Rule 05.3'}[kind]
        rows.append(f'<tr><th scope="row"><span class="rn">{name}</span><span class="rj">{job}</span>'
                    f'<span class="rj">{thr}</span></th>{"".join(cells)}</tr>')
    css = (f'.wr{{container-type:inline-size}}'
           f'table{{width:100%;border-collapse:collapse;{ctx.ty("bodySmall")}}}'
           f'th,td{{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'thead th{{{ctx.ty("label")}}}'
           f'tbody th{{font-weight:400;width:24%}}'
           f'.rn{{display:block;{ctx.ty("ui")}}}.rj{{display:block;color:{v("oa.color.text.secondary.onNewsprint")};{ctx.ty("caption")}}}'
           f'td span{{display:block}}.nm{{margin-top:6px;{ctx.ty("ui")}}}.rr{{{ctx.ty("dataLabel")}}}.nt{{margin-top:4px;{ctx.ty("caption")}}}'
           f'.aa{{{ctx.ty("h4", "floor")}}}'
           f'.ch{{width:40px;height:20px}}.hl{{width:40px;height:10px;border-top:1px solid}}'
           f'.fr{{width:32px;height:16px;margin:2px;outline:2px solid;outline-offset:2px}}'
           f'@container (max-width:40rem){{thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}'
           f'table,tbody,tr,th,td{{display:block}}tr{{margin-bottom:16px}}tbody th{{width:auto;padding-left:0}}'
           f'td{{display:grid;grid-template-columns:6.5rem 44px 1fr;gap:4px 12px;align-items:start;border-bottom:0}}'
           f'td::before{{content:attr(data-s);grid-row:span 3;{ctx.ty("label")}}}td span{{grid-column:3}}td .aa,td .ch,td .hl,td .fr{{grid-column:2;grid-row:1 / span 3}}}}')
    html = (f'<style>{css}</style><div class="wr"><table role="table"><caption class="vh" style="position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)">'
            f'Color roles on each surface, with the color each role takes and its measured contrast against the surface</caption>'
            f'<thead><tr><th scope="col">Role</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    return html


def s_05_roles(ctx):
    html = roles_matrix(ctx)
    alt = ('A table of nine color roles across the four surfaces, each cell drawn on its surface with a sample, the color '
           'the role takes and its measured ratio.')
    ctx.spec('s-05-roles', html, '05', None, alt, readable=True,
             notes='A readable table (D2-255). Every ratio computed from tokens.json. Stacks into one block per role under '
                   '40 rem.')


def s_05_3(ctx):
    alt_base = ('An Illustrative phone page at 360 px on Newsprint: the wordmark with its red ampersand, the school board '
                'headline, body text, a hinge divider with a Charcoal ampersand, a Charcoal panel of dates')
    ctx.spec('s-05-3-correct', phone(ctx, 'plain'), '05', '05.3',
             alt_base + ', and one red button, Sign up to speak, with a Charcoal edge.', width=360, illustrative=True,
             notes='Signature red: the wordmark ampersand. Working red: the ask, precedence 2.')
    ctx.spec('s-05-3-failure', phone(ctx, 'threejobs'), '05', '05.3',
             'The same Illustrative phone page with three reds: the date April 14 in the headline, a red bar under the '
             'headline, and the red Sign up to speak button.', width=360, illustrative=True, exempt=['contrast', 'red'],
             notes='A labeled failure case: red date text at 28 px fails 3 to 1 on purpose.')
    ctx.spec('s-05-3-corrective', phone(ctx, 'error'), '05', '05.3',
             'The same Illustrative phone page with an email field in its error state: a red bar on the field, a message on '
             'a pale red band that reads Error: Enter an email address so the clerk can confirm your time to speak, a red '
             'error glyph, and below it the Sign up to speak button in Charcoal with a White label.', width=360,
             illustrative=True,
             notes='The error takes the working red (precedence 1); the ask steps down to the primary button.')


def s_05_ask(ctx):
    tiles = []
    facts = {}
    for s in SURF:
        on = ON[s]
        fill = f'oa.component.button.ask.fill.{on}'
        lab = f'oa.component.button.ask.label.{on}'
        surf = f'oa.color.surface.{s}'
        rf = ctx.ratio(fill, surf)
        rl = ctx.ratio(lab, fill)
        lines = [f'Fill on {SNAME[s]} {rf}:1', f'Label on fill {rl}:1, 19 px bold']
        edge = 'none'
        if s == 'newsprint':
            kl = 'oa.component.button.ask.keyline.onNewsprint'
            rk = ctx.ratio(kl, surf)
            lines.insert(1, f'Charcoal keyline {rk}:1')
            edge = f'inset 0 0 0 1px {ctx.v(kl)}'
        if s == 'prussian':
            lines.append('Red never sits on Prussian')
        facts[s] = lines
        dr = '' if s == 'prussian' else ' data-red="working" data-red-job="ask"'
        tiles.append(f'<div class="tl"{dr} style="background:{ctx.v(surf)};color:{ctx.v("oa.color.text.primary." + on)}">'
                     f'<p class="sn">{SNAME[s]}</p>'
                     f'<span class="ask" style="background:{ctx.v(fill)};color:{ctx.v(lab)};box-shadow:{edge}">Sign up to speak</span>'
                     f'<ul>{"".join(f"<li>{x}</li>" for x in lines)}</ul></div>')
    css = (f'.gr{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr))}}'
           f'.tl{{padding:24px}}.sn{{margin:0 0 16px;{ctx.ty("label")}}}'
           f'.ask{{display:flex;align-items:center;justify-content:center;min-height:52px;padding:0 20px;{ctx.ty("ask")}}}'
           f'ul{{list-style:none;margin:16px 0 0;padding:0;{ctx.ty("caption")}}}li{{padding:2px 0}}')
    html = f'<style>{css}</style><div class="gr">{"".join(tiles)}</div>'
    alt = ('The ask button, Sign up to speak, on the four surfaces. ' +
           ' '.join(f'{SNAME[s]}: ' + '; '.join(facts[s]) + '.' for s in SURF))
    ctx.spec('s-05-ask', html, '05', None, alt, notes='Ratios computed from tokens.json.')


STATES = [
    ('Hover', 'hover', 'The fill steps from Charcoal to Prussian and the label underlines.'),
    ('Focus', 'focus', 'A 2 px Verdigris ring with a 2 px gap, shown at once.'),
    ('Disabled', 'disabled', 'A dashed edge, readable text and a line that says what makes it available.'),
    ('Loading', 'loading', 'A still outline and the words that say what is loading.'),
    ('Selected', 'selected', 'The paired surface, a 4 px bar and a check.'),
    ('Muted', 'muted', 'Regular weight and an outline mark.'),
    ('Warning', 'warning', 'A triangle, the word Warning and a 4 px bar. Warning has no hue of its own.'),
    ('Error', 'error', 'The word Error, a glyph and the fix in plain words, on the Error Band.'),
    ('Empty', 'empty', 'A dashed region that says what is missing and what to do next.'),
    ('Success', 'success', 'A Verdigris check and a word such as Saved.'),
]


def s_05_4(ctx):
    v = ctx.v
    N = 'onNewsprint'
    btn = (f'display:inline-flex;align-items:center;min-height:44px;padding:0 16px;{ctx.ty("ui")}')
    samples = {
        'hover': f'<span class="b" style="background:{v("oa.color.action.primary.fillHover." + N)};color:{v("oa.color.action.primary.label." + N)};text-decoration:underline;text-underline-offset:.2em">Download SVG</span>',
        'focus': f'<span class="b" style="background:{v("oa.color.action.primary.fill." + N)};color:{v("oa.color.action.primary.label." + N)};outline:2px solid {v("oa.color.focus.ring." + N)};outline-offset:2px">Download SVG</span>',
        'disabled': f'<span class="b" style="color:{v("oa.color.state.disabled.text." + N)};border:1px dashed {v("oa.color.state.disabled.edge." + N)}">Download PNG</span><span class="why">Choose a size to download.</span>',
        'loading': f'<span class="ld"><span class="lv" style="border-color:{v("oa.color.state.loading.mark." + N)}"></span><span style="color:{v("oa.color.state.loading.text." + N)}">Loading tracker</span></span>',
        'selected': f'<span class="sel" style="background:{v("oa.color.state.selected.band." + N)};box-shadow:inset 4px 0 0 {v("oa.color.state.selected.bar." + N)}">'
                    f'<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7" fill="none" stroke="{v("oa.color.text.primary." + N)}" stroke-width="2"/></svg>Track</span>',
        'muted': f'<span class="ld"><span class="lv" style="border-color:{v("oa.color.state.muted.mark." + N)}"></span><span style="color:{v("oa.color.state.muted.text." + N)}">Closed hearing</span></span>',
        'warning': f'<span class="msg" style="box-shadow:inset 4px 0 0 {v("oa.color.state.warning.mark." + N)};color:{v("oa.color.state.warning.text." + N)}">'
                   f'<svg width="18" height="16" viewBox="0 0 18 16" aria-hidden="true"><path d="M9 1.5L17 15H1z" fill="none" stroke="{v("oa.color.state.warning.mark." + N)}" stroke-width="1.5" stroke-linejoin="miter"/><path d="M9 6v4.5M9 12v1.5" stroke="{v("oa.color.state.warning.mark." + N)}" stroke-width="1.5"/></svg>'
                   f'<span><b>Warning:</b> This page uses figures from 2024.</span></span>',
        'error': f'<span class="msg" data-red="working" data-red-job="error" style="background:{v("oa.color.state.error.band." + N)};box-shadow:inset 4px 0 0 {v("oa.color.state.error.mark." + N)};color:{v("oa.color.state.error.text." + N)}">'
                 f'<svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="9" cy="9" r="7.5" fill="{v("oa.color.state.error.mark." + N)}" stroke="{v("oa.color.border.strong." + N)}"/><path d="M6 6l6 6M12 6l-6 6" stroke="{v("oa.color.text.primary.onCharcoal")}" stroke-width="1.75"/></svg>'
                 f'<span><b>Error:</b> Enter a ZIP code with five digits.</span></span>',
        'empty': f'<span class="em" style="border-color:{v("oa.color.state.empty.edge." + N)};color:{v("oa.color.state.empty.text." + N)}">No saved explainers yet. Choose Save on any explainer to keep it here.</span>',
        'success': f'<span class="ld"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="9" cy="9" r="8" fill="{v("oa.color.state.success.mark." + N)}"/><path d="M5 9.5l2.5 2.5 5.5-5.5" fill="none" stroke="{v("oa.color.text.primary.onCharcoal")}" stroke-width="2"/></svg>'
                   f'<span style="color:{v("oa.color.state.success.text." + N)}">Saved</span></span>',
    }
    rows = ''.join(f'<li><span class="nm">{n}</span><span class="sm">{samples[k]}</span><span class="cu">{cue}</span></li>'
                   for n, k, cue in STATES)
    css = (f'.wr{{container-type:inline-size}}'
           f'ul{{list-style:none;margin:0;padding:0}}'
           f'li{{display:grid;grid-template-columns:7rem minmax(0,16rem) minmax(0,1fr);gap:8px 20px;align-items:center;padding:12px 0;border-bottom:1px solid {v("oa.color.border.hairline." + N)}}}'
           f'.nm{{{ctx.ty("label")}}}.cu{{{ctx.ty("bodySmall")}}}'
           f'.b{{{btn}}}.why{{display:block;margin-top:6px;color:{v("oa.color.text.secondary." + N)};{ctx.ty("caption")}}}'
           f'.ld{{display:inline-flex;align-items:center;gap:10px;{ctx.ty("ui")}}}'
           f'.lv{{display:block;width:16px;height:16px;border:2px solid;border-radius:50%}}'
           f'.sel{{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px 0 14px;{ctx.ty("ui")}}}'
           f'.msg{{display:grid;grid-template-columns:18px 1fr;gap:10px;align-items:start;padding:10px 12px 10px 14px;{ctx.ty("bodySmall")}}}'
           f'.msg svg{{margin-top:3px}}.msg b{{font-weight:700}}'
           f'.em{{display:block;padding:12px;border:1px dashed;{ctx.ty("bodySmall")}}}'
           f'.hd{{margin:0 0 4px}}'
           f'@container (max-width:36rem){{li{{grid-template-columns:1fr}}}}')
    html = f'<style>{css}</style><div class="wr"><p class="hd">{B.ILLUS}</p><ul>{rows}</ul></div>'
    alt = ('Ten interface states on Newsprint, labeled Illustrative, each with a sample and its cue: '
           + ' '.join(f'{n}: {cue}' for n, _, cue in STATES))
    ctx.spec('s-05-4-correct', html, '05', '05.4', alt, illustrative=True,
             notes='Fluid sheet. Every text and mark color is a state token; every sample changes text or shape too.')

    red, ver = ctx.hx(P('pillarRed')), ctx.hx(P('verdigris'))
    rv = ctx.ratio(P('pillarRed'), P('verdigris'), 'contrast Pillar Red against Verdigris')
    gr, gv = C.css_gray(red), C.css_gray(ver)
    ctx.fig('grayscale Pillar Red', gr, 'CSS grayscale(1): 0.2126 R + 0.7152 G + 0.0722 B on the encoded values')
    ctx.fig('grayscale Verdigris', gv, 'CSS grayscale(1): 0.2126 R + 0.7152 G + 0.0722 B on the encoded values')
    rowsf = (f'<li><span class="dt" data-red="working" data-red-job="status" style="background:{v(P("pillarRed"))}"></span>Budget hearing</li>'
             f'<li><span class="dt" style="background:{v(P("verdigris"))}"></span>Zoning vote</li>')
    cssf = (f'.pr{{display:flex;flex-wrap:wrap;gap:24px}}.col{{flex:1 1 14rem}}'
            f'.k{{margin:0 0 8px;{ctx.ty("label")};color:{v("oa.color.text.secondary." + N)}}}'
            f'ul{{list-style:none;margin:0;padding:0;{ctx.ty("ui")}}}'
            f'li{{display:flex;align-items:center;gap:12px;min-height:44px;border-bottom:1px solid {v("oa.color.border.hairline." + N)}}}'
            f'.dt{{width:12px;height:12px;border-radius:50%;flex:none}}.g ul{{filter:grayscale(1)}}')
    htmlf = (f'<style>{cssf}.hd{{margin:0 0 16px}}</style><p class="hd">{B.ILLUS}</p><div class="pr"><div class="col"><p class="k">In color</p><ul>{rowsf}</ul></div>'
             f'<div class="col g"><p class="k">In grayscale</p><ul>{rowsf}</ul></div></div>')
    ctx.spec('s-05-4-failure', htmlf, '05', '05.4',
             f'Two Illustrative tracker rows, Budget hearing with a red dot and Zoning vote with a Verdigris dot, and no word '
             f'for either status. Beside them the same rows in grayscale, where the two dots print as nearly the same gray.',
             illustrative=True, notes=f'Pillar Red against Verdigris {rv} to 1; in grayscale {gr} and {gv}.')


# Payroll change by sector, January 2022 to September 2026, thousands and percent (FRED copies of BLS CES series),
# read from work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json, dataset payrolls-by-sector, row 2026-09.
def load_jobs():
    import json
    d = json.loads((C.ROOT / 'work/boards/phase-2/data-viz/shared/20261106_Chart-Data.json').read_text())
    ds = d['datasets']['payrolls-by-sector']
    pick = ['CES6562000001', 'USLAH', 'USGOVT', 'USCONS', 'MANEMP', 'USINFO']
    rows = {r['series_id']: r for r in ds['rows'] if r['date'] == '2026-09-01'}
    out = [{'sector': rows[s]['sector'], 'change': rows[s]['change_since_2022_01_thousands'],
            'pct': rows[s]['pct_change_since_2022_01']} for s in pick]
    allsec = [r for r in ds['rows'] if r['date'] == '2026-09-01' and r['series_id'] not in ('PAYEMS', 'USPRIV')]
    top = max(allsec, key=lambda r: r['change_since_2022_01_thousands'])
    assert top['series_id'] == 'CES6562000001', top
    return out, ds['source_line'], len(allsec)


def bar_chart(ctx, keyline=True):
    rows, src, nsec = load_jobs()
    vmax = max(r['change'] for r in rows)
    vmin = min(0, min(r['change'] for r in rows))
    span = vmax - vmin
    zero = -vmin / span * 100
    v = ctx.v
    out = []
    for i, r in enumerate(rows):
        w = abs(r['change']) / span * 100
        left = zero if r['change'] >= 0 else zero - w
        red = i == 0
        fill = v('oa.chart.color.point.onNewsprint') if red else v('oa.chart.color.context.onNewsprint')
        edge = f';box-shadow:inset 0 0 0 1px {v("oa.chart.color.pointKeyline.onNewsprint")}' if red and keyline else ''
        val = C.signed(r['change'], 0)
        dr = ' data-red="working" data-red-job="the point the title names"' if red else ''
        out.append(f'<li{dr}><span class="lb{" s" if red else ""}">{r["sector"]}</span><span class="tr">'
                   f'<span class="br" style="left:{left:.3f}%;width:{w:.3f}%;background:{fill}{edge}"></span>'
                   f'<span class="vl" style="left:calc({(left + w if r["change"] >= 0 else zero):.3f}% + 6px)">{val}</span></span></li>')
    big = f'{rows[0]["change"] / 1000:.1f}'
    title = (f'Health care and social assistance added {big} million payroll jobs from January 2022 to September 2026, '
             f'the most of the six sectors shown.')
    css = (f'.ch{{max-width:45rem}}'
           f'.ek{{margin:0;{ctx.ty("label")};color:{v("oa.color.text.secondary.onNewsprint")}}}'
           f'.tt{{margin:6px 0 0;{ctx.ty("h4")};text-wrap:balance}}'
           f'.mu{{margin:8px 0 0;{ctx.ty("caption")};color:{v("oa.color.text.secondary.onNewsprint")}}}'
           f'ol{{list-style:none;margin:16px 0 0;padding:0}}'
           f'li{{display:grid;grid-template-columns:minmax(7rem,38%) 1fr;gap:12px;align-items:center;min-height:36px}}'
           f'.lb{{{ctx.ty("bodySmall")};line-height:1.25}}.lb.s{{font-weight:600}}'
           f'.tr{{position:relative;display:block;height:24px;margin-right:4.5rem;'
           f'background:linear-gradient({v("oa.chart.color.baseline.onNewsprint")},{v("oa.chart.color.baseline.onNewsprint")}) {zero:.3f}% 0/1.5px 100% no-repeat}}'
           f'.br{{position:absolute;top:0;height:24px}}'
           f'.vl{{position:absolute;top:3px;white-space:nowrap;{ctx.ty("dataLabel")}}}'
           f'.so{{margin:12px 0 0;{ctx.ty("caption")};color:{v("oa.color.text.secondary.onNewsprint")}}}')
    html = (f'<style>{css}</style><div class="ch"><p class="ek">Finding</p><p class="tt">{title}</p>'
            f'<p class="mu">Change in payroll jobs, thousands, seasonally adjusted</p><ol>{"".join(out)}</ol>'
            f'<p class="so">{src}</p></div>')
    return html, title, rows, src, nsec


def s_05_5(ctx):
    html, title, rows, src, nsec = bar_chart(ctx, keyline=True)
    rp = ctx.ratio('oa.chart.color.point.onNewsprint', P('newsprint'), 'contrast Pillar Red on Newsprint')
    rk = ctx.ratio('oa.chart.color.pointKeyline.onNewsprint', P('newsprint'), 'contrast Charcoal keyline on Newsprint')
    rc = ctx.ratio('oa.chart.color.context.onNewsprint', P('newsprint'), 'contrast Stone context bars on Newsprint')
    vals = '; '.join(f'{r["sector"]} {C.signed(r["change"], 0)}' for r in rows)
    ctx.spec('s-05-5-correct', html, '05', '05.5',
             f'A bar chart 600 px wide titled {title} Bars, in thousands of jobs: {vals}. The health care bar is Pillar Red '
             f'with a 1 px Charcoal edge; the others are Stone. Source line below.', width=600,
             notes=f'Data: payrolls-by-sector in the shared chart data, September 2026 row; {nsec} sector series checked '
                   f'for the most. 600 px wide, so its type takes the phone floor (D2-254).')
    html2, *_ = bar_chart(ctx, keyline=False)
    ctx.spec('s-05-5-failure', html2, '05', '05.5',
             f'The same bar chart with the health care bar in Pillar Red and no edge, so its outline blurs into the '
             f'Newsprint page.', width=600, notes='The red bar has no keyline; text in the chart still passes.')
    ctx.fig('chart rows', vals, 'payrolls-by-sector, row 2026-09-01, change_since_2022_01_thousands')
    return rp, rk, rc, src


VERDICT_RED = {'newsprint': 'Signature marks; a working mark takes a keyline', 'white': 'Marks and fills; never text',
               'charcoal': 'Marks and fills; never text', 'prussian': 'Never: red does not sit on Prussian'}


def verdict(ctx, fg, s):
    if fg == s:
        return None
    if fg == 'pillarRed':
        return VERDICT_RED[s]
    r = C.contrast(ctx.hx(P(fg)), ctx.hx(P(s)))
    if r >= 4.5:
        return 'Text at any size'
    if r >= 3:
        return 'Large text and marks'
    return 'Not for text or marks'


def s_05_pairs(ctx):
    v = ctx.v
    head = ''.join(f'<th scope="col">{SNAME[s]}</th>' for s in SURF)
    rows = []
    for fg in ['charcoal', 'newsprint', 'white', 'prussian', 'stone', 'verdigris', 'pillarRed']:
        cells = []
        for s in SURF:
            bg = v(P(s))
            ink = v(f'oa.color.text.primary.{ON[s]}')
            vd = verdict(ctx, fg, s)
            if vd is None:
                cells.append(f'<td style="background:{bg};color:{ink}" data-s="{SNAME[s]}"><span class="rr">Same color</span></td>')
                continue
            r = ctx.ratio(P(fg), P(s), f'contrast {PNAME[fg]} on {SNAME[s]}')
            exact = C.contrast(ctx.hx(P(fg)), ctx.hx(P(s)))
            if fg != 'pillarRed' and exact >= 4.5:
                smp = f'<span class="aa" aria-hidden="true" style="color:{v(P(fg))}">Aa</span>'
            elif fg != 'pillarRed' and exact >= 3:
                smp = f'<span class="aa lg" aria-hidden="true" style="color:{v(P(fg))}">Aa</span>'
            else:
                edge = f';box-shadow:inset 0 0 0 1px {v("oa.color.border.strong.onNewsprint")}' if (fg == 'pillarRed' and s == 'newsprint') else ''
                sw = ' data-red="swatch"' if fg == 'pillarRed' else ''
                smp = f'<span class="ch"{sw} aria-hidden="true" style="background:{v(P(fg))}{edge}"></span>'
            if fg == 'pillarRed' and s == 'prussian':
                smp = '<span class="ch none" aria-hidden="true"></span>'
            cells.append(f'<td style="background:{bg};color:{ink}" data-s="{SNAME[s]}">{smp}<span class="rr">{r}:1</span>'
                         f'<span class="vd">{vd}</span></td>')
        sw = ' data-red="swatch"' if fg == 'pillarRed' else ''
        rows.append(f'<tr><th scope="row"><span class="sw"{sw} aria-hidden="true" style="background:{v(P(fg))}"></span>{PNAME[fg]}</th>{"".join(cells)}</tr>')
    css = (f'.wr{{container-type:inline-size}}table{{width:100%;border-collapse:collapse;{ctx.ty("bodySmall")}}}'
           f'th,td{{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'thead th{{{ctx.ty("label")}}}tbody th{{{ctx.ty("ui")};white-space:nowrap}}'
           f'.sw{{display:inline-block;width:14px;height:14px;margin-right:8px;vertical-align:-2px;box-shadow:inset 0 0 0 1px {v("oa.color.border.strong.onNewsprint")}}}'
           f'td span{{display:block}}.rr{{margin-top:4px;{ctx.ty("dataLabel")}}}.vd{{{ctx.ty("caption")}}}'
           f'.aa{{{ctx.ty("body")};font-weight:var(--oa-font-weight-semibold)}}.aa.lg{{{ctx.ty("h4", "ceil")};line-height:1}}'
           f'.ch{{width:40px;height:20px}}.ch.none{{box-shadow:inset 0 0 0 1px currentColor;background:transparent}}'
           f'@container (max-width:40rem){{thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}'
           f'table,tbody,tr,th,td{{display:block}}tr{{margin-bottom:16px}}tbody th{{padding-left:0}}'
           f'td{{display:grid;grid-template-columns:6.5rem 44px 1fr;gap:2px 12px;align-items:start;border-bottom:0}}'
           f'td::before{{content:attr(data-s);grid-row:span 2;{ctx.ty("label")}}}td span{{grid-column:3}}'
           f'td .aa,td .ch{{grid-column:2;grid-row:1 / span 2}}td .rr{{margin-top:0}}}}')
    html = (f'<style>{css}</style><div class="wr"><table role="table"><thead><tr><th scope="col">Color</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')
    ctx.spec('s-05-pairs', html, '05', None,
             'A table of the seven colors set on the four surfaces, each cell drawn on its surface with a sample, the measured '
             'ratio and what the pair may carry.', readable=True,
             notes='All 28 cells computed from tokens.json. Samples: Aa at body size where text passes, Aa at 24 px bold '
                   'where only large text passes, a chip where only marks or nothing pass.')


def s_05_6(ctx):
    v = ctx.v
    tints = [k for k in ctx.T.node('oa.color.tint') if not k.startswith('$')]
    ctx.fig('count of chart tints', str(len(tints)), 'keys of oa.color.tint in tokens.json')
    rows_spec = [
        ('oa.color.derived.deepStone', 'Deep Stone', 'Stone 18% toward Charcoal',
         'Secondary and disabled text on Newsprint and White',
         [('oa.color.derived.deepStone', P('newsprint'), 'text on Newsprint'), ('oa.color.derived.deepStone', P('white'), 'text on White')]),
        ('oa.color.derived.dimNewsprint', 'Dim Newsprint', 'Newsprint 25% toward Charcoal',
         'Secondary and disabled text on Charcoal and Prussian',
         [('oa.color.derived.dimNewsprint', P('charcoal'), 'text on Charcoal'), ('oa.color.derived.dimNewsprint', P('prussian'), 'text on Prussian')]),
        ('oa.color.derived.errorBand', 'Error Band', 'Pillar Red 88% toward Newsprint',
         'The ground of an error message on Newsprint and White',
         [(P('charcoal'), 'oa.color.derived.errorBand', 'Charcoal text on it'), ('oa.color.derived.deepStone', 'oa.color.derived.errorBand', 'Deep Stone text on it')]),
        ('oa.color.tint.stoneN70', 'Gridline', 'Stone 70% toward Newsprint', 'Chart gridlines on Newsprint; decoration only',
         [('oa.color.tint.stoneN70', P('newsprint'), 'on Newsprint')]),
        ('oa.color.tint.prussianN62', 'Light Prussian', 'Prussian 62% toward Newsprint', 'The light Prussian step of the diverging scale',
         [(P('charcoal'), 'oa.color.tint.prussianN62', 'Charcoal label on it')]),
        ('oa.color.tint.verdigrisN55', 'Light Verdigris', 'Verdigris 55% toward Newsprint', 'The light Verdigris step of the diverging scale',
         [(P('charcoal'), 'oa.color.tint.verdigrisN55', 'Charcoal label on it')]),
    ]
    rows = []
    alt_bits = []
    for path, name, recipe, job, pairs in rows_spec:
        hexv = ctx.hx(path)
        ext = ctx.T.ext(path)
        der = ext.get('derivation') or {}
        meas = '; '.join(f'{lab} {ctx.ratio(a, b)}:1' for a, b, lab in pairs)
        rows.append(f'<tr><td><span class="sw" aria-hidden="true" style="background:{v(path)}"></span></td><th scope="row">{name}'
                    f'<code>{C.css_name(path)}</code></th><td>{recipe} in OKLab<span class="hx">&#35;{hexv[1:]}</span></td>'
                    f'<td>{job}</td><td class="n">{meas}</td></tr>')
        alt_bits.append(f'{name}, {recipe}, {hexv}: {job}; {meas}')
    css = (f'.wr{{container-type:inline-size}}table{{width:100%;border-collapse:collapse;{ctx.ty("bodySmall")}}}'
           f'th,td{{text-align:left;vertical-align:top;padding:12px 12px 12px 0;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'thead th{{{ctx.ty("label")}}}tbody th{{{ctx.ty("ui")}}}tbody th code,.hx{{display:block;{ctx.ty("caption")};color:{v("oa.color.text.secondary.onNewsprint")}}}'
           f'.sw{{display:block;width:48px;height:48px;box-shadow:inset 0 0 0 1px {v("oa.color.border.strong.onNewsprint")}}}'
           f'.n{{{ctx.ty("dataLabel")}}}'
           f'@container (max-width:40rem){{thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}'
           f'table,tbody,tr,th,td{{display:block}}tr{{position:relative;padding:12px 0 12px 64px;border-bottom:1px solid {v("oa.color.border.hairline.onNewsprint")}}}'
           f'th,td{{padding:2px 0;border:0}}td:first-child{{position:absolute;left:0;top:14px}}}}')
    html = (f'<style>{css}</style><div class="wr"><table role="table"><thead><tr><th scope="col"><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)">Swatch</span></th><th scope="col">Name and token</th>'
            f'<th scope="col">Recipe</th><th scope="col">One job</th><th scope="col">Measured</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    ctx.spec('s-05-6-correct', html, '05', '05.6',
             'A table of six tints, each with its swatch, name, token, recipe, hex value, one job and measured ratio. '
             + ' '.join(b + '.' for b in alt_bits), readable=True,
             notes='A readable table (D2-255). Recipes read from each token\'s derivation in tokens.json; ratios computed '
                   'here.')

    # failure: a gray made with opacity
    comp = C.composite(ctx.hx(P('charcoal')), ctx.hx(P('newsprint')), 0.4)
    ro = ctx.ratio(comp, P('newsprint'), 'contrast Charcoal at 40 percent opacity on Newsprint')
    ctx.fig('Charcoal at 40 percent opacity on Newsprint, composited', comp, 'sRGB alpha compositing, as browsers paint it')
    rd = ctx.ratio('oa.color.derived.deepStone', P('newsprint'))
    cssf = (f'.cd{{padding:24px;border-top:4px solid {v("oa.color.border.strong.onNewsprint")}}}'
            f'.ey{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0;{ctx.ty("label")};color:{v("oa.color.text.secondary.onNewsprint")}}}'
            f'.ey .illus{{margin:0}}.hd{{margin:8px 0 0;{ctx.ty("h4")}}}'
            f'.mt{{margin:12px 0 0;{ctx.ty("caption")};color:{v(P("charcoal"))};opacity:.4}}')
    htmlf = (f'<style>{cssf}</style><div class="cd"><p class="ey"><span>Tracker · State bills</span>{B.ILLUS}</p>'
             f'<p class="hd">Paid family leave bill moves to a committee vote</p>'
             f'<p class="mt">Updated November 6, 2026 · two sources</p></div>')
    ctx.spec('s-05-6-failure', htmlf, '05', '05.6',
             f'An Illustrative tracker card on Newsprint with the kicker Tracker, State bills, the headline Paid family leave '
             f'bill moves to a committee vote, and a metadata line in Charcoal at 40 percent opacity that measures {ro} to 1.',
             width=360, illustrative=True, exempt=['contrast'],
             notes=f'Composite {comp}; the Deep Stone token measures {rd} to 1 on the same ground.')
    return len(tints), ro, rd


def s_05_7(ctx):
    v = ctx.v
    N = 'onNewsprint'
    steps = []
    words = ['Falls a lot', 'Falls a little', 'Little change', 'Rises a little', 'Rises a lot']
    arrows = ['▼▼', '▼', '■', '▲', '▲▲']
    Ls = []
    for i in range(1, 6):
        fill = f'oa.chart.color.diverging.fill.step{i}.{N}'
        lab = f'oa.chart.color.diverging.label.step{i}.{N}'
        r = ctx.ratio(lab, fill)
        L = C.oklab(ctx.hx(fill))[0]
        Ls.append(L)
        ctx.fig(f'OKLab lightness diverging step {i}', f'{L:.3f}', 'OKLab L of the token hex')
        steps.append((fill, lab, r, words[i - 1], arrows[i - 1], L))
    cells = ''.join(f'<li style="background:{v(f)};color:{v(l)}"><span class="ar" aria-hidden="true">{a}</span><span class="wd">{w}</span>'
                    f'<span class="rt">{r}:1</span></li>' for f, l, r, w, a, L in steps)
    gcells = ''.join(f'<li style="background:{v(f)};color:{v(l)}"><span class="ar" aria-hidden="true">{a}</span><span class="wd">{w}</span></li>'
                     for f, l, r, w, a, L in steps)
    seq, seq_r = [], []
    for i in range(1, 6):
        fill = f'oa.chart.color.sequential.fill.step{i}.{N}'
        lab = f'oa.chart.color.sequential.label.step{i}.{N}'
        r = ctx.ratio(lab, fill)
        seq_r.append(r)
        seq.append(f'<li style="background:{v(fill)};color:{v(lab)}"><span class="wd">Step {i}</span><span class="rt">{r}:1</span></li>')
    roles = [('Subject', 'oa.chart.color.subject.onNewsprint', 'The series the title names'),
             ('Context', 'oa.chart.color.context.onNewsprint', 'Every other series'),
             ('Gridline', 'oa.chart.color.gridline.onNewsprint', 'Decoration only'),
             ('The one point', 'oa.chart.color.point.onNewsprint', 'Working red, with a keyline')]
    rl, role_r = [], []
    for n, path, job in roles:
        r = ctx.ratio(path, P('newsprint'))
        role_r.append((n, r))
        edge = f';box-shadow:inset 0 0 0 1px {v("oa.chart.color.pointKeyline.onNewsprint")}' if 'point' in path else ''
        sw = ' data-red="swatch"' if 'point' in path else ''
        rl.append(f'<li><span class="ln"{sw} style="background:{v(path)}{edge}"></span><span><b>{n}</b> {job}<span class="rt2">{r}:1 on Newsprint</span></span></li>')
    # color-vision separation of the diverging scale's neighbors
    hexes = [ctx.hx(f) for f, *_ in steps]
    worst = {}
    for kind in ['normal'] + list(C.CVD):
        hs = hexes if kind == 'normal' else [C.simulate(h, kind) for h in hexes]
        worst[kind] = min(C.delta_ok(a, b) for a, b in zip(hs, hs[1:]))
        ctx.fig(f'diverging B smallest neighbor distance, {kind}', f'{worst[kind]:.3f}',
                'OKLab Euclidean distance between neighboring steps; Machado 2009 severity 1.0 in linear sRGB')
    css = (f'.k{{margin:24px 0 8px;{ctx.ty("label")};color:{v("oa.color.text.secondary." + N)}}}.k:first-child{{margin-top:0}}'
           f'.sc{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr))}}'
           f'.sc li{{display:flex;flex-direction:column;gap:2px;min-height:96px;padding:10px 8px}}'
           f'.ar{{display:inline-block;align-self:flex-start;padding:0 4px;border:1px solid currentColor;{ctx.ty("dataLabel")};line-height:1.4}}'
           f'.wd{{{ctx.ty("caption")};line-height:1.25;margin-top:4px}}.rt{{margin-top:auto;{ctx.ty("dataLabel")}}}'
           f'.g{{filter:grayscale(1)}}.g li{{min-height:72px}}'
           f'.rl{{list-style:none;margin:0;padding:0;display:grid;gap:12px 24px;grid-template-columns:repeat(auto-fill,minmax(min(100%,18rem),1fr));{ctx.ty("bodySmall")}}}'
           f'.rl li{{display:flex;gap:10px;align-items:flex-start}}.rl b{{font-weight:600}}.ln{{flex:none;width:28px;height:14px;margin-top:4px}}'
           f'.rt2{{display:block;{ctx.ty("caption")};color:{v("oa.color.text.secondary." + N)}}}'
           f'@container (max-width:30rem){{.sc li{{padding:8px 4px}}}}.wr{{container-type:inline-size}}')
    html = (f'<style>{css}</style><div class="wr">'
            f'<p class="k">Roles on Newsprint</p><ul class="rl">{"".join(rl)}</ul>'
            f'<p class="k">The diverging scale, Prussian to Verdigris, with the direction in a boxed arrow</p><ul class="sc">{cells}</ul>'
            f'<p class="k">The same scale in grayscale</p><ul class="sc g">{gcells}</ul>'
            f'<p class="k">Sequential Verdigris, for amounts with no direction</p><ul class="sc">{"".join(seq)}</ul></div>')
    div_txt = '; '.join(f'{w}, {a_w} arrow, label {r} to 1' for (f, l, r, w, a, L), a_w in
                        zip(steps, ['two down', 'one down', 'square', 'one up', 'two up']))
    ctx.spec('s-05-7-correct', html, '05', '05.7',
             'The chart palette on Newsprint. Four roles: '
             + ', '.join(f'{n} {r} to 1' for n, r in role_r)
             + '; the subject in Charcoal, the context in Stone, the gridline in a light Stone tint and the one point in '
             'Pillar Red with a Charcoal edge. The diverging scale in five steps from strong Prussian through a pale '
             f'midpoint to strong Verdigris, each with a boxed arrow, its words and its label ratio: {div_txt}. The same '
             'scale in grayscale, where both ends print dark. Sequential Verdigris in five steps, with label ratios '
             + ', '.join(seq_r[:-1]) + f' and {seq_r[-1]} to 1.',
             notes='Every fill and label is an oa.chart token; label ratios computed here.')
    # failure: a red to blue diverging scale
    fsteps = [(v(P('pillarRed')), v(P('white'))), (None, v(P('charcoal'))), (v('oa.chart.color.diverging.fill.step3.onNewsprint'), v(P('charcoal'))),
              (v('oa.chart.color.diverging.fill.step2.onNewsprint'), v(P('charcoal'))), (v(P('prussian')), v(P('white')))]
    fcells = []
    for i, (f, l) in enumerate(fsteps):
        if f is None:
            f = f'color-mix(in oklab, {v(P("pillarRed"))} 45%, {v(P("newsprint"))})'
        dr = ' data-red="working" data-red-job="rising values"' if i < 2 else ''
        fcells.append(f'<li{dr} style="background:{f};color:{l}"><span class="wd">{words[4 - i]}</span></li>')
    bcss, band = ctx.fail_band()
    cssf = (f'.sc{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr))}}'
            f'.sc li{{min-height:96px;padding:10px 8px}}.wd{{{ctx.ty("caption")};line-height:1.25}}'
            f'.k{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 8px;{ctx.ty("label")};color:{v("oa.color.text.secondary." + N)}}}'
            f'.k .illus{{margin:0}}{bcss}')
    htmlf = (f'<style>{cssf}</style>{band}<p class="k"><span>Change in turnout by state</span>{B.ILLUS}</p>'
             f'<ul class="sc">{"".join(fcells)}</ul>')
    ctx.spec('s-05-7-failure', htmlf, '05', '05.7',
             'A band across the top reads Failure case: do not publish. Below it, an Illustrative five-step scale labeled '
             'Change in turnout by state that runs from Pillar Red for Rises a lot through a pale midpoint to Prussian for '
             'Falls a lot, with no arrows.', illustrative=True, exempt=['contrast'],
             notes='The light red step is a color-mix() in the fragment, not a token, because the failure needs a red tint '
                   'the token set refuses. The band keeps the failure marked in any crop (BE-S4).')
    return worst, Ls, [st[2] for st in steps], seq_r


# ------------------------------------------------------------------------------------------------ the chapter
def build(ctx):
    v = ctx.ratio
    s_05_1(ctx)
    s_05_palette(ctx)
    s_05_2(ctx)
    s_05_roles(ctx)
    s_05_3(ctx)
    s_05_ask(ctx)
    s_05_4(ctx)
    rp, rk, rc, src = s_05_5(ctx)
    s_05_pairs(ctx)
    n_tints, r_opacity, r_deep = s_05_6(ctx)
    worst, Ls, div_r, seq_r = s_05_7(ctx)

    ch_n = v(P('charcoal'), P('newsprint'))
    st_n = v(P('stone'), P('newsprint'))
    ds_n = v('oa.color.derived.deepStone', P('newsprint'))
    ds_w = v('oa.color.derived.deepStone', P('white'))
    dn_c = v('oa.color.derived.dimNewsprint', P('charcoal'))
    dn_p = v('oa.color.derived.dimNewsprint', P('prussian'))
    w_p = v(P('white'), P('prussian'))
    n_c = v(P('newsprint'), P('charcoal'))
    ch_w = v(P('charcoal'), P('white'))
    red_n = v(P('pillarRed'), P('newsprint'))
    red_w = v(P('pillarRed'), P('white'))
    red_c = v(P('pillarRed'), P('charcoal'))
    red_p = v(P('pillarRed'), P('prussian'))
    ver_n = v(P('verdigris'), P('newsprint'))
    red_ver = v(P('pillarRed'), P('verdigris'))
    wl_red = v(P('white'), P('pillarRed'))
    n_pr = v(P('newsprint'), P('prussian'))
    eb_c = v(P('charcoal'), 'oa.color.derived.errorBand')
    stone_c = v(P('stone'), P('charcoal'))

    if ctx.stage == 'final':
        s1 = ctx.R['share s-05-1-correct']['shares']
        s1f = ctx.R['share s-05-1-failure']['shares']
        nc, nf = round(s1['newsprint']), round(s1f['newsprint'])
        rc_share = share_txt(ctx, 's-05-1-correct', 'pillarRed')
        chc = round(s1['charcoal'])
        prc = round(s1['prussian'])
        chf = round(s1f['charcoal'])
        prf = round(s1f['prussian'])
    else:
        nc = nf = chc = prc = chf = prf = 0
        rc_share = '0'

    RULE_053 = ("The wordmark’s ampersand and the lockmark’s lever are signature red and do not count, and neither do the "
                "ampersands inside the hinge diagram and the hinge-circle badge, which are identity marks. The hinge diagram "
                "never shares a view with the wordmark and never stands in for the hinge divider. An icon’s red accent counts "
                "as signature red when the icon stands alone, as an app tile, an avatar or a single feature icon. In a row or "
                "a menu, icons go one color and only the current one keeps its red, and that red counts as signature red. "
                "Each view (one screen, card, slide or printed page) then carries one working red, in this order of "
                "precedence: an error the reader must fix; the step a reader can take now; the one point the headline names, "
                "which in a systems figure is where a reform acts. One job may take several marks, such as each target of one "
                "reform. A hinge headline’s ampersand uses the view’s working red. The hinge divider’s ampersand takes its "
                "surface’s ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. In the guide "
                "itself, specimens, labeled failure cases and palette swatches do not count. Red never sits on Prussian.")
    # Rule 05.3 must match the token file's copy, which quotes D2-01 with DR-66, apostrophes aside
    src_rule = ctx.T.data.get('$extensions', {}).get('org.oathandaction', {}).get('redRule')
    if isinstance(src_rule, dict):
        src_rule = src_rule.get('text')
    if src_rule and src_rule.replace("'", '’') != RULE_053:
        raise ValueError('Rule 05.3 differs from the wording in tokens.json')
    ctx.fig('Rule 05.3 matches tokens.json redRule.text', 'yes' if src_rule else 'not found in tokens.json', 'string comparison, straight apostrophes read as curly')

    ch = {
        'number': '05', 'anchor': 'color', 'title': 'Color', 'part': 'Foundations',
        'instruction': 'Choose a surface first, then the text and graphic colors that pass on it.',
        'intro': [
            'Oath & Action works in seven colors, and each one has a job. Newsprint, a warm off-white, is the page most of '
            'our work sits on, and Charcoal carries the words. Pillar Red marks the one thing a reader should see first in '
            'each view, meaning each screen, card, slide or printed page. The other four do narrower work: Prussian, our '
            'dark blue, holds panels of dates and figures, Stone draws hairlines, Verdigris, a muted green, shows success '
            'and focus, and White serves specimens and email.',
            'Every pair in this chapter carries a contrast ratio, a measure of how far apart two colors sit in lightness. '
            'It runs from 1 to 1 for the same color up to 21 to 1 for black on white, by the formula in the Web Content '
            'Accessibility Guidelines (WCAG). We measured each ratio on the token values, the exact colors our code names. '
            'Pick the surface first, and the tables tell you which text and marks can sit on it.'],
        'rules': [
            {
                'id': '05.1', 'title': 'Cover most of every view in Newsprint.',
                'rule': ['Newsprint covers 60 to 85 percent of every view. A dark panel in Charcoal or Prussian marks a turn '
                         'in the reading, so a section holds one at most, and Pillar Red stays within 5 percent. Across a '
                         'body of work, the seven colors keep the shares in the palette sheet below this rule.'],
                'tokens': [P(k) for k in PAL],
                'why': {'text': ['A warm, light page keeps long reading calm, and readers come to know Newsprint as ours '
                                 'before they read a word. A dark panel works as a signal only while it stays rare. Each one '
                                 'tells the reader the section has turned, for example from an explanation to the dates '
                                 'that follow from it.'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-05-1-correct',
                            'caption': f'One view at true size: a phone page about a school board vote. Measured from the '
                                       f'rendered page, Newsprint covers {nc} percent. Charcoal covers {chc} percent as the one '
                                       f'dark panel, the type and the rules, and Pillar Red {rc_share}, counting the wordmark’s '
                                       f'ampersand.'},
                'failure': {'specimen': 's-05-1-failure',
                            'caption': f'<strong>Fails the proportion.</strong> The same page set on Charcoal and Prussian. '
                                       f'Newsprint falls to {nf} percent and dark surfaces take {chf + prf}, so no panel can '
                                       f'mark a turn. Every text pair here still passes 4.5 to 1, and the fault lies in how '
                                       f'much of the view is dark.'},
                'specs': [{'label': 'Newsprint in each view', 'value': '60 to 85 percent', 'token': P('newsprint')},
                          {'label': 'Dark panels', 'value': 'Charcoal or Prussian, one per section at most', 'token': 'oa.color.surface.prussian'},
                          {'label': 'Pillar Red in each view', 'value': 'Within 5 percent, signature red included', 'token': P('pillarRed')}] +
                         [{'label': f'{PNAME[k]} across a body of work', 'value': (f'{SHARE[k][0]} to {SHARE[k][1]} percent' if SHARE[k] else 'As needed'),
                           'token': P(k)} for k in PAL if k not in ('newsprint',)],
                'files': ['work/build/tokens/tokens.css', 'work/build/tokens/tokens.json'],
                'related': ['07', '12', '26'],
                'builders': ['Set a page’s ground with its surface class, such as <code>.oa-surface-newsprint</code>. The '
                             'class points the short names, such as <code>--oa-color-text-primary</code>, at that surface’s '
                             'tokens, so a panel changes surface with one class.'],
            },
            {
                'id': '05.2', 'title': 'Set text only on color pairs that pass.',
                'rule': ['Text under 24 px, or under 18.66 px in bold, needs a contrast ratio of 4.5 to 1 against its '
                         'surface, and larger text needs 3 to 1. Take the primary and secondary text tokens for the surface. '
                         'For any other pair, read its measured ratio in the tables below before you use it.'],
                'tokens': [f'oa.color.text.{r}.{ON[s]}' for r in ('primary', 'secondary') for s in SURF],
                'why': {'text': [f'WCAG 2.2 success criterion 1.4.3 Contrast (Minimum) sets 4.5 to 1 for text and 3 to 1 '
                                 f'for large text, which it defines as 18 point, or 14 point bold: 24 px and 18.66 px on '
                                 f'screen. Readers with low vision need that margin, and so does anyone reading a phone in '
                                 f'sunlight.',
                                 f'Stone, the secondary text color in our fifth edition, measures {st_n} to 1 on Newsprint. '
                                 f'Secondary text on light surfaces now takes Deep Stone, Stone mixed 18 percent toward '
                                 f'Charcoal, at {ds_n} to 1. On dark surfaces it takes Dim Newsprint, Newsprint mixed 25 '
                                 f'percent toward Charcoal, at {dn_c} to 1 on Charcoal and {dn_p} on Prussian.'],
                        'basis': 'WCAG 2.2 SC 1.4.3'},
                'correct': {'specimen': 's-05-2-correct',
                            'caption': f'The same short article on each surface at true size, body text at 17 px and '
                                       f'captions at 14 px. Primary text measures {ch_n} to 1 on Newsprint, {ch_w} on '
                                       f'White, {n_c} on Charcoal and {w_p} on Prussian; secondary text measures {ds_n}, '
                                       f'{ds_w}, {dn_c} and {dn_p}.'},
                'failure': {'specimen': 's-05-2-failure',
                            'caption': f'<strong>Fails 1.4.3.</strong> The caption in Stone measures {st_n} to 1 and the '
                                       f'red link {red_n} to 1, both under the 4.5 to 1 that 14 px text needs. A reader with '
                                       f'low vision loses the caption first, and the red link spends the view’s one red on '
                                       f'a line of small text.'},
                'specs': [{'label': f'{"Primary" if r == "primary" else "Secondary"} text on {SNAME[s]}',
                           'value': f'{ctx.hx("oa.color.text." + r + "." + ON[s])}, {v("oa.color.text." + r + "." + ON[s], "oa.color.surface." + s)} to 1',
                           'token': f'oa.color.text.{r}.{ON[s]}'} for s in SURF for r in ('primary', 'secondary')] + [
                          {'label': 'Large text starts at', 'value': '24 px, or 18.66 px bold', 'token': 'oa.type.h4'}],
                'files': ['work/build/tokens/tokens.css'],
                'related': ['06', '19', '26'],
                'builders': ['Choose the surface, then the role: secondary text on Prussian is '
                             '<code>--oa-color-text-secondary-on-prussian</code>. Inside a surface class, '
                             '<code>--oa-color-text-secondary</code> resolves to the same value. A pair with no token is a '
                             'pair we have not measured, so add a token under Rule 05.6 before you use it.'],
            },
            {
                'id': '05.3', 'title': 'Give each view one working red.',
                'rule': [RULE_053],
                'tokens': ['oa.color.identity.signature.onNewsprint', 'oa.color.state.error.mark.onNewsprint',
                           'oa.color.action.ask.fill.onNewsprint', 'oa.color.data.emphasisRed.onNewsprint',
                           'oa.component.button.ask.keyline.onNewsprint', 'oa.color.identity.hingeDivider.onNewsprint'],
                'why': {'text': ['One red tells the eye where to go first. The order settles which mark gets it when two '
                                 'compete: a reader has to fix an error before taking a step, and a step a reader can take '
                                 'matters more than a point we want to make. Signature red is part of the marks themselves, '
                                 'so it never competes with the working red.',
                                 f'Red never sits on Prussian, where it measures {red_p} to 1 and reads as a party pair of '
                                 f'red and blue. On Newsprint it measures {red_n} to 1, so a working red mark there takes a '
                                 f'keyline, a 1 px Charcoal edge drawn inside the mark (Rule 05.5).'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-05-3-correct',
                            'caption': 'One view at true size, with two reds. The wordmark’s ampersand is signature red and '
                                       'does not count. The button is the working red: Sign up to speak is the step a reader '
                                       'can take now. The hinge divider’s ampersand takes Charcoal, the ink of Newsprint. The '
                                       'dates sit on a Charcoal panel, and 24 px of Newsprint part it from the red button.'},
                'failure': {'specimen': 's-05-3-failure',
                            'caption': '<strong>Fails Rule 05.3.</strong> Three jobs share the red: the date in the headline, '
                                       'a bar under it and the button. The eye has nowhere to land first, and the red date '
                                       'also fails 3 to 1 as large text.'},
                'corrective': {'specimen': 's-05-3-corrective',
                               'caption': 'When the reader’s entry has an error, the error takes the view’s red and the ask '
                                          'steps down to the Charcoal primary button until the reader fixes it. The message '
                                          f'sits on the Error Band, where Charcoal text measures {eb_c} to 1.'},
                'specs': [
                    {'label': 'Signature red on Newsprint, White and Charcoal', 'value': f'Pillar Red; {red_n}, {red_w} and {red_c} to 1', 'token': 'oa.color.identity.signature.onNewsprint'},
                    {'label': 'Signature marks on Prussian', 'value': f'White, {w_p} to 1', 'token': 'oa.color.identity.signature.onPrussian'},
                    {'label': 'Working red, first claim', 'value': 'An error the reader must fix', 'token': 'oa.color.state.error.mark.onNewsprint'},
                    {'label': 'Working red, second claim', 'value': 'The step a reader can take now', 'token': 'oa.color.action.ask.fill.onNewsprint'},
                    {'label': 'Working red, third claim', 'value': 'The one point the headline names', 'token': 'oa.color.data.emphasisRed.onNewsprint'},
                    {'label': 'Keyline on a red mark on Newsprint', 'value': f'Charcoal, 1 px, {ch_n} to 1', 'token': 'oa.component.button.ask.keyline.onNewsprint'},
                    {'label': 'Hinge divider ampersand', 'value': 'Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian', 'token': 'oa.color.identity.hingeDivider.onNewsprint'},
                    {'label': 'Ask label', 'value': f'White on Pillar Red, {wl_red} to 1, 19 px bold or larger', 'token': 'oa.type.ask'},
                ],
                'files': [WORDMARK16, 'work/build/tokens/tokens.json'],
                'related': ['03', '04', '14', '17'],
                'builders': ['Count the reds before you ship a view. Mark each red element with <code>data-red</code>: '
                             '<code>signature</code> for the marks, <code>working</code> with <code>data-red-job</code> for '
                             'the one job. The shared check fails a view with two working jobs or any red over Prussian. '
                             'When an error appears, swap the ask to <code>--oa-component-button-primary-fill-on-newsprint</code>.'],
            },
            {
                'id': '05.4', 'title': 'Show every state with a word or a shape as well as a color.',
                'rule': ['Each interface state, from hover to error, changes its text or its shape along with its color. A '
                         'disabled control stays readable and says what will make it available. State colors are their own '
                         'set, kept apart from identity color and from the chart palettes in chapter 14.'],
                'tokens': ['oa.color.focus.ring.onNewsprint', 'oa.color.state.selected.band.onNewsprint',
                           'oa.color.state.selected.bar.onNewsprint', 'oa.color.state.warning.mark.onNewsprint',
                           'oa.color.state.error.band.onNewsprint', 'oa.color.state.error.mark.onNewsprint',
                           'oa.color.state.success.mark.onNewsprint', 'oa.color.state.disabled.edge.onNewsprint',
                           'oa.color.state.empty.edge.onNewsprint'],
                'why': {'text': [f'WCAG 2.2 success criterion 1.4.1 Use of Color asks that a state show something besides '
                                 f'color, and 1.4.11 Non-text Contrast asks 3 to 1 for the edges and focus rings that show '
                                 f'one. Pillar Red and Verdigris measure {red_ver} to 1 against each other, so a red error '
                                 f'and a Verdigris success look alike to many readers unless a word and a glyph differ too.'],
                        'basis': 'WCAG 2.2 SC 1.4.1 and 1.4.11'},
                'correct': {'specimen': 's-05-4-correct',
                            'caption': f'Ten states on Newsprint at true size, each with its cue. The focus ring measures '
                                       f'{ver_n} to 1, the warning mark {ch_n} and the error glyph keeps a Charcoal edge. '
                                       f'Nothing here uses opacity.'},
                'failure': {'specimen': 's-05-4-failure',
                            'caption': f'<strong>Fails 1.4.1.</strong> Two tracker rows that differ only by the hue of a '
                                       f'dot. The dots measure {red_ver} to 1 against each other, and in grayscale they print '
                                       f'as {C.css_gray(ctx.hx(P("pillarRed")))} and {C.css_gray(ctx.hx(P("verdigris")))}, two '
                                       f'near grays that say nothing about which row has the problem.'},
                'specs': [
                    {'label': 'Focus ring on light surfaces', 'value': f'Verdigris, 2 px, 2 px gap; {ver_n} to 1 on Newsprint', 'token': 'oa.color.focus.ring.onNewsprint'},
                    {'label': 'Focus ring on dark surfaces', 'value': f'Newsprint; {n_c} to 1 on Charcoal, {n_pr} on Prussian', 'token': 'oa.color.focus.ring.onCharcoal'},
                    {'label': 'Selected', 'value': 'The paired surface, a 4 px bar and a check glyph', 'token': 'oa.color.state.selected.band.onNewsprint'},
                    {'label': 'Error ground', 'value': f'Error Band, {ctx.hx("oa.color.derived.errorBand")}; Charcoal text {eb_c} to 1', 'token': 'oa.color.state.error.band.onNewsprint'},
                    {'label': 'Disabled', 'value': f'Deep Stone text and dashed edge, {ds_n} to 1, with a reason line', 'token': 'oa.color.state.disabled.text.onNewsprint'},
                    {'label': 'State bar', 'value': '4 px', 'token': 'oa.border.width.bar'},
                ],
                'related': ['11', '17', '18'],
                'builders': ['Change two things in every state: the color and either the words or the shape. Use '
                             '<code>aria-disabled="true"</code> so a disabled control keeps its focus and its reason line can '
                             'be read. Never fade a control with opacity; take the state token instead.'],
            },
            {
                'id': '05.5', 'title': 'Keep marks that carry meaning at 3 to 1, and give red on Newsprint a Charcoal keyline.',
                'rule': [f'An icon, a chart mark, a control’s edge or a focus ring needs a ratio of 3 to 1 against its '
                         f'surface. Pillar Red measures {red_n} to 1 on Newsprint, so a red mark that carries meaning there '
                         f'takes a 1 px Charcoal keyline. Stone passes for marks on light surfaces, and a hairline that '
                         f'carries no meaning may sit lower.'],
                'tokens': ['oa.color.graphic.essential.onNewsprint', 'oa.color.graphic.subtle.onNewsprint',
                           'oa.color.border.strong.onNewsprint', 'oa.color.border.hairline.onNewsprint',
                           'oa.chart.color.pointKeyline.onNewsprint', 'oa.border.width.hairline'],
                'why': {'text': [f'WCAG 2.2 success criterion 1.4.11 Non-text Contrast asks 3 to 1 for the parts of a '
                                 f'graphic a reader needs and for the edges of controls. The keyline gives a red mark an edge '
                                 f'the eye can find, at {rk} to 1, and the fill keeps its red. Stone context bars measure '
                                 f'{rc} to 1, so they pass without help.'],
                        'basis': 'WCAG 2.2 SC 1.4.11'},
                'correct': {'specimen': 's-05-5-correct',
                            'caption': f'A finding at true size, 600 px wide. The bar the title names takes the view’s working red with a '
                                       f'1 px Charcoal keyline at {rk} to 1; the other sectors stay in Stone at {rc} to 1.'},
                'failure': {'specimen': 's-05-5-failure',
                            'caption': f'<strong>Fails 1.4.11.</strong> Without its keyline the red bar measures {rp} to 1 '
                                       f'against Newsprint, under the 3 to 1 a mark needs, and its edge softens into the page.'},
                'specs': [
                    {'label': 'Essential marks on Newsprint', 'value': f'Charcoal, {ch_n} to 1', 'token': 'oa.color.graphic.essential.onNewsprint'},
                    {'label': 'Supporting marks on Newsprint', 'value': f'Stone, {st_n} to 1', 'token': 'oa.color.graphic.subtle.onNewsprint'},
                    {'label': 'Control edges on Newsprint', 'value': f'Charcoal, {ch_n} to 1', 'token': 'oa.color.border.strong.onNewsprint'},
                    {'label': 'Hairline on Newsprint', 'value': f'Stone, {st_n} to 1, decoration only', 'token': 'oa.color.border.hairline.onNewsprint'},
                    {'label': 'Hairline on Charcoal', 'value': f'Stone, {stone_c} to 1, decoration only', 'token': 'oa.color.border.hairline.onCharcoal'},
                    {'label': 'Keyline on red', 'value': '1 px Charcoal, inside the mark', 'token': 'oa.border.width.hairline'},
                ],
                'sources_note': None,
                'related': ['12', '14', '18'],
                'builders': ['Draw the keyline inside the shape, with <code>box-shadow: inset 0 0 0 1px</code> in HTML or a '
                             '1 px stroke on an inner path in SVG, so the mark keeps its size. On White and Charcoal, where '
                             f'red measures {red_w} and {red_c} to 1, a red mark needs no keyline.'],
            },
            {
                'id': '05.6', 'title': 'Give each tint one named job, and keep tints off identity marks.',
                'rule': ['A tint is one palette color mixed toward Newsprint or Charcoal by a recorded amount, for one job. '
                         'It enters only as a token, with its measured ratio. The wordmark, the ampersand, the lockmark and '
                         'the pillar marks stay in solid palette colors, and no color on a page comes from lowering opacity.'],
                'tokens': ['oa.color.derived.deepStone', 'oa.color.derived.dimNewsprint', 'oa.color.derived.errorBand',
                           'oa.color.tint.stoneN70', 'oa.color.tint.prussianN62', 'oa.color.tint.verdigrisN55'],
                'why': {'text': ['Our fifth edition said “There are no tints.” Charts, error messages and selected rows need '
                                 'lighter and darker steps that no palette color supplies, so Edition 06 allows a tint that '
                                 'meets five conditions: a measured need, a recorded mix, one job, a passing ratio on every '
                                 'surface it serves and a registered token.',
                                 f'We mix in OKLab, a color space where equal steps look equal, which keeps a tint’s hue '
                                 f'steady as it lightens. Opacity gives up that control. Charcoal at 40 percent on Newsprint '
                                 f'measures {r_opacity} to 1, where the Deep Stone token measures {r_deep}.'],
                        'basis': 'Design judgment'},
                'correct': {'specimen': 's-05-6-correct',
                            'caption': f'Six of the token set’s tints, each with its recipe, its one job and its measured '
                                       f'ratio. The set holds three derived colors and {n_tints} chart tints; chapter 26 '
                                       f'lists every one.'},
                'failure': {'specimen': 's-05-6-failure',
                            'caption': f'<strong>Fails 1.4.3 and Rule 05.6.</strong> The date line is Charcoal at 40 percent '
                                       f'opacity, a gray no token names. It measures {r_opacity} to 1, and its color changes '
                                       f'with whatever sits behind it.'},
                'specs': [
                    {'label': 'Deep Stone', 'value': f'{ctx.hx("oa.color.derived.deepStone")}, Stone 18% toward Charcoal; {ds_n} to 1 on Newsprint, {ds_w} on White', 'token': 'oa.color.derived.deepStone'},
                    {'label': 'Dim Newsprint', 'value': f'{ctx.hx("oa.color.derived.dimNewsprint")}, Newsprint 25% toward Charcoal; {dn_c} to 1 on Charcoal, {dn_p} on Prussian', 'token': 'oa.color.derived.dimNewsprint'},
                    {'label': 'Error Band', 'value': f'{ctx.hx("oa.color.derived.errorBand")}, Pillar Red 88% toward Newsprint; Charcoal text {eb_c} to 1', 'token': 'oa.color.derived.errorBand'},
                    {'label': 'Opacity', 'value': 'Two decorative watermarks only, never text or marks', 'token': 'oa.opacity.watermarkOnLight'},
                ],
                'files': ['work/build/tokens/src/oa-tokens.src.mjs'],
                'related': ['12', '14', '26'],
                'builders': ['Write a new tint as a recipe in the token source, such as '
                             '<code>mix(\'stone\', \'newsprint\', 0.70)</code>, and keep hex values out of pages. The '
                             'generator computes the hex and every '
                             'ratio, and the rule test fails a tint with no registered need. In CSS the same mix is '
                             '<code>color-mix(in oklab, var(--oa-color-palette-stone), var(--oa-color-palette-newsprint) 70%)</code>.'],
            },
            {
                'id': '05.7', 'title': 'Set charts and the atlas on Newsprint, in the chart palette.',
                'rule': ['Newsprint is the page color for charts and the atlas. The series a title names takes Charcoal, and '
                         'every other series takes Stone. When the title names one point, such as a single bar, that point '
                         'takes the view’s working red with a Charcoal keyline, as in Rule 05.5. Values that rise and fall '
                         'from a midpoint take the diverging scale, which runs from Prussian through a pale middle to '
                         'Verdigris, with an arrow or a printed sign for the direction. Every party takes one neutral ink, '
                         'with its name printed on the mark.'],
                'tokens': ['oa.chart.color.subject.onNewsprint', 'oa.chart.color.context.onNewsprint',
                           'oa.chart.color.diverging.fill.step1.onNewsprint', 'oa.chart.color.diverging.fill.step5.onNewsprint',
                           'oa.chart.color.sequential.fill.step5.onNewsprint', 'oa.chart.color.party.mark.onNewsprint',
                           'oa.chart.color.point.onNewsprint'],
                'why': {'text': ['Neither end of the diverging scale belongs to a party, so a reader sees a rise or a fall '
                                 'before any side. A scale from red to blue reads as a party split in the United States, and '
                                 'Rule 01.3 keeps it out of our charts. Both ends of our scale print as dark grays, so the '
                                 'arrow carries the direction for any reader who cannot tell the hues apart. On Newsprint, a '
                                 'chart shared on its own still reads as ours.'],
                        'basis': 'Design judgment; Rules 01.1 and 01.3'},
                'correct': {'specimen': 's-05-7-correct',
                            'caption': 'The chart palette on Newsprint at true size: four roles, the diverging scale with its '
                                       'boxed arrows, the same scale in grayscale and the sequential Verdigris steps. Every '
                                       'label on a fill passes 4.5 to 1. Chapter 14 holds the full chart palette, with the '
                                       'dark ground and the grayscale proofs of each chart.'},
                'failure': {'specimen': 's-05-7-failure',
                            'caption': '<strong>Fails Rules 01.1 and 01.3.</strong> A scale from red to blue reads as '
                                       'Republican against Democratic before anyone reads its key, and it spends the view’s '
                                       'red on every rising cell.'},
                'specs': [
                    {'label': 'Chart ground', 'value': 'Newsprint; Charcoal for dark views', 'token': 'oa.color.surface.newsprint'},
                    {'label': 'Subject', 'value': f'Charcoal, {ch_n} to 1', 'token': 'oa.chart.color.subject.onNewsprint'},
                    {'label': 'Context', 'value': f'Stone, {st_n} to 1', 'token': 'oa.chart.color.context.onNewsprint'},
                    {'label': 'The one point', 'value': f'Pillar Red, {red_n} to 1, with a 1 px Charcoal keyline at {ch_n} to 1', 'token': 'oa.chart.color.point.onNewsprint'},
                    {'label': 'Diverging scale', 'value': 'Prussian, light Prussian, a pale midpoint, light Verdigris, strong Verdigris', 'token': 'oa.chart.color.diverging.fill.step1.onNewsprint'},
                    {'label': 'Labels on the diverging scale', 'value': f'{div_r[0]}, {div_r[1]}, {div_r[2]}, {div_r[3]} and {div_r[4]} to 1, from Prussian to Verdigris', 'token': 'oa.chart.color.diverging.label.step1.onNewsprint'},
                    {'label': 'Labels on sequential Verdigris', 'value': f'{seq_r[0]}, {seq_r[1]}, {seq_r[2]}, {seq_r[3]} and {seq_r[4]} to 1, from step 1 to step 5', 'token': 'oa.chart.color.sequential.label.step1.onNewsprint'},
                    {'label': 'Neighboring steps under color-vision simulation', 'value': f'At least {min(worst.values()):.3f} apart in OKLab, about {min(worst.values()) / 0.02:.0f} times the 0.02 that CSS Color 4 treats as the smallest visible difference', 'token': None},
                    {'label': 'Lightness in grayscale', 'value': f'Ends at {Ls[0]:.2f} and {Ls[4]:.2f}, the midpoint at {Ls[2]:.2f}, in OKLab lightness', 'token': None},
                    {'label': 'Party marks', 'value': 'One neutral ink, the party’s name on the mark', 'token': 'oa.chart.color.party.mark.onNewsprint'},
                    {'label': 'Measurements', 'value': 'Our palette measurements on White, Newsprint and Charcoal, November 6, 2026', 'token': None},
                ],
                'files': ['work/boards/phase-2/data-viz/shared/20261106_Palette-Lab.json'],
                'related': ['13', '14', '15', '21'],
                'builders': ['Take chart colors from <code>oa.chart.color</code>, whose tokens follow the page color. The '
                             'diverging scale exists on Newsprint only until a Charcoal ramp is measured. Print the value or '
                             'the direction on every diverging cell.'],
            },
        ],
        'extras': [
            {'after_rule': '05.1', 'specimen': 's-05-palette', 'label': 'The seven colors',
             'caption': 'The seven colors with their values, jobs and shares across a body of work. The hex values are '
                        'locked in our identity rules, and the shares come from our fifth edition.'},
            {'after_rule': '05.2', 'specimen': 's-05-roles', 'label': 'Color roles on each surface',
             'caption': 'Text-safe and graphic-safe roles on each surface. Every ratio is measured against its surface on the '
                        'token values. Text roles need 4.5 to 1, marks and edges 3 to 1, and hairlines carry no meaning.'},
            {'after_rule': '05.3', 'specimen': 's-05-ask', 'label': 'The ask on four surfaces',
             'caption': f'The ask on each surface at true size. White on Pillar Red measures {wl_red} to 1, which passes only '
                        f'as large text, so the label never sets below 19 px bold. On Prussian the ask turns Newsprint.'},
            {'after_rule': '05.5', 'specimen': 's-05-pairs', 'label': 'Every palette pair, measured',
             'caption': 'Every palette pair, measured. “Text at any size” means 4.5 to 1 or more; “Large text and marks” '
                        'means 3 to 1 or more. Pillar Red never sets text, whatever its ratio.'},
        ],
        'sources': [src,
                    'W3C, Web Content Accessibility Guidelines (WCAG) 2.2, W3C Recommendation, success criteria 1.4.1, 1.4.3 '
                    'and 1.4.11, https://www.w3.org/TR/WCAG22/.',
                    'W3C, CSS Color Module Level 4, Candidate Recommendation Draft, the gamut-mapping algorithm’s '
                    'just-noticeable difference, an OKLCh difference of 0.02, https://www.w3.org/TR/css-color-4/. Retrieved November 6, 2026.',
                    'Machado, G. M., Oliveira, M. M. and Fernandes, L. A. F., “A Physiologically-based Model for Simulation of '
                    'Color Vision Deficiency,” IEEE Transactions on Visualization and Computer Graphics 15, no. 6 (2009), '
                    'severity 1.0, as the palette lab applies it.'],
    }
    # drop helper keys the contract does not hold
    for r in ch['rules']:
        r.pop('sources_note', None)
        r['specs'] = [{k: x for k, x in s.items() if x is not None} for s in r['specs']]
    return ch
