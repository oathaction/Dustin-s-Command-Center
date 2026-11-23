// Website renderer (chat 11): chapter 20's pages, drawn from the design director's page specs
// (work/handoffs/phase-4/20261121_Web-Page-Specs.md, sections 0 to 7) with the site's words from the chapter 20 generator
// (DD-3: phase4_ch20_build.py --page-words <id>; until it exists, the file OA_PAGE_WORDS names, a stand-in from the specs'
// drafts). One renderer draws every page kind and every view the guide asks for:
//   page "home" (A06), "article" (A07), "act" (A08), each full length at its widths and themes, and one window tall (R1);
//   part "masthead" (A04: the article page's masthead band, closed, and the menu open one window tall) and part "footer" (A05).
// Each page lays out by container queries on its own root (.ws, reset to 1rem, its fluid type restated in cqi, contract C3),
// so the same markup draws a standalone export at its window and a guide frame at its width. Chapter 18's masthead, dialog,
// switch and their scripts are read from their files (site-parts.mjs); the chart kit draws S10, S66 and S86 by its own code
// (web-page.mjs chart_figure), and a frame keeps only the drawing its width shows (R4); icons come from the guide's sprite.
//
// Content keys (layout; words come from the generator unless words_file names a file): id, type "web-site", page, part
// ("page", "masthead" or "footer"), guide, widths [{w, vh, platform}], views [C4 keys: "1440-light", "390-light-screen",
// "390-light-open"], export_name, export_date (YYYYMMDD, PR-S2), words_file (PR-M2: a file holding the generator's entry
// shape for this page, with "site" or without it), charts {id: [desk, phone]}, plate_head, plate_line.
import fs from 'fs';
import path from 'path';
import { spawnSync } from 'child_process';
import { ROOT, esc, fluid_cqi, mark, touch, type_css } from '../lib.mjs';
import { chart_figure, res_switch_css, sprite } from './web-page.mjs';
import { UTILITY_SPRITE, close_on_widen_js, masthead, masthead_css, masthead_js, switch_css, switch_head_js, switch_js } from './site-parts.mjs';

export const type = 'web-site';
const GEN = 'work/build/scripts/phase-4/phase4_ch20_build.py';
const L3 = 'work/build/assets/identity/lockups/20261110_L3-Horizontal-Master.svg';
const LOCK24 = 'work/build/assets/identity/lockmark/20261109_Lockmark-24px-Master-Outline.svg';
const AMP16 = 'work/build/assets/identity/ampersand/20261028_Amp-B-16px-Master.svg';
const AMP24 = 'work/build/assets/identity/ampersand/20261028_Amp-B-24px-Master.svg';
const AMP14FIT = 'work/build/assets/identity/ampersand/20261109_Amp-B-14px-End-Mark-Fit-B.svg';
const BP = { phone: 24.375, tablet: 48, desktop: 64, wide: 90 };   // chapter 07's breakpoints, in em
const NAV_BP = 64;                                                // the parts sit in the bar from 64em (spec 2.2)
const PILLAR_SYMS = ['cl-019', 'cl-020', 'cl-021', 'cl-022'];

// ---------------------------------------------------------------------------------------------------------------- words
let WORDS = null;
export function words() {
  if (WORDS) { touch(WORDS.__from); return WORDS; }
  if (fs.existsSync(path.join(ROOT, GEN))) {
    const r = spawnSync('python3', ['-I', path.join(ROOT, GEN), '--page-words', 'all'], { encoding: 'utf8', cwd: ROOT });
    if (r.status !== 0) throw new Error('page words: ' + (r.stderr || r.stdout).trim().slice(0, 400));
    fs.readFileSync(path.join(ROOT, GEN));   // the generator is a plate input (DD-3)
    WORDS = JSON.parse(r.stdout);
    WORDS.__from = GEN;
  } else if (process.env.OA_PAGE_WORDS) {
    WORDS = JSON.parse(fs.readFileSync(process.env.OA_PAGE_WORDS, 'utf8'));
    WORDS.__from = process.env.OA_PAGE_WORDS;
  } else {
    throw new Error(`no page words: ${GEN} is not written yet; set OA_PAGE_WORDS to a stand-in file`);
  }
  return WORDS;
}
const PAGE_ID = { home: 'A06', article: 'A07', act: 'A08' };
// DD-6: the trackers' marks are chapter 11's own drawing (tools/ch11_marks.py runs apply_systems_ch11.py's steps_svg and
// sample, read-only); the states map from the generator's words to chapter 11's
const CH11 = { done: 'done', now: 'now', ahead: 'notyet', never: 'skipped', stopped: 'stopped' };
const ch11_state = (x) => (x.state === 'now' && x.take_part ? 'take' : CH11[x.state]);
function ch11(reqs) {
  const f = path.join(process.env.TMPDIR || '/tmp', `oa-ch11-${process.pid}-${Date.now()}.json`);
  fs.writeFileSync(f, JSON.stringify(reqs));
  const r = spawnSync('python3', ['-I', path.join(ROOT, 'work/build/app-kit/tools/ch11_marks.py'), f], { encoding: 'utf8' });
  fs.unlinkSync(f);
  if (r.status !== 0) throw new Error('chapter 11 marks: ' + (r.stderr || r.stdout).trim().slice(0, 400));
  fs.readFileSync(path.join(ROOT, 'work/build/scripts/phase-2/apply_systems_ch11.py'));   // an input of the plate (C4)
  return JSON.parse(r.stdout);
}
// the marks' colors, resolved on the element that holds them, so a mark inside a Charcoal panel takes the panel's inks
const MARK_VARS = '--ink:var(--oa-color-graphic-essential);--sub:var(--oa-color-graphic-subtle);--bg:var(--oa-color-surface);'
  + '--txt:var(--oa-color-text-primary);--txt2:var(--oa-color-text-secondary);--red:var(--oa-color-palette-pillar-red);'
  + '--key:var(--oa-component-button-ask-keyline-on-newsprint)';
const STEP_SAY = (w, st) => String(st === 'take' ? w.now : w[st]).toLowerCase();
// the words for one application: its own entry, whose "site" holds the shared words; A04 and A05 take the article's
function page_words(W, id, page) {
  const e = W[id];
  if (!e) throw new Error(`the generator prints no words for ${id}`);
  const pw = e.article ? { ...e.article } : { ...e };
  pw.site = e.site;
  return pw;
}
const kick = (k) => (Array.isArray(k) ? k : [k, null]);

// ---------------------------------------------------------------------------------------------------------------- style
const g = (k) => `--c:var(--oa-layout-grid-${k}-columns);--g:var(--oa-layout-grid-${k}-gutter);--m:var(--oa-layout-grid-${k}-margin)`;
const at = (em, body) => `@container ws (min-width: ${em}em){${body}}`;
// W2 (the accessibility lead's walk): a rule for the dark page, chosen or by the device, keyed as tokens.css keys the dark
// tokens: an explicit Dark on the page or the frame, and the device's dark where no Light was chosen
// chat 11c: exported for the atlas pages' own dark rules, keyed as the website's
// PR-S8 (chat 12): a page that names its own theme keeps it; the root's Dark reaches only a page that names none, so a
// frame drawn and labeled light stays light when a reader sets the guide dark. The root's arm keeps the old first
// selector's specificity (0,2,0) by :where(), so the cascade on the working pages is as before.
export const dark = (sel, decl) => `.ws[data-oa-theme="dark"] ${sel},:where(:root[data-oa-theme="dark"]) .ws:not([data-oa-theme]) ${sel}{${decl}}`
  + `@media (prefers-color-scheme: dark){:root:not([data-oa-theme="light"]) .ws:not([data-oa-theme="light"]) ${sel}{${decl}}}`;
const under = (em, body) => `@container ws (max-width: ${em - 0.001}em){${body}}`;

export function site_css() {
  return `
.ws{container:ws/inline-size;font-size:1rem;${fluid_cqi()};position:relative;background:var(--oa-color-surface);color:var(--oa-color-text-primary);font-kerning:normal;font-variant-ligatures:common-ligatures}
.ws *{box-sizing:border-box}
.ws-in{${g('phone-small')};position:relative;font:var(--oa-type-body)}
${at(BP.phone, `.ws-in{${g('phone')}}`)}
${at(BP.tablet, `.ws-in{${g('tablet')}}`)}
${at(BP.desktop, `.ws-in{${g('desktop')}}`)}
${at(BP.wide, `.ws-in{${g('wide')}}`)}
.ws-g{display:grid;grid-template-columns:repeat(var(--c),minmax(0,1fr));column-gap:var(--g);padding-inline:var(--m);max-width:none;margin:0}
.ws-g>*{grid-column:1/-1;min-width:0}
.ws p,.ws h1,.ws h2,.ws h3,.ws ul,.ws ol,.ws blockquote,.ws figure{margin:0}
.ws a{color:inherit}
.ws a:focus-visible,.ws button:focus-visible,.ws input:focus-visible+.oa-theme-face{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring);outline-offset:var(--oa-border-focus-offset)}
.ws .vh{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.ws svg[data-icon]{flex:none}
/* the skip link (spec 0) */
.ws-skip{position:absolute;left:var(--m);top:8px;z-index:3;display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);padding:8px 16px;background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label) !important;font:var(--oa-type-ui);text-decoration:none;transform:translateY(-200%)}
.ws-skip:focus{transform:none}
/* the masthead (spec 2), over chapter 18's own style */
.ws .oa-masthead{border-bottom-color:var(--oa-color-border-hairline)}
.ws .oa-masthead-bar{min-height:56px;padding:0 var(--m);gap:0 16px;flex-wrap:nowrap}
.ws .oa-masthead-home{min-height:var(--oa-size-target-touch);display:inline-flex;align-items:center}
.ws .ws-h1home{display:contents;font:inherit}
.ws .ws-l3,.ws .oa-masthead-wm--16{display:none}
.ws .oa-masthead-wm--24{display:block}
.ws .ws-l3{color:var(--oa-color-text-primary);--amp:var(--oa-color-identity-signature);--lever:var(--oa-color-identity-signature);--link:var(--oa-color-palette-stone);--line:var(--oa-color-palette-stone)}
${dark('.ws-l3', '--link:var(--oa-color-text-primary);--line:var(--oa-color-text-primary)')}
${under(BP.phone, '.ws .oa-masthead-wm--24{display:none}.ws .oa-masthead-wm--16{display:block}.ws .oa-masthead-home{padding-block:14px}')}
${at(BP.tablet, '.ws .oa-masthead-wm--24,.ws .oa-masthead-wm--16{display:none}.ws .ws-l3{display:block}.ws .oa-masthead-bar{min-height:80px}')}
.ws .oa-masthead-nav{display:none}
.ws .oa-masthead-menu{display:inline-flex;margin-left:auto}
.ws .oa-site-switch-bar{display:none}
.ws .oa-site-switch-menu{margin-top:24px}
${at(NAV_BP, `.ws .oa-masthead-bar{flex-wrap:wrap;padding-bottom:16px}
 .ws .oa-masthead-home{height:80px}
 .ws .oa-masthead-nav{display:flex;align-items:center;height:80px;margin-left:auto}
 .ws .oa-masthead-menu{display:none}
 .ws .oa-masthead-parts{gap:0 var(--ws-part-gap,16px);flex-wrap:nowrap}
 .ws .oa-masthead-parts>li:nth-child(5){position:relative}
 .ws .oa-masthead-parts>li:nth-child(5)::before{content:"";position:absolute;left:calc(var(--ws-part-gap,16px) / -2);top:12px;width:1px;height:20px;background:var(--oa-color-border-hairline)}
 .ws .oa-site-switch-bar{display:flex;flex:0 0 100%;justify-content:flex-end;align-items:center;gap:12px;height:44px}
 .ws .oa-site-switch-bar .oa-theme-legend{float:left;margin:0}
 .ws .oa-site-switch-bar .oa-theme-row{flex-wrap:nowrap}`)}
${at(BP.wide, '.ws{--ws-part-gap:32px}')}
/* the menu (spec 3) */
.ws .oa-masthead-dialog{padding:0 var(--m) 32px}
.ws .oa-masthead-dialog-head{min-height:56px}
.ws .oa-masthead-dialog-nav{margin-top:24px}
.ws .oa-masthead-list>li:nth-child(4){border-bottom-color:var(--oa-color-border-strong)}
.ws.ws-open{min-height:var(--ws-vh)}
.ws-in>.ws-foot:first-child{margin-top:0}
.ws.ws-open .oa-masthead-dialog{display:block;position:absolute;inset:0;width:100%;height:var(--ws-vh);z-index:4;overflow:hidden}
/* the footer (spec 4) */
.ws-foot{margin-top:104px}
.ws-foot-lists{border-top:2px solid var(--oa-color-border-strong);padding-top:48px}
.ws-strip{margin-top:48px;padding-block:40px}
${at(BP.tablet, '.ws-strip{padding-block:56px}')}
${dark('.ws-strip', 'box-shadow:inset 0 1px 0 var(--oa-color-border-hairline-on-charcoal)')}
.ws-foot nav>.ws-g{padding-inline:0;row-gap:32px}
.ws-foot .grp{grid-column:span 2}
${at(BP.tablet, '.ws-foot .grp{grid-column:span 2}')}
${at(BP.desktop, '.ws-foot .grp{grid-column:span 3}')}
.ws-foot h2{${type_css('label')};color:var(--oa-color-text-secondary);margin:0 0 8px}
.ws-foot ul{list-style:none;padding:0}
.ws-foot li a{display:flex;align-items:center;min-height:var(--oa-size-target-touch);${type_css('body-small')};color:var(--oa-color-text-primary);text-decoration:none}
.ws-foot li a:hover{text-decoration:underline;text-decoration-thickness:1px}
.ws-foot .row{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 24px}
.ws-foot .sig{display:flex;align-items:center;gap:12px;${type_css('body-small')};color:var(--oa-color-text-primary)}
.ws-foot .sig svg{display:block;color:var(--oa-color-text-primary);--link:var(--oa-color-text-primary);--line:var(--oa-color-text-primary);--lever:var(--oa-color-identity-signature-on-charcoal)}
.ws-foot .addr{display:flex;align-items:center;gap:8px;${type_css('caption')};color:var(--oa-color-text-secondary)}
${under(BP.tablet, '.ws-foot .addr{flex:0 0 100%}.ws-foot .row{row-gap:8px}')}
.ws-illus{${type_css('label')};padding:2px 6px;border:1px solid var(--oa-color-border-strong-on-charcoal);color:var(--oa-color-text-secondary)}
/* panels: one a section, Charcoal in both themes, with a 1 px edge on the dark page (Rule 20.5's correct plate) */
${dark('.ws-panel', 'box-shadow:inset 0 0 0 1px var(--oa-color-border-hairline-on-charcoal)')}
/* main */
.ws-main{display:block;padding-top:32px}
${at(BP.tablet, '.ws-main{padding-top:48px}')}
/* the pillar row, 24 px (Rule 09.1) */
.ws-prow{display:flex;flex-wrap:wrap;align-items:center;row-gap:8px;list-style:none;padding:0;margin:0 0 32px !important}
.ws-prow li{display:flex;align-items:center;${type_css('body')};color:var(--oa-color-text-primary)}
.ws-prow li svg.pi{color:var(--oa-component-icon-ink);margin:0 8px 0 -1px}
.ws-prow li svg.ar{width:16px;height:16px;margin:0 12px}
.ws-prow li[aria-current] .w{font-weight:var(--oa-font-weight-bold);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:5px}
/* kicker (Rule 01.21) */
.ws-kick{display:flex;align-items:center;flex-wrap:wrap;${type_css('label')}}
.ws-kick .a{color:var(--oa-color-text-primary)}
.ws-kick .d{color:var(--oa-color-text-secondary);margin-inline:8px}
.ws-kick svg{color:var(--oa-component-icon-ink);margin-right:8px;margin-block:calc((var(--oa-type-label-line-height) * 1em - 24px) / 2)}
.ws-kick .b{color:var(--oa-color-text-secondary)}
/* figures and links */
.ws-fig{margin-block:48px}
.ws-fig .oac-fig{margin:0}
.ws-out{white-space:nowrap}
.ws-nw{white-space:nowrap}
.ws-out svg{width:16px;height:16px;margin-left:4px;vertical-align:-2px}
.ws-end{white-space:nowrap}
.ws-end svg{margin-left:.5em}
.ws-end .m16{height:.831em;width:auto;vertical-align:-.052em}
.ws-end .f14{display:none;vertical-align:0}
@media (resolution: 1dppx){.ws-end .f14{display:inline}.ws-end .m16{display:none}}
.ws-p{${type_css('body')};text-wrap:pretty;max-width:var(--oa-layout-measure-body-ideal)}
.ws-p+.ws-p{margin-top:16px !important}
.ws-p a{text-decoration-thickness:1px;text-underline-offset:.15em}
.ws-p a:hover{text-decoration-thickness:2px}
.ws-src{${type_css('caption')};color:var(--oa-color-text-secondary);max-width:var(--oa-layout-measure-body-ideal);margin-top:24px !important}
.ws-h2{${type_css('h3')};text-wrap:balance;margin:80px 0 16px !important}
.ws-h3{${type_css('h4')};text-wrap:balance;margin:0 0 16px !important}
/* Rule 07.4: a heading after a block of the section sits 48 px under it and 16 px over its own text */
.ws-body>.ws-h3:not(:first-child),.ws-body+.ws-body>.ws-h3:first-child{margin-top:48px !important}
/* the home page (spec 5) */
.ws-home{row-gap:48px}
.ws-sec{display:block;min-width:0}
.ws-cell{position:relative;display:flex;align-items:center;min-height:88px;padding:20px}
.ws-cell h2{display:flex;align-items:center;gap:12px;${type_css('intro', { size: '1.1875rem' })};font-weight:var(--oa-font-weight-bold);color:var(--oa-color-text-primary)}
.ws-cell h2 svg{color:var(--oa-color-text-primary)}
.ws-cell .ar{position:absolute;width:24px;height:24px;color:var(--oa-color-text-primary);right:20px;top:calc(50% - 12px);transform:rotate(90deg)}
.ws-card{padding-top:24px}
.ws-card>*+*{margin-top:12px !important}
.ws-card .ws-kick+*{margin-top:16px !important}
.ws-card h3{${type_css('h3')};text-wrap:balance}
/* W5 (AL-15): the headline link's box reaches the 44 px target from its own line height, the type unmoved */
.ws-card h3 a{--pad:max(0px, calc((var(--oa-size-target-touch) - 1lh) / 2));display:block;padding-block:var(--pad);margin-block:calc(-1 * var(--pad));text-decoration:none}
.ws-card h3 a:hover,.ws-card h3 a:focus-visible{text-decoration:underline;text-decoration-thickness:2px}
.ws-card .dek{${type_css('body-small')};text-wrap:pretty}
.ws-card .st{${type_css('body-small')}}
.ws-card .ws-trk svg{display:block;max-width:100%;height:auto}
.ws-card .st b{font-weight:var(--oa-font-weight-bold)}
.ws-card .dt,.ws-card .src{${type_css('caption')};color:var(--oa-color-text-secondary)}
.ws-card .dt+.src{margin-top:8px !important}
.ws-card .go{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);${type_css('ui')};text-decoration-thickness:1px;text-underline-offset:.2em}
.ws-card .go:hover{text-decoration-thickness:2px}
${at(BP.tablet, `.ws-cell{min-height:112px;padding:32px 24px}.ws-cell h2{font-size:1.375rem}.ws-card{padding-top:32px}`)}
${at(BP.desktop, `.ws-home{row-gap:48px}
 .ws-home>.ws-sec{grid-column:span 6}
 .ws-home>.ws-sec .ws-cell{margin-right:calc(var(--g) / -2)}
 .ws-home>.ws-sec:nth-child(2n) .ws-cell{margin-right:0;margin-left:calc(var(--g) / -2)}
 .ws-home>.ws-sec .ws-cell .ar{transform:none;right:calc(var(--g) / -2);z-index:1}
 .ws-home>.ws-sec:nth-child(2) .ws-cell .ar{right:24px}
 .ws-home>.ws-sec:nth-child(4) .ws-cell .ar{display:none}
 .ws-home>.ws-atlas{grid-column:1/-1}`)}
${at(BP.wide, `.ws-home>.ws-sec{grid-column:span 3}
 .ws-home>.ws-sec .ws-cell,.ws-home>.ws-sec:nth-child(2n) .ws-cell{margin-inline:calc(var(--g) / -2)}
 .ws-home>.ws-sec:first-child .ws-cell{margin-left:0}
 .ws-home>.ws-sec:nth-child(4) .ws-cell{margin-right:0}
 .ws-home>.ws-sec:nth-child(2) .ws-cell .ar{right:calc(var(--g) / -2)}`)}
.ws-cell .ar.last{display:none}
${dark('.ws-cell', 'box-shadow:inset 0 1px 0 var(--oa-color-border-hairline-on-charcoal),inset 0 -1px 0 var(--oa-color-border-hairline-on-charcoal)')}
.ws-atlas{margin-top:32px}
.ws-atlas .lab{${type_css('label')};color:var(--oa-color-text-secondary);margin-bottom:8px !important}
.ws-abar{padding:24px}
${at(BP.tablet, '.ws-abar{padding:32px}')}
.ws-atlas h2{${type_css('section')};text-wrap:balance;color:var(--oa-color-text-primary)}
.ws-atlas .intro{${type_css('intro')};text-wrap:pretty;margin:32px 0 48px !important}
.ws-atlas .pair{display:grid;grid-template-columns:repeat(var(--c),minmax(0,1fr));column-gap:var(--g);row-gap:32px;align-items:start}
.ws-atlas .pair>*{grid-column:1/-1;min-width:0}
.ws-qs .lab{color:var(--oa-color-text-secondary);margin-bottom:8px !important}
.ws-qs ul{list-style:none;padding:0;border-top:2px solid var(--oa-color-border-strong)}
.ws-qs li{border-bottom:1px solid var(--oa-color-border-hairline)}
.ws-qs li a{display:block;min-height:var(--oa-size-target-touch);padding-block:10px;${type_css('body')};color:var(--oa-color-text-primary);text-decoration:none}
.ws-qs li a:hover{text-decoration:underline}
.ws-qs li a svg{width:16px;height:16px;margin-left:8px;vertical-align:-2px}
.ws-qs .open{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);margin-top:24px;${type_css('ui')};color:var(--oa-color-text-primary);text-decoration-thickness:1px;text-underline-offset:.2em}
${at(BP.desktop, `.ws-atlas .intro{grid-column:1/9}.ws-atlas .pair .ws-qs{grid-column:1/6}.ws-atlas .pair .ws-fig{grid-column:6/13;margin:0}`)}
${at(BP.wide, `.ws-atlas .intro{grid-column:1/8}.ws-atlas .pair .ws-qs{grid-column:1/5}.ws-atlas .pair .ws-fig{grid-column:5/13}`)}
.ws-atlas .pair .ws-fig{margin:0}
.ws-atlas>.ws-g{padding-inline:0}
/* the article and the Act page (specs 6 and 7) */
.ws-art .ws-h1{${type_css('title')};text-wrap:balance}
.ws-act .ws-h1{${type_css('section')};text-wrap:balance}
.ws-open-col>*+*{margin-top:24px !important}
.ws-open-col .ws-kick+.ws-h1{margin-top:24px !important}
.ws-open-col .ws-h1+*{margin-top:32px !important}
.ws-intro{${type_css('intro')};text-wrap:pretty}
.ws-checked{${type_css('caption')};color:var(--oa-color-text-secondary)}
.ws-by{display:flex;flex-wrap:wrap;column-gap:24px;align-items:baseline;padding-top:16px;border-top:1px solid var(--oa-color-border-hairline)}
.ws-by .nm{${type_css('ui')}}
.ws-by time{${type_css('caption')};color:var(--oa-color-text-secondary)}
.ws-count,.ws-fact{padding:24px;align-self:start}
:is(.ws-count,.ws-fact) .fig{${type_css('figure')};color:var(--oa-color-text-primary)}
/* a figure fits its panel at every width: from 64em to 90em the grid gives the panel four of twelve columns (235 px inside
   at 1,024), so the figure steps down the type scale to the section size (the panel cannot be a query container itself:
   that would size its fluid type by the panel) */
@container ws (min-width: 64em) and (max-width: 89.99em){:is(.ws-count,.ws-fact) .fig{font-size:var(--oa-type-section-font-size);line-height:var(--oa-type-section-line-height)}}
:is(.ws-count,.ws-fact) .l1{${type_css('body')};color:var(--oa-color-text-primary);margin-top:8px !important}
:is(.ws-count,.ws-fact) .l2{${type_css('body-small')};color:var(--oa-color-text-secondary);margin-top:8px !important}
:is(.ws-count,.ws-fact) .src{${type_css('caption')};color:var(--oa-color-text-secondary);margin-top:16px !important}
.ws-fact-w{margin-top:32px;align-self:start}
.ws-fact-src{${type_css('caption')};color:var(--oa-color-text-secondary);margin-top:8px !important}
${at(BP.tablet, '.ws-count,.ws-status,.ws-fact{padding:32px}')}
${at(BP.desktop, '.ws-has-fact>.ws-fact-w{grid-column:9/13;grid-row:1;margin-top:80px}.ws-has-fact>.ws-body:nth-child(1){grid-row:1}')}
.ws-stack{display:contents}
${at(BP.desktop, `.ws-art .ws-head{grid-template-rows:auto auto auto auto 1fr}
 .ws-art .ws-lead2{grid-row:5;align-self:start}
 .ws-act .ws-head{grid-template-rows:auto 1fr}
 .ws-act .ws-op2{grid-row:2;align-self:start}
 .ws-art .ws-prow-w,.ws-art .ws-kick-w,.ws-art .ws-h1-w{grid-column:2/12}
 .ws-art .ws-lead{grid-column:2/9}
 .ws-art .ws-count{grid-column:9/13;grid-row:4/6}
 .ws-art .ws-body{grid-column:2/9}
 .ws-art .ws-fig{grid-column:2/10}
 .ws-act .ws-op{grid-column:2/9}
 .ws-act .ws-status{grid-column:9/13;grid-row:1/3}
 .ws-act .ws-body{grid-column:2/9}
 .ws-act .ws-doc{grid-column:1/13}
 .ws-act .ws-sum{grid-column:2/10}
 .ws-act .ws-fig{grid-column:2/10}
 .ws-act .ws-cpanel{grid-column:2/12}`)}
${at(BP.wide, `.ws-art .ws-prow-w,.ws-art .ws-kick-w,.ws-art .ws-h1-w{grid-column:3/11}
 .ws-art .ws-lead{grid-column:3/9}
 .ws-art .ws-body{grid-column:3/8}
 .ws-art .ws-fig{grid-column:3/9}
 .ws-act .ws-op{grid-column:3/9}
 .ws-act .ws-body{grid-column:3/8}
 .ws-act .ws-doc{grid-column:1/13}
 .ws-act .ws-sum{grid-column:3/9}
 .ws-act .ws-fig{grid-column:3/9}
 .ws-act .ws-cpanel{grid-column:3/11}`)}
/* DD12-Q1 (chat 12): the comment panel keeps specs 11.5's wide body columns, cols 3 to 10 (2 to 11 from 64em), which hold
   the Comment screen inside Rule 05.1; its words stop at the body measure, inside the chart's edge at col 8 (CR-15) */
${under(BP.desktop, '.ws-art .ws-count{margin-top:32px}.ws-art .ws-count+.ws-lead2{margin-top:32px}.ws-act .ws-status{margin-top:24px}')}
.ws-lead>*+*{margin-top:32px !important}
.ws-body>*{max-width:var(--oa-layout-measure-body-ideal)}
/* the status panel's upright steps (Rule 11.6) and the ask (Rules 11.4, 11.7; AL-13) */
.ws-status{padding:24px;align-self:start}
.ws-status .lab,.ws-cpanel .lab{${type_css('label')};color:var(--oa-color-text-secondary);margin-bottom:16px !important}
.ws-steps{list-style:none;padding:0;position:relative}
.ws-steps li{position:relative;display:grid;grid-template-columns:42px 1fr;column-gap:10px;padding-bottom:12px}
.ws-steps li::before{content:"";position:absolute;left:20.5px;top:21px;bottom:-21px;width:1px;background:var(--sub)}
.ws-steps li.on::before{left:20px;width:2px;background:var(--ink)}
.ws-steps li:last-child::before{display:none}
.ws-steps .mkw{position:relative;z-index:1;display:block;width:42px;height:42px}
.ws-steps li>span:last-child{padding-top:9px}
.ws-steps .c{position:relative;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:var(--oa-font-weight-bold) 14px/1 var(--oa-font-family-reading);font-variant-numeric:tabular-nums}
.ws-steps .done .c{background:var(--oa-color-text-primary);color:var(--oa-color-surface)}
.ws-steps .now .c{box-shadow:inset 0 0 0 3px var(--oa-color-text-primary);color:var(--oa-color-text-primary)}
.ws-steps .ahead .c{box-shadow:inset 0 0 0 1.5px var(--oa-color-text-secondary);color:var(--oa-color-text-secondary)}
.ws-steps .tp{position:absolute;right:-4px;top:-4px;width:14px;height:14px;border-radius:50%;background:var(--oa-color-surface);display:block}
.ws-steps .tp::after{content:"";position:absolute;left:1.5px;top:1.5px;width:11px;height:11px;border-radius:50%;background:var(--oa-color-palette-pillar-red);box-shadow:inset 0 0 0 1px var(--oa-color-palette-charcoal)}
.ws-steps .nm{font:var(--oa-font-weight-semibold) 17px/1.35 var(--oa-font-family-reading);color:var(--oa-color-text-primary);padding-top:2px}
.ws-steps .ahead .nm{color:var(--oa-color-text-secondary)}
.ws-steps .sw{${type_css('label')};color:var(--oa-color-text-secondary);display:block;margin-top:2px}
.ws-steps .nt{font:var(--oa-font-weight-regular) 15px/1.45 var(--oa-font-family-reading);color:var(--oa-color-text-secondary);display:block;margin-top:2px}
.ws-box{margin-top:4px;padding:16px 0 0;border-top:1px solid var(--oa-color-border-hairline-on-charcoal);${type_css('body-small')}}
.ws-box b{display:block;font-weight:var(--oa-font-weight-bold)}
.ws-box .ws-ask-lab{margin:16px 0 8px !important}
.ws-ask{display:inline-flex;flex-wrap:wrap;align-items:center;column-gap:.28em;width:fit-content;min-height:48px;padding:12px 16px;background:var(--oa-color-action-ask-fill-on-charcoal);color:var(--oa-color-action-ask-label-on-charcoal) !important;${type_css('ask')};text-decoration:none;max-width:100%}
.ws-ask>span{white-space:nowrap}
/* the ask breaks into its two phrases, as wide as the longer, wherever its panel has less room than its words (304 px).
   The query container is a wrapper around the ask alone: a container also sets what cqi means inside it, so a panel made a
   container would size its fluid type by the panel (found 21:15: the comment panel's h4 at 21.6 px for the page's 24) */
.ws-ask-w{container:ask/inline-size}
@container ask (max-width: 19rem){.ws-ask{width:min-content}}
.ws-nb{white-space:nowrap}
.ws-ask svg{width:16px;height:16px;margin-left:6px;vertical-align:-2px}
.ws-ask:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring-on-charcoal) !important}
.ws-addr{${type_css('caption')};color:var(--oa-color-text-secondary);overflow-wrap:anywhere;margin-top:12px !important}
.ws-doc{padding:24px}
${at(BP.tablet, '.ws-doc{padding:32px}')}
.ws-doc .lab{${type_css('label')};color:var(--oa-color-text-secondary);margin-bottom:8px !important}
.ws-doc .parts{${type_css('body-small')};color:var(--oa-color-text-primary)}
.ws-doc .dot{margin-inline:8px}
.ws-sum{margin:32px 0 48px}
.ws-sum blockquote{border-left:2px solid var(--oa-color-border-strong);padding-left:24px}
.ws-sum blockquote p{${type_css('quote')};color:var(--oa-color-text-primary)}
.ws-sum .cite{${type_css('caption')};color:var(--oa-color-text-secondary);margin-top:16px !important}
${at(BP.tablet, '.ws-cpanel{padding:32px}')}
.ws-hinge{display:flex;align-items:center;gap:12px;margin:80px 0 48px;color:var(--oa-color-identity-hinge-divider)}
.ws-hinge::before,.ws-hinge::after{content:"";flex:1;height:1px;background:currentColor}
.ws-hinge svg{display:block;flex:none}
.ws-hinge+.ws-h2{margin-top:0 !important}
.ws-ol{${type_css('body')};padding-left:1.6em;max-width:var(--oa-layout-measure-body-ideal)}
.ws-ol li+li{margin-top:16px}
.ws-ol li::marker{font-weight:var(--oa-font-weight-bold);font-variant-numeric:tabular-nums}
.ws-cpanel{padding:24px;margin:32px 0 48px}
.ws-cpanel .lab{margin-bottom:8px !important}
.ws-cpanel .line{${type_css('h4')};color:var(--oa-color-text-primary);margin-bottom:24px !important}
.ws-cpanel>*{max-width:var(--oa-layout-measure-body-ideal)}
.ws-glance{border-collapse:collapse;${type_css('body-small')};font-variant-numeric:tabular-nums;max-width:var(--oa-layout-measure-body-ideal)}
.ws-glance th,.ws-glance td{text-align:left;vertical-align:top;padding:8px 16px 8px 0;border-top:1px solid var(--oa-color-border-hairline)}
.ws-glance th{font-weight:var(--oa-font-weight-semibold)}
.ws-links{list-style:none;padding:0;margin-top:16px !important}
.ws-links li a{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);${type_css('body-small')};text-decoration-thickness:1px}
.ws-sec-end{margin-bottom:48px !important}
.ws-stepbox-w{margin-top:24px}
/* DD-6, 12.1: from 64em the step box spans the content width, its words held to the body's columns by padding equal to
   the columns before them (one column and gutter at 1024, two at 1440) */
.ws-g{--colw:calc((100cqi - 2 * var(--m) - (var(--c) - 1) * var(--g)) / var(--c))}
${at(BP.desktop, `.ws-art .ws-stepbox-w{grid-column:1/-1}.ws-art .ws-stepbox{max-width:none;padding:32px 32px 32px calc(var(--colw) + var(--g))}
 .ws-art .ws-stepbox .ws-p{max-width:min(var(--oa-layout-measure-body-ideal),calc(7 * var(--colw) + 6 * var(--g)))}`)}
${at(BP.wide, `.ws-art .ws-stepbox{padding-left:calc(2 * var(--colw) + 2 * var(--g))}
 .ws-art .ws-stepbox .ws-p{max-width:min(var(--oa-layout-measure-body-ideal),calc(5 * var(--colw) + 4 * var(--g)))}`)}
.ws-stepbox{padding:24px;color:var(--oa-color-text-primary)}
.ws-stepbox .ws-p{color:var(--oa-color-text-primary)}
${at(BP.tablet, '.ws-stepbox{padding:32px}')}
.ws-body:empty{display:none}
.ws-h2--tight{margin-bottom:24px !important}
.ws-mail{margin-top:24px !important}
.ws-glance-checked{margin-top:16px !important}
.ws-op2{margin-top:24px}
.ws-steps--words li{grid-template-columns:1fr;padding-bottom:12px}
.ws-steps--words li::before{display:none}
.ws-box p b{display:block}
`;
}

// ---------------------------------------------------------------------------------------------------------------- parts
const use = (id, px, cls = '', extra = '') => `<svg viewBox="0 0 ${px} ${px}" width="${px}" height="${px}" aria-hidden="true" focusable="false"${cls ? ` class="${cls}"` : ''}${extra}><use href="#oa-sym-${id}"/></svg>`;
// a Civic Line icon at 24 px: the fit at 1x, the master at 2x (the guide's pair)
const cl24 = (id, cls = '') => `<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"${cls ? ` class="${cls}"` : ''} data-icon="${id.toUpperCase()}"><use class="oa-at-1x" href="#oa-sym-${id}-24px"/><use class="oa-at-2x" href="#oa-sym-${id}"/></svg>`;
const cl48 = (id, cls = '') => `<svg viewBox="0 0 128 128" width="48" height="48" aria-hidden="true" focusable="false"${cls ? ` class="${cls}"` : ''} data-icon="${id.toUpperCase()}"><use href="#oa-sym-${id}"/></svg>`;
const out_mark = (w) => `<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false" data-icon="U-another-site"><use href="#oa-sym-u-another-site-16px"/></svg><span class="vh"> ${esc(w)}</span>`;
// an outside link (Rule 11.15): its last word held to the 16 px mark, "(another site)" for screen readers
// CR-13 and CD-S11 (chat 12): a page's text breaks only where a reader would. A docket (FDA-2025-N-2699-0001), a report
// code (G22-CG-ISD) and a section citation (201(ff)(3)(B)) stay whole; a one-letter prefix stays with its word (N-acetyl,
// L-cysteine); a time keeps its "p.m." (a no-break space); a web address breaks only after a slash. Words inside drawings
// (SVG), styles, scripts and titles are left as they are, and so is every attribute.
const HOLD_RE = /((?:https?:\/\/)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:gov|org|com|net|edu)(?:\/[^\s<]*[^\s<.,;:)])?)|(\b[A-Z]{2,}-\d{4}-[A-Z]-\d{4}(?:-\d{4})?\b)|(\b[A-Z0-9]{2,}(?:-[A-Z0-9]{2,}){2,}\b)|(\b[A-Z]-[a-z]{2,}\b)|(\b\d+(?:\([0-9A-Za-z]{1,3}\)){2,})|(\b\d{1,2}(?::\d{2})?) ([ap]\.m\.)/g;
const nw = (t) => `<span class="ws-nw">${t}</span>`;
function hold_text(t) {
  return t.replace(HOLD_RE, (m, url, dk, code, pre, cite, hh, ap) => {
    if (url) {
      // each run of the address up to and with its slash stays whole; a break may follow a slash that ends a run
      const runs = url.match(/[^/]*\/+|[^/]+$/g) || [url];
      return runs.map((r, i) => nw(r) + (i < runs.length - 1 ? '<wbr>' : '')).join('');
    }
    if (hh) return `${hh}&nbsp;${ap}`;
    return nw(m);
  });
}
export function hold(html_) {
  // the text between tags, outside <svg>, <style>, <script>, <title> and <textarea>
  let svg = 0, raw = null;
  return html_.split(/(<[^>]+>)/).map((part) => {
    if (part.startsWith('<')) {
      const t = (part.match(/^<\/?([a-zA-Z][\w:-]*)/) || [])[1];
      const tag = t ? t.toLowerCase() : '';
      const close = part.startsWith('</');
      if (raw) { if (close && tag === raw) raw = null; return part; }
      if (tag === 'svg' && !part.endsWith('/>')) svg += close ? -1 : 1;
      else if (!close && ['style', 'script', 'title', 'textarea'].includes(tag)) raw = tag;
      return part;
    }
    return raw || svg > 0 || !part.trim() ? part : hold_text(part);
  }).join('');
}

// CD-M1 and CR-1 (chat 12): `wrap` holds the words in one span, for a link drawn as a flex box (the Act page's source links),
// where the words before the held last word would be an anonymous flex item and lose their trailing space
function out_link(words_, href, cls = '', another = '(another site)', wrap = false) {
  const ws = String(words_).split(' ');
  const last = ws.pop();
  const inner = `${esc(ws.join(' '))}${ws.length ? ' ' : ''}<span class="ws-out">${esc(last)}${out_mark(another)}</span>`;
  return `<a href="${esc(href)}"${cls ? ` class="${cls}"` : ''}>${wrap ? `<span>${inner}</span>` : inner}</a>`;
}

function kicker(k_, symbol) {
  const k = kick(k_);
  return `<p class="ws-kick"><span class="a">${esc(k[0])}</span>${k[1] ? `<span class="d" aria-hidden="true">·</span>${symbol ? cl24(symbol) : ''}<span class="b">${esc(k[1])}</span>` : ''}</p>`;
}

function pillar_row(current) {
  const names = ['Explain', 'Track', 'Connect', 'Act'];
  return `<ol class="ws-prow">` + names.map((n, i) => `<li${n === current ? ' aria-current="true"' : ''}>${cl24(PILLAR_SYMS[i], 'pi')}<span class="w">${n}</span>`
    + (i < 3 ? use('u-arrow-16px', 16, 'ar') : '') + `</li>`).join('') + `</ol>`;
}

// chat 11c: exported for the atlas pages (renderers/atlas-page.mjs), which draw the website's own footer by import
export function footer(W) {
  const f = W.footer;
  const groups = f.groups.map(([h, links], i) => `<div class="grp"><h2 id="{pid}-fg${i}">${esc(h)}</h2><ul aria-labelledby="{pid}-fg${i}">`
    + links.map(([w, href]) => `<li><a href="${esc(href)}">${esc(w)}</a></li>`).join('') + `</ul></div>`).join('');
  // DD-4, 10.1: the lists on the page's own ground under a 2 px rule, then the closing strip, the footer's one dark panel
  return `<footer class="ws-foot" data-oa-section="Footer"><div class="ws-g"><div class="ws-foot-lists">`
    + `<nav aria-label="${esc(f.nav_label)}"><div class="ws-g">${groups}</div></nav></div></div>`
    + `<div class="ws-strip oa-surface-charcoal ws-panel"><div class="ws-g"><div class="row"><p class="sig">${mark(LOCK24, { width: 24, height: 24, red: 'signature' })}<span>${esc(f.tagline)}</span></p>`
    + `<p class="addr"><span>${esc(f.address)}</span><span class="ws-illus">${esc(f.illustrative)}</span></p></div></div></div>`
    + `</footer>`;
}

// the article's last paragraph with its outside link and B after its last word (Rule 04.6)
function paragraph(b) {
  let t = esc(b.p);
  if (b.link) {
    const a = b.link_kind === 'another-site' ? out_link(b.link[0], b.link[1], '', b.hidden || '(another site)') : `<a href="${esc(b.link[1])}">${esc(b.link[0])}</a>`;
    if (t.includes('{link}')) t = t.replace('{link}', a);
    else {
      const lw = esc(b.link[0]);
      const i = t.indexOf(lw);
      if (i < 0) throw new Error(`the link's words "${b.link[0]}" are not in its paragraph`);
      t = t.slice(0, i) + a + t.slice(i + lw.length);
    }
  }
  if (b.end_mark) {
    const m = t.match(/(\S+)$/);
    t = t.slice(0, m.index) + `<span class="ws-end">${m[1]}${mark(AMP14FIT, { cls: 'f14', width: 13, height: 13 })}${mark(AMP16, { cls: 'm16', width: 14, height: 16 })}</span>`;
  }
  return `<p class="ws-p">${t}</p>`;
}

// a figure for one frame: the chart kit's figure with its ids suffixed for the frame, and only the drawing its column shows
// (R4: the kit's lean switch shows the phone drawing in a figure under 480 px); col_w null keeps both (the export)
function figure(fig, pid, col_w) {
  let h = fig.html.replace(/id="oac-[a-z0-9-]+/g, (m) => m + '-' + pid)
    .replace(/(aria-(?:labelledby|describedby|controls)=")([^"]+)"/g, (m, a, v) => a + v.split(' ').map((x) => (x.startsWith('oac-') ? x + '-' + pid : x)).join(' ') + '"')
    .replace(/href="#(oac-[a-z0-9-]+)"/g, `href="#$1-${pid}"`);
  if (col_w != null) {
    const drop = col_w < 480 ? 'oac-desk' : 'oac-phone';
    h = h.replace(new RegExp(`<svg class="oac-svg ${drop}"[\\s\\S]*?</svg>(?=<svg class="oac-svg|</div>)`), '');
  }
  return `<div class="ws-fig">${h}</div>`;
}

// ---------------------------------------------------------------------------------------------------------------- pages
// Rule 11.5's card row: chapter 11's drawing with the first circle on the text edge and each next 60 px on, 57 on the
// 309 px card at 1440; screen readers get the steps in words (Rule 11.2's hidden list)
function card_tracker(t, marks, w) {
  if ((t.pending || []).length) return '';
  const svg = marks.rows[`${t.kind}:${w || 'page'}`];
  const say = t.steps.map((x) => `<li>Step ${x.n}, ${esc(x.name)}: ${esc(STEP_SAY(marks.words, ch11_state(x)))}.</li>`).join('');
  return `<div class="ws-trk">${svg}<ol class="vh">${say}</ol></div>`;
}

function home_main(A, figs, pid, cols, marks, w) {
  const secs = A.pillars.map((p, i) => {
    // status words: runs of [text, bold] (DD-3), Rule 11.1's status words and Rule 11.4's "You can take part now." in bold
    const st = p.status ? `<p class="st">${p.status.map(([t, bold]) => (bold ? `<b>${esc(t)}</b>` : esc(t))).join(' ')}</p>` : '';
    return `<section class="ws-sec" data-oa-section="${esc(p.word)}" aria-labelledby="${pid}-p${i}">`
      + `<div class="ws-cell oa-surface-charcoal ws-panel"><h2 id="${pid}-p${i}">${cl48(p.icon)}<span>${esc(p.word)}</span></h2>`
      + (i < 3 ? use('u-arrow-24px', 24, 'ar') : '') + `</div>`
      + `<div class="ws-card">${kicker(p.kicker, p.symbol)}<h3><a href="${esc(p.href)}">${esc(p.headline)}</a></h3>`
      + `<p class="dek">${esc(p.dek)}</p>` + (p.tracker ? card_tracker(p.tracker, marks, w) : '') + st
      + (p.dateline ? `<p class="dt">${esc(p.dateline)}</p>` : '')
      + (p.source ? `<p class="src">${esc(p.source)}</p>` : '')
      + (p.link ? `<a class="go" href="${esc(p.link[1])}">${esc(p.link[0])}</a>` : '')
      + `</div></section>`;
  }).join('');
  const at_ = A.atlas;
  // DD-4, 10.2: the atlas's title bar heads the section as its one dark panel; the questions sit on Newsprint, each arrow
  // held to its question's last word
  const held = (q) => { const t = esc(q); const m = t.match(/(\S+)$/); return t.slice(0, m.index) + `<span class="ws-nb">${m[1]}${use('u-arrow-16px', 16)}</span>`; };
  const qs = at_.questions.map(([q, href]) => `<li><a href="${esc(href)}">${held(q)}</a></li>`).join('');
  const atlas = `<section class="ws-atlas" data-oa-section="Atlas" aria-labelledby="${pid}-atlas"><div class="ws-abar oa-surface-charcoal ws-panel"><p class="lab">${esc(at_.label)}</p>`
    + `<h2 id="${pid}-atlas">${esc(at_.heading)}</h2></div><div class="ws-g"><p class="intro">${esc(at_.intro)}</p></div>`
    + `<div class="pair"><div class="ws-qs"><p class="lab">${esc(at_.panel_label)}</p><ul>${qs}</ul>`
    + `<a class="open" href="${esc(at_.open[1])}">${esc(at_.open[0])}</a></div>${figure(figs[at_.chart], pid, cols ? cols.atlas : null)}</div></section>`;
  return `<div class="ws-g ws-home">${secs}<div class="ws-atlas-w" style="grid-column:1/-1">${atlas.replace('class="pair"', 'class="pair"')}</div></div>`;
}

function article_main(A, figs, pid, cols) {
  const by = `<p class="ws-by"><span class="nm">${esc(A.byline[0])}</span><time datetime="${esc(A.byline[2])}">${esc(A.byline[1])}</time></p>`;
  const count = `<div class="ws-count oa-surface-charcoal ws-panel"><p class="fig">${esc(A.count.figure)}</p><p class="l1">${esc(A.count.line1)}</p>`
    + `<p class="l2">${esc(A.count.line2)}</p><p class="src">${esc(A.count.source)}</p></div>`;
  const head = `<div class="ws-g ws-head"><div class="ws-prow-w">${pillar_row(A.current)}</div><div class="ws-kick-w">${kicker(A.kicker, A.symbol)}</div>`
    + `<div class="ws-h1-w" style="margin-top:24px"><h1 class="ws-h1">${esc(A.headline)}</h1></div>`
    + `<div class="ws-lead" style="margin-top:32px"><p class="ws-intro">${esc(A.intro)}</p></div>${count}`
    + `<div class="ws-lead ws-lead2" style="margin-top:32px">${by}</div></div>`;
  // DD-4, 10.3: the Count section's fact box, its one dark panel, after its first paragraph (beside it from 64em)
  const cf = A.count_fact;
  // DD-5, 11.1: the box keeps the figure and its two lines; its source line stands 8 px under it, on Newsprint
  const fact = cf ? `<div class="ws-fact-w"><div class="ws-fact oa-surface-charcoal ws-panel"><p class="fig">${esc(cf.figure)}</p><p class="l1">${esc(cf.line1)}</p><p class="l2">${esc(cf.line2)}</p></div><p class="ws-fact-src">${esc(cf.source)}</p></div>` : '';
  const secs = A.sections.map((s, i) => `<section class="ws-g${s.key === 'Count' && fact ? ' ws-has-fact' : ''}" data-oa-section="${esc(s.key)}" aria-labelledby="${pid}-s${i}">`
    // the section's heading opens the body block of its first paragraphs, so the text sits directly under its heading
    // whatever stands beside it (Rule 07.4; found 21:14: the fact box's height had pushed the paragraph 160 px down)
    + s.blocks.reduce((acc, b) => { if (b.chart) acc.push({ fig: b.chart }); else if (acc.length && acc[acc.length - 1].ps) acc[acc.length - 1].ps.push(b); else acc.push({ ps: [b] }); return acc; }, [])
      // DD-5, 11.2: the closing step (the paragraph that ends on B) stands in a step box, the section's one dark panel
      .map((g, j) => (g.fig ? (j === 0 ? `<div class="ws-body"><h2 class="ws-h2" id="${pid}-s${i}">${esc(s.heading)}</h2></div>` : '') + figure(figs[g.fig], pid, cols ? cols.figure : null)
        : `<div class="ws-body">${j === 0 ? `<h2 class="ws-h2" id="${pid}-s${i}">${esc(s.heading)}</h2>` : ''}${g.ps.filter((b) => !b.end_mark).map(paragraph).join('')}</div>`
          + g.ps.filter((b) => b.end_mark).map((b) => `<div class="ws-body ws-stepbox-w"><div class="ws-stepbox oa-surface-charcoal ws-panel">${paragraph(b)}</div></div>`).join(''))
        + (j === 0 && s.key === 'Count' ? fact : '')).join('')
    + (i === A.sections.length - 1 ? `<div class="ws-body"><p class="ws-src">${esc(A.def_source)}</p></div>` : '')
    + `</section>`).join('');
  return `<article class="ws-art">${head}${secs}</article>`;
}

function ask(A) {
  return `<div class="ws-ask-w">${ask_link(A)}</div>`;
}
function ask_link(A) {
  const a = A.ask;
  // DD-5, 11.4: as wide as its words: the words before the last in one unbroken phrase, the last held to its mark in the
  // other, so on a phone the ask breaks between them and stays as wide as its longer line; a docket number stays whole
  const ws = String(a.words).split(' ');
  const last = ws.pop();
  return `<a href="${esc(a.href)}" class="ws-ask" data-red="working" data-red-job="take part now">`
    + (ws.length ? `<span>${esc(ws.join(' '))}</span>` : '') + `<span class="ws-out">${esc(last)}${out_mark(a.hidden || '(another site)')}</span></a>`;
}
const runs = (rs) => rs.map(([t, bold]) => (bold ? `<b>${esc(t)}</b>` : esc(t))).join(' ');

function act_main(A, figs, pid, cols, marks) {
  const S = A.status;
  const sw = S.state_words || { done: 'Done', now: 'Now', ahead: 'Not yet' };
  // Rule 11.6's upright steps; while a step is pending (Request R3) the steps print as words with no circles, and the
  // pending step is left out, since no step is drawn from a guess (DD-3)
  const pending = (S.pending || []).length > 0;
  const shown = S.steps.filter((x) => x.state !== 'pending');
  // Rule 11.6's upright steps, each mark chapter 11's own (sample at 28 px); the line 2 px into a step the record has
  // reached and 1 px after the current one
  const steps = shown.map((x, i) => `<li class="${x.state}${shown[i + 1] && shown[i + 1].state !== 'ahead' ? ' on' : ''}">${pending ? '' : `<span class="mkw">${marks.steps[x.n]}</span>`}`
    + `<span><span class="nm"><span class="vh">Step ${x.n}: </span>${esc(x.name)}</span><span class="sw">${esc(sw[x.state] || '')}</span>${x.note ? `<span class="nt">${esc(x.note)}</span>` : ''}</span></li>`).join('');
  const status = `<div class="ws-status oa-surface-charcoal ws-panel"><p class="lab">${esc(S.label)}</p><ol class="ws-steps${pending ? ' ws-steps--words' : ''}" start="${shown[0].n}">${steps}</ol>`
    + `<div class="ws-box"><p>${runs(S.box)}</p><p class="lab ws-ask-lab">${esc(A.comment.panel_label)}</p>${ask(A)}<p class="ws-addr">${esc(A.ask.address)}</p></div></div>`;
  const by = `<p class="ws-by"><span class="nm">${esc(A.byline[0])}</span><time datetime="${esc(A.byline[2])}">${esc(A.byline[1])}</time></p>`;
  const head = `<div class="ws-g ws-head"><div class="ws-op ws-open-col">${pillar_row(A.current)}${kicker(A.kicker)}<h1 class="ws-h1">${esc(A.headline)}</h1>`
    + `<p class="ws-intro">${esc(A.intro)}</p></div>${status}<div class="ws-op ws-open-col ws-op2"><p class="ws-checked">${esc(A.checked)}</p>${by}</div></div>`;
  const P = A.proposal;
  const sides = P.sides ? `<div class="ws-body"><h3 class="ws-h3">${esc(P.sides.heading)}</h3>${P.sides.paragraphs.map((x) => `<p class="ws-p">${esc(x)}</p>`).join('')}</div>` : '';
  // DD-4, 10.4: a document strip, the section's one dark panel, then the agency's summary on Newsprint with a rule at its left
  const doc = `<div class="ws-doc oa-surface-charcoal ws-panel"><p class="lab">${esc(P.doc_label)}</p><p class="parts">${P.doc_parts.map((x) => `<span class="ws-nb">${esc(x)}</span>`).join('<span class="dot" aria-hidden="true"> · </span>')}</p></div>`;
  const prop = `<section class="ws-g" data-oa-section="Proposal" aria-labelledby="${pid}-prop"><div class="ws-body"><h2 class="ws-h2 ws-h2--tight" id="${pid}-prop">${esc(P.heading)}</h2></div>`
    + doc + `<div class="ws-sum"><blockquote cite="${esc(P.cite_href)}"><p>“${esc(P.quote)}”</p></blockquote><p class="cite">${esc(P.cite)}</p></div>`
    + sides + `<div class="ws-body"><h3 class="ws-h3">${esc(P.decides_heading)}</h3><p class="ws-p">${esc(P.decides)}</p></div>`
    + figure(figs[P.chart], pid, cols ? cols.figure : null) + `</section>`;
  const C = A.comment;
  const glance = `<table class="ws-glance"><tbody>${C.glance.map(([k, v]) => `<tr><th scope="row">${esc(k)}</th><td>${esc(v)}</td></tr>`).join('')}</tbody></table>`;
  const comm = `<section class="ws-g" data-oa-section="Comment" aria-labelledby="${pid}-comment">`
    + `<div class="ws-body"><div class="ws-hinge" aria-hidden="true">${mark(AMP24, { width: 21, height: 24 })}</div>`
    + `<h2 class="ws-h2 ws-h2--tight" id="${pid}-comment">${esc(C.heading)}</h2>`
    + `<ol class="ws-ol">${C.steps.map((x) => `<li>${esc(x)}</li>`).join('')}</ol></div>`
    // DD-4, 10.5: the comment panel right after the steps, so it stands in the section's opening screen
    + `<div class="ws-cpanel oa-surface-charcoal ws-panel"><p class="lab">${esc(C.panel_label)}</p><p class="line">${esc(C.deadline)}</p>${ask(A)}<p class="ws-addr">${esc(A.ask.address)}</p></div>`
    + `<div class="ws-body"><p class="ws-p ws-sec-end">${esc(C.mail)}</p><h3 class="ws-h3">${esc(C.others_heading)}</h3><p class="ws-p ws-sec-end">${esc(C.others)}</p>`
    + `<h3 class="ws-h3">${esc(C.glance_heading)}</h3>${glance}<p class="ws-checked ws-glance-checked">${esc(C.checked)}</p>`
    + `<ul class="ws-links">${C.links.map(([w, h]) => `<li>${out_link(w, h, '', A.ask.hidden || '(another site)', true)}</li>`).join('')}</ul></div></section>`;
  return `<article class="ws-act">${head}${prop}${comm}</article>`;
}

// A frame shows one width, so it carries only the masthead parts that width shows (bytes; the working page keeps them all):
// the element that opens at the first match of `open`, removed whole with every element of its tag nested inside it
function drop(html, open, tag) {
  const i = html.search(open);
  if (i < 0) return html;
  const re = new RegExp(`<${tag}\\b|</${tag}>`, 'g');
  re.lastIndex = i + 1;
  let depth = 1, m;
  while ((m = re.exec(html))) { depth += m[0][1] === '/' ? -1 : 1; if (!depth) return html.slice(0, i) + html.slice(m.index + m[0].length); }
  return html;
}
// chat 11c: exported for the atlas pages, whose frames carry the masthead as the website's frames do
export function frame_masthead(head, w, open) {
  const em = w / 16;
  if (em >= BP.tablet) { head = drop(head, /<svg class="oa-masthead-wm oa-masthead-wm--24"/, 'svg'); head = drop(head, /<svg class="oa-masthead-wm oa-masthead-wm--16"/, 'svg'); }
  else { head = drop(head, /<svg [^>]*class="ws-l3"/, 'svg'); head = drop(head, em >= BP.phone ? /<svg class="oa-masthead-wm oa-masthead-wm--16"/ : /<svg class="oa-masthead-wm oa-masthead-wm--24"/, 'svg'); }
  if (em >= NAV_BP) head = drop(head, /<button\s+type="button"\s+class="oa-masthead-menu"/, 'button');
  else head = drop(head, /<fieldset class="oa-theme oa-site-switch-bar"/, 'fieldset');
  if (!open) { head = drop(head, /<dialog\b/, 'dialog'); head = head.replace(/\saria-controls="[^"]*-menu"/, ''); }
  return head;
}

// chat 11c: the site's head for a page, the masthead from site-parts.mjs with L3 in its home link, the site's words, the
// home page's h1 and current link, the menu open for a frame that shows it, and only what a frame's width shows;
// exported for the atlas pages (renderers/atlas-page.mjs), which draw the same head by import. parts: [{label, href,
// current}]; sw: the switches' { theme, target, group }
export function site_head({ pid, parts, site, sw, theme_for = null, home_page = false, open = false, width = null }) {
  let head = masthead({ pid, parts: parts.map((p) => ({ ...p, href: theme_for ? `#${pid}-main` : p.href })), home: { href: theme_for ? `#${pid}-main` : '/', name: site.home_name }, sw });
  // L3 from 48em, in the home link with chapter 18's two wordmark masters (spec 2.1)
  head = head.replace(/(<a class="oa-masthead-home"[^>]*>)/, `$1${mark(L3, { cls: 'ws-l3', width: 282, height: 48, label: site.home_name, red: 'signature' })}`);
  head = head.replace(/aria-label="Parts of the site"/, `aria-label="${esc(site.nav_label)}"`)
    .replace(/>Menu<\/span><\/button>/, `>${esc(site.menu.button)}</span></button>`)
    .replace(/(id="[^"]*-menu-name">)Menu</, `$1${esc(site.menu.title)}<`)
    .replace(/<span>Close the menu<\/span>/, `<span>${esc(site.menu.close)}</span>`)
    .replace(/aria-label="Parts of the site, in the menu"/, `aria-label="${esc(site.menu.nav_label)}"`);
  if (home_page) head = head.replace(/(<a class="oa-masthead-home"[^>]*)>/, '$1 aria-current="page">').replace(/(<a class="oa-masthead-home"[\s\S]*?<\/a>)/, '<h1 class="ws-h1home">$1</h1>');
  if (open) head = head.replace(/<dialog\b/, '<dialog open');
  if (width) head = frame_masthead(head, width, open);
  if (theme_for) head = head.replace(/\saria-controls="([^"]+)"/, ' aria-controls="$1"');
  return head;
}

// ---------------------------------------------------------------------------------------------------------------- render
function columns(spec, w) {
  // the figure's column at a width, for R4 and R8 (spec 5.4, 6.2, 7.2): under 64em the content width; from 64em the spec's
  // columns; each chart is drawn at exactly this width for a frame, so no frame scales a drawing past its true size, capped
  // at the chart's artboard (chart_figure), the widest its figure shows
  const W = { 1440: { figure: 644, atlas: 866.7 }, 1024: { figure: 621.3, atlas: 540.7 } };
  if (W[w]) return W[w];
  const m = w < 390 ? 16 : 20;
  return { figure: w - 2 * m, atlas: w - 2 * m };
}

// PR-M2, the web half (chat 12): a page's words may come from its own content file. "words_file" names a JSON file (from
// the project folder, or absolute) holding the entry the generator prints for a page: the page's own words, and "site" for
// the masthead and footer. Without "site" the page takes the studio site's words from the generator; without "words_file"
// every word comes from the generator, as for the studio's own pages (DD-3).
function own_words(spec) {
  if (!spec.words_file) return null;
  const f = path.isAbsolute(spec.words_file) ? spec.words_file : path.join(ROOT, spec.words_file);
  if (!fs.existsSync(f)) throw new Error(`${spec.id}: its words file ${spec.words_file} is not there (PR-M2)`);
  const e = JSON.parse(fs.readFileSync(f, 'utf8'));   // read through fs, so the file is one of the plate's inputs (C4)
  return { e, from: spec.words_file };
}

export async function render(spec) {
  const own = own_words(spec);
  const W = own && own.e.site ? { [spec.id]: own.e, __from: own.from }
    : own ? (() => { const G = words(); return { [spec.id]: { ...own.e, site: (G.A07 || G[Object.keys(G).find((k) => G[k] && G[k].site)]).site }, __from: own.from }; })()
    : words();
  const page = spec.page;
  const pw = page_words(W, spec.id, page);
  const site = pw.site;
  const charts = spec.charts || {};
  // the working page's figures: the kit's lean pair, a desk drawing and a phone drawing, switched by the figure's width
  const figs = {};
  for (const [cid, [desk, phone]] of Object.entries(charts)) figs[cid] = await chart_figure(cid, 'oac-' + cid, desk, phone);
  // R8: for each captured width, each chart drawn at the column it fills there (the frame and its capture use these)
  const figs_at = {};
  for (const wv of spec.widths || []) {
    figs_at[wv.w] = {};
    const c = columns(spec, wv.w);
    for (const cid of Object.keys(charts)) {
      const colw = +(page === 'home' ? c.atlas : c.figure).toFixed(1);
      figs_at[wv.w][cid] = await chart_figure(cid, 'oac-' + cid, colw, colw);
    }
  }
  // DD-6: chapter 11's marks for this page: the cards' rows at each width (309 px at 1440, else 324) and the upright steps
  const reqs = [], keys = [];
  for (const p of pw.pillars || []) {
    if (!p.tracker || (p.tracker.pending || []).length) continue;
    const states = p.tracker.steps.map(ch11_state);
    for (const w of [...(spec.widths || []).map((x) => x.w), 'page']) {
      reqs.push({ kind: 'row', states, W: w === 1440 ? 309 : 324, d: 24 });
      keys.push(['row', `${p.tracker.kind}:${w}`]);
    }
  }
  for (const x of ((pw.status || {}).steps || [])) {
    if (x.state === 'pending') continue;
    reqs.push({ kind: 'mark', state: ch11_state(x), d: 28, num: x.n });
    keys.push(['step', x.n]);
  }
  const marks = { rows: {}, steps: {}, css: '', words: {} };
  if (reqs.length) {
    const got = ch11(reqs);
    marks.css = got.css; marks.words = got.words;
    got.svgs.forEach((svg, i) => { const [k, id] = keys[i]; marks[k === 'row' ? 'rows' : 'steps'][id] = svg; });
  }
  // DR-316 (AL11-1): the current part's link carries aria-current="page" on that part's own front page and "true" on the
  // pages inside it. The kit draws no part's front page: its article sits inside Explain and its Act page inside Act, so
  // both take "true"; the home page marks its home link "page" (below)
  const parts = site.parts.map(([label, href]) => ({ label, href, current: pw.current && label === pw.current ? 'true' : false }));
  const body = ({ pid, theme, theme_for = null, part = 'page', width = null, vh = null, open = false, fig_w = null } = {}) => {
    const group = `oa-theme-${pid}`;
    const sw = { theme: theme_for ? theme : 'device', target: theme_for, group };
    const head = site_head({ pid, parts, site, sw, theme_for, home_page: page === 'home', open, width });
    const fw = width || fig_w;
    const cols = fw ? columns(spec, fw) : null;
    const F = fw && figs_at[fw] ? figs_at[fw] : figs;
    let main = part !== 'page' ? '' : page === 'home' ? home_main(pw, F, pid, cols, marks, fw) : page === 'article' ? article_main(pw, F, pid, cols) : act_main(pw, F, pid, cols, marks);
    // W3 (2.1.1): on a working page each chart table's scroll frame is a Tab stop, a named group (the guide's pattern,
    // D4-92); a guide frame is a picture and takes none
    if (!width) main = main.replace(/<div class="oac-tw" role="group"/g, '<div class="oac-tw" role="group" tabindex="0"');
    main = hold(main);   // CR-13, CD-S11
    const parts_ = {
      masthead: head,
      main: `<main id="${pid}-main" class="ws-main" tabindex="-1">${main}</main>`,
      footer: footer(site).replace(/\{pid\}/g, pid),
    };
    const inner = part === 'masthead' ? parts_.masthead : part === 'footer' ? parts_.footer
      : `<a class="ws-skip" href="#${pid}-main">${esc(site.skip)}</a>${parts_.masthead}${parts_.main}${parts_.footer}`;
    const style = vh ? ` style="--ws-vh:${vh}px"` : '';
    return `<div class="ws${open ? ' ws-open' : ''}" id="${pid}"${theme_for ? ` data-oa-theme="${theme}"` : ''}${style} data-oa-application="${esc(spec.id)}"><div class="ws-in">${inner}</div></div>`;
  };
  const kit_css = Object.values(figs)[0] ? Object.values(figs)[0].css : '';
  const syms = [...UTILITY_SPRITE, 'oa-sym-u-arrow-16px', 'oa-sym-u-arrow-24px', ...PILLAR_SYMS.flatMap((x) => [`oa-sym-${x}`, `oa-sym-${x}-24px`]),
    ...(pw.symbol ? [`oa-sym-${pw.symbol}`, `oa-sym-${pw.symbol}-24px`] : []),
    ...((pw.pillars || []).filter((p) => p.symbol).flatMap((p) => [`oa-sym-${p.symbol}`, `oa-sym-${p.symbol}-24px`]))];
  return {
    id: spec.id, type, page, part: spec.part || 'page', title: pw.title, words_from: W.__from,
    // chapter 11's mark style (MARK_CSS), each selector held inside a website page, with the marks' colors on their holders
    css: site_css() + '\n' + masthead_css() + '\n' + switch_css() + '\n'
      + (marks.css ? marks.css.replace(/\.mk\b/g, '.ws .mk') + `.ws-trk,.ws-steps{${MARK_VARS}}` : ''),
    // the guide shell's 1x and 2x icon switch (DR-179), which the guide's page already carries and an export page needs
    export_css: res_switch_css(),
    kit_css, figs, sprite: sprite([...new Set(syms)]),
    body, widths: spec.widths, views: spec.views,
    scripts: { head: switch_head_js(), tail: [masthead_js(), switch_js(), close_on_widen_js(NAV_BP)].join('\n') },
    head_extra: '',
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}
