// Atlas page renderer (chat 11c; chapter 21's plan, sections 3 and 9.1): every page of our systems atlas, Who Do They
// Answer To?, drawn inside the website's shell. The skip link, the masthead with its parts, the menu and the theme switch
// come from site-parts.mjs, and the footer and the site's style from web-site.mjs, by import (never a copy of their
// markup), so the atlas and the website draw one masthead and one footer (AL-04, 3.2.6). The masthead marks "Who Do They
// Answer To?" as the current part: aria-current="page" on the atlas home and "true" on every page inside it (DR-316). Under
// it the atlas adds its title bar, a breadcrumb below the home and, from 64em, the locator (plan 3.1).
//
// Every value comes from the model through the figure step (tools/atlas_figures.py, which imports chapter 15's drawing
// code), and every word the page adds from chapter 21's generator (phase4_ch21_build.py --page-words all; contract C9),
// the site's own words from chapter 20's. The style is the website's wherever the rules match (DR-319): the page carries
// web-site's style and adds atlas-page's few rules of its own, which go into the guide once, in the head, as
// plates/atlas-page.css.
//
// Templates: home, reform, register, loop, loop-index, how-to-read; part and issue for the atlas's next pages, drawn by no
// content file this chapter (plan 9.1).
import fs from 'fs';
import path from 'path';
import { spawnSync } from 'child_process';
import { ROOT, CODE, component_css, esc, touch, type_css } from '../lib.mjs';
import { site_css, footer, frame_masthead, words as site_words } from './web-site.mjs';
import { sprite, sprite_icons, res_switch_css } from './web-page.mjs';
import { UTILITY_SPRITE, close_on_widen_js, masthead, masthead_css, masthead_js, switch_css, switch_head_js, switch_js } from './site-parts.mjs';

export const type = 'atlas-page';
export const GEN = 'work/build/scripts/phase-4/phase4_ch21_build.py';
const SITE_GEN = 'work/build/scripts/phase-4/phase4_ch20_build.py';
const FIGURES = 'work/build/app-kit/tools/atlas_figures.py';
const BP = { phone: 24.375, tablet: 48, desktop: 64, wide: 90 };   // chapter 07's breakpoints, in em, as the website's
const NAV_BP = 64;
const ATLAS_PART = 'Who Do They Answer To?';                       // DR-307: the part's name among the site's parts
const at = (em, body) => `@container ws (min-width: ${em}em){${body}}`;
const under = (em, body) => `@container ws (max-width: ${em - 0.001}em){${body}}`;

// ---------------------------------------------------------------------------------------------------------------- words
let AW = null;
export function atlas_words() {
  if (AW) { touch(AW.__from); return AW; }
  if (fs.existsSync(path.join(ROOT, GEN))) {
    const r = spawnSync('python3', ['-I', path.join(ROOT, GEN), '--page-words', 'all'], { encoding: 'utf8', cwd: ROOT });
    if (r.status !== 0 || !r.stdout.trim().startsWith('{')) throw new Error('atlas page words: ' + (r.stderr || r.stdout).trim().slice(0, 400));
    AW = JSON.parse(r.stdout);
    AW.__from = GEN;
  } else if (process.env.OA_ATLAS_WORDS) {
    AW = JSON.parse(fs.readFileSync(process.env.OA_ATLAS_WORDS, 'utf8'));
    AW.__from = process.env.OA_ATLAS_WORDS;
  } else {
    throw new Error(`no atlas page words: ${GEN} is not written yet; set OA_ATLAS_WORDS to a stand-in file (contract C9)`);
  }
  return AW;
}
// one key of the page's words; a key the generator does not print stops the build with its name (contract C9)
function need_words(o, keys, where) {
  for (const k of keys) if (o == null || o[k] == null) throw new Error(`the atlas page words for ${where} hold no "${k}" (contract C9)`);
  return o;
}
const fill = (t, vals) => String(t).replace(/\{(\w+)\}/g, (m, k) => (vals[k] != null ? vals[k] : m));
// a template's words escaped, its {keys} filled with markup (a typed chip in place of a bare ID, house rule H11)
const fill_html = (t, vals) => esc(t).replace(/\{(\w+)\}/g, (m, k) => (vals[k] != null ? vals[k] : m));

// ---------------------------------------------------------------------------------------------------------------- model
function figures(spec) {
  const f = path.join(process.env.TMPDIR || '/tmp', `oa-atlas-${process.pid}-${Date.now()}.json`);
  fs.writeFileSync(f, JSON.stringify(spec));
  const r = spawnSync('python3', ['-I', path.join(ROOT, FIGURES), f], { encoding: 'utf8', cwd: ROOT, maxBuffer: 64 * 1024 * 1024 });
  fs.unlinkSync(f);
  if (r.status !== 0) throw new Error('atlas figures: ' + (r.stderr || r.stdout).trim().slice(0, 600));
  const out = JSON.parse(r.stdout);
  for (const rel of out.inputs) touch(rel);   // contract C4: the model and chapter 15's code are the plate's inputs
  return out;
}

// ---------------------------------------------------------------------------------------------------------------- parts
// A typed chip (Rule 18.24, chapter 18's c-18-id-chip): the kind word and the ID, plain or as a link, with the marks the
// atlas test reads. The kind word is the one the model files the ID under, passed by the caller from the record it reads.
export function chip(kind, id, { href = null, evidence = null, cls = '' } = {}) {
  const a = ` data-atlas-kind="${esc(kind)}" data-atlas-id="${esc(id)}"${evidence ? ` data-evidence-href="${esc(evidence)}"` : ''}`;
  const inner = `${esc(kind)} <span class="oa-chip-id">${esc(id)}</span>`;
  return href ? `<a class="oa-chip oa-chip--link${cls ? ' ' + cls : ''}" href="${esc(href)}"${a}>${inner}</a>`
    : `<span class="oa-chip${cls ? ' ' + cls : ''}"${a}>${inner}</span>`;
}
// the paths and anchors of contract C9 (the data lead's R5): a connection's line on the sheet of the variable it moves
const low = (x) => String(x).toLowerCase();
const conn_href = (c) => `/atlas/register/${low(c.sheet)}#register-${low(c.id)}`;

// the title bar (plan 3.1): the atlas's name, its subtitle and snapshot from the model, then the five views as a named
// navigation, the current one marked as Rule 17.10 marks a current link; under 48em the views sit behind chapter 18's
// button-built disclosure, "Atlas views" (Rule 18.8), which opens them in place
function title_bar({ pid, A, M, current, open }) {
  need_words(A, ['views_label', 'views', 'snapshot'], 'the title bar');
  const chev = sprite_icons(fs.readFileSync(path.join(CODE, 'c-18-disclosure.html'), 'utf8').match(/<svg\s+class="oa-disclosure-chevron"[\s\S]*?<\/svg>/)[0]).replace(/\s*\n\s*/g, ' ');
  const links = A.views.map(([w, href]) => `<li><a class="wa-tb-link" href="${esc(href)}"${w === current ? ' aria-current="page"' : ''}>${esc(w)}</a></li>`).join('');
  return `<div class="wa-tb" data-oa-disclosure><div class="ws-g wa-tb-g">`
    + `<div class="wa-tb-name"><p class="wa-tb-atlas">${esc(M.title)}</p>`
    + `<p class="wa-tb-sub"><span>${esc(M.subtitle)}</span> <span class="wa-tb-snap" data-status-date="${esc(M.snapshot)}">${esc(fill(A.snapshot, { date: M.snapshot_words }))}</span></p></div>`
    + `<button type="button" class="oa-disclosure-summary oa-disclosure-button wa-tb-toggle" aria-expanded="${open ? 'true' : 'false'}" aria-controls="${pid}-views">`
    + `<span class="oa-disclosure-label">${esc(A.views_label)}</span>${chev}</button>`
    + `<nav class="wa-tb-nav" id="${pid}-views" aria-label="${esc(A.views_label)}"${open ? '' : ' hidden'}><ul class="wa-tb-list">${links}</ul></nav>`
    + `</div></div>`;
}

// the breadcrumb (AL-09) on every page below the home: the crumbs the generator gives, then the page's own chip
function breadcrumb({ A, crumbs, own }) {
  if (!crumbs) return '';
  const items = crumbs.map(([w, href]) => `<li><a href="${esc(href)}">${esc(w)}</a></li>`).join('');
  return `<nav class="wa-bc" aria-label="${esc(A.breadcrumb_label || 'Breadcrumb')}"><div class="ws-g"><ol class="wa-bc-list">${items}<li aria-current="page">${own}</li></ol></div></nav>`;
}

// the locator (Rule 12.7): the parts as boxes, 88 by 41 px, the page's parts filled in ink; a picture named in words
function locator({ A, parts, filled }) {
  const cols = 4, bw = 19, bh = 17, gx = 4, gy = 7;
  const boxes = parts.map((p, i) => {
    const x = 1 + (i % cols) * (bw + gx), y = 1 + Math.floor(i / cols) * (bh + gy);
    return `<rect x="${x}" y="${y}" width="${bw}" height="${bh}"${filled.includes(p.id) ? ' class="on"' : ''} data-atlas-part="${esc(p.id)}"/>`;
  }).join('');
  const names = parts.filter((p) => filled.includes(p.id)).map((p) => p.title).join(' and ');
  return `<svg class="wa-loc" viewBox="0 0 88 41" width="88" height="41" role="img" aria-label="${esc(fill(A.locator_alt || '{part}', { part: names }))}">${boxes}</svg>`;
}

// ---------------------------------------------------------------------------------------------------------------- views
function view_loop({ pid, P, F, theme }) {
  const v = F.view, lp = v.loop;
  need_words(P, ['steps', 'read_label', 'arithmetic', 'weakest', 'stepper_ready', 'chooser_legend', 'also_aim', 'records', 'sections'], 'the loop page');
  const S = P.sections;
  const step_chip = (s) => chip('Connection', s.id, { href: conn_href(s), evidence: conn_href(s) });
  const grade_line = v.steps.map((s) => `${step_chip(s)} ${esc(s.grade.word)}`).join(' ');
  const head = `<header class="wa-head" data-oa-part="head"><p class="wa-kind">${chip('Loop', lp.id)} <span>${esc(lp.kind)}</span></p>`
    + `<h1 class="wa-h1">“${esc(lp.title)}”</h1>`
    + `<p class="wa-grades">${grade_line}</p>`
    + `<p class="wa-closure">${esc(lp.closure)}</p></header>`;
  const read = `<section class="wa-sec" data-oa-section="Read" data-oa-part="read"><h2 class="ws-h2">${esc(S.read)}</h2>`
    + `<p class="ws-p wa-read" data-atlas-reads="${esc(v.reads)}">${esc(v.read_aloud)}</p>`
    + `<p class="ws-p wa-arith" data-count="${v.minus}" data-count-of="loop:${esc(lp.id)}:minus">${esc(fill(P.arithmetic, { n: v.minus }))}</p></section>`;
  const reds = new Set(v.figure.red);
  const marks = v.figure.svg;
  if (P.steps.length !== v.steps.length) throw new Error(`the loop page's words hold ${P.steps.length} stepper lines for ${v.steps.length} steps (contract C9)`);
  const stepper_steps = P.steps.map((st, i) => `<li class="oa-stepper-step" data-oa-hold="${esc(st.hold)}" data-atlas-kind="Connection" data-atlas-id="${esc(v.steps[i].id)}"`
    + ` data-sign="${esc(v.steps[i].sign)}" data-type="${esc(v.steps[i].type)}" data-delay="${esc(v.steps[i].delay.key)}" data-grade="${esc(v.steps[i].grade.key)}"`
    + ` data-evidence-href="${esc(conn_href(v.steps[i]))}"${v.steps[i].id === v.weakest ? ' data-weakest="true"' : ''}><span class="oa-stepper-line">${esc(st.line)}</span>&#32;<span class="oa-stepper-more">${esc(st.more || '')}</span></li>`).join('');
  const ctl = fs.readFileSync(path.join(CODE, 'c-18-loop-stepper.html'), 'utf8').match(/<div\s+class="oa-stepper-controls"[\s\S]*?<\/button>\s*<\/div>/)[0];
  const controls = sprite_icons(ctl).replace(/\s*\n\s*/g, ' ').replace('aria-label="Steps of the loop"', `aria-label="${esc(fill(P.stepper_group || 'Steps of Loop {id}', { id: lp.id }))}"`)
    .replace(/aria-describedby="oa-stepper-why"/g, `aria-describedby="${pid}-why"`);
  const why = `<p class="oa-stepper-why" id="${pid}-why">${esc(P.stepper_why || '')}</p>`;
  const drawing = `<section class="wa-sec" data-oa-section="Drawing" data-oa-part="drawing"><div class="oa-stepper wa-stepper" data-oa-stepper data-oa-part="stepper">`
    + `<figure class="wa-fig">${marks}</figure>`
    + (v.weakest ? `<p class="ws-p wa-weak">${step_chip(v.steps.find((s) => s.id === v.weakest))} ${esc(P.weakest)}</p>` : '')
    + `<p class="oa-stepper-status" role="status" data-oa-ready="${esc(P.stepper_ready)}">${esc(P.stepper_ready)}</p>`
    + controls + why
    + `<ol class="oa-stepper-steps" role="list">${stepper_steps}</ol></div></section>`;
  const choices = v.offered.map((r, k) => `<label class="oa-choice-item"><input class="oa-choice-input" type="radio" name="${pid}-reform" value="${esc(r.id)}"${r.id === v.chosen ? ' checked' : ''}>`
    + `<span class="oa-choice-face"><span class="oa-choice-label">${chip('Reform', r.id)} “${esc(r.title)}”</span></span></label>`).join('');
  const tags = Object.entries(v.tags).filter(([t, rs]) => rs.length && (v.steps.some((s) => s.id === t) || v.variables.some((x) => x.id === t)))
    .map(([t, rs]) => `<li class="wa-tag" data-atlas-tag-for="${esc(t)}">${rs.map((r) => chip('Reform', r)).join(' ')} ${esc(fill(P.also_aim, { target: t }))}</li>`).join('');
  const panels = v.offered.map((r) => reform_panel(r, P, F)).join('');
  const chooser = `<section class="wa-sec wa-chooser" data-oa-section="Reforms" data-oa-part="chooser"><fieldset class="oa-choice"><legend class="oa-choice-legend">${fill_html(P.chooser_legend, { id: chip('Loop', lp.id) })}</legend>`
    + `<div class="oa-choice-row oa-choice-row--list">${choices}</div></fieldset><ul class="wa-tags">${tags}</ul>${panels}</section>`;
  const words = `<section class="wa-sec" data-oa-section="Words"><h2 class="ws-h2">${esc(S.words)}</h2>`
    + ['summary', 'case', 'qualification', 'adaptation'].map((k) => `<p class="ws-p wa-stored" data-atlas-field="${k}">${esc(lp[k])}</p>`).join('') + `</section>`;
  const evidence = `<section class="wa-sec" data-oa-section="Evidence"><h2 class="ws-h2">${esc(S.evidence)}</h2><ul class="wa-ev">`
    + v.steps.map((s) => `<li>${step_chip(s)} ${esc(s.name)}</li>`).join('') + `</ul>`
    + `<p class="ws-p"><a href="/atlas/register?loop=${esc(lp.id)}" data-count="${lp.records.length}" data-count-of="loop:${esc(lp.id)}:records">${esc(fill(P.records, { n: lp.records.length }))}</a></p></section>`;
  return head + read + drawing + chooser + words + evidence;
}

// a reform's effects, one family a row (Rule 15.16; the data lead's R12): the family's name, the code whole with its
// qualifier and true minus signs, and the model's words for the code; never a total
const MINUS = '\u2212';
function effect_rows(r, P, F) {
  const words = F.effect_words || {};
  const say = (code) => {
    const parts_ = String(code).split(/\s+to\s+/);
    const w = (c) => words[(c.match(/^[+\-]?[SML0?]/) || [''])[0]] || '';
    return parts_.map(w).filter(Boolean).join(' to ');
  };
  return `<ul class="wa-ef">` + r.effects.map((e) => `<li data-effect-family="${esc(e.family)}" data-effect-code="${esc(e.code)}" data-atlas-reform="${esc(r.id)}">`
    + `<span class="wa-ef-f">${esc(e.name)}</span> <b class="wa-ef-c">${esc(String(e.code).replace(/-/g, MINUS))}</b>${say(e.code) ? `<span class="wa-ef-w">, ${esc(say(e.code))}</span>` : ''}</li>`).join('') + `</ul>`;
}
// a reform's routes, each with its own check date or "Not checked" (Rules 13.10, 15.24), never the reform's status date
function route_rows(r, P) {
  return `<ul class="wa-rt">` + r.routes.map((x) => `<li data-route="${esc(x.code)}" data-checked="${esc(x.checked || 'none')}" data-atlas-reform="${esc(r.id)}">`
    + `${chip('Route', x.code, { href: `/atlas/routes/${low(x.code)}` })} <span>${esc(x.name || '')}</span>, <span>${esc(x.who)}</span>, <span>${esc(x.feasibility)}</span>`
    + (x.note ? `. <span class="wa-stored" data-atlas-field="note">${esc(x.note)}</span>` : '')
    + `. <span class="wa-rt-d">${x.checked ? esc(fill(P.checked, { date: x.checked_words })) : esc(P.not_checked)}</span></li>`).join('') + `</ul>`;
}
function reform_panel(r, P, F) {
  need_words(P, ['effects_head', 'routes_head', 'not_checked', 'checked'], 'a reform panel');
  return `<div class="wa-panel" data-oa-panel="${esc(r.id)}"><p class="wa-pn-h"><a class="oa-chip oa-chip--link" href="/atlas/reforms/${low(r.id)}" data-atlas-kind="Reform" data-atlas-id="${esc(r.id)}">Reform <span class="oa-chip-id">${esc(r.id)}</span></a> “${esc(r.title)}”</p>`
    + `<p class="wa-pn-k">${esc(fill(P.effects_head, { date: F.model.snapshot_words }))}</p>${effect_rows(r, P, F)}`
    + `<p class="wa-pn-k">${esc(P.routes_head)}</p>${route_rows(r, P)}</div>`;
}

const VIEWS = { loop: view_loop };

// ---------------------------------------------------------------------------------------------------------------- style
// atlas-page's own rules, over the website's style (DR-319): the title bar, the breadcrumb, the locator and the views'
// blocks. Colors only by token; type only by token.
export function atlas_css(fig_css) {
  return `
.ws .wa-tb{border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}
.ws .wa-tb-g{align-items:center;min-height:56px;row-gap:0}
.ws .wa-tb-atlas{${type_css('label')};color:var(--oa-color-text-primary)}
.ws .wa-tb-sub{${type_css('body-small')};color:var(--oa-color-text-secondary)}
.ws .wa-tb-list{list-style:none;margin:0;padding:0}
.ws .wa-tb-link{display:flex;align-items:center;min-height:var(--oa-size-target-touch);${type_css('ui')};text-decoration:none;color:var(--oa-color-text-primary)}
.ws .wa-tb-link[aria-current]{font-weight:var(--oa-font-weight-bold);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:5px}
.ws .wa-tb-toggle{justify-self:end}
${under(BP.tablet, `.ws .wa-tb-g{grid-template-columns:minmax(0,1fr) auto}.ws .wa-tb-name{grid-column:1}.ws .wa-tb-sub{display:none}.ws .wa-tb-toggle{grid-column:2}.ws .wa-tb-nav{grid-column:1/-1}.ws .wa-tb-list li{border-top:1px solid var(--oa-color-border-hairline)}`)}
${at(BP.tablet, `.ws .wa-tb-toggle{display:none}.ws .wa-tb-nav,.ws .wa-tb-nav[hidden]{display:block}.ws .wa-tb-name{grid-column:1/7}.ws .wa-tb-nav{grid-column:7/-1;justify-self:end}.ws .wa-tb-list{display:flex;gap:0 24px}`)}
.ws .wa-bc-list{list-style:none;display:flex;flex-wrap:wrap;align-items:center;gap:0 8px;padding:12px 0 0;margin:0;${type_css('body-small')}}
.ws .wa-bc-list li+li::before{content:"/";margin-right:8px;color:var(--oa-color-text-secondary)}
.ws .wa-bc-list a{display:inline-flex;align-items:center;min-height:var(--oa-size-target-minimum)}
.ws .wa-loc{display:none}
${at(BP.desktop, `.ws .wa-loc{display:block;position:absolute;right:var(--m);margin-top:-41px}.ws .wa-loc rect{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:1px}.ws .wa-loc rect.on{fill:var(--oa-color-graphic-essential)}`)}
.ws .wa-h1{${type_css('title')};text-wrap:balance}
.ws .wa-kind{display:flex;flex-wrap:wrap;align-items:center;gap:8px;${type_css('label')};color:var(--oa-color-text-secondary)}
.ws .wa-grades,.ws .wa-closure{${type_css('intro')}}
.ws .wa-fig{margin:0}
.ws .wa-fig .sv{max-width:100%;height:auto}
.ws .wa-tags,.ws .wa-ev{list-style:none;padding:0;margin:16px 0 0}
.ws .wa-tag,.ws .wa-ev li{${type_css('data-label')};display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:8px}
.ws .wa-sec{display:block;margin-top:48px}
.ws .wa-chooser .wa-panel{display:none}
${[1, 2, 3, 4, 5].map((k) => `.ws .wa-chooser:has(.oa-choice-item:nth-child(${k}) .oa-choice-input:checked) .wa-panel:nth-of-type(${k})`).join(',')}{display:block}
@media print{.ws .wa-chooser .wa-panel{display:block}}
.ws .wa-ef,.ws .wa-rt{list-style:none;margin:0;padding:0;${type_css('body-small')}}
.ws .wa-ef li,.ws .wa-rt li{padding:8px 0;border-top:1px solid var(--oa-color-border-hairline)}
.ws .wa-ef-c{font-weight:var(--oa-font-weight-bold);font-variant-numeric:tabular-nums}
.ws .wa-pn-k{${type_css('label')};color:var(--oa-color-text-secondary);margin:24px 0 8px}
${fig_css}
`;
}

// ---------------------------------------------------------------------------------------------------------------- render
export async function render(spec) {
  const AWd = atlas_words();
  const pw = AWd[spec.id];
  if (!pw) throw new Error(`the atlas page words hold no entry for ${spec.id} (contract C9)`);
  need_words(pw, ['title', 'atlas', 'current_view', 'page'], spec.id);
  const SW = site_words();
  const site = (SW.A06 || Object.values(SW).find((x) => x && x.site) || {}).site;
  if (!site) throw new Error('chapter 20\'s words hold no site entry');
  const F = figures(spec);
  const M = F.model;
  const is_home = spec.view === 'home';
  const parts_ = site.parts.map(([label, href]) => ({ label, href, current: label === ATLAS_PART ? (is_home ? 'page' : 'true') : false }));
  const fn = VIEWS[spec.view];
  if (!fn) throw new Error(`the atlas renderer draws no ${spec.view} view yet (templates land with the design director's specs)`);
  const own = spec.record ? chip(spec.view === 'loop' ? 'Loop' : spec.view === 'reform' ? 'Reform' : spec.view === 'register' ? 'Domain' : '', spec.record) : '';
  const body = ({ pid, theme, theme_for = null, part = 'page', width = null, vh = null, open = false } = {}) => {
    const group = `oa-theme-${pid}`;
    const sw = { theme: theme_for ? theme : 'device', target: theme_for, group };
    let head = masthead({ pid, parts: parts_.map((p) => ({ ...p, href: theme_for ? `#${pid}-main` : p.href })), home: { href: theme_for ? `#${pid}-main` : '/', name: site.home_name }, sw });
    head = head.replace(/aria-label="Parts of the site"/, `aria-label="${esc(site.nav_label)}"`)
      .replace(/>Menu<\/span><\/button>/, `>${esc(site.menu.button)}</span></button>`)
      .replace(/(id="[^"]*-menu-name">)Menu</, `$1${esc(site.menu.title)}<`)
      .replace(/<span>Close the menu<\/span>/, `<span>${esc(site.menu.close)}</span>`)
      .replace(/aria-label="Parts of the site, in the menu"/, `aria-label="${esc(site.menu.nav_label)}"`);
    if (width) head = frame_masthead(head, width, false);   // a frame carries only the masthead its width shows, as chapter 20's
    const main = fn({ pid, P: pw.page, F, theme, width });
    const inner = `<a class="ws-skip" href="#${pid}-main">${esc(site.skip)}</a>${head}`
      + title_bar({ pid, A: pw.atlas, M, current: pw.current_view, open })
      + breadcrumb({ A: pw.atlas, crumbs: pw.crumbs, own })
      + (is_home ? '' : `<div class="ws-g">${locator({ A: pw.atlas, parts: F.parts, filled: F.locator })}</div>`)
      + `<main id="${pid}-main" class="ws-main" tabindex="-1"><div class="ws-g"><div class="wa-body">${main}</div></div></main>`
      + footer(site).replace(/\{pid\}/g, pid);
    const style = vh ? ` style="--ws-vh:${vh}px"` : '';
    return `<div class="ws" id="${pid}"${theme_for ? ` data-oa-theme="${theme}"` : ''}${style} data-oa-application="${esc(spec.id)}"`
      + ` data-atlas-view="${esc(spec.view)}"${spec.record ? ` data-atlas-record="${esc(spec.record)}"` : ''} data-atlas-model="${esc(M.sha256)}"><div class="ws-in">${inner}</div></div>`;
  };
  const comp = ['id-chip', 'disclosure', 'loop-stepper', 'choice', 'toggle', 'filter-bar'].map((c) => component_css(c)).join('\n');
  const syms = [...UTILITY_SPRITE, 'oa-sym-u-chevron-24px', 'oa-sym-u-play-24px', 'oa-sym-u-pause-24px', 'oa-sym-u-reset-24px', 'oa-sym-u-arrow-24px'];
  const js = (n) => fs.readFileSync(path.join(CODE, `c-18-${n}.js`), 'utf8');
  return {
    id: spec.id, type, page: spec.view, part: 'page', title: pw.title, words_from: AWd.__from,
    // the page's own style for an export: the website's, chapter 18's components, then the atlas's own rules
    css: site_css() + '\n' + masthead_css() + '\n' + switch_css() + '\n' + comp + '\n' + atlas_css(F.figure_css),
    // in the guide the website's style is already in the head (plates/web-site.css); the atlas plate carries its own
    plate_css: comp + '\n' + atlas_css(F.figure_css), styles: ['web-site'],
    export_css: res_switch_css(), kit_css: '', sprite: sprite([...new Set(syms)]),
    body, widths: spec.widths, views: spec.views,
    scripts: { head: switch_head_js(), tail: [masthead_js(), switch_js(), close_on_widen_js(NAV_BP), js('disclosure'), js('loop-stepper')].join('\n') },
    // contract C4 and C9: the plate's words are chapter 21's entry for this page and chapter 20's site words
    words_records: [{ generator: GEN, id: spec.id }, { generator: SITE_GEN, id: 'A06:site' }],
    atlas: { model: M.sha256, view: spec.view, record: spec.record || null },
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}
