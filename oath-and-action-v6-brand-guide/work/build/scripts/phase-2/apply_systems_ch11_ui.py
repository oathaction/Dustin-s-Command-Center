"""Chapter 11, round 2 (systems designer, November 10, 2026): the utility icons, the error, success and warning marks,
and the five live specimens (D2-516), as rules 11.11 to 11.16. apply_systems_ch11.py calls build_ui() and owns the
chapter file; this module holds the words, the specimens and their scripts.

Sources: the accessibility audit (20261109_Stage-B-Accessibility-Audit.md, sections 1 and 2), the utility finals and their
manifest (work/build/assets/utility/, DR-161 to DR-178), the engineer's <use> pattern (20261110_Promotion-Engineer-Notes.md),
Rule 05.3's order of precedence for the working red, and Atlas V7's loop R10 for the stepper.

Live specimens are components, not pictures: manifest "interactive": true, so the shell names the stage as a group and
guide_check.js runs its name, target, keyboard, focus, state and forced-color checks inside them. Each component sets
forced-color-adjust back to auto, so its controls take the system's colors as a product's would, while the stage around
it keeps the guide's (AX-S6). Scripts find their elements by data attributes from document.currentScript, since the build
prefixes every id and every class in a specimen.
"""
import json
import re

LOOP_ID = 'R10'
CHECK_41 = ('CL-001 CL-004 CL-006 CL-010 CL-013 CL-019 CL-020 CL-021 CL-022 CL-023 CL-024 CL-028 CL-031 CL-032 CL-039 '
            'CL-040 CL-047 CL-048 CL-050 CL-051 CL-054 CL-057 CL-060 CL-061 CL-067 CL-068 CL-070 CL-071 CL-072 R-05 R-06 '
            'R-08 R-09 R-14 R-15 R-17 R-19 R-23 R-27 R-37 R-45').split()   # chapter 10's construction text, section 10

# The 18 finals in the order of the audit's ranks, with the words that go beside each (audit 1.1 and 1.2; the manifest)
ICONS = [
    ('close', 'Close', 'Close, or Close the menu where two things could close'),
    ('menu', 'Menu', 'Menu'),
    ('arrow', 'Arrow', 'Next page; mirrored, Previous page; turned up or down, the order a column is sorted in'),
    ('chevron', 'Chevron', 'The row’s own words; down while closed, up while open'),
    ('download', 'Download', 'Download, then the file, its type and its size'),
    ('another-site', 'Another site', 'After a link’s last word, with the hidden words “(another site)”'),
    ('search', 'Search', 'The field’s label, such as Search the symbols'),
    ('filter', 'Filter', 'Filters, and how many are on'),
    ('copy', 'Copy', 'Copy, and what it copies'),
    ('play', 'Play', 'Play, or Play again once the run has ended'),
    ('pause', 'Pause', 'Pause, on the same button while it plays'),
    ('reset', 'Reset', 'Reset or Start over, with its object, such as Reset the loop'),
    ('error', 'Error', 'Error, then the fix, such as Enter a ZIP code with five digits'),
    ('success', 'Success', 'What happened, such as You’re signed up'),
    ('selected-check', 'Selected check', 'A chip’s own word, while the chip is on'),
    ('view-full-size', 'View full size', 'View the map full size'),
    ('sort', 'Sort', 'Beside a column heading’s word'),
    ('warning', 'Warning', 'The notice, such as Checked April 20'),
]
MIRROR = {24: 'matrix(-1 0 0 1 24 0)', 16: 'matrix(-1 0 0 1 16 0)'}
OPEN = {24: 'rotate(180 12 12)', 16: 'rotate(180 8 8)'}
TURN_RIGHT = {24: 'rotate(-90 12 12)'}


def tpl(html):
    """A hidden copy of markup a script inserts later: the build finds its <use> and puts the symbol in the sprite."""
    return f'<template data-tpl>{html}</template>'


def ui_css(ctx, live=True):
    """The controls every live specimen shares: a 44 px button with its icon before its word, the unavailable state with
    its reason, the focus ring and the visually hidden text. Colors from the Newsprint surface's tokens."""
    T, v = ctx.ty, ctx.v
    for k in ('text.primary', 'text.secondary', 'border.strong', 'border.hairline', 'focus.ring'):
        v(f'oa.color.{k}.onNewsprint')        # recorded; the short names below point at these on a Newsprint stage
    return (f':scope{{--ink:{v("oa.color.text.primary")};--sec:{v("oa.color.text.secondary")};'
            f'--edge:{v("oa.color.border.strong")};--hair:{v("oa.color.border.hairline")};'
            f'--ring:{v("oa.color.focus.ring")};--ground:{v("oa.color.surface.newsprint")};'
            f'--paper:{v("oa.color.surface.white")};--dis:{v("oa.component.button.disabled.label.onNewsprint")};'
            f'--disedge:{v("oa.component.button.disabled.edge.onNewsprint")};--touch:{v("oa.size.target.touch")}}}'
            f'.ui{{{"forced-color-adjust:auto;" if live else ""}background:var(--ground);color:var(--ink);padding:20px 16px 24px;{T("body")}}}'
            f':where(.ui p){{margin:0}}'
            f'.ui .b{{display:inline-flex;align-items:center;gap:8px;min-height:var(--touch);min-width:var(--touch);margin:0;'
            f'padding:0 14px 0 10px;border:1px solid var(--edge);border-radius:0;background:var(--ground);color:var(--ink);'
            f'{T("ui")};text-align:left;cursor:pointer}}'
            f'.ui .b svg{{flex:none;display:block}}.ui .b.nx{{padding:0 10px 0 14px}}.ui .b.wd{{padding:0 14px}}'
            f'.ui .b:hover{{box-shadow:inset 0 0 0 1px var(--edge)}}'
            f'.ui :focus-visible{{outline:2px solid var(--ring);outline-offset:2px}}'
            f'.ui .b[aria-disabled="true"]{{color:var(--dis);border-style:dashed;border-color:var(--disedge);cursor:not-allowed;box-shadow:none}}'
            f'.why{{margin-top:8px;{T("bodySmall")};color:var(--sec);min-height:1.5em}}'
            f'.vh{{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}}'
            f'.lab{{{T("label")};color:var(--sec)}}')


def script(js):
    """A specimen's script, wrapped so it finds its own stage and touches nothing outside it."""
    js = re.sub(r'\s*\n\s*', ' ', js.strip())
    return f'<script>(function(){{var S=document.currentScript.closest("[data-specimen]");if(!S)return;{js}}})();</script>'


# ------------------------------------------------------------------------------------------------ 11.11 the reader
def s_reader(ctx, m):
    T, u = ctx.ty, m.uicon
    css = ui_css(ctx) + (
        f'.rn{{margin:8px 0 12px;{T("h4", "floor")}}}'
        f'.vw{{overflow-x:auto;margin:0 0 12px;border:1px solid var(--hair);background:var(--paper)}}'
        f'.pg{{width:100%;box-sizing:border-box;padding:16px;min-height:132px}}'
        f'[data-zoom="full"] .pg{{width:480px}}'
        f'.pr{{{T("label")};color:var(--sec)}}.pt{{margin-top:8px;{T("h4", "floor")}}}'
        f'.ln{{display:block;height:8px;margin-top:10px;background:var(--hair)}}.ln.s{{width:62%}}'
        f'.pn{{margin:0 0 10px;{T("ui")};font-variant-numeric:tabular-nums}}'
        f'.bar{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.ui .bar .b{{padding:0 10px;white-space:nowrap}}'
        f'.ui .bar .nx{{justify-content:flex-end}}'
        f'.zm{{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}}'
        f'.ui .zm .b[aria-pressed="true"]{{font-weight:700;text-decoration:underline;text-decoration-thickness:2px;'
        f'text-underline-offset:4px;box-shadow:inset 0 0 0 1px var(--edge)}}')
    html = (f'<style>{css}</style><div class="ui" data-ui="reader"><p><span class="illus">Illustrative</span></p>'
            f'<p class="rn">How a county pays for its roads</p>'
            f'<div class="vw" role="group" aria-label="The report page" tabindex="0" data-view data-zoom="fit"><div class="pg" aria-hidden="true">'
            f'<p class="pr">How a county pays for its roads · page <span data-out="pg">1</span></p>'
            f'<p class="pt" data-out="pt">Where the money comes from</p><span class="ln"></span><span class="ln"></span>'
            f'<span class="ln s"></span></div></div>'
            f'<p class="pn" role="status" data-out="n">Page 1 of 12</p>'
            f'<div class="bar" role="group" aria-label="Pages">'
            f'<button type="button" class="b" data-act="prev" aria-disabled="true" aria-describedby="rd-why">'
            f'{u("arrow", transform=MIRROR[24])}Previous page</button>'
            f'<button type="button" class="b nx" data-act="next">Next page{u("arrow")}</button></div>'
            f'<p class="why" id="rd-why" data-out="why">This is the first page.</p>'
            f'<div class="zm" role="group" aria-label="Page size">'
            f'<button type="button" class="b wd" aria-pressed="true" data-zoom="fit">Fit width</button>'
            f'<button type="button" class="b wd" aria-pressed="false" data-zoom="full">Full size</button></div>'
            + script('''
var R=S.querySelector('[data-ui="reader"]'),n=1,N=12,
P=R.querySelector('[data-act="prev"]'),X=R.querySelector('[data-act="next"]'),
O=R.querySelector('[data-out="n"]'),W=R.querySelector('[data-out="why"]'),G=R.querySelector('[data-out="pg"]'),
H=R.querySelector('[data-out="pt"]'),V=R.querySelector('[data-view]'),
T=['Where the money comes from','What a mile of road costs','Repairs that wait','Who decides the list'];
function off(b,y){if(y){b.setAttribute('aria-disabled','true');b.setAttribute('aria-describedby',W.id);}
else{b.removeAttribute('aria-disabled');b.removeAttribute('aria-describedby');}}
function draw(){O.textContent='Page '+n+' of '+N;G.textContent=n;H.textContent=T[(n-1)%4];off(P,n===1);off(X,n===N);
W.textContent=n===1?'This is the first page.':(n===N?'This is the last page.':'');}
P.addEventListener('click',function(){if(n>1){n--;draw();}});
X.addEventListener('click',function(){if(n<N){n++;draw();}});
R.querySelectorAll('[data-zoom][aria-pressed]').forEach(function(b){b.addEventListener('click',function(){
R.querySelectorAll('[data-zoom][aria-pressed]').forEach(function(c){c.setAttribute('aria-pressed',c===b?'true':'false');});
V.setAttribute('data-zoom',b.getAttribute('data-zoom'));});});
draw();''') + '</div>')
    alt = ('A live report reader at 360 px, Illustrative. A page of the report How a county pays for its roads sits in a '
           'frame, with “Page 1 of 12” under it. Two buttons follow, Previous page with the arrow mirrored before its '
           'word and Next page with the arrow after it, each 44 px tall. On the first page, Previous page is unavailable: '
           'its outline is dashed, and the line under it says “This is the first page.” Two word buttons, Fit width and '
           'Full size, change the size of the page; Fit width is pressed, bold and underlined.')
    return m.spec(ctx, 's-11-11-correct', html, '11.11', alt, width=360, interactive=True, illustrative=True,
                  notes='Live (D2-516). Previous page keeps focus while unavailable, with aria-disabled and its reason '
                        'through aria-describedby (G-4); the page count is a polite status line (A-9); zoom stays words '
                        '(DR-154).')


def s_reader_fail(ctx, m):
    T, u = ctx.ty, m.uicon
    fcss, band = ctx.fail_band(flush=True)
    info = ('<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" '
            'r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 11v6M12 7.5v.5" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')
    css = ui_css(ctx, live=False) + fcss + (
        f'.bar{{display:flex;gap:6px;align-items:center;margin-top:44px}}'
        f'.g{{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border:1px solid var(--edge)}}'
        f'.pn{{margin:0 6px;{T("ui")}}}.tw{{position:relative}}'
        f'.tt{{position:absolute;right:-4px;bottom:40px;white-space:nowrap;padding:6px 10px;background:var(--ink);'
        f'color:var(--ground);{T("caption")}}}'
        f'.ps{{margin-left:auto}}.cur{{position:absolute;right:6px;top:18px}}')
    cursor = ('<svg class="cur" viewBox="0 0 16 20" width="16" height="20" aria-hidden="true" focusable="false"><path '
              'd="M1 1v15l4-4 3 7 3-1.5-3-6.5h6z" style="fill:var(--ground);stroke:var(--ink)" stroke-width="1.2"/></svg>')
    html = (f'<style>{css}</style>{band}<div class="ui"><p><span class="illus">Illustrative</span></p>'
            f'<div class="bar"><span class="g">{u("arrow", transform=MIRROR[24])}</span><span class="pn">1 / 12</span>'
            f'<span class="g">{u("arrow")}</span><span class="tw ps"><span class="g">{info}</span>'
            f'<span class="tt">About this report</span>{cursor}</span>'
            f'<span class="g">{u("view-full-size")}</span></div></div>')
    alt = ('Labeled Failure case: do not publish. An Illustrative report toolbar at 360 px with four buttons that show '
           'icons and no words: a left arrow, “1 / 12”, a right arrow, an information mark and four corners. Each button '
           'is 32 px square. A pointer hovers over the information mark, and a dark box above it reads “About this '
           'report”, the only place the button’s name appears.')
    return m.spec(ctx, 's-11-11-failure', html, '11.11', alt, width=360, illustrative=True,
                  notes='Picture of a fault: glyph-only buttons, 32 px targets, a name shown only on hover (SC 1.4.13, '
                        '2.5.3). The information mark is drawn here as the fault and is no icon of the set (DR-154).')


def s_icons(ctx, m):
    """The 18 finals with their words, at 24 and 16 px: a readable list (D2-255)."""
    T, u = ctx.ty, m.uicon
    css = (f'.ic{{list-style:none;margin:0;padding:0;border-top:1px solid {ctx.v("oa.color.border.hairline.onNewsprint")};'
           f'display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,17rem),1fr));column-gap:24px}}'
           f'.ic li{{display:grid;grid-template-columns:64px minmax(0,1fr);gap:12px;align-items:start;padding:12px 0;'
           f'border-bottom:1px solid {ctx.v("oa.color.border.hairline.onNewsprint")}}}'
           f'.g{{display:flex;align-items:center;gap:12px;height:24px;margin-top:1px;color:{ctx.v("oa.component.icon.ink.onNewsprint")}}}'
           f'.g svg{{display:block;flex:none}}'
           f'.nm{{display:block;{T("ui")};font-weight:700}}.wd{{display:block;margin-top:2px;{T("caption")};'
           f'color:{ctx.v("oa.color.text.secondary.onNewsprint")};text-wrap:pretty}}'
           f'.hd{{margin:0 0 12px;{T("caption")};color:{ctx.v("oa.color.text.secondary.onNewsprint")}}}')
    lis = ''.join(f'<li><span class="g">{u(k, 24)}{u(k, 16)}</span><span><span class="nm">{nm}</span>'
                  f'<span class="wd">{w}</span></span></li>' for k, nm, w in ICONS)
    html = (f'<style>{css}</style><p class="hd">Each icon at 24 px, then its own 16 px drawing, with the word that goes '
            f'beside it.</p><ul class="ic">{lis}</ul>')
    alt = ('The 18 utility icons, each drawn at 24 px and then at 16 px from its own 16 px drawing, with its name and the '
           'word that goes beside it. ' + ' '.join(f'{nm}: {w}.' for _, nm, w in ICONS))
    return m.spec(ctx, 's-11-icons', html, None, alt, readable=True,
                  notes='A readable list (D2-255) of the 18 finals in the audit’s order, drawn from the sprite: '
                        'oa-sym-u-<name>-24px and -16px (DR-161 to DR-178).')


# ------------------------------------------------------------------------------------------------ 11.12 the library and the phone menu
def library_data(m):
    lab = json.loads((m.ROOT / 'work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json').read_text())
    kind = {'topic': 't', 'atlas variable': 'a', 'atlas reform': 'a', 'topic and atlas variable': 'ta', 'pillar': 'p'}
    rows = [[r['id'], r['label'], kind[r['class']], 1 if r['id'] in CHECK_41 else 0] for r in lab['rows']]
    if len(rows) != 124 or sum(r[3] for r in rows) != 41:
        raise SystemExit(f'library data: {len(rows)} rows and {sum(r[3] for r in rows)} at 24 px; chapter 10 holds 124 and 41')
    return rows


def s_library(ctx, m):
    T, u = ctx.ty, m.uicon
    rows = library_data(m)
    n_atlas = sum(1 for r in rows if 'a' in r[2])
    css = ui_css(ctx) + (
        f'.l{{display:block;margin:0 0 6px;{T("ui")};font-weight:600}}'
        f'.fd{{display:flex;align-items:center;min-height:var(--touch);border:1px solid var(--edge);background:var(--paper)}}'
        f'.fd > svg{{flex:none;margin:0 8px 0 10px}}'
        f'.ui .q{{flex:1 1 auto;min-width:0;align-self:stretch;margin:0;padding:0 4px;border:0;background:transparent;'
        f'color:var(--ink);{T("body")}}}'
        f'.ui .clr{{display:inline-flex;align-items:center;justify-content:center;width:var(--touch);height:var(--touch);'
        f'margin:-1px -1px -1px 0;padding:0;border:0;background:transparent;color:var(--ink);cursor:pointer}}'
        f'.ui .clr[hidden]{{display:none}}'
        f'.r2{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}}.ui .r2 .ex{{padding:0 10px}}'
        f'.sh{{margin-top:12px;padding:12px 0 4px;border-top:1px solid var(--hair)}}'
        f'.gl{{margin:0 0 6px;{T("label")};color:var(--sec)}}'
        f'.cs{{list-style:none;margin:0 0 12px;padding:0;display:flex;flex-wrap:wrap;gap:8px}}'
        f'.ui .ch{{padding:0 14px}}.ui .ch[aria-pressed="true"]{{font-weight:700;border-width:2px;padding:0 13px 0 9px}}'
        f'.rs{{margin-top:16px;{T("ui")};font-weight:700}}'
        f'.hs{{list-style:none;margin:6px 0 0;padding:0;{T("bodySmall")}}}.hs li{{padding:4px 0;border-top:1px solid var(--hair)}}'
        f'.hs b{{display:inline-block;min-width:4.25em;font-variant-numeric:tabular-nums}}')

    def chip(f, word, on=False):
        mark = u('selected-check') if on else ''
        return (f'<li><button type="button" class="b ch" aria-pressed="{"true" if on else "false"}" data-f="{f}">'
                f'{mark}{word}</button></li>')
    data = json.dumps(rows, ensure_ascii=False, separators=(',', ':'))
    html = (f'<style>{css}</style><div class="ui" data-ui="library">'
            f'<label class="l" for="lb-q">Search the symbols</label>'
            f'<div class="fd">{u("search")}<input class="q" id="lb-q" type="text" autocomplete="off" spellcheck="false" '
            f'data-q><button type="button" class="clr" aria-label="Clear the search" data-act="clear" hidden>{u("close")}'
            f'</button></div>'
            f'<div class="r2"><button type="button" class="b" aria-expanded="true" aria-controls="lb-sh" data-act="sheet">'
            f'{u("filter")}<span data-out="count">Filters, 1 on</span>{u("chevron", transform=OPEN[24])}</button>'
            f'<button type="button" class="b ex" data-act="none">Clear filters</button></div>'
            f'<div class="sh" id="lb-sh" data-sheet><p class="gl" id="lb-k">Kind</p><ul class="cs" aria-labelledby="lb-k">'
            f'{chip("t", "Topic")}{chip("a", "Atlas", True)}{chip("p", "Pillar")}</ul>'
            f'<p class="gl" id="lb-s">Size</p><ul class="cs" aria-labelledby="lb-s">{chip("24", "Reads at 24 px")}</ul></div>'
            f'<p class="rs" role="status" data-out="res">{n_atlas} of 124 symbols</p><ul class="hs" data-out="hits"></ul>'
            + tpl(u('selected-check')) + f'<script type="application/json" data-rows>{data}</script>'
            + script('''
var L=S.querySelector('[data-ui="library"]'),D=JSON.parse(L.querySelector('[data-rows]').textContent),
Q=L.querySelector('[data-q]'),C=L.querySelector('[data-act="clear"]'),F=L.querySelector('[data-act="sheet"]'),
Z=L.querySelector('[data-act="none"]'),H=L.querySelector('[data-sheet]'),K=L.querySelector('[data-out="count"]'),
O=L.querySelector('[data-out="res"]'),U=L.querySelector('[data-out="hits"]'),M=L.querySelector('template[data-tpl]'),
B=[].slice.call(L.querySelectorAll('[data-f]'));
function on(b){return b.getAttribute('aria-pressed')==='true';}
function mark(b,y){var g=b.querySelector('svg');if(y&&!g){b.insertBefore(M.content.firstElementChild.cloneNode(true),b.firstChild);}
if(!y&&g){g.remove();}b.setAttribute('aria-pressed',y?'true':'false');}
function run(){var q=Q.value.trim().toLowerCase(),k=B.filter(function(b){return on(b)&&b.getAttribute('data-f')!=='24';})
.map(function(b){return b.getAttribute('data-f');}),s=B.filter(function(b){return on(b)&&b.getAttribute('data-f')==='24';}).length,
r=D.filter(function(d){return(!k.length||k.some(function(x){return d[2].indexOf(x)>=0;}))&&(!s||d[3])&&
(!q||d[0].toLowerCase().indexOf(q)>=0||d[1].toLowerCase().indexOf(q)>=0);}),n=B.filter(on).length;
K.textContent='Filters, '+n+' on';Z.hidden=!n;C.hidden=!Q.value;O.textContent=r.length+' of 124 symbols';
U.textContent='';r.slice(0,3).forEach(function(d){var li=document.createElement('li'),b=document.createElement('b');
b.textContent=d[0];li.appendChild(b);li.appendChild(document.createTextNode(' '+d[1]));U.appendChild(li);});}
Q.addEventListener('input',run);
C.addEventListener('click',function(){Q.value='';run();Q.focus();});
F.addEventListener('click',function(){var o=F.getAttribute('aria-expanded')!=='true';F.setAttribute('aria-expanded',o?'true':'false');
H.hidden=!o;F.querySelector('[data-icon="U-chevron"] use').setAttribute('transform',o?'rotate(180 12 12)':'');});
B.forEach(function(b){b.addEventListener('click',function(){mark(b,!on(b));run();});});
Z.addEventListener('click',function(){B.forEach(function(b){mark(b,false);});run();F.focus();});
run();''') + '</div>')
    alt = ('The symbol library’s search and filter bar, live at 360 px. A field labeled Search the symbols holds the '
           'magnifier before the text; once you type, a cross at its end clears the search, named “Clear the search”. '
           'Under it, the Filters button carries the funnel, the words “Filters, 1 on” and a chevron pointing up, since '
           'the filters are open, and a word button, Clear filters. The open filters show Kind: Topic, Atlas and Pillar, '
           'and Size: Reads at 24 px. Atlas is on, so it carries a check and a heavier outline, and the status line '
           f'reads “{n_atlas} of 124 symbols”, with the first three listed by ID and name.')
    return m.spec(ctx, 's-11-12-correct', html, '11.12', alt, width=360, interactive=True,
                  notes='Live (D2-516). Labels and kinds read from the editor’s label table for chapter 10; the 41 from '
                        'chapter 10’s construction text, section 10. Chips carry aria-pressed and the Selected check (C-5); '
                        'the count is a polite status line (A-9); Clear the search is the one glyph-only control (A-4).')


def s_library_fail(ctx, m):
    T, u = ctx.ty, m.uicon
    fcss, band = ctx.fail_band(flush=True)
    css = ui_css(ctx, live=False) + fcss + (
        f'.bar{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px}}'
        f'.pn{{{T("ui")};margin-right:auto}}'
        f'.src{{display:flex;align-items:center;justify-content:space-between;min-height:var(--touch);margin-top:16px;'
        f'padding:0 4px 0 0;border-top:1px solid var(--hair);border-bottom:1px solid var(--hair);{T("ui")};font-weight:600}}')
    html = (f'<style>{css}</style>{band}<div class="ui"><p><span class="illus">Illustrative</span></p>'
            f'<div class="bar"><span class="pn">Page 3 of 12</span><span class="b">{u("chevron", transform="rotate(90 12 12)")}'
            f'Previous</span><span class="b nx">Next{u("chevron", transform=TURN_RIGHT[24])}</span></div>'
            f'<p class="src"><span>Sources for this page</span>{u("chevron")}</p></div>')
    alt = ('Labeled Failure case: do not publish. An Illustrative report reader at 360 px. Its Previous and Next buttons '
           'carry chevrons turned left and right, and below them the row Sources for this page carries the same '
           'chevron pointing down, where it opens the row. One drawing turns the page in one place and opens a row in '
           'another.')
    return m.spec(ctx, 's-11-12-failure', html, '11.12', alt, width=360, illustrative=True,
                  notes='Picture of a fault: the chevron does two jobs in one view (D2-507).')


def s_menu(ctx, m, rule_titles):
    """The phone menu: Menu opens a panel that holds focus; Close and Escape shut it and focus returns to Menu. The rows
    open with the chevron. Links lead to this chapter's own groups and rules, so every link lands."""
    T, u = ctx.ty, m.uicon
    css = ui_css(ctx) + (
        f'.ui{{padding:0;position:relative;min-height:440px}}'
        f'.mh{{display:flex;align-items:center;gap:12px;min-height:60px;padding:0 16px;border-bottom:1px solid var(--hair)}}'
        f'.lc{{flex:1 1 auto;{T("ui")};font-weight:700}}'
        f'.bd{{padding:20px 16px}}.bd p + p{{margin-top:12px}}.k{{{T("label")};color:var(--sec)}}'
        f'.hl{{{T("h4", "floor")}}}'
        f'.dl{{position:absolute;inset:0;overflow-y:auto;background:var(--ground)}}.dl[hidden]{{display:none}}'
        f'.dh{{display:flex;align-items:center;gap:12px;min-height:60px;padding:0 16px;border-bottom:1px solid var(--edge)}}'
        f'.dt{{flex:1 1 auto;{T("ui")};font-weight:700}}'
        f'.ps{{list-style:none;margin:0;padding:0 16px 16px}}.ps > li{{border-bottom:1px solid var(--hair)}}'
        f'.ui .rw{{display:flex;width:100%;align-items:center;gap:8px;min-height:var(--touch);padding:8px 0;border:0;'
        f'background:transparent;color:var(--ink);{T("ui")};font-weight:700;text-align:left;cursor:pointer}}'
        f'.rw span{{flex:1 1 auto}}.rw svg{{flex:none}}'
        f'.rl{{list-style:none;margin:0 0 8px;padding:0}}.rl[hidden]{{display:none}}'
        f'.rl a{{display:flex;align-items:center;min-height:var(--touch);padding:4px 0 4px 12px;color:var(--ink);'
        f'{T("bodySmall")};text-underline-offset:3px}}')
    groups = []
    for gi, (title, ids) in enumerate(rule_titles, 1):
        links = ''.join(f'<li><a href="#rule-{i.replace(".", "-")}">{i} {t}</a></li>' for i, t in ids)
        groups.append(f'<li><button type="button" class="rw" aria-expanded="false" aria-controls="pm-g{gi}" data-row>'
                      f'<span>{gi} {title}</span>{u("chevron")}</button><ul class="rl" id="pm-g{gi}" hidden>{links}</ul></li>')
    html = (f'<style>{css}</style><div class="ui" data-ui="menu"><div class="mh" data-bg><p class="lc">11 Status and utility '
            f'icons</p><button type="button" class="b" aria-haspopup="dialog" aria-expanded="false" aria-controls="pm-d" '
            f'data-act="open">{u("menu")}Menu</button></div>'
            f'<div class="bd" data-bg><p class="k">Chapter 11</p><p class="hl">Status and utility icons</p>'
            f'<p>Give each record state or interface action a glyph and a word that read without color.</p></div>'
            f'<div class="dl" id="pm-d" role="dialog" aria-modal="true" aria-label="In this chapter" hidden data-dlg>'
            f'<div class="dh"><p class="dt">In this chapter</p><button type="button" class="b" data-act="close">'
            f'{u("close")}Close the menu</button></div><ul class="ps">{"".join(groups)}</ul></div>'
            + script('''
var W=S.querySelector('[data-ui="menu"]'),D=W.querySelector('[data-dlg]'),O=W.querySelector('[data-act="open"]'),
X=W.querySelector('[data-act="close"]'),G=[].slice.call(W.querySelectorAll('[data-bg]'));
function shut(back){D.hidden=true;O.setAttribute('aria-expanded','false');G.forEach(function(g){g.inert=false;});if(back)O.focus();}
O.addEventListener('click',function(){D.hidden=false;O.setAttribute('aria-expanded','true');G.forEach(function(g){g.inert=true;});X.focus();});
X.addEventListener('click',function(){shut(true);});
D.addEventListener('keydown',function(e){if(e.key==='Escape'){e.preventDefault();e.stopPropagation();shut(true);return;}
if(e.key!=='Tab')return;var f=[].slice.call(D.querySelectorAll('button,a[href]')).filter(function(x){return x.offsetParent!==null;}),
a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus();}
else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus();}});
W.querySelectorAll('[data-row]').forEach(function(r){r.addEventListener('click',function(){var o=r.getAttribute('aria-expanded')!=='true';
r.setAttribute('aria-expanded',o?'true':'false');r.nextElementSibling.hidden=!o;
r.querySelector('use').setAttribute('transform',o?'rotate(180 12 12)':'');});});
D.querySelectorAll('a[href]').forEach(function(a){a.addEventListener('click',function(){shut(false);});});''') + '</div>')
    alt = ('A live phone menu at 360 px. The bar names the chapter, 11 Status and utility icons, and holds a Menu button '
           'with three bars before the word. Menu opens a panel over the page, In this chapter, which holds focus until '
           'Close the menu, with its cross, or the Escape key shuts it; focus then returns to Menu. The panel lists the '
           'chapter’s four groups as rows, each with a chevron that points down while the row is closed and up while it '
           'is open, and each opens to links to its rules.')
    return m.spec(ctx, 's-11-menu', html, None, alt, width=360, interactive=True,
                  notes='Live (D2-516): the dialog holds focus, Escape and Close return focus to Menu (G-3); the page '
                        'behind it is inert while it is open.')


# ------------------------------------------------------------------------------------------------ 11.13 another site
SOURCES_LIVE = [
    ('Nebraska Legislature,', '“Lawmaking in Nebraska”', 'https://nebraskalegislature.gov/about/lawmaking.php'),
    ('FOIA.gov,', '“Frequently Asked Questions”', 'https://www.foia.gov/faq.html'),
    ('5 U.S.C. 553, rulemaking, at the Legal Information', 'Institute', 'https://www.law.cornell.edu/uscode/text/5/553'),
]


def s_links(ctx, m):
    T, u = ctx.ty, m.uicon
    css = ui_css(ctx) + (
        f'.k{{margin:0 0 4px;{T("label")};color:var(--sec)}}'
        f'.sl{{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}}.sl li{{border-bottom:1px solid var(--hair)}}'
        f'.sl a{{display:block;min-height:var(--touch);box-sizing:border-box;padding:11px 0;color:var(--ink);{T("bodySmall")};'
        f'text-underline-offset:3px}}'
        f'.nw{{white-space:nowrap}}.nw svg{{display:inline-block;vertical-align:-2px;margin-left:4px}}')
    lis = ''.join(f'<li><a href="{url}">{a} <span class="nw">{b}{u("another-site", 16)}</span>'
                  f'<span class="vh"> (another site)</span></a></li>' for a, b, url in SOURCES_LIVE)
    html = (f'<style>{css}</style><div class="ui"><p class="k">Sources</p><ul class="sl">{lis}</ul></div>')
    alt = ('A live list of three sources at 360 px, each a link to another site that opens in the same tab: Nebraska '
           'Legislature, “Lawmaking in Nebraska”; FOIA.gov, “Frequently Asked Questions”; and 5 U.S.C. 553, rulemaking, '
           'at the Legal Information Institute. After each link’s last word sits the 16 px mark for another site, an '
           'arrow leaving a box, kept on the line with that word. Each link stands 44 px tall, and a screen reader hears '
           '“(another site)” at the end of its name.')
    return m.spec(ctx, 's-11-13-correct', html, '11.13', alt, width=360, interactive=True,
                  notes='Live links to the research lead’s sources (section 5 and 7), same tab (D2-513); the 16 px mark '
                        'is the first 16 px utility icon on a page (D2-577).')


def s_links_fail(ctx, m):
    T, u = ctx.ty, m.uicon
    fcss, band = ctx.fail_band(flush=True)
    css = ui_css(ctx, live=False) + fcss + (
        f'.tx{{width:250px;{T("body")}}}.tx .a{{text-decoration:underline;text-underline-offset:3px}}'
        f'.tx svg{{display:block;margin-top:2px}}.n{{margin-top:12px;{T("caption")};color:var(--sec)}}')
    html = (f'<style>{css}</style>{band}<div class="ui"><p><span class="illus">Illustrative</span></p>'
            f'<p class="tx" style="margin-top:12px">The proposed rule and its comment form are on <span class="a">the agency’s '
            f'rulemaking page</span>{u("another-site")}</p>'
            f'<p class="n">Opens in a new tab, with nothing said about it.</p></div>')
    alt = ('Labeled Failure case: do not publish. An Illustrative sentence at 360 px ends with the link “the agency’s '
           'rulemaking page”. Its mark for another site, drawn at 24 px inside the sentence, has wrapped onto a line of its '
           'own under the words. A note says the link opens a new tab with nothing said about it.')
    return m.spec(ctx, 's-11-13-failure', html, '11.13', alt, width=360, illustrative=True,
                  notes='Picture of a fault: a 24 px mark inside running text, broken from its word, and a new tab with no '
                        'warning (D2-513).')


# ------------------------------------------------------------------------------------------------ 11.14 the loop stepper
def loop_steps(m):
    d = json.loads((m.ROOT / 'work/extract/atlas-v7-data.json').read_text())
    lp = d['loops'][LOOP_ID]
    links = d['links'] if isinstance(d['links'], dict) else {x['id']: x for x in d['links']}
    labels = [lab for lab, _ in lp['chain_labels']]
    signs = [sg for _, sg in lp['chain']]
    steps = []
    for i, lid in enumerate(lp['links']):
        a, b = labels[i], labels[(i + 1) % len(labels)]
        plural = a.endswith('seats')
        verb = ('raise' if plural else 'raises') if signs[i] == '+' else ('lower' if plural else 'lowers')
        b_low = b[0].lower() + b[1:]
        steps.append([curly(f'{a} {verb} {b_low}.'), curly(links[lid]['plain'])])
    return curly(lp['title']), labels[0], steps


def curly(t):
    """The atlas's text with typographic apostrophes and quotes, as the guide sets every word."""
    t = re.sub(r"(?<=\w)'(?=\w)", '’', t)
    t = re.sub(r"(?<=\w)'", '’', t)
    t = re.sub(r'"(?=\w)', '“', t)
    return t.replace('"', '”')


def stepper(ctx, m, live=True):
    T, u = ctx.ty, m.uicon
    title, first, steps = loop_steps(m)
    css = ui_css(ctx) + (
        f'.k{{{T("label")};color:var(--sec)}}.t{{margin-top:6px;{T("h4", "floor")};text-wrap:balance}}'
        f'.st{{margin:16px 0;padding:14px;border:1px solid var(--hair);background:var(--paper);min-height:9.5rem}}'
        f'.sn{{{T("ui")};font-weight:700;font-variant-numeric:tabular-nums}}.sx{{margin-top:6px;{T("bodySmall")};text-wrap:pretty}}'
        f'.cl{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.ui .cl .b{{padding:0 10px;white-space:nowrap}}'
        f'.ui .cl .nx{{justify-content:flex-end}}'
        f'.cl svg[hidden]{{display:none}}')
    start = f'Start at {first.lower()}, and suppose they rise. Press Play, or Next step to follow one link at a time.'
    data = json.dumps(steps, ensure_ascii=False, separators=(',', ':'))
    head = (f'<p class="k">From our systems atlas, loop {LOOP_ID}</p><p class="t">{title}</p>'
            f'<div class="st" aria-live="polite"><p class="sn" data-out="sn">Ready</p><p class="sx" data-out="sx">{start}</p></div>')
    if live:
        ctl = (f'<div class="cl" role="group" aria-label="Steps of the loop">'
               f'<button type="button" class="b" data-act="play">{u("play")}{u("pause").replace("<svg ", "<svg hidden ", 1)}'
               f'<span data-out="pw">Play</span></button>'
               f'<button type="button" class="b" data-act="reset" aria-disabled="true" aria-describedby="lp-why">'
               f'{u("reset")}Reset the loop</button>'
               f'<button type="button" class="b" data-act="prev" aria-disabled="true" aria-describedby="lp-why">'
               f'{u("arrow", transform=MIRROR[24])}Previous step</button>'
               f'<button type="button" class="b nx" data-act="next">Next step{u("arrow")}</button></div>'
               f'<p class="why" id="lp-why" data-out="why">At the start, so Previous step and Reset wait until you move on.</p>')
        js = f'<script type="application/json" data-steps>{data}</script>' + script('''
var L=S.querySelector('[data-ui="loop"]'),D=JSON.parse(L.querySelector('[data-steps]').textContent),i=0,t=null,
Y=L.querySelector('[data-act="play"]'),R=L.querySelector('[data-act="reset"]'),P=L.querySelector('[data-act="prev"]'),
X=L.querySelector('[data-act="next"]'),W=L.querySelector('[data-out="why"]'),A=L.querySelector('[data-out="sn"]'),
B=L.querySelector('[data-out="sx"]'),I=Y.querySelectorAll('svg'),V=Y.querySelector('[data-out="pw"]'),A0=A.textContent,B0=B.textContent;
function off(b,y){if(y){b.setAttribute('aria-disabled','true');b.setAttribute('aria-describedby',W.id);}
else{b.removeAttribute('aria-disabled');b.removeAttribute('aria-describedby');}}
function show(){A.textContent=i?'Step '+i+' of '+D.length+': '+D[i-1][0]:A0;B.textContent=i?D[i-1][1]:B0;
off(P,!i);off(R,!i);off(X,i===D.length);
W.textContent=!i?'At the start, so Previous step and Reset wait until you move on.':(i===D.length?'At the last step. Reset the loop to start again.':'');
var p=!!t;I[0].toggleAttribute('hidden',p);I[1].toggleAttribute('hidden',!p);V.textContent=p?'Pause':(i===D.length?'Play again':'Play');}
function stop(){if(t){clearInterval(t);t=null;}}
function go(){if(i<D.length){i++;}if(i===D.length){stop();}show();}
Y.addEventListener('click',function(){if(t){stop();show();return;}if(i===D.length){i=0;}t=setInterval(go,2400);go();});
X.addEventListener('click',function(){if(i<D.length){stop();i++;show();}});
P.addEventListener('click',function(){if(i>0){stop();i--;show();}});
R.addEventListener('click',function(){if(i>0){stop();i=0;show();}});
show();''')
        return css, f'<div class="ui" data-ui="loop">{head}{ctl}{js}</div>', title, steps
    return css, head, title, steps


def s_stepper(ctx, m):
    css, body, title, steps = stepper(ctx, m)
    html = f'<style>{css}</style>{body}'
    alt = (f'A live loop stepper at 360 px for loop {LOOP_ID} from our systems atlas, “{title}”. A box shows the step '
           'and its sentence, and starts at “Ready”. Four buttons sit under it, each 44 px tall with its icon beside its '
           'word: Play, which turns to Pause while the steps run and to Play again at the end; Reset the loop, with an open '
           'circle and one arrowhead; Previous step, with the arrow mirrored; and Next step, with the arrow after its word. '
           'At the start, Previous step and Reset are unavailable, and a line says why. Each step names the link and '
           'gives the atlas’s sentence for it, starting with “' + steps[0][0] + '”')
    return m.spec(ctx, 's-11-14-correct', html, '11.14', alt, width=360, interactive=True,
                  notes='Live (D2-516). Steps from Atlas V7’s loop R10 (chain labels, signs and each link’s plain '
                        'sentence). Playback starts only on a press (E-3); unavailable controls keep focus with their '
                        'reason (G-4); the step box is a polite live region (A-9).')


def s_stepper_fail(ctx, m):
    T, u = ctx.ty, m.uicon
    css, head, title, _ = stepper(ctx, m, live=False)
    fcss, band = ctx.fail_band(flush=True)
    cl24 = ('<svg viewBox="0 0 128 128" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-024" '
            'data-icon-family="topic"><use href="#oa-sym-cl-024"/></svg>')
    ctl = (f'<div class="cl"><span class="b">{u("play")}Play</span><span class="b">{cl24}Start over</span>'
           f'<span class="b">{u("arrow", transform=MIRROR[24])}Previous step</span>'
           f'<span class="b nx">Next step{u("arrow")}</span></div>')
    html = f'<style>{css}{fcss}</style>{band}<div class="ui">{head}{ctl}</div>'
    alt = (f'Labeled Failure case: do not publish. The same loop stepper for loop {LOOP_ID}, “{title}”, at 360 px. Its '
           'Start over button carries CL-024, the feedback loop drawing, two arrows that carry a change between two boxes '
           'and back, in place of the Reset icon.')
    return m.spec(ctx, 's-11-14-failure', html, '11.14', alt, width=360,
                  notes='Picture of a fault: a topic drawing standing for an interface action (D2-515), from the sprite '
                        '(CL-024 is among the 41 that read at 24 px, one color).')


# ------------------------------------------------------------------------------------------------ 11.15 the three marks
def marks_css(ctx):
    T, v = ctx.ty, ctx.v
    return (f'.er{{display:grid;grid-template-columns:24px minmax(0,1fr);gap:8px;margin-top:8px;padding:10px 12px;'
            f'background:{v("oa.color.state.error.band.onNewsprint")};color:{v("oa.color.state.error.text.onNewsprint")};'
            f'border-left:4px solid {v("oa.color.state.error.mark.onNewsprint")};{T("bodySmall")}}}'
            f'.er[hidden],.ok[hidden]{{display:none}}.er svg,.ok svg,.wn svg{{display:block;margin-top:-1px}}'
            f'.er b,.ok b,.wn b{{font-weight:700}}'
            f'.ok{{display:grid;grid-template-columns:24px minmax(0,1fr);gap:8px;margin-top:12px;padding:10px 0;'
            f'{T("bodySmall")}}}.ok svg{{color:{v("oa.color.state.success.mark.onNewsprint")}}}'
            f'.wn{{display:grid;grid-template-columns:24px minmax(0,1fr);gap:8px;padding:10px 12px;'
            f'border-left:4px solid {v("oa.color.state.warning.mark.onNewsprint")};{T("bodySmall")}}}'
            f'.wn svg{{color:{v("oa.color.state.warning.mark.onNewsprint")}}}')


def s_form(ctx, m):
    T, u, v = ctx.ty, m.uicon, ctx.v
    css = ui_css(ctx) + marks_css(ctx) + (
        f'.t{{margin-top:8px;{T("h4", "floor")};text-wrap:balance}}.d{{margin:8px 0 16px;{T("bodySmall")}}}'
        f'.f{{margin:0 0 16px}}.l{{display:block;{T("ui")};font-weight:600}}.h{{{T("caption")};color:var(--sec)}}'
        f'.ui .in{{display:block;box-sizing:border-box;width:100%;min-height:48px;margin-top:6px;padding:0 12px;'
        f'border:1px solid var(--edge);background:var(--paper);color:var(--ink);{T("body")}}}'
        f'.ui .in[aria-invalid="true"]{{border-left:4px solid {v("oa.color.state.error.mark.onNewsprint")};padding-left:9px}}'
        f'.ui .ask{{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;border:0;cursor:pointer;'
        f'background:{v("oa.component.button.ask.fill.onNewsprint")};color:{v("oa.component.button.ask.label.onNewsprint")};'
        f'box-shadow:inset 0 0 0 1px {v("oa.component.button.ask.keyline.onNewsprint")};{T("ask")}}}'
        f'.ui .ask[data-yield]{{background:{v("oa.component.button.primary.fill.onNewsprint")};'
        f'color:{v("oa.component.button.primary.label.onNewsprint")};box-shadow:none}}'
        f'@media (forced-colors:active){{.ui .ask{{border:1px solid ButtonText}}}}')

    def field(key, label, hint, attrs):
        hid = f'fm-{key}-h'
        h = f'<p class="h" id="{hid}">{hint}</p>' if hint else ''
        desc = f' aria-describedby="{hid}"' if hint else ''
        return (f'<div class="f" data-field="{key}"><label class="l" for="fm-{key}">{label}</label>{h}'
                f'<input class="in" id="fm-{key}" {attrs}{desc} data-in="{key}">'
                f'<div class="er" id="fm-{key}-er" hidden data-err="{key}">{u("error")}<span><b>Error:</b> <span data-msg></span></span></div></div>')
    html = (f'<style>{css}</style><div class="ui" data-ui="form"><p><span class="illus">Illustrative</span></p>'
            f'<p class="t">Get a reminder before the March 3 hearing</p>'
            f'<p class="d">We email you two days before the hearing on H.99001, with how to send testimony.</p>'
            f'<form novalidate data-form>'
            + field('email', 'Email', '', 'type="email" autocomplete="email" spellcheck="false"')
            + field('zip', 'ZIP code', 'Five digits', 'type="text" inputmode="numeric" autocomplete="postal-code"')
            + f'<button type="submit" class="ask" data-red="working" data-red-job="take part now" data-ask>Remind me</button></form>'
            f'<div role="status" data-out="ok"></div>'
            + tpl(f'<div class="ok">{u("success")}<span><b>You’re signed up.</b> We’ll email you on March 1, two '
                  f'days before the hearing.</span></div>')
            + script('''
var F=S.querySelector('[data-ui="form"]'),A=F.querySelector('[data-ask]'),K=F.querySelector('[data-out="ok"]'),
M={email:'Enter an email address with an @, such as name@example.com.',zip:'Enter a ZIP code with five digits.'},
V={email:function(x){return/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(x);},zip:function(x){return/^[0-9]{5}$/.test(x);}};
function mark(k,bad){var i=F.querySelector('[data-in="'+k+'"]'),e=F.querySelector('[data-err="'+k+'"]'),
d=(i.getAttribute('aria-describedby')||'').split(' ').filter(function(x){return x&&x!==e.id;}),f=i.closest('[data-field]');
if(bad){i.setAttribute('aria-invalid','true');d.push(e.id);e.querySelector('[data-msg]').textContent=M[k];e.hidden=false;
f.setAttribute('data-red','working');f.setAttribute('data-red-job','error');}
else{i.removeAttribute('aria-invalid');e.hidden=true;f.removeAttribute('data-red');f.removeAttribute('data-red-job');}
if(d.length){i.setAttribute('aria-describedby',d.join(' '));}else{i.removeAttribute('aria-describedby');}return bad?i:null;}
F.querySelector('[data-form]').addEventListener('submit',function(ev){ev.preventDefault();var first=null;
['email','zip'].forEach(function(k){var i=F.querySelector('[data-in="'+k+'"]'),b=mark(k,!V[k](i.value.trim()));first=first||b;});
if(first){A.setAttribute('data-yield','');A.removeAttribute('data-red');A.removeAttribute('data-red-job');K.textContent='';first.focus();return;}
A.removeAttribute('data-yield');A.setAttribute('data-red','working');A.setAttribute('data-red-job','take part now');
K.textContent='';K.appendChild(F.querySelector('template[data-tpl]').content.firstElementChild.cloneNode(true));});''') + '</div>')
    alt = ('A live sign-up form at 360 px, Illustrative: “Get a reminder before the March 3 hearing”, with an Email field, a '
           'ZIP code field with the hint “Five digits” and the red button Remind me, the view’s one working red. Sent '
           'with a field wrong, each wrong field takes a red bar at its left edge and a message under it on the pale '
           'Error Band, with a red bar, the error mark in ink and the words “Error:” and the fix, such as “Enter a ZIP '
           'code with five digits.” The error then holds the red, so Remind me turns Charcoal until the fields are right, '
           'and focus moves to the first wrong field. Sent right, the success mark and “You’re signed up. We’ll email you '
           'on March 1, two days before the hearing.” appear in a status line.')
    return m.spec(ctx, 's-11-15-correct', html, '11.15', alt, width=360, interactive=True, illustrative=True,
                  notes='Live (D2-516). Fields carry aria-invalid and aria-describedby to their message (SC 3.3.1, 3.3.3); '
                        'the ask yields to Charcoal primary while an error shows (Rule 05.3); success goes to a status line '
                        '(A-9). The error mark draws in ink and the error’s red is the 4 px bar (see notes, D2-xxx).')


def s_form_fail(ctx, m):
    T, u, v = ctx.ty, m.uicon, ctx.v
    fcss, band = ctx.fail_band(flush=True)
    css = ui_css(ctx, live=False) + fcss + (
        f'.l{{display:block;margin-top:12px;{T("ui")};font-weight:600}}'
        f'.in{{display:flex;align-items:center;min-height:48px;margin-top:6px;padding:0 12px;border:1px solid var(--edge);'
        f'background:var(--paper);{T("body")}}}'
        f'.bad{{display:flex;align-items:center;gap:6px;margin-top:6px;color:{v("oa.color.palette.pillarRed")};{T("bodySmall")}}}'
        f'.bad svg{{display:block}}')
    html = (f'<style>{css}</style>{band}<div class="ui"><p><span class="illus">Illustrative</span></p>'
            f'<span class="l">ZIP code</span><span class="in">0217</span>'
            f'<p class="bad" data-red="working" data-red-job="error">{u("close")}Invalid</p></div>')
    alt = ('Labeled Failure case: do not publish. An Illustrative ZIP code field at 360 px holding four digits, 0217. Under '
           'it, red text reads “Invalid” beside a red cross, the Close icon. Nothing says “Error”, which rule the entry '
           'broke or how to fix it, and the red text measures 2.96 to 1 on Newsprint.')
    return m.spec(ctx, 's-11-15-failure', html, '11.15', alt, width=360, illustrative=True, exempt=['contrast'],
                  notes='Labeled failure: red text at 2.96 to 1 on Newsprint on purpose, and the cross, which means Close, '
                        'standing for an error (D2-509).')


def s_marks(ctx, m):
    """The three marks in use, each with its words: a readable list (D2-255)."""
    T, u = ctx.ty, m.uicon
    css = marks_css(ctx) + (
        f'.mk3{{list-style:none;margin:0;padding:0;display:grid;gap:16px}}'
        f'.n{{margin:0 0 6px;{T("label")};color:{ctx.v("oa.color.text.secondary.onNewsprint")}}}'
        f'.mk3 .er,.mk3 .ok{{margin-top:0}}.mk3 .ok{{padding:10px 12px;border-left:4px solid transparent}}')
    items = [
        ('Error', f'<div class="er">{u("error")}<span><b>Error:</b> Enter a ZIP code with five digits.</span></div>'),
        ('Success', f'<div class="ok">{u("success")}<span><b>You’re signed up.</b> We’ll email you on March 1.</span></div>'),
        ('Warning', f'<div class="wn">{u("warning")}<span><b>Checked April 20.</b> The agency may have acted since.</span></div>'),
    ]
    html = (f'<style>{css}</style><ul class="mk3">'
            + ''.join(f'<li><p class="n">{n}</p>{b}</li>' for n, b in items) + '</ul>')
    alt = ('The three marks at true size, each in its message. Error: a circle holding an exclamation mark, in ink, on the '
           'pale Error Band with a 4 px red bar at its left, beside “Error: Enter a ZIP code with five digits.” Success: a '
           'check leaving an open circle, in Verdigris, beside “You’re signed up. We’ll email you on March 1.” Warning: a '
           'triangle holding an exclamation mark, in ink, with a 4 px Charcoal bar, beside “Checked April 20. The agency '
           'may have acted since.”')
    return m.spec(ctx, 's-11-marks', html, None, alt, readable=True, illustrative=True,
                  notes='A readable list (D2-255). The error’s red is the bar; the mark draws in ink (see notes).')


# ------------------------------------------------------------------------------------------------ 11.16 which red yields
def yield_view(ctx, m, fail=False):
    """One view at 360 px where an error, the take-part mark and an intervention marker meet. Correct: the error holds
    the red (Rule 05.3's first claim); the take-part disc and the marker keep their shapes and words in ink, and the ask
    steps down to Charcoal. Failure: all three claim red."""
    T, u, v = ctx.ty, m.uicon, ctx.v
    bill = dict(id='H.99009', title='All-party primaries', states=['done', 'take', 'notyet', 'notyet', 'notyet', 'notyet'],
                line='Testimony is open until March 3.', take='Send written testimony by March 3.',
                cta='How to send testimony')
    css = (m.piece_css(ctx, 'n', 's') + marks_css(ctx) + (
        f'.ky{{margin:12px 0 0;{T("label")};color:var(--txt2)}}.ch{{margin:6px 0 12px;{T("h4", "floor")};text-wrap:balance}}'
        f'.cd .rows{{border:0}}.cd .row{{padding:0;border:0}}'
        f'.fg{{margin:16px 0 0;padding:12px 0 0;border-top:1px solid var(--hair)}}.fk{{{T("label")};color:var(--txt2)}}'
        f'.lp{{display:flex;align-items:center;gap:6px;margin-top:10px}}.lp svg{{flex:none}}'
        f'.pl{{flex:1 1 0;display:flex;align-items:center;justify-content:center;min-height:44px;padding:4px 8px;'
        f'border:2px solid var(--ink);border-radius:999px;background:var(--bg);{T("dataLabel")};text-align:center}}'
        f'.pl.tg{{border-width:3px;font-weight:700}}'
        f'.fn{{margin-top:8px;{T("bodySmall")};text-wrap:pretty}}.fn b{{font-weight:700}}'
        f'.fm{{margin-top:16px;padding-top:12px;border-top:1px solid var(--hair)}}'
        f'.l{{display:block;{T("ui")};font-weight:600}}'
        f'.in{{display:flex;align-items:center;min-height:48px;margin-top:6px;padding:0 9px;border:1px solid var(--strong);'
        f'border-left:4px solid {v("oa.color.state.error.mark.onNewsprint")};background:{v("oa.color.surface.white")};{T("body")}}}'
        f'.ask{{display:inline-flex;align-items:center;min-height:48px;margin-top:16px;padding:0 20px;{T("ask")}}}'
        f'.ask.y{{background:{v("oa.component.button.primary.fill.onNewsprint")};color:{v("oa.component.button.primary.label.onNewsprint")}}}'
        f'.ask.r{{background:{v("oa.component.button.ask.fill.onNewsprint")};color:{v("oa.component.button.ask.label.onNewsprint")};'
        f'box-shadow:inset 0 0 0 1px {v("oa.component.button.ask.keyline.onNewsprint")}}}'
        f'.pl.rd{{border-color:var(--red)}}'))
    arrow = ('<svg class="mk" width="14" height="10" viewBox="0 0 14 10" aria-hidden="true" focusable="false">'
             '<path d="M0 5h11M8 1.5l4 3.5-4 3.5" class="si nf" stroke-width="1.5"/></svg>')
    tgt = (' rd" data-red="working" data-red-job="where it acts' if fail else '')
    fig = (f'<div class="fg"><p class="fk">Where the bill would act, in our systems atlas</p><div class="lp">'
           f'<span class="pl">Safe seats</span>{arrow}<span class="pl tg{tgt}">Primary decisiveness</span>{arrow}'
           f'<span class="pl">Electoral pressure</span></div>'
           f'<p class="fn"><b>Reform R-01 acts here.</b> All-party primaries would move the choice a primary makes in a '
           f'safe seat to every voter.</p></div>')
    err = (f'<div class="fm" data-red="working" data-red-job="error"><span class="l">Email for a reminder</span>'
           f'<span class="in">name@example</span><div class="er">{u("error")}<span><b>Error:</b> Enter an email address '
           f'with an @, such as name@example.com.</span></div></div>')
    ask = (f'<span class="ask r" data-red="working" data-red-job="take part now">Remind me</span>' if fail
           else '<span class="ask y">Remind me</span>')
    row = m.row(bill, 'card', red=fail)
    return css, (f'<div class="pc"><p>{m.ILLUS}</p><div class="cd"><p class="ky">Tracker · State bills</p>'
                 f'<p class="ch">The House hears the all-party primary bill on March 3</p><ul class="rows">{row}</ul></div>'
                 f'{fig}{err}{ask}</div>')


def s_yield(ctx, m):
    css, body = yield_view(ctx, m)
    html = f'<style>{css}</style>{body}'
    alt = ('One Illustrative view at 360 px on Newsprint where three marks could claim red. A story card for bill H.99009, '
           'All-party primaries, shows six numbered steps with the take-part mark on step 2, its small disc drawn in '
           'Charcoal, and the words “You can take part now. Send written testimony by March 3.” Under it, a small figure '
           'from our systems atlas draws three linked ovals, Safe seats, Primary decisiveness and Electoral pressure, with '
           'Primary decisiveness outlined heavier in Charcoal and the words “Reform R-01 acts here.” Last, an email field '
           'holds an error: a red bar at its left and a message on the pale Error Band, “Error: Enter an email address with '
           'an @, such as name@example.com.” The error is the only red in the view, and the Remind me button is Charcoal.')
    return m.spec(ctx, 's-11-16-correct', html, '11.16', alt, width=360, illustrative=True,
                  notes='Rule 05.3’s order: an error first, then the step a reader can take, then where a reform acts. The '
                        'take-part disc and the marker yield to ink with their shapes and words (C-4). The marker follows '
                        'System 1’s target: the variable’s outline at 3 px.')


def s_yield_fail(ctx, m):
    css, body = yield_view(ctx, m, fail=True)
    fcss, band = ctx.fail_band(flush=True)
    html = f'<style>{css}{fcss}</style>{band}{body}'
    alt = ('Labeled Failure case: do not publish. The same Illustrative view, with red in three jobs: the take-part disc on '
           'step 2 and the Remind me button, the outline of Primary decisiveness where reform R-01 acts, and the error bar '
           'on the email field. The eye has three reds to choose from, and the error that blocks the reader looks no more '
           'urgent than the rest.')
    return m.spec(ctx, 's-11-16-failure', html, '11.16', alt, width=360, illustrative=True, exempt=['red'],
                  notes='Labeled failure: three working-red jobs in one view on purpose (Rule 05.3).')


# ------------------------------------------------------------------------------------------------ rules
def build_ui(ctx, m, rule_titles):
    """Specimens and rules 11.11 to 11.16, the groups they open, and their extras."""
    s_reader(ctx, m)
    s_reader_fail(ctx, m)
    s_icons(ctx, m)
    s_library(ctx, m)
    s_library_fail(ctx, m)
    s_menu(ctx, m, rule_titles)
    s_links(ctx, m)
    s_links_fail(ctx, m)
    s_stepper(ctx, m)
    s_stepper_fail(ctx, m)
    s_form(ctx, m)
    s_form_fail(ctx, m)
    s_marks(ctx, m)
    s_yield(ctx, m)
    s_yield_fail(ctx, m)
    r = ctx.ratio
    red_n = r('oa.color.palette.pillarRed', 'oa.color.surface.newsprint')
    red_band = r('oa.color.palette.pillarRed', 'oa.color.derived.errorBand', 'contrast Pillar Red on the Error Band')
    ink_band = r('oa.color.state.error.text.onNewsprint', 'oa.color.derived.errorBand', 'contrast Charcoal on the Error Band')
    verd = r('oa.color.state.success.mark.onNewsprint', 'oa.color.surface.newsprint')
    ring = r('oa.color.focus.ring.onNewsprint', 'oa.color.surface.newsprint')
    files = ['work/build/assets/utility/svg-24/', 'work/build/assets/utility/svg-16/',
             'work/build/assets/utility/20261110_Utility-Icons-Manifest.json']
    rules = [
        {
            'id': '11.11', 'title': 'Set each utility icon beside its word, at 24 px by a control and 16 px only inside a line of text.',
            'rule': ['A utility icon names an action on a page, such as Close, Download or Filter. It sits beside its '
                     'word: 24 px wide beside the word of a button or link, and 16 px wide only inside a line of text or a '
                     'table heading, where it comes from its own 16 px drawing. Three icons sit beside other words that '
                     'carry their meaning: the sort mark beside a column’s heading, the mark after a link to another site '
                     'and the chevron beside a row’s words. The clear control inside a search field is the one icon with no '
                     'word; its field’s label gives the context, and its name is “Clear the search”.',
                     'Share, zoom, print and information stay words. Their usual signs repeat drawings we already use, such '
                     'as the two rings of the Connect pillar icon and the atlas’s plus and minus, and an information mark '
                     'invites help that shows only on hover.'],
            'tokens': ['oa.component.icon.utility.line.medium', 'oa.size.icon.medium', 'oa.size.icon.small',
                       'oa.size.target.touch'],
            'why': {'text': ['A reader who meets an icon beside its word learns the sign once and reads it faster after '
                             'that, and the word carries the meaning for anyone who does not know the sign. With the word '
                             'showing, the icon stays hidden from screen readers, so nobody hears the action twice, and a '
                             'control’s name starts with the words a reader sees, which voice control needs. A name that '
                             'shows only on hover never reaches a phone, a keyboard or a magnified screen.'],
                    'basis': 'WCAG 2.2 SC 2.5.3 and 1.4.13'},
            'correct': {'specimen': 's-11-11-correct',
                        'caption': 'A report reader’s toolbar, live at 360 px. Each icon sits beside its word, every '
                                   'control stands 44 px tall, Previous page says why it is unavailable on the first page, '
                                   'and the page’s size stays two words.'},
            'failure': {'specimen': 's-11-11-failure',
                        'caption': '<strong>Fails Rule 11.11.</strong> The toolbar shows icons with no words, each 32 px '
                                   'square, and its information mark gives its name only in a box that appears on hover.'},
            'specs': [
                {'label': 'Beside a control’s word', 'value': 'The 24 px drawing, 2 px line, 8 px from the word',
                 'token': 'oa.component.icon.utility.line.medium'},
                {'label': 'Inside a line of text or a table heading', 'value': 'The 16 px drawing, 1.5 px line, on the '
                                                                               'line with its word', 'token': 'oa.size.icon.small'},
                {'label': 'Control', 'value': 'At least 44 px tall; 44 by 44 px where the icon stands with no word',
                 'token': 'oa.size.target.touch'},
                {'label': 'Color', 'value': 'The word’s ink, through currentColor; never red',
                 'token': 'oa.component.icon.ink.onNewsprint'},
                {'label': 'Name', 'value': 'Starts with the visible word; the icon carries aria-hidden'},
                {'label': 'No icon for', 'value': 'Share, copy link, zoom, print, information, home, settings, layers, '
                                                  'loading, a phone call, email or alerts'},
            ],
            'files': files,
            'related': ['17', '18'],
            'builders': ['Draw the icon from the sprite inside the control, beside its word: <code>&lt;svg viewBox="0 0 24 '
                         '24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="U-download" '
                         'data-icon-family="utility"&gt;&lt;use href="#oa-sym-u-download-24px"/&gt;&lt;/svg&gt;</code>. Take '
                         'a 16 px icon from <code>svg-16/</code>, and never scale the 24 px drawing down. An unavailable '
                         'control keeps its focus, takes <code>aria-disabled="true"</code> and points with '
                         '<code>aria-describedby</code> to words that say why.'],
        },
        {
            'id': '11.12', 'title': 'Give each drawing one meaning.',
            'rule': ['The arrow means Next. Mirrored, it means Previous, and turned up or down it shows the order a column '
                     'is sorted in. The chevron opens and closes a row: it points down while the row is closed and up '
                     'while it is open. The cross closes, and an error is a circle holding an exclamation mark. Copy’s two '
                     'sheets never turn into a check; the result goes to a status line in words, with the success or the '
                     'error mark.',
                     'Menu’s three bars stay bars while the menu is open, and the open menu carries its own Close.'],
            'tokens': ['oa.motion.duration.standard'],
            'why': {'text': ['A reader learns a sign once and trusts it after that. If the chevron also turned pages, a '
                             'reader could not tell a row that opens from a page that turns, and a Copy icon that turned '
                             'into a check would look like a choice someone had made.'],
                    'basis': 'WCAG 2.2 SC 3.2.4; design judgment'},
            'correct': {'specimen': 's-11-12-correct',
                        'caption': 'The symbol library’s search and filter bar, live at 360 px. The funnel opens the '
                                   'filters, the chevron shows they are open, a check marks the filter that is on, and the '
                                   'cross clears the search.'},
            'failure': {'specimen': 's-11-12-failure',
                        'caption': '<strong>Fails Rule 11.12.</strong> The chevron turns the page in the toolbar and opens '
                                   'the sources below it, so one drawing does two jobs in one view.'},
            'specs': [
                {'label': 'Arrow', 'value': 'Next as drawn; Previous mirrored; the sort order in use turned up or down'},
                {'label': 'Chevron', 'value': 'Down while closed, up while open; the turn takes 200 ms or less, and none '
                                              'when a reader asks for less motion', 'token': 'oa.motion.duration.standard'},
                {'label': 'Cross', 'value': 'Close, and the clear control in a search field'},
                {'label': 'Selected check', 'value': 'Inside a chip that is on, before its word, with a heavier outline'},
                {'label': 'Copy', 'value': 'The two sheets stay; the result goes to a status line'},
                {'label': 'Menu', 'value': 'Three bars, open or closed; the open menu holds Close and the Escape key, and '
                                           'focus returns to Menu'},
            ],
            'files': ['work/build/assets/utility/20261110_Utility-Icons-Manifest.json'],
            'related': ['17', '18'],
            'builders': ['Turn and mirror the arrow and the chevron with the transforms in the utility manifest, on the '
                         '<code>&lt;use&gt;</code>, so every line stays on the pixel grid. At 16 px the down arrow is a '
                         'mirror across the diagonal, <code>matrix(0 1 1 0 0 0)</code>, which keeps its shaft on the up '
                         'arrow’s pixel column.'],
        },
        {
            'id': '11.13', 'title': 'Mark a link to another site, and open it in the same tab.',
            'rule': ['A link that leaves our site opens in the same tab. Its mark, an arrow leaving a box, follows the '
                     'link’s last word at 16 px and stays on the line with that word, and the words “(another site)” end '
                     'the link’s name for screen readers. A link that must open a new tab says so instead: “(opens in a '
                     'new tab)”.'],
            'tokens': ['oa.size.icon.small', 'oa.size.target.minimum'],
            'why': {'text': ['A reader knows before pressing that the link leaves Oath & Action. A new tab that opens '
                             'unannounced takes away the Back button and can strand a screen reader or magnifier user on a '
                             'page they did not choose.'],
                    'basis': 'WCAG 2.2 SC 3.2.5; design judgment'},
            'correct': {'specimen': 's-11-13-correct',
                        'caption': 'Three sources, live at 360 px. Each link opens in the same tab, its mark follows its '
                                   'last word, and each stands 44 px tall in the list.'},
            'failure': {'specimen': 's-11-13-failure',
                        'caption': '<strong>Fails Rule 11.13.</strong> The link opens a new tab and says nothing about it, '
                                   'and its 24 px mark has broken from its word onto a line of its own.'},
            'specs': [
                {'label': 'Mark', 'value': 'Another site, 16 px, after the last word, in a span that does not wrap',
                 'token': 'oa.size.icon.small'},
                {'label': 'Hidden words', 'value': '“(another site)”, or “(opens in a new tab)” where it does'},
                {'label': 'Target', 'value': 'In running text, the line, at least 24 px tall; in a list of sources, 44 px '
                                             'tall', 'token': 'oa.size.target.minimum'},
            ],
            'files': ['work/build/assets/utility/svg-16/20261110_Utility-Another-Site-16px.svg'],
            'related': ['13', '24'],
            'builders': ['Wrap the last word and the mark in <code>&lt;span style="white-space: nowrap"&gt;</code>, then '
                         'the hidden words in a visually hidden span inside the link, so its name reads “... (another '
                         'site)”. Leave out <code>target="_blank"</code>.'],
        },
        {
            'id': '11.14', 'title': 'Draw interface actions with utility icons, never with topic or atlas symbols.',
            'rule': ['A topic or atlas symbol names a subject: a feedback loop, public records, a vote. It never stands for '
                     'an action on a page. Reset is the utility icon’s open circle with one arrowhead, Download is the '
                     'arrow into a tray, and each sits beside its word.'],
            'why': {'text': ['A symbol that works as a button in one place and names a subject in another teaches the '
                             'reader two meanings for one drawing. CL-024, Feedback loop, comes nearest to the refresh sign '
                             'a builder reaches for, and a loop stepper is the place a builder would reach for it.'],
                    'basis': 'Design judgment; Rule 10.1'},
            'correct': {'specimen': 's-11-14-correct',
                        'caption': 'A loop stepper from our systems atlas, live at 360 px. Play, Reset the loop, Previous '
                                   'step and Next step each carry a utility icon beside the word, and the unavailable ones '
                                   'say why.'},
            'failure': {'specimen': 's-11-14-failure',
                        'caption': '<strong>Fails Rule 11.14.</strong> CL-024, the feedback loop drawing, stands in for '
                                   'Reset. A reader learns it as a button here and meets it next as the subject of a story '
                                   'about feedback loops.'},
            'specs': [
                {'label': 'Reset', 'value': 'Three quarters of a circle with one arrowhead; “Reset” or “Start over” and its object'},
                {'label': 'Play and Pause', 'value': 'One button: its icon and word change together; playback starts only '
                                                     'on a press'},
                {'label': 'Topic and atlas symbols', 'value': 'Beside their own word, never inside a button that does '
                                                              'something (Rule 10.1)'},
            ],
            'related': ['10', '15'],
            'builders': ['When a control needs an icon the utility set lacks, use the word alone and ask the editor; do not '
                         'borrow a drawing from chapter 10.'],
        },
        {
            'id': '11.15', 'title': 'Give each error, success and warning its mark and its words.',
            'rule': ['An error, a success and a warning each take their mark before their words. The error mark is a '
                     'circle holding an exclamation mark, in the text’s ink, on the pale Error Band with a 4 px red bar, '
                     'and its words start “Error:” and say how to fix it. The success mark is a check leaving an open '
                     'circle, in Verdigris, beside what happened. The warning mark is a triangle holding an exclamation '
                     'mark, in ink, beside the notice, such as the date a record was last checked.',
                     'A field with an error carries the red bar at its left edge and points to its message, and focus moves '
                     'to the first field to fix. Copy, Search, Filter and Sort write their results to a status line in '
                     'words.'],
            'tokens': ['oa.color.state.error.mark.onNewsprint', 'oa.color.state.error.band.onNewsprint',
                       'oa.color.state.error.text.onNewsprint', 'oa.color.state.success.mark.onNewsprint',
                       'oa.color.state.warning.mark.onNewsprint'],
            'why': {'text': [f'Each state has a shape and a word, so none rests on color. The error mark draws in ink '
                             f'because Pillar Red measures {red_band} to 1 on the Error Band and {red_n} on Newsprint, '
                             f'under the 3 to 1 a mark needs; in ink it measures {ink_band} to 1, and the red bar carries '
                             f'the error’s claim on the view’s red. Verdigris measures {verd} to 1 on Newsprint.'],
                    'basis': 'WCAG 2.2 SC 1.4.1, 1.4.11, 3.3.1 and 4.1.3'},
            'correct': {'specimen': 's-11-15-correct',
                        'caption': 'A sign-up form, live at 360 px. Send it with a field wrong to see the error mark, its '
                                   'words and the red bar, and the red button step down to Charcoal; send it right to see '
                                   'the success mark.'},
            'failure': {'specimen': 's-11-15-failure',
                        'caption': '<strong>Fails Rule 11.15 and WCAG 2.2 SC 1.4.1.</strong> The message is red text beside '
                                   'a cross. The cross means Close, the red text measures 2.96 to 1, and nothing says '
                                   '“Error” or how to fix the entry.'},
            'specs': [
                {'label': 'Error', 'value': 'The mark in ink on the Error Band, a 4 px Pillar Red bar at the left, “Error:” '
                                            'and the fix', 'token': 'oa.color.state.error.band.onNewsprint'},
                {'label': 'Field with an error', 'value': 'A 4 px red bar at its left edge, aria-invalid and '
                                                          'aria-describedby to its message', 'token': 'oa.color.state.error.mark.onNewsprint'},
                {'label': 'Success', 'value': f'The mark in Verdigris, {verd} to 1, beside what happened',
                 'token': 'oa.color.state.success.mark.onNewsprint'},
                {'label': 'Warning', 'value': 'The mark in ink, never red, with a 4 px bar in ink; never for an evidence '
                                              'grade or an Illustrative label', 'token': 'oa.color.state.warning.mark.onNewsprint'},
                {'label': 'Size', 'value': '24 px beside a message; 16 px inside a line of text'},
            ],
            'files': ['work/build/assets/utility/svg-24/20261110_Utility-Error-24px.svg',
                      'work/build/assets/utility/svg-24/20261110_Utility-Success-24px.svg',
                      'work/build/assets/utility/svg-24/20261110_Utility-Warning-24px.svg'],
            'related': ['05', '17'],
            'builders': ['Put an error message in <code>role="alert"</code> or in a status line the field points to, and a '
                         'success or a result in <code>role="status"</code>. Draw the bar as a left border, which stays '
                         'visible when the system forces its own colors.'],
        },
        {
            'id': '11.16', 'title': 'When an error, the take-part mark and an intervention marker meet, give the error the red.',
            'rule': ['Rule 05.3 gives each view one working red, in this order: an error the reader must fix, then the '
                     'step a reader can take now, then the one point the headline names, which in a systems figure is '
                     'where a reform acts. So when the three meet in one view, the error keeps the red. The take-part '
                     'mark yields: its disc draws in the surface’s ink, keeps its place on the ring, and “You can take '
                     'part now” stays beside it, while the ask button steps down to Charcoal. The intervention marker '
                     'yields too: its outline stays heavier, in ink, with its words.',
                     'Once the reader fixes the error, the red goes back to the take-part mark and the ask. The '
                     'intervention marker takes the red only in a view with no error and no step to take.'],
            'tokens': ['oa.color.state.error.mark.onNewsprint', 'oa.component.button.primary.fill.onNewsprint',
                       'oa.component.mark.takePart.disc'],
            'why': {'text': ['A reader has to fix an error before taking any step, and a step a reader can take matters '
                             'more than a point we want to make. Each mark keeps its shape and its words when it yields, '
                             'so nothing it says is lost; only the color moves.'],
                    'basis': 'Rule 05.3; WCAG 2.2 SC 1.4.1'},
            'correct': {'specimen': 's-11-16-correct',
                        'caption': 'One view at 360 px. The email field’s error holds the red. The take-part disc on step '
                                   '2 and the heavier outline where reform R-01 acts stay in Charcoal with their words, '
                                   'and Remind me is Charcoal until the error is fixed.'},
            'failure': {'specimen': 's-11-16-failure',
                        'caption': '<strong>Fails Rules 11.16 and 05.3.</strong> The error, the take-part mark and the '
                                   'intervention marker all take red, so the error that blocks the reader looks no more '
                                   'urgent than the rest.'},
            'specs': [
                {'label': 'First claim', 'value': 'An error the reader must fix', 'token': 'oa.color.state.error.mark.onNewsprint'},
                {'label': 'Second claim', 'value': 'The step a reader can take now: the take-part mark and the ask',
                 'token': 'oa.component.mark.takePart.disc'},
                {'label': 'Third claim', 'value': 'Where a reform acts: the intervention marker'},
                {'label': 'A mark that yields', 'value': 'Keeps its shape, its place and its words, in the surface’s ink'},
                {'label': 'The ask while an error shows', 'value': 'Charcoal primary button',
                 'token': 'oa.component.button.primary.fill.onNewsprint'},
            ],
            'related': ['05', '12', '15'],
            'builders': ['Mark each red with <code>data-red="working"</code> and its <code>data-red-job</code>. When an error '
                         'appears, move the red: draw the take-part disc and the marker in ink, swap the ask to '
                         '<code>--oa-component-button-primary-fill-on-newsprint</code>, and swap them back once the error is '
                         'gone.'],
        },
    ]
    extras = [
        {'after_rule': '11.11', 'specimen': 's-11-icons', 'label': 'The 18 utility icons',
         'caption': 'Every utility icon at its two sizes, with the word that goes beside it.'},
        {'after_rule': '11.12', 'specimen': 's-11-menu', 'label': 'A phone menu, live at 360 px',
         'caption': 'Menu opens the chapter’s contents over the page and holds focus until Close or the Escape key shuts '
                    'it, and focus then returns to Menu. Each row’s chevron opens its list of rules.'},
        {'after_rule': '11.15', 'specimen': 's-11-marks', 'label': 'The three marks in their messages',
         'caption': 'Error, success and warning at true size, each with its words.'},
    ]
    groups = [
        {'before_rule': '11.11', 'number': 3, 'title': 'Utility icons',
         'line': 'A utility icon names an action on a page, such as Close, Download or Filter, and sits beside its word.'},
        {'before_rule': '11.15', 'number': 4, 'title': 'Error, success and warning',
         'line': 'Three marks give a message its shape, and the words beside them say what happened and what to do.'},
    ]
    ctx.fig('focus ring on Newsprint', ring, 'oa.color.focus.ring.onNewsprint against oa.color.surface.newsprint')
    return rules, extras, groups
