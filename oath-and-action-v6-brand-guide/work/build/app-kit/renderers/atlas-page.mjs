// Atlas page renderer (chat 11c; chapter 21's plan, sections 3 and 9.1; the design director's atlas view specs,
// work/handoffs/phase-4/20261122_Atlas-View-Specs.md): every page of our systems atlas, Who Do They Answer To?, drawn
// inside the website's shell. The skip link and the site's head (the masthead with L3, its parts, the menu and the theme
// switch) come from web-site.mjs's site_head(), which draws them from site-parts.mjs, and the footer from web-site.mjs's
// footer(), by import, never a copy of their markup, so the atlas and the website draw one masthead and one footer
// (AL-04, 3.2.6). The masthead marks "Who Do They Answer To?" as the current part: aria-current="page" on the atlas home
// and "true" on every page inside it (DR-316). Under it the atlas adds its title bar, a breadcrumb below the home and,
// from 48em, the locator (specs 2 and 3).
//
// Every value comes from the model through the figure step (tools/atlas_figures.py, which imports chapter 15's drawing
// code), and every word the page adds from chapter 21's generator (phase4_ch21_build.py --page-words all; contract C9),
// the site's own words from chapter 20's. The style is the website's wherever the rules match (DR-319): a guide plate
// stands on plates/web-site.css and adds plates/atlas-page.css, whose every rule starts with .ws.wa, so no chapter 20
// frame moves (specs 0 and 5).
//
// Templates: home, reform, register, loop, loop-index, how-to-read; part and issue for the atlas's next pages, drawn by no
// content file this chapter (plan 9.1).
import fs from 'fs';
import path from 'path';
import { spawnSync } from 'child_process';
import { ROOT, CODE, component_css, esc, touch, type_css } from '../lib.mjs';
import { site_css, footer, site_head, dark, words as site_words } from './web-site.mjs';
import { sprite, sprite_icons, res_switch_css } from './web-page.mjs';
import { UTILITY_SPRITE, close_on_widen_js, masthead_css, masthead_js, switch_css, switch_head_js, switch_js } from './site-parts.mjs';

export const type = 'atlas-page';
// contract C4: the atlas test and the figure step are code every atlas plate is drawn and judged by
export const code_inputs = () => ['work/build/app-kit/tools/atlas_figures.py', 'work/build/app-kit/tools/atlas_test.py'];
export const GEN = 'work/build/scripts/phase-4/phase4_ch21_build.py';
const SITE_GEN = 'work/build/scripts/phase-4/phase4_ch20_build.py';
const FIGURES = 'work/build/app-kit/tools/atlas_figures.py';
const BP = { phone: 24.375, tablet: 48, desktop: 64, wide: 90 };   // chapter 07's breakpoints, in em, as the website's
const NAV_BP = 64;
const at = (em, body) => `@container ws (min-width: ${em}em){${body}}`;
const under = (em, body) => `@container ws (max-width: ${em - 0.001}em){${body}}`;
const MINUS = '−';

// ---------------------------------------------------------------------------------------------------------------- words
let AW = null;
export function atlas_words() {
  if (AW) { touch(AW.__from); return AW; }
  if (fs.existsSync(path.join(ROOT, GEN))) {
    const r = spawnSync('python3', ['-I', path.join(ROOT, GEN), '--page-words', 'all'], { encoding: 'utf8', cwd: ROOT, maxBuffer: 16 * 1024 * 1024 });
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
// the keys of the page's words a block needs; a key the generator does not print stops the build with its name (C9)
function need(o, keys, where) {
  for (const k of keys) if (o == null || o[k] == null) throw new Error(`the atlas page words for ${where} hold no "${k}" (contract C9)`);
  return o;
}
const fill = (t, vals) => String(t).replace(/\{(\w+)\}/g, (m, k) => (vals[k] != null ? vals[k] : m));
// a template's words escaped, its {keys} filled with markup (a chip in place of a bare ID, house rule H11)
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

// ---------------------------------------------------------------------------------------------------------------- paths
// contract C9's paths and anchors (the data lead's R5): a connection's line on the sheet of the variable it moves
const low = (x) => String(x).toLowerCase();
export const PATHS = {
  Connection: (id, I) => `/atlas/register/${low(I[id].sheet)}#register-${low(id)}`,
  Variable: (id, I) => `/atlas/register/${low(I[id].sheet)}#variable-${low(id)}`,
  Loop: (id) => `/atlas/loops/${low(id)}`,
  Reform: (id) => `/atlas/reforms/${low(id)}`,
  Domain: (id) => `/atlas/register/${low(id)}`,
  Route: (id) => `/atlas/routes/${low(id)}`,
  Claim: (id) => `#claim-${low(id)}`,
};

// A typed chip (Rule 18.24, chapter 18's c-18-id-chip): the kind word and the ID, plain or as a link, with the marks the
// atlas test reads. The kind is the one the model files the ID under, given by the caller from the record it reads.
export function chip(kind, id, { href = null, evidence = false, cls = '', current = false } = {}) {
  const ev = evidence && href ? ` data-evidence-href="${esc(href)}"` : '';
  const a = ` data-atlas-kind="${esc(kind)}" data-atlas-id="${esc(id)}"${ev}`;
  const inner = `${esc(kind)} <span class="oa-chip-id">${esc(id)}</span>`;
  return href ? `<a class="oa-chip oa-chip--link${cls ? ' ' + cls : ''}" href="${esc(href)}"${current ? ' aria-current="page"' : ''}${a}>${inner}</a>`
    : `<span class="oa-chip${cls ? ' ' + cls : ''}"${a}>${inner}</span>`;
}
// a linked chip for a record of one of the kinds with a page or a line (R5); a connection's and a variable's link is its
// evidence, the line that grades it
const link_chip = (kind, id, I, opts = {}) => chip(kind, id, { href: PATHS[kind] ? PATHS[kind](id, I) : null, evidence: kind === 'Connection' || kind === 'Variable', ...opts });

// The atlas's stored text, as stored (DR-37), with each bare ID of the ten kinds set in its typed chip (the data lead's
// R11): a kind word the prose gives before it is taken into the chip; a code two collections share with no kind word
// stops the build
const KIND_WORDS = ['Variable', 'Connection', 'Loop', 'Reform', 'Issue', 'Claim', 'Domain'];
function stored(text, I) {
  const t = esc(text).replace(/'/g, '’');
  return t.replace(/(?:\b(variable|connection|loop|reform|issue|claim|domain)\s+)?(?<![\w/#-])([A-Z]{1,3}-?\d+[a-z]?)(?![\w-])/gi, (m, word, id) => {
    const rec = I[id];
    if (!rec || /^[a-z]/.test(id)) return m;
    let kind = word ? KIND_WORDS.find((k) => k.toLowerCase() === word.toLowerCase()) : null;
    if (!kind) {
      const ks = rec.kinds.filter((k) => k !== 'Route');
      if (ks.length !== 1) throw new Error(`the stored text "${text.slice(0, 60)}" holds ${id} with no kind word, and ${id} is a ${ks.join(' and a ')} (R11)`);
      kind = ks[0];
    }
    if (!rec.kinds.includes(kind)) return m;
    return link_chip(kind, id, I);
  });
}

// ---------------------------------------------------------------------------------------------------------------- shell
const CHEV = () => sprite_icons(fs.readFileSync(path.join(CODE, 'c-18-disclosure.html'), 'utf8').match(/<svg\s+class="oa-disclosure-chevron"[\s\S]*?<\/svg>/)[0]).replace(/\s*\n\s*/g, ' ');

// the title bar (specs 2): a Charcoal band with the atlas's name, its subtitle and snapshot, and the five views; under
// 64em the views sit behind chapter 18's button-built disclosure, closed on load
function title_bar({ pid, A, M, current, cur_val, open }) {
  need(A, ['views_label', 'views_button', 'views', 'snapshot'], 'the title bar');
  const date = `<time datetime="${esc(M.snapshot)}">${esc(M.snapshot_words)}</time>`;
  const links = A.views.map(([w, href]) => `<li><a class="oa-masthead-row-link oa-masthead-part" href="${esc(href)}"${w === current ? ` aria-current="${cur_val}"` : ''}>${esc(w)}</a></li>`).join('');
  return `<nav class="wa-bar oa-surface-charcoal" aria-label="${esc(A.views_label)}" data-oa-disclosure><div class="wa-bar-in">`
    + `<p class="wa-name"><span class="n">${esc(M.title)}</span><span class="wa-sub"><span class="ws-nb s1">${esc(M.subtitle)}</span><span class="dot s1" aria-hidden="true"> · </span>`
    + `<span class="ws-nb" data-status-date="${esc(M.snapshot)}">${fill_html(A.snapshot, { date })}</span></span></p>`
    + `<button type="button" class="oa-masthead-menu oa-disclosure-button wa-views-btn" aria-expanded="${open ? 'true' : 'false'}" aria-controls="${pid}-views">`
    + `<span>${esc(A.views_button)}</span>${CHEV()}</button>`
    + `<ul class="wa-views" id="${pid}-views"${open ? '' : ' hidden'}>${links}</ul></div></nav>`;
}

// the locator (Rule 12.7; specs 3.2): eight boxes on whole pixels, the page's parts filled in ink
const LOC = { X: [0, 0, 88, 8], A: [0, 11, 15, 15], B: [18, 11, 15, 15], C: [36, 11, 16, 15], D: [55, 11, 15, 15], E: [73, 11, 15, 15], EC: [0, 29, 52, 12], TC: [55, 29, 33, 12] };
function locator({ A, filled, href }) {
  const boxes = Object.entries(LOC).map(([k, [x, y, w, h]]) => `<rect x="${x + 0.5}" y="${y + 0.5}" width="${w - 1}" height="${h - 1}" data-part="${k}"${filled.includes(k) ? ' data-current' : ''}/>`).join('');
  const names = filled.map((k) => (A.parts && A.parts[k] ? A.parts[k][0] : k)).join(' and ');
  return `<a class="wa-loc" href="${esc(href)}"><svg viewBox="0 0 88 41" width="88" height="41" aria-hidden="true" focusable="false">${boxes}</svg>`
    + `<span class="vh">${esc(fill(A.locator_alt || '{part}', { part: names }))}</span></a>`;
}

// the breadcrumb (specs 3.1): the places, then the current page, a record's typed chip in bold or the view's words
function breadcrumb({ A, crumbs, own, loc }) {
  const items = crumbs.map(([w, href]) => `<li><a href="${esc(href)}">${esc(w)}</a><span class="sep" aria-hidden="true">/</span></li>`).join('');
  return `<nav class="wa-crumbs" aria-label="${esc(A.breadcrumb_label)}"><ol>${items}<li>${own}</li></ol>${loc}</nav>`;
}

// ---------------------------------------------------------------------------------------------------------------- blocks
const ticks = (n) => `<svg class="wa-ticks" viewBox="0 0 ${6 * n} 12" width="${6 * n}" height="12" aria-hidden="true" focusable="false">`
  + Array.from({ length: n }, (_, i) => `<line x1="${2 + 6 * i}" y1="1" x2="${2 + 6 * i}" y2="11"/>`).join('') + `</svg>`;
const count = (n, key, words) => `<span data-count="${n}" data-count-of="${esc(key)}">${words}</span>`;
const sec = (key, h2id, h2, body, extra = '') => `<section class="wa-sec" data-oa-section="${esc(key)}"${h2id ? ` aria-labelledby="${h2id}"` : ''}${extra}>`
  + (h2 ? `<div class="ws-g"><h2 class="ws-h2" id="${h2id}">${esc(h2)}</h2></div>` : '') + body + `</section>`;
const quote = (html, field) => `<blockquote class="wa-q" data-atlas-field="${esc(field)}"><p class="ws-p">${html}</p></blockquote>`;
// the h1's title in curly quotation marks, held to its first and last words (Rule 18.22)
function quoted_title(t) {
  const w = String(t).split(' ');
  if (w.length < 3) return `<span class="ws-nb">“${esc(t)}”</span>`;
  return `<span class="ws-nb">“${esc(w[0])}</span> ${esc(w.slice(1, -1).join(' '))} <span class="ws-nb">${esc(w[w.length - 1])}”</span>`;
}

// a reform's effects, one family a row (Rule 15.16; the data lead's R12): the family's name, the pips, the code whole
// with its qualifier and true minus signs, and the model's words for the code; never a total
function effect_rows(r, F) {
  const words = F.effect_words || {};
  const say = (code) => String(code).split(/\s+to\s+/).map((c) => words[(c.match(/^[+\-]?[SML0?]/) || [''])[0]] || '').filter(Boolean).join(' to ');
  return `<ul class="wa-ef">` + r.effects.map((e) => `<li data-effect-family="${esc(e.family)}" data-effect-code="${esc(e.code)}" data-atlas-reform="${esc(r.id)}">`
    + `<span class="f">${esc(e.name)}</span>${e.pips || ''}<span class="c"><b>${esc(String(e.code).replace(/-/g, MINUS))}</b>${say(e.code) ? `, ${esc(say(e.code))}` : ''}</span></li>`).join('') + `</ul>`;
}
// a reform's routes, each with its own check date or "Not checked" (Rules 13.10, 15.24), never the reform's status date
function route_rows(r, A, I) {
  return `<ul class="wa-rt">` + r.routes.map((x) => `<li data-route="${esc(x.code)}" data-checked="${esc(x.checked || 'none')}" data-atlas-reform="${esc(r.id)}">`
    + `<span class="n">${link_chip('Route', x.code, I)} ${esc(x.name || '')}</span><span>${esc(x.who)}</span><span>${esc(x.feasibility)}</span>`
    + (x.note ? `<span class="wa-stored" data-atlas-field="note">${stored(x.note, I)}</span>` : '')
    + `<span class="d">${x.checked ? esc(fill(A.checked, { date: x.checked_words })) : esc(A.not_checked)}</span></li>`).join('') + `</ul>`;
}

// ---------------------------------------------------------------------------------------------------------------- loop
function view_loop({ pid, P, A, F, panels }) {
  const v = F.view, lp = v.loop, I = F.ids;
  need(P, ['kind', 'facts_label', 'facts', 'minus_even', 'minus_odd', 'stepper_heading', 'read_label', 'arithmetic', 'parity_even', 'parity_odd',
    'weakest_line', 'also_aim', 'steps', 'chooser_legend', 'effects_heading', 'routes_heading', 'record_heading', 'record_labels', 'evidence_heading',
    'step_word', 'records_line'], 'the loop page');
  const kind_word = A.kinds[lp.type];
  const steps = v.steps;
  const sc = (s) => link_chip('Connection', s.id, I);
  // head (specs 7 and 8.1)
  const gl = v.grade_line.map((g) => fill_html(P.grade_line || '{grade} for {from} to {to}', { grade: esc(g.grade.word), from: link_chip('Variable', g.from, I), to: link_chip('Variable', g.to, I) })).join('; ');
  const even = v.minus % 2 === 0;
  const weak = steps.find((s) => s.id === v.weakest);
  const facts = `<div class="wa-facts${panels.includes('Loop') ? ' oa-surface-charcoal ws-panel' : ''}" data-oa-part="facts"><p class="lab">${esc(P.facts_label)}</p><dl>`
    + `<div><dt>${esc(P.facts.kind)}</dt><dd>${esc(kind_word)}</dd></div>`
    + `<div><dt>${esc(P.facts.steps)}</dt><dd>${count(steps.length, `loop:${lp.id}:steps`, String(steps.length))}</dd></div>`
    + `<div><dt>${esc(P.facts.minus)}</dt><dd>${count(v.minus, `loop:${lp.id}:minus`, esc(fill(even ? P.minus_even : P.minus_odd, { n: v.minus })))}</dd></div>`
    + `<div><dt>${esc(P.facts.closure)}</dt><dd class="wa-stored" data-atlas-field="closure">${stored(lp.closure, I)}</dd></div>`
    + `<div><dt>${esc(P.facts.delay)}</dt><dd>${lp.delay && lp.delay.ticks ? ticks(lp.delay.ticks) + ' ' + esc(lp.delay.words) : ''}</dd></div>`
    + (weak ? `<div><dt>${esc(P.facts.weakest)}</dt><dd>${sc(weak)} ${esc(weak.grade.word)}</dd></div>` : '')
    + `</dl></div>`;
  const head = `<div class="ws-g wa-head"><div class="wa-op"><p class="ws-kick">${chip('Loop', lp.id)}<span class="d" aria-hidden="true">·</span><span class="b">${esc(fill(P.kind, { kind: kind_word }))}</span></p>`
    + `<h1 class="ws-h1 wa-t1" id="${pid}-h1">${quoted_title(lp.title)}</h1><p class="ws-intro wa-gl">${gl}</p></div>${facts}</div>`;
  // the read-aloud line (the data lead's R4): each variable's chip with its direction, each connection's chip with its
  // sign's word, in the order the loop runs; its marks name the directions for the atlas test (T4)
  const say = (tok) => (tok.includes(':') ? `${link_chip('Variable', tok.split(':')[0], I)} ${esc(tok.split(':')[1])}` : `${link_chip('Connection', tok, I)} ${esc(A.signs[steps.find((s) => s.id === tok).sign])}`);
  const line = v.reads.split(' ').map(say).join(', ');
  const read = `<div class="wa-read" data-oa-part="read"><p class="lab">${esc(P.read_label)}</p><p class="ws-p" data-atlas-reads="${esc(v.reads)}">${line}.</p>`
    + `<p class="wa-small">${esc(P.arithmetic)}</p><p class="wa-small">${count(v.minus, `loop:${lp.id}:minus`, esc(fill(even ? P.parity_even : P.parity_odd, { n: v.minus })))}</p></div>`;
  // the drawing, chapter 15's loop by the figure step, with the other reforms' ink tags under it (Rule 21.5)
  const tags = steps.filter((s) => (v.tags[s.id] || []).length).map((s) => `<li class="wa-tag">${sc(s)} ${fill_html(P.also_aim, { chips: v.tags[s.id].map((r) => chip('Reform', r)).join(' and ') })}</li>`).join('');
  const drawing = `<div class="wa-draw" data-oa-part="drawing"><figure class="wa-fig">${v.figure.svg}</figure>`
    + (weak ? `<p class="wa-small wa-weak">${sc(weak)} ${esc(P.weakest_line)}</p>` : '') + (tags ? `<ul class="wa-tags">${tags}</ul>` : '') + `</div>`;
  // the stepper, chapter 18's code set read from its files (Rule 21.13; AL-22, AL-24)
  if (P.steps.length !== steps.length) throw new Error(`the loop page's words hold ${P.steps.length} stepper lines for ${steps.length} steps (contract C9)`);
  const src = fs.readFileSync(path.join(CODE, 'c-18-loop-stepper.html'), 'utf8');
  const controls = sprite_icons(src.match(/<div\s+class="oa-stepper-controls"[\s\S]*?<\/button>\s*<\/div>/)[0]).replace(/\s*\n\s*/g, ' ')
    .replace('aria-label="Steps of the loop"', `aria-label="${esc(fill(P.stepper_group || 'Steps of Loop {id}', { id: lp.id }))}"`)
    .replace(/aria-describedby="oa-stepper-why"/g, `aria-describedby="${pid}-why"`);
  const why = src.match(/<p class="oa-stepper-why"[\s\S]*?<\/p>/)[0].replace(/\s*\n\s*/g, ' ').replace('id="oa-stepper-why"', `id="${pid}-why"`);
  const items = P.steps.map((st, i) => `<li class="oa-stepper-step" data-oa-hold="${esc(st.hold)}" data-atlas-kind="Connection" data-atlas-id="${esc(steps[i].id)}"`
    + ` data-sign="${esc(steps[i].sign)}" data-type="${esc(steps[i].type)}" data-delay="${esc(steps[i].delay.key)}" data-grade="${esc(steps[i].grade.key)}"`
    + `${steps[i].id === v.weakest ? ' data-weakest="true"' : ''}><span class="oa-stepper-line">${esc(st.line)}</span>&#32;<span class="oa-stepper-more">${esc(st.more || '')}</span></li>`).join('');
  const ready = P.stepper_ready || '';
  const stepper = `<div class="oa-stepper wa-stepper" data-oa-stepper data-oa-part="stepper"><p class="oa-stepper-status" role="status" data-oa-ready="${esc(ready)}">${esc(ready)}</p>`
    + controls + why + `<ol class="oa-stepper-steps" role="list">${items}</ol></div>`;
  // the chooser (Rule 15.20), chapter 18's choice, and the chosen reform's panel
  const check = sprite_icons(fs.readFileSync(path.join(CODE, 'c-18-choice.html'), 'utf8').match(/<svg\s+class="oa-choice-check"[\s\S]*?<\/svg>/)[0]).replace(/\s*\n\s*/g, ' ');
  const choices = v.offered.map((r) => `<label class="oa-choice-item"><input class="oa-choice-input" type="radio" name="${pid}-reform" value="${esc(r.id)}"${r.id === v.chosen ? ' checked' : ''}>`
    + `<span class="oa-choice-face">${check}<span class="oa-choice-label">${chip('Reform', r.id)} “${esc(r.title)}”</span></span></label>`).join('');
  const panels_ = v.offered.map((r) => `<div class="wa-panel" data-oa-panel="${esc(r.id)}"><h3 class="ws-h3">${chip('Reform', r.id, { href: PATHS.Reform(r.id) })} “${esc(r.title)}”</h3>`
    + `<p class="wa-small">${esc(r.band_words || '')}</p>`
    + `<p class="lab">${esc(P.effects_heading)}</p><p class="wa-small" data-status-date="${esc(r.status.checked)}" data-atlas-reform="${esc(r.id)}">${esc(fill(A.as_of, { date: r.status.checked_words }))}</p>${effect_rows(r, F)}`
    + `<p class="lab">${esc(P.routes_heading)}</p>${route_rows(r, A, I)}</div>`).join('');
  const chooser = `<div class="ws-g wa-choose" data-oa-part="chooser"><fieldset class="oa-choice"><legend class="oa-choice-legend">${esc(P.chooser_legend)}</legend>`
    + `<div class="oa-choice-row oa-choice-row--list">${choices}</div></fieldset><div class="wa-panels">${panels_}</div></div>`;
  const sec2 = `<div class="ws-g wa-two">${read}${drawing}</div><div class="ws-g wa-two"><div></div>${stepper}</div>${chooser}`;
  // the loop in the atlas's words, as stored (DR-37), and the evidence a step away (Rule 21.7)
  const rec = ['summary', 'case', 'qualification', 'adaptation'].map((k) => `<h3 class="ws-h3">${esc(P.record_labels[k])}</h3>${quote(stored(lp[k], I), k)}`).join('');
  const ev = `<ul class="wa-ev">` + steps.map((s, i) => `<li data-atlas-kind="Connection" data-atlas-id="${esc(s.id)}" data-sign="${esc(s.sign)}" data-type="${esc(s.type)}" data-delay="${esc(s.delay.key)}" data-grade="${esc(s.grade.key)}">`
    + `<span class="st">${esc(fill(P.step_word, { n: i + 1 }))}</span>${sc(s)}<span class="gr">${F.grade_samples[s.grade.key] || ''}${s.grade.key === 'documented' ? F.record_square : ''} ${esc(s.grade.word)}</span>`
    + `<span class="ct wa-stored" data-atlas-field="citation">${stored(s.citation, I)}</span></li>`).join('') + `</ul>`
    + `<p class="ws-p wa-recs"><a href="/atlas/register?loop=${low(lp.id)}">${count(lp.records.length, `loop:${lp.id}:records`, esc(fill(P.records_line, { n: lp.records.length })))}</a></p>`;
  return sec('Loop', null, null, head, ` aria-labelledby="${pid}-h1"`)
    + sec('Stepper', `${pid}-s2`, P.stepper_heading, sec2)
    + sec('Record', `${pid}-s3`, P.record_heading, `<div class="ws-g"><div class="wa-col7">${rec}</div></div>`)
    + sec('Evidence', `${pid}-s4`, P.evidence_heading, `<div class="ws-g"><div class="wa-col8">${ev}</div></div>`);
}

// ---------------------------------------------------------------------------------------------------------------- reform
function view_reform({ pid, P, A, F, panels, spec }) {
  const v = F.view, r = v.reform, I = F.ids;
  need(P, ['status_label', 'problem', 'remedy', 'where_heading', 'where_note', 'touches', 'aims_here', 'grades_heading', 'source_link', 'effects_heading',
    'effects_confidence', 'routes_heading', 'routes_head', 'complements_heading', 'sources_summary'], 'the reform page');
  const band = (A.bands && A.bands[r.band]) || r.band;
  const gw = (g) => `<b>${esc(g.word)}</b>`;
  const status = `<div class="wa-facts${panels.includes('Reform') ? ' oa-surface-charcoal ws-panel' : ''}" data-oa-part="status"><p class="lab">${esc(P.status_label)}</p>`
    + `<p class="wa-small wa-stored" data-atlas-field="status">${stored(r.status.text, I)}</p>`
    + `<p class="wa-small" data-status-date="${esc(r.status.checked)}" data-atlas-reform="${esc(r.id)}">${esc(fill(A.as_of, { date: r.status.checked_words }))}</p>`
    + `<dl><div><dt>${esc(P.problem)}</dt><dd><a href="#${pid}-problem">${gw(r.problem.grade)}</a></dd></div><div><dt>${esc(P.remedy)}</dt><dd><a href="#${pid}-remedy">${gw(r.remedy.grade)}</a></dd></div></dl>`
    + `<p class="wa-cap">${esc(r.band_words || '')}</p></div>`;
  const head = `<div class="ws-g wa-head"><div class="wa-op"><p class="ws-kick">${chip('Reform', r.id)}<span class="d" aria-hidden="true">·</span><span class="b">${esc(band)}</span></p>`
    + `<h1 class="ws-h1 wa-t1" id="${pid}-h1">${esc(r.title)}</h1><p class="ws-intro wa-stored" data-atlas-field="summary">${stored(r.summary, I)}</p></div>${status}</div>`;
  // where it acts: the figure step's drawing of the targets, red, with the other reforms' ink tags (Rules 12.5, 21.5)
  const tv = v.targets.filter((t) => 'part' in t);
  const tags = Object.entries(v.tags).filter(([, rs]) => rs.length).map(([t, rs]) => `<li class="wa-tag">${link_chip('Variable', t, I)}: ${rs.map((x) => chip('Reform', x, { href: PATHS.Reform(x) })).join(' ')} ${esc(P.aims_here)}</li>`).join('');
  const targets_words = tv.map((t) => `${link_chip('Variable', t.id, I)} “${esc(t.title)}”`).join(' and ');
  const note = `<div class="wa-note"><p class="wa-small">${fill_html(P.where_note, { reform: chip('Reform', r.id), targets: targets_words })}</p>`
    + tv.map((t) => `<p class="wa-small">${link_chip('Variable', t.id, I)} <span class="wa-stored" data-atlas-field="increase_means">${stored(t.increase_means, I)}</span></p>`).join('')
    + v.loops_named.filter((l) => !l.drawn).map((l) => `<p class="wa-small">${fill_html(P.touches, { loop: link_chip('Loop', l.id, I) })}</p>`).join('') + `</div>`;
  const where = `<div class="ws-g wa-where" data-oa-part="targets"><div class="wa-draw"><h3 class="ws-h3">${esc(P.where_heading)}</h3>`
    + (v.figure ? `<figure class="wa-fig">${v.figure.svg}</figure>` : '') + (tags ? `<ul class="wa-tags">${tags}</ul>` : '') + `</div>${note}</div>`;
  // the two grades apart (Rule 15.12), the contested remedy's two readings side by side (H08), split where the content
  // file says (remedy_split, the sentence of the stored text that opens the second reading)
  // sentences end at a stop followed by a space and a capital, so "1.3 million" stays whole
  const sents = r.remedy.text.split(/(?<=[.!?])\s+(?=[A-Z])/);
  const k = (spec.remedy_split || 0) - 1;
  const readings = k > 0 && k < sents.length ? [sents.slice(0, k).join(' ').trim(), sents.slice(k).join(' ').trim()] : [r.remedy.text];
  if (readings.some((x) => !x)) throw new Error('remedy_split leaves a reading empty (the specs, section 9)');
  const src_of = v.sources.map((s) => s.id);
  const rhead = (lbl, g, id) => `<div class="wa-gh" id="${id}"><p class="lab">${esc(lbl)}</p><p class="wa-gw">${esc(g.word)}</p><p class="wa-small">${esc(g.gloss)}</p></div>`;
  const reading_src = (i) => (src_of[i + 1] ? ` <a href="#${pid}-source-${low(src_of[i + 1])}">${esc(P.source_link)}</a>` : '');
  const grades = `<div class="ws-g wa-grade">${rhead(P.problem, r.problem.grade, `${pid}-problem`)}<div class="wa-rd">${quote(stored(r.problem.text, I), 'problem')}</div></div>`
    + `<div class="ws-g wa-grade wa-remedy">${rhead(P.remedy, r.remedy.grade, `${pid}-remedy`)}`
    + readings.map((x, i) => `<div class="wa-rd" data-reading="${i + 1}">${quote(stored(x, I) + reading_src(i), 'remedy')}</div>`).join('') + `</div>`;
  const effects = `<p class="wa-small" data-status-date="${esc(r.status.checked)}" data-atlas-reform="${esc(r.id)}">${esc(fill(A.as_of, { date: r.status.checked_words }))}</p>`
    + effect_rows(r, F) + `<p class="wa-small">${esc(fill(P.effects_confidence, { text: r.effects_confidence }))}</p>`;
  const routes = route_rows(r, A, I) + `<h3 class="ws-h3">${esc(P.complements_heading)}</h3>`
    + `<ul class="wa-cl">` + v.complements.map((c) => `<li>${link_chip('Reform', c.id, I)} “${esc(c.title)}”</li>`).join('') + `</ul>`;
  const srcs = `<details class="oa-disclosure wa-src"><summary class="oa-disclosure-summary"><span class="oa-disclosure-label">${esc(P.sources_summary)}</span>${CHEV()}</summary>`
    + `<div class="oa-disclosure-body"><ul>` + v.sources.map((s) => `<li id="${pid}-source-${low(s.id)}" class="wa-small">${esc([s.publisher, s.title, s.year].filter(Boolean).join(', '))}${s.url ? `, <span class="ws-nb">${esc(s.url)}</span>` : ''}</li>`).join('')
    + `</ul></div></details>`;
  return sec('Reform', null, null, head + where, ` aria-labelledby="${pid}-h1"`)
    + sec('Grades', `${pid}-s2`, P.grades_heading, grades, ' data-oa-part="grades"')
    + sec('Effects', `${pid}-s3`, P.effects_heading, `<div class="ws-g"><div class="wa-col8">${effects}</div></div>`, ' data-oa-part="effects"')
    + sec('Routes', `${pid}-s4`, P.routes_heading, `<div class="ws-g"><div class="wa-col8">${routes}</div></div>`, ' data-oa-part="routes"')
    + sec('Sources', null, null, `<div class="ws-g"><div class="wa-col8">${srcs}</div></div>`);
}

const VIEWS = { loop: view_loop, reform: view_reform };

// ---------------------------------------------------------------------------------------------------------------- style
// atlas-page's own rules, over the website's (DR-319; specs 5): every rule starts with .ws.wa, so no chapter 20 frame
// moves. Colors and type only by token.
export function atlas_css(fig_css) {
  const W = '.ws.wa';
  return `
/* the title bar (specs 2) */
${W} .wa-bar{display:block;padding-block:8px}
${dark('.wa-bar', 'box-shadow:inset 0 -1px 0 var(--oa-color-border-hairline-on-charcoal)')}
${W} .wa-bar-in{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;column-gap:32px;min-height:40px;padding-inline:var(--m)}
${W} .wa-name{display:flex;flex-direction:column;margin:0}
${W} .wa-name .n{${type_css('label')};color:var(--oa-color-text-primary)}
${W} .wa-sub{${type_css('caption')};color:var(--oa-color-text-secondary)}
${under(BP.tablet, `${W} .wa-sub .s1{display:none}`)}
${W} .wa-views{list-style:none;margin:0;padding:0}
${W} .wa-views-btn{margin-left:auto}
${W} .wa-views-btn .oa-disclosure-chevron{transition:transform var(--oa-motion-duration-standard)}
${W} .wa-views-btn[aria-expanded="true"] .oa-disclosure-chevron{transform:rotate(180deg)}
@media (prefers-reduced-motion: reduce){${W} .wa-views-btn .oa-disclosure-chevron{transition:none}}
${under(NAV_BP, `${W} .wa-views{flex:0 0 100%;margin-top:8px;border-top:1px solid var(--oa-color-border-hairline)}${W} .wa-views li{border-bottom:1px solid var(--oa-color-border-hairline)}${W} .wa-views a[aria-current]{text-decoration:none}`)}
${at(NAV_BP, `${W} .wa-views,${W} .wa-views[hidden]{display:flex;gap:0 var(--ws-part-gap,16px)}${W} .wa-views a,${W} .wa-views a[aria-current]{padding:0;background:none;border-left:0}${W} .wa-views a:hover{text-underline-offset:.3em}`)}
/* the breadcrumb and the locator (specs 3) */
${W} .wa-crumbs{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-top:8px;padding-inline:var(--m)}
${W} .wa-crumbs ol{display:flex;flex-wrap:wrap;align-items:center;list-style:none;margin:0;padding:0;${type_css('body-small')}}
${W} .wa-crumbs li{display:flex;align-items:center;min-height:var(--oa-size-target-touch)}
${W} .wa-crumbs a:not(.oa-chip){display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);color:var(--oa-color-text-primary);text-decoration-thickness:1px;text-underline-offset:.2em}
${W} .wa-crumbs a:not(.oa-chip):hover{text-decoration-thickness:2px}
${W} .wa-crumbs a[aria-current]{font-weight:var(--oa-font-weight-bold);text-decoration:none}
${W} .wa-crumbs .sep{margin-inline:8px;color:var(--oa-color-text-secondary)}
${W} .wa-loc{display:none;flex:none;margin-top:2px}
${W} .wa-loc svg{display:block}
${W} .wa-loc rect{fill:var(--oa-color-surface);stroke:var(--oa-color-graphic-subtle);stroke-width:1px}
${W} .wa-loc rect[data-current]{fill:var(--oa-color-graphic-essential);stroke:var(--oa-color-graphic-essential)}
${at(BP.tablet, `${W} .wa-loc{display:block}`)}
${W} .wa-crumbs+.ws-main{padding-top:24px}
/* main (specs 7) */
${W} .wa-sec{display:block}
${W} .wa-head{row-gap:32px}
${W} .wa-op>*+*{margin-top:24px !important}
${W} .wa-op .ws-h1+*{margin-top:32px !important}
${W} .wa-t1{${type_css('section')};text-wrap:balance}
${W} .lab{${type_css('label')};color:var(--oa-color-text-secondary);margin:0 0 8px !important}
${W} .wa-small{${type_css('body-small')}}
${W} .wa-cap{${type_css('caption')};color:var(--oa-color-text-secondary);margin-top:16px !important}
${W} .wa-facts{padding:24px;align-self:start}
${at(BP.tablet, `${W} .wa-facts{padding:32px}`)}
${W} .wa-facts dl{margin:0;${type_css('body-small')}}
${W} .wa-facts dl>div{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);column-gap:12px;padding:8px 0;border-bottom:1px solid var(--oa-color-border-hairline)}
${W} .wa-facts dt{font-weight:var(--oa-font-weight-semibold)}
${W} .wa-facts dd{margin:0}
${W} .wa-ticks line{stroke:var(--oa-color-graphic-essential);stroke-width:2px}
${W} .wa-q{margin:0;padding-left:24px;border-left:2px solid var(--oa-color-border-strong)}
${W} .wa-q+.ws-h3{margin-top:32px !important}
${W} .wa-fig{margin:0}
${W} .wa-fig .sv{display:block;max-width:100%;height:auto}
${W} .wa-draw,${W} .wa-read,${W} .wa-note{min-width:0}
${W} .wa-two{row-gap:24px;margin-top:0}
${W} .wa-two+.wa-two{margin-top:24px}
${W} .wa-read>*+*{margin-top:16px !important}
${W} .wa-tags,${W} .wa-ev,${W} .wa-cl{list-style:none;margin:16px 0 0;padding:0}
${W} .wa-tag{${type_css('data-label')};display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:8px}
${W} .wa-weak{margin-top:8px !important}
${W} .wa-stepper{min-width:0}
${W} .wa-choose{margin-top:48px;row-gap:24px}
${W} .wa-panels .wa-panel{display:none}
${[1, 2, 3, 4, 5].map((k) => `${W} .wa-choose:has(.oa-choice-item:nth-child(${k}) .oa-choice-input:checked) .wa-panel:nth-child(${k})`).join(',')}{display:block}
@media print{${W} .wa-panels .wa-panel{display:block}}
${W} .wa-panels{padding-top:16px;border-top:2px solid var(--oa-color-border-strong)}
${W} .wa-panel .lab{margin-top:24px !important}
${W} .wa-ef,${W} .wa-rt{list-style:none;margin:0;padding:0;${type_css('body-small')}}
${W} .wa-ef li,${W} .wa-rt li{display:flex;flex-wrap:wrap;align-items:center;column-gap:12px;min-height:var(--oa-size-target-touch);padding:8px 0;border-bottom:1px solid var(--oa-color-border-hairline)}
${W} .wa-ef .f{flex:0 0 12em;font-weight:var(--oa-font-weight-semibold)}
${W} .wa-ef .pp .j{stroke:var(--oa-color-graphic-essential)}
${W} .wa-rt .n{flex:0 0 100%;font-weight:var(--oa-font-weight-semibold)}
${W} .wa-ev li{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;padding:16px 0;border-bottom:1px solid var(--oa-color-border-hairline);${type_css('body-small')}}
${W} .wa-ev .st{font-weight:var(--oa-font-weight-semibold)}
${W} .wa-ev .gr{display:inline-flex;align-items:center;gap:6px}
${W} .wa-ev .ct{flex:0 0 100%}
${W} .wa-recs{margin-top:32px !important}
${W} .wa-gw{${type_css('h4')}}
${W} .wa-grade{row-gap:24px;margin-top:0}
${W} .wa-grade+.wa-grade{margin-top:48px}
${W} .wa-where{margin-top:48px;row-gap:24px}
${W} .wa-note>*+*{margin-top:12px !important}
${W} .wa-src{margin-top:16px}
${W} .wa-src ul{margin:0;padding-left:20px}
${at(BP.desktop, `${W} .wa-op{grid-column:1/9}${W} .wa-head>.wa-facts{grid-column:9/13;grid-row:1}
 ${W} .wa-two>:first-child{grid-column:1/5}${W} .wa-two>:last-child{grid-column:5/13}
 ${W} .wa-two .wa-fig .sv{max-width:min(100%,640px)}
 ${W} .wa-choose>fieldset{grid-column:1/5}${W} .wa-choose>.wa-panels{grid-column:5/13}
 ${W} .wa-col7{grid-column:1/8}${W} .wa-col8{grid-column:1/9}
 ${W} .wa-where>.wa-draw{grid-column:1/8}${W} .wa-where>.wa-note{grid-column:8/13}
 ${W} .wa-grade>.wa-gh{grid-column:1/5}${W} .wa-grade>.wa-rd{grid-column:5/13}${W} .wa-remedy>.wa-rd{grid-column:span 4}`)}
${fig_css}
`;
}

// ---------------------------------------------------------------------------------------------------------------- render
export async function render(spec) {
  const AWd = atlas_words();
  const pw = AWd[spec.id];
  if (!pw) throw new Error(`the atlas page words hold no entry for ${spec.id} (contract C9)`);
  need(pw, ['title', 'atlas', 'current_view', 'page'], spec.id);
  need(pw.atlas, ['views_label', 'views_button', 'views', 'snapshot', 'breadcrumb_label', 'locator_alt', 'not_checked', 'checked', 'as_of', 'kinds', 'signs'], `${spec.id}'s atlas words`);
  const SW = site_words();
  const site = (SW.A06 || {}).site;
  if (!site) throw new Error("chapter 20's words hold no site entry");
  const F = figures(spec);
  const M = F.model, A = pw.atlas;
  const is_home = spec.view === 'home';
  const record_page = spec.view === 'loop' || spec.view === 'reform';
  const parts_ = site.parts.map(([label, href]) => ({ label, href, current: label === M.title ? (is_home ? 'page' : 'true') : false }));
  const fn = VIEWS[spec.view];
  if (!fn) throw new Error(`the atlas renderer draws no ${spec.view} view yet (its hand-over from the design director)`);
  const kind = { loop: 'Loop', reform: 'Reform' }[spec.view];
  const view_href = (A.views.find(([w]) => w === pw.current_view) || [])[1] || '/atlas';
  const panels = spec.panels || [];
  const body = ({ pid, theme, theme_for = null, part = 'page', width = null, vh = null, open = false } = {}) => {
    const sw = { theme: theme_for ? theme : 'device', target: theme_for, group: `oa-theme-${pid}` };
    const head = site_head({ pid, parts: parts_, site, sw, theme_for, home_page: false, open: false, width });
    const own = record_page ? chip(kind, spec.record, { href: PATHS[kind](spec.record), current: true, cls: 'wa-cur' })
      : `<a href="${esc(view_href)}" aria-current="page">${esc(pw.current_view)}</a>`;
    const loc = F.locator.length && ['loop', 'reform', 'register'].includes(spec.view) ? locator({ A, filled: F.locator, href: theme_for ? `#${pid}-main` : '/atlas' }) : '';
    const main = fn({ pid, P: pw.page, A, F, panels, spec, width });
    const inner = `<a class="ws-skip" href="#${pid}-main">${esc(site.skip)}</a>${head}`
      + title_bar({ pid, A, M, current: pw.current_view, cur_val: record_page ? 'true' : 'page', open })
      + (pw.crumbs ? breadcrumb({ A, crumbs: pw.crumbs, own, loc }) : '')
      + `<main id="${pid}-main" class="ws-main" tabindex="-1">${main}</main>`
      + footer(site).replace(/\{pid\}/g, pid);
    const style = vh ? ` style="--ws-vh:${vh}px"` : '';
    return `<div class="ws wa" id="${pid}"${theme_for ? ` data-oa-theme="${theme}"` : ''}${style} data-oa-application="${esc(spec.id)}"`
      + ` data-atlas-view="${esc(spec.view)}"${spec.record ? ` data-atlas-record="${esc(spec.record)}"` : ''} data-atlas-model="${esc(M.sha256)}"><div class="ws-in">${inner}</div></div>`;
  };
  const comp = ['id-chip', 'disclosure', 'loop-stepper', 'choice', 'toggle', 'filter-bar'].map((c) => component_css(c)).join('\n');
  const syms = [...UTILITY_SPRITE, 'oa-sym-u-chevron-24px', 'oa-sym-u-play-24px', 'oa-sym-u-pause-24px', 'oa-sym-u-reset-24px', 'oa-sym-u-arrow-24px'];
  const js = (n) => fs.readFileSync(path.join(CODE, `c-18-${n}.js`), 'utf8');
  const own_css = comp + '\n' + atlas_css(F.figure_css);
  return {
    id: spec.id, type, page: spec.view, part: 'page', title: pw.title, words_from: AWd.__from,
    // the working page's style: the website's, then chapter 18's components and the atlas's own rules
    css: site_css() + '\n' + masthead_css() + '\n' + switch_css() + '\n' + own_css,
    // in the guide the website's style is already in the head (plates/web-site.css); the atlas plate carries its own
    plate_css: own_css, styles: ['web-site'],
    export_css: res_switch_css(), kit_css: '', sprite: sprite([...new Set(syms)]),
    body, widths: spec.widths, views: spec.views,
    scripts: { head: switch_head_js(), tail: [masthead_js(), switch_js(), close_on_widen_js(NAV_BP), js('disclosure'), js('loop-stepper')].join('\n') },
    // contract C4 and C9: the plate's words are chapter 21's entry for this page and chapter 20's site words
    words_records: [{ generator: GEN, id: spec.id }, { generator: SITE_GEN, id: 'A06:site' }],
    atlas: { model: M.sha256, view: spec.view, record: spec.record || null },
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}
