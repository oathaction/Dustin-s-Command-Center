// Web page renderer (DR-297, chat 10): an article page, laid out on chapter 07's grid by container queries on its own
// root, so the same markup lays out at its own width in a standalone page and inside a guide frame. Its fluid type sizes
// are the tokens' own restated in cqi (lib.fluid_cqi), for the same reason. Chapter 18's theme switch, the chart kit's
// figure and the guide's sprite are reused from their own files and code. Layout from
// work/handoffs/phase-4/20261121_Kit-Sample-Specs.md, section 2.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { spawnSync } from 'child_process';
import { ROOT, CODE, esc, fluid_cqi, mark, type_css } from '../lib.mjs';

export const type = 'web-page';
const require = createRequire(import.meta.url);
const WORDMARK24 = 'work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg';
const LOCK24 = 'work/build/assets/identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg';
const AMP16 = 'work/build/assets/identity/ampersand/20261028_Amp-B-16px-Master.svg';
const AMP14FIT = 'work/build/assets/identity/ampersand/20261109_Amp-B-14px-End-Mark-Fit-B.svg';
const KIT = path.join(ROOT, 'work/build/chart-kit');
const SHELL_CSS = path.join(ROOT, 'work/build/guide/shell/guide-shell.css');

// the chart kit's static figure, drawn by the kit's own code: a desk drawing at 621 px and a phone drawing at 328 px, the
// narrowest column each serves, so a drawing only ever scales up and no word in it drops under 13 px (the kit's lean
// switch shows the phone drawing in a figure under 480 px)
let KITMOD = null;
async function kit() {
  if (!KITMOD) {
    const m = await import(path.join(KIT, 'oa-chart.mjs'));
    KITMOD = { m, K: m.load_kit(), C: require(path.join(KIT, 'checks.js')) };
  }
  return KITMOD;
}
export async function chart_figure(id, fid, desk = 621, phone = 328) {
  const { m, K, C } = await kit();
  const sp = path.join(KIT, 'specs', `${id}.json`);
  const spec = JSON.parse(fs.readFileSync(sp, 'utf8'));
  const res = m.run_spec(spec, { grounds: ['newsprint'], widths: [1440, 390], spec_path: sp, sweep: false, no_narrow: true });
  const faults = [...res.faults];
  // 22:07 call: a figure never shows wider than its artboard (kit.css caps .oac-fig there, 720 px for a reading chart), so a
  // column wider than the artboard draws at the artboard; drawn wider, the drawing scaled down and set its words under 13 px
  const art = K.artboard(spec, K.token_reader(m.TOK.newsprint));
  desk = Math.min(desk, art); phone = Math.min(phone, art);
  const draw = (w, cls) => {
    const d = K.draw(spec, res.rows, { width: w, ground: 'newsprint', tokens: m.TOK.newsprint, extra: m.extra_rows({ datasets: res.datasets }) });
    faults.push(...C.check_drawing(spec, d, m.TOK.newsprint, `${w} px for the article`));
    return d.svg.replace('class="oac-svg"', `class="oac-svg ${cls}"`);
  };
  const svg = draw(desk, 'oac-desk') + draw(phone, 'oac-phone');
  // K.figure holds phrases together with HTML spans across the whole figure, opts.svg included, and an HTML <span> inside
  // an inline SVG's text ends the SVG when the page is parsed; so the figure is written around a mark and the drawings go
  // in after (the kit's lean method has the same fault: engineer notes, "Not fixed")
  const MARK = '<!--oa-app-drawings-->';
  const html = K.figure(spec, res.rows, { id: fid, svg: MARK, art_attrs: ' data-oa-lean', guide: true }).replace(MARK, svg);
  if (html.indexOf(svg) < 0) faults.push('figure: the drawings did not go in');
  return { html, faults, css: m.kit_parts().css, spec_id: spec.id, title: spec.title };
}

// chapter 18's theme switch, read from its own file: the fieldset alone, its target and its radio group named for this page
function theme_switch(theme, target_id, group) {
  const src = fs.readFileSync(path.join(CODE, 'c-18-theme-switch.html'), 'utf8');
  let fs_ = src.match(/<fieldset class="oa-theme"[\s\S]*?<\/fieldset>/)[0];
  fs_ = target_id ? fs_.replace(/data-oa-theme-for="[^"]*"/, `data-oa-theme-for="${target_id}"`) : fs_.replace(/\s*data-oa-theme-for="[^"]*"/, '');
  fs_ = fs_.replace(/name="oa-theme"/g, `name="${group}"`).replace(/\s+checked>/g, '>');
  fs_ = fs_.replace(new RegExp(`(value="${theme}")`), '$1 checked');
  // chat 11 (contract C4): the Selected check is the guide's sprite symbol, drawn by <use>, never the file's inline path
  fs_ = sprite_icons(fs_);
  return fs_.replace(/\s*\n\s*/g, ' ').replace(/<input\s+/g, '<input ');
}
// A utility icon a component file draws inline (<svg ... data-icon="U-<name>" ...><path .../></svg>) becomes a <use> of the
// guide's sprite at the svg's own size; the file keeps its own markup. Throws on an icon the sprite lacks.
export const SPRITE_UTILITY = ['another-site', 'arrow', 'chevron', 'close', 'copy', 'download', 'error', 'filter', 'menu', 'pause',
  'play', 'reset', 'search', 'selected-check', 'sort', 'success', 'view-full-size', 'warning'];
export function sprite_icons(html) {
  return html.replace(/(<svg\b[^>]*\bdata-icon="U-([a-z-]+)"[^>]*>)([\s\S]*?)(<\/svg>)/g, (m, open, name, inner, close) => {
    if (!SPRITE_UTILITY.includes(name)) throw new Error(`the guide's sprite has no utility icon ${name}`);
    const px = /\swidth="16"/.test(open) ? 16 : 24;
    return `${open}<use href="#oa-sym-u-${name}-${px}px"/>${close}`;
  });
}
export const switch_css = () => fs.readFileSync(path.join(CODE, 'c-18-theme-switch.css'), 'utf8');
export const switch_js = () => fs.readFileSync(path.join(CODE, 'c-18-theme-switch.js'), 'utf8');
export const switch_head_js = () => fs.readFileSync(path.join(CODE, 'c-18-theme-switch.head.js'), 'utf8');
// the shell's 1x and 2x switch for a drawing with a pixel fit (DR-179), read from the shell's own style
export function res_switch_css() {
  const t = fs.readFileSync(SHELL_CSS, 'utf8');
  return [t.match(/\.oa-at-2x \{ display: none \}/), t.match(/@media \(min-resolution: 2dppx\) \{[^\n]*\}\s*\}/)].map((x) => (x ? x[0] : '')).join('\n');
}
// the guide's own sprite code draws the kicker's symbol (tools/sprite_symbols.py)
export function sprite(ids) {
  const r = spawnSync('python3', ['-I', path.join(ROOT, 'work/build/app-kit/tools/sprite_symbols.py'), ...ids], { encoding: 'utf8' });
  if (r.status !== 0) throw new Error('sprite: ' + (r.stderr || '').trim());
  return r.stdout.trim();
}

// the page's own style: the grid by container queries on .wa (chapter 07's columns, gutters and margins by token). A
// container query's em reads the container's own font size, so .wa resets to 1rem: its breakpoints then fall where a media
// query's em would put them (Rule 07.5), whatever size the page around a frame sets
export function page_css() {
  const g = (k) => `--c:var(--oa-layout-grid-${k}-columns);--g:var(--oa-layout-grid-${k}-gutter);--m:var(--oa-layout-grid-${k}-margin)`;
  return `
.wa{container:wa/inline-size;font-size:1rem;${fluid_cqi()};background:var(--oa-color-surface);color:var(--oa-color-text-primary);font-kerning:normal;font-variant-ligatures:common-ligatures}
.wa *{box-sizing:border-box}
.wa-in{${g('phone-small')};position:relative}
@container wa (min-width: 24.375em){.wa-in{${g('phone')}}}
@container wa (min-width: 48em){.wa-in{${g('tablet')}}}
@container wa (min-width: 64em){.wa-in{${g('desktop')}}}
@container wa (min-width: 90em){.wa-in{${g('wide')}}}
.wa-row{display:block;max-width:none;margin-inline:0;padding-inline:var(--m)}
.wa-g{max-width:none;margin:0;display:grid;grid-template-columns:repeat(var(--c),minmax(0,1fr));column-gap:var(--g);padding-inline:var(--m)}
.wa-g>*{grid-column:1/-1;min-width:0}
.wa a{color:inherit}
.wa a:focus-visible,.wa input:focus-visible+.oa-theme-face{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring);outline-offset:2px}
.wa-skip{position:absolute;left:var(--m);top:8px;z-index:2;padding:8px 16px;background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label) !important;${type_css('ui')};transform:translateY(-200%)}
.wa-skip:focus{transform:none}
.wa-strip{padding-block:8px;border-bottom:1px solid var(--oa-color-border-hairline);margin:0}
.wa-strip .k{${type_css('label')};color:var(--oa-color-text-primary);margin-right:8px}
.wa-strip .n{${type_css('caption')};color:var(--oa-color-text-secondary)}
.wa-head{border-bottom:1px solid var(--oa-color-border-hairline);padding-bottom:16px}
.wa-head .bar{display:flex;align-items:center;min-height:56px}
.wa-home{display:inline-flex;color:var(--oa-color-text-primary);--amp:var(--oa-color-identity-signature)}
.wa-home svg{display:block}
@container wa (min-width: 48em){
 .wa-head{display:flex;align-items:center;justify-content:space-between;min-height:80px;padding-bottom:0}
 .wa-head .oa-theme{display:flex;align-items:center;gap:12px}
 .wa-head .oa-theme-legend{float:left;margin:0}
}
.wa-main{display:block;max-width:none;margin:0;padding:64px 0 0}
@container wa (min-width: 64em){.wa-main{padding-top:104px}}
.wa-kick{margin:0 0 24px;display:flex;align-items:center;flex-wrap:wrap;${type_css('label', { size: '0.8125rem' })}}
.wa-kick .a{color:var(--oa-color-text-primary)}
.wa-kick .d{color:var(--oa-color-text-secondary);margin-inline:8px}
.wa-kick svg{color:var(--oa-component-icon-ink);margin-right:8px;flex:none}
.wa-kick .b{color:var(--oa-color-text-secondary)}
.wa-h1{margin:0;${type_css('title')};text-wrap:balance}
.wa-intro{margin:32px 0 0;${type_css('intro')};text-wrap:pretty;max-width:var(--oa-layout-measure-intro-max)}
.wa-by{margin:32px 0 0;padding-top:16px;border-top:1px solid var(--oa-color-border-hairline);display:flex;flex-wrap:wrap;column-gap:24px;align-items:baseline;max-width:var(--oa-layout-measure-intro-max)}
.wa-by .nm{${type_css('ui')};color:var(--oa-color-text-primary)}
.wa-by time{${type_css('caption')};color:var(--oa-color-text-secondary)}
@container wa (min-width: 48em){.wa-by time{position:relative}.wa-by time::before{content:"·";position:absolute;left:-15px;color:var(--oa-color-text-secondary)}}
.wa-h2{margin:80px 0 16px;${type_css('h3')};text-wrap:balance}
.wa-p{margin:0;${type_css('body')};text-wrap:pretty;max-width:var(--oa-layout-measure-body-ideal)}
.wa-p+.wa-p{margin-top:16px}
.wa-fig{margin-block:48px}
.wa-fig .oac-fig{margin:0}
.wa-end{white-space:nowrap}
.wa-end svg{margin-left:.5em}
.wa-end .m16{height:.831em;width:auto;vertical-align:-.052em}
.wa-end .f14{display:none;vertical-align:0}
@media (resolution: 1dppx){.wa-end .f14{display:inline}.wa-end .m16{display:none}}
.wa-src{margin:24px 0 0;${type_css('caption')};color:var(--oa-color-text-secondary);max-width:var(--oa-layout-measure-body-ideal)}
.wa-foot{margin-top:104px;padding-block:32px 40px;border-top:1px solid var(--oa-color-border-hairline-on-charcoal)}
.wa-foot .r1{display:flex;align-items:center;gap:12px;margin:0;${type_css('body-small')};color:var(--oa-color-text-primary)}
.wa-foot .r1 svg{flex:none;color:var(--oa-color-text-primary);--link:var(--oa-color-text-primary);--lever:var(--oa-color-identity-signature-on-charcoal)}
.wa-foot .r2{margin:16px 0 0;${type_css('caption')};color:var(--oa-color-text-secondary)}
@container wa (min-width: 48em){.wa-open{grid-column:1/9}.wa-lead{grid-column:1/8}.wa-body{grid-column:1/8}.wa-fig{grid-column:1/9}}
@container wa (min-width: 64em){.wa-open{grid-column:2/12}.wa-lead{grid-column:2/10}.wa-body{grid-column:2/9}.wa-fig{grid-column:2/10}}
@container wa (min-width: 90em){.wa-open{grid-column:3/11}.wa-lead{grid-column:3/-1}.wa-body{grid-column:3/8}.wa-fig{grid-column:3/9}}
`;
}

// The page's landmarks (header, main, footer, section) set every box property they rely on through their own classes,
// which outrank a host page's element rules (a guide shell's main {...}), so a frame lays out as the page does alone.
// The page at one theme. pid prefixes every id (unique per frame on a measurement page); theme_for names the element the
// switch sets (a frame's own root) or, left null, the page's root.
export function page_html(spec, fig, { pid = 'wa', theme = 'light', theme_for = null, group = 'oa-theme' } = {}) {
  const words = (s) => esc(s);
  const last = spec.p2.trim().split(' ');
  const end_word = last.pop();
  const end = `<span class="wa-end">${words(end_word)}${mark(AMP14FIT, { cls: 'f14', width: 13, height: 13 })}${mark(AMP16, { cls: 'm16', width: 14, height: 16 })}</span>`;
  const sym = `<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-031" data-icon-family="topic">`
    + `<use class="oa-at-1x" href="#oa-sym-${spec.kicker_symbol}-24px"/><use class="oa-at-2x" href="#oa-sym-${spec.kicker_symbol}"/></svg>`;
  return `<div class="wa" id="${pid}"${theme_for ? ` data-oa-theme="${theme}"` : ''} data-oa-application="${esc(spec.id)}"><div class="wa-in">`
    + `<a class="wa-skip" href="#${pid}-main">${words(spec.skip)}</a>`
    + `<aside class="wa-row wa-strip" aria-label="About this sample"><span class="k">${words(spec.strip[0])}</span><span class="n">${words(spec.strip[1])}</span></aside>`
    + `<header class="wa-row wa-head"><div class="bar"><a class="wa-home" href="#${pid}" aria-label="${esc(spec.home_name)}">`
    + mark(WORDMARK24, { width: 221, height: 24, red: 'signature' }) + `</a></div>${theme_switch(theme, theme_for, group)}</header>`
    + `<main id="${pid}-main" class="wa-main" tabindex="-1"><article>`
    + `<div class="wa-g"><div class="wa-open"><p class="wa-kick"><span class="a">${words(spec.kicker[0])}</span><span class="d" aria-hidden="true">·</span>${sym}<span class="b">${words(spec.kicker[1])}</span></p>`
    + `<h1 class="wa-h1">${words(spec.headline)}</h1></div>`
    + `<div class="wa-lead"><p class="wa-intro">${words(spec.intro)}</p>`
    + `<p class="wa-by"><span class="nm">${words(spec.byline[0])}</span><time datetime="${spec.date_iso}">${words(spec.byline[1])}</time></p></div></div>`
    + `<section class="wa-g" aria-labelledby="${pid}-s1"><div class="wa-body"><h2 class="wa-h2" id="${pid}-s1">${words(spec.section)}</h2>`
    + `<p class="wa-p">${words(spec.p1)}</p></div>`
    + `<div class="wa-fig">${fig.replace(/id="oac-[a-z0-9-]+/g, (m) => m + '-' + pid).replace(/(aria-(?:labelledby|describedby|controls)=")([^"]+)"/g, (m, a, v) => a + v.split(' ').map((x) => x.startsWith('oac-') ? x + '-' + pid : x).join(' ') + '"').replace(/href="#(oac-[a-z0-9-]+)"/g, `href="#$1-${pid}"`)}</div>`
    + `<div class="wa-body"><p class="wa-p">${words(last.join(' '))} ${end}</p><p class="wa-src">${words(spec.def_source)}</p></div></section>`
    + `</article></main>`
    + `<footer class="wa-row wa-foot oa-surface-charcoal"><p class="r1">${mark(LOCK24, { width: 24, height: 24, red: 'signature' })}<span>${words(spec.tagline)}</span></p>`
    + `<p class="r2">${words(spec.footer_note)}</p></footer>`
    + `</div></div>`;
}

export async function render(spec) {
  const fig = await chart_figure(spec.chart, 'oac-' + spec.chart);
  return {
    id: spec.id, type, unit: 'px', alt: spec.alt, fig,
    css: page_css() + '\n' + switch_css() + '\n' + res_switch_css(),
    sprite: sprite([`oa-sym-${spec.kicker_symbol}`, `oa-sym-${spec.kicker_symbol}-24px`, 'oa-sym-u-selected-check-24px']),
    page: (o) => page_html(spec, fig.html, o),
    widths: spec.widths, themes: ['light', 'dark'],
    exports: spec.widths.flatMap((x) => ['light', 'dark'].map((t) => ({ kind: 'png', full_page: true, theme: t, platform: x.platform,
      name: `${spec.export_name}-${x.w}-${t === 'light' ? 'Light' : 'Dark'}`, viewport: [x.w, x.vh] }))),
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}
