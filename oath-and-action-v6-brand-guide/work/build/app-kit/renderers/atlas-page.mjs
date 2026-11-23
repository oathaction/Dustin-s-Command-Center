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
export const code_inputs = () => ['work/build/app-kit/tools/atlas_figures.py', 'work/build/app-kit/tools/atlas_test.py', 'work/build/app-kit/tools/atlas_contrast.py'];
export const GEN = 'work/build/scripts/phase-4/phase4_ch21_build.py';
const SITE_GEN = 'work/build/scripts/phase-4/phase4_ch20_build.py';
const FIGURES = 'work/build/app-kit/tools/atlas_figures.py';
const BP = { phone: 24.375, tablet: 48, desktop: 64, wide: 90 };   // chapter 07's breakpoints, in em, as the website's
const NAV_BP = 64;
const at = (em, body) => `@container ws (min-width: ${em}em){${body}}`;
const under = (em, body) => `@container ws (max-width: ${em - 0.001}em){${body}}`;
const MINUS = '−';
const NUMW = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'];
const nword = (n) => (n >= 0 && n < 10 ? NUMW[n] : String(n));   // house rule H06: one to nine in words in prose

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
// a word the generator does not print yet: drawn as ⟦key⟧, listed in the log, and failed by the atlas test (T16), so a
// view can be drawn and checked for layout while the editor writes, and never ships with a gap
// chapter 18's icons by the guide's sprite, each keeping the turn its source drawing gives its path (the stepper's
// Previous step draws the arrow mirrored, transform="matrix(-1 0 0 1 24 0)"; the sprite's symbol points right)
const sprite_icons_turned = (html) => sprite_icons(html.replace(/(<svg\b[^>]*\bdata-icon="U-[a-z-]+"[^>]*>)([\s\S]*?)(<\/svg>)/g, (m, open, inner, close) => {
  const t = (inner.match(/\stransform="([^"]+)"/) || [])[1];
  return t ? `${open.replace('<svg', `<svg data-turn="${t}"`)}${inner}${close}` : m;
})).replace(/<svg data-turn="([^"]+)"([^>]*)>(<use [^>]*?)\/>/g, '<svg$2>$3 transform="$1"/>');
export const MISSING = new Set();
const wd = (o, k, where) => (o && o[k] != null ? o[k] : (MISSING.add(`${where}.${k}`), `⟦${k}⟧`));
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
  // the stored text's straight marks set as the typographer's pair: an opening mark at a word's start, else a closing one
  const t = esc(text).replace(/(^|[\s(“—])'/g, '$1‘').replace(/'/g, '’');
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
const CHECK = () => sprite_icons(fs.readFileSync(path.join(CODE, 'c-18-toggle.html'), 'utf8').match(/<svg\s+class="oa-toggle-check"[\s\S]*?<\/svg>/)[0]).replace(/\s*\n\s*/g, ' ');
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
// specs 14.1: the section band, Charcoal across the content width, the section's h2 and its lede
const sband = (h2id, h2, lede) => `<div class="ws-g"><div class="wa-sband oa-surface-charcoal ws-panel"><h2 class="ws-h2" id="${h2id}">${esc(h2)}</h2>`
  + (lede ? `<div class="wa-lede">${lede}</div>` : '') + `</div></div>`;
const bsec = (key, h2id, h2, lede, body, extra = '') => `<section class="wa-sec wa-bsec" data-oa-section="${esc(key)}" aria-labelledby="${h2id}"${extra}>${sband(h2id, h2, lede)}${body}</section>`;
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
    + `<span class="n">${link_chip('Route', x.code, I)} ${esc(x.name || '')}</span><span>${esc(x.who)}</span><span data-feasibility="${esc(x.feasibility)}">${esc((A.feasibility || {})[x.feasibility] || wd({}, `feasibility.${x.feasibility}`, 'ATLAS'))}</span>`
    + (x.note ? `<span class="wa-stored" data-atlas-field="note">${stored(x.note, I)}</span>` : '')
    + `<span class="d">${x.checked ? esc(fill(A.checked, { date: x.checked_words })) : esc(A.not_checked)}</span></li>`).join('') + `</ul>`;
}

// ---------------------------------------------------------------------------------------------------------------- loop
function view_loop({ pid, P, A, F, panels, spec }) {
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
    + `<div class="wa-wide48"><dt>${esc(P.facts.closure)}</dt><dd class="wa-stored" data-atlas-field="closure">${stored(lp.closure, I)}</dd></div>`
    + `<div><dt>${esc(P.facts.delay)}</dt><dd>${lp.delay && lp.delay.ticks ? ticks(lp.delay.ticks) + ' ' + esc(lp.delay.words) : ''}</dd></div>`
    + (weak ? `<div><dt>${esc(P.facts.weakest)}</dt><dd>${sc(weak)} ${esc(weak.grade.word)}</dd></div>` : '')
    + `</dl></div>`;
  const head = `<div class="ws-g wa-head"><div class="wa-op"><p class="ws-kick">${chip('Loop', lp.id)}<span class="d" aria-hidden="true">·</span><span class="b">${esc(fill(P.kind, { kind: kind_word }))}</span></p>`
    + `<h1 class="ws-h1 wa-t1" id="${pid}-h1">${quoted_title(lp.title)}</h1><p class="ws-intro wa-gl">${gl}</p>`
    + `<p class="wa-cap wa-narrow48"><span class="wa-stored" data-atlas-field="closure">${stored(lp.closure, I)}</span></p></div>${facts}</div>`;
  // the read-aloud line (the data lead's R4): each variable's chip with its direction, each connection's chip with its
  // sign's word, in the order the loop runs; its marks name the directions for the atlas test (T4)
  // the editor's templates (DD-11C-6): read_start, read_step for each connection, then read_end_same or read_end_other by
  // the direction the loop comes back in; dirs gives the words for rises and falls
  const toks = v.reads.split(' ');
  const dirw = (d) => esc((P.dirs || {})[d === 'rises' ? 'up' : 'down'] || d);
  const vtitle = (id) => (v.variables.find((x) => x.id === id) || {}).title || '';
  const vchip = (t) => { const id = t.split(':')[0]; const tt = vtitle(id); return `${link_chip('Variable', id, I)} ${esc(tt.charAt(0).toLowerCase() + tt.slice(1))}`; };
  let line = fill_html(wd(P, 'read_start', 'A14'), { var: vchip(toks[0]) });
  for (let i = 1; i < toks.length; i += 2) {
    const st = steps.find((x) => x.id === toks[i]);
    line += ' ' + fill_html(wd(P, 'read_step', 'A14'), { conn: link_chip('Connection', toks[i], I), sign: esc(A.signs[st.sign]), var: vchip(toks[i + 1]), dir: dirw(toks[i + 1].split(':')[1]) });
  }
  line += ' ' + esc(wd(P, toks[toks.length - 1].endsWith(':rises') ? 'read_end_same' : 'read_end_other', 'A14'));
  const read = `<div class="wa-read" data-oa-part="read"><p class="lab">${esc(P.read_label)}</p><p class="ws-p" data-atlas-reads="${esc(v.reads)}">${line}</p>`
    + `<p class="wa-small">${count(v.minus, `loop:${lp.id}:minus`, esc(fill(even ? P.parity_even : P.parity_odd, { n: nword(v.minus) })))}</p></div>`;
  // the drawing, chapter 15's loop by the figure step, with the other reforms' ink tags under it (Rule 21.5)
  const tags_for = (rid) => {
    const others = v.offered.filter((r) => r.id !== rid).map((r) => r.id);
    return steps.map((s) => [s, others.filter((o) => v.offered.find((r) => r.id === o).targets.includes(s.id))]).filter(([, rs]) => rs.length)
      .map(([s, rs]) => `<li class="wa-tag">${sc(s)} ${fill_html(rs.length === 1 ? wd(P, 'also_aim_one', 'A14') : P.also_aim, { chips: rs.map((r) => chip('Reform', r)).join(' and ') })}</li>`).join('');
  };
  const listw = (xs) => (xs.length < 2 ? xs.join('') : xs.slice(0, -1).join(', ') + ' and ' + xs[xs.length - 1]);
  const acts_for = (r) => {
    const on = r.targets.filter((t) => steps.some((s) => s.id === t) || v.variables.some((x) => x.id === t));
    const off = r.targets.filter((t) => !on.includes(t));
    const ch = (t) => (steps.some((s) => s.id === t) || I[t].kinds.includes('Connection') && !I[t].kinds.includes('Variable') ? link_chip('Connection', t, I) : link_chip('Variable', t, I));
    if (!on.length) return `<p class="wa-small wa-acts">${fill_html(wd(P, 'chosen_none', 'A14'), { reform: chip('Reform', r.id), off: listw(off.map(ch)) })}</p>`;
    return `<p class="wa-small wa-acts">${fill_html(wd(P, 'chosen_note', 'A14'), { reform: chip('Reform', r.id), targets: listw(on.map(ch)) })}`
      + (off.length ? ` ${fill_html(wd(P, 'chosen_off', 'A14'), { off: listw(off.map(ch)) })}` : '') + `</p>`;
  };
  const tags = v.offered.map((r) => `<div class="wa-fv${r.id === v.chosen ? ' wa-fv--on' : ''}" data-atlas-for="${esc(r.id)}">${acts_for(r)}<ul class="wa-tags">${tags_for(r.id)}</ul></div>`).join('');
  // E11c-2: one drawing a reform the chooser offers, the chosen one shown in the markup, the checked radio's shown by CSS
  const figs = v.offered.map((r) => `<div class="wa-fv${r.id === v.chosen ? ' wa-fv--on' : ''}" data-atlas-for="${esc(r.id)}">${v.figures[r.id]}</div>`).join('');
  const drawing = `<div class="wa-draw" data-oa-part="drawing"><figure class="wa-fig">${figs}</figure>`
    + (weak ? `<p class="wa-small wa-weak">${sc(weak)} ${esc(P.weakest_line)}</p>` : '') + `<div class="wa-tagsets">${tags}</div></div>`;
  // the stepper, chapter 18's code set read from its files (Rule 21.13; AL-22, AL-24)
  if (P.steps.length !== steps.length) throw new Error(`the loop page's words hold ${P.steps.length} stepper lines for ${steps.length} steps (contract C9)`);
  const src = fs.readFileSync(path.join(CODE, 'c-18-loop-stepper.html'), 'utf8');
  const controls = sprite_icons_turned(src.match(/<div\s+class="oa-stepper-controls"[\s\S]*?<\/button>\s*<\/div>/)[0]).replace(/\s*\n\s*/g, ' ')
    .replace('aria-label="Steps of the loop"', `aria-label="${esc(fill(P.stepper_group || 'Steps of Loop {id}', { id: lp.id }))}"`)
    .replace(/aria-describedby="oa-stepper-why"/g, `aria-describedby="${pid}-why"`);
  const why = src.match(/<p class="oa-stepper-why"[\s\S]*?<\/p>/)[0].replace(/\s*\n\s*/g, ' ').replace('id="oa-stepper-why"', `id="${pid}-why"`);
  const items = P.steps.map((st, i) => `<li class="oa-stepper-step" data-oa-hold="${esc(st.hold)}" data-atlas-kind="Connection" data-atlas-id="${esc(steps[i].id)}"`
    + ` data-sign="${esc(steps[i].sign)}" data-type="${esc(steps[i].type)}" data-delay="${esc(steps[i].delay.key)}" data-grade="${esc(steps[i].grade.key)}"`
    + `${steps[i].id === v.weakest ? ' data-weakest="true"' : ''}><span class="oa-stepper-line">${stored(st.line, I)}</span>&#32;<span class="oa-stepper-more">${st.more ? stored(st.more, I) : ''}</span></li>`).join('');
  const ready = wd(P, 'stepper_ready', 'A14');
  const at_ = spec.step ? Math.min(spec.step, steps.length) : 0;
  let items_ = items, controls_ = controls, status_ = esc(ready);
  if (at_) {
    // chapter 18's script's state after `at_` presses of Next step: the current step marked, the steps ahead marked, the
    // status line saying the step, Next step unavailable at the last step and Previous step and Reset the loop available
    let k = 0;
    items_ = items.replace(/<li class="oa-stepper-step"/g, (m) => { k += 1; return m + (k === at_ ? ' aria-current="step"' : '') + (k > at_ ? ' data-oa-ahead' : ''); });
    const st = P.steps[at_ - 1];
    status_ = stored(`Step ${at_} of ${steps.length}: ${st.line}${st.more ? ' ' + st.more : ''}`, I);
    controls_ = controls.replace(/(<button[^>]*class="oa-stepper-(?:prev|reset)")([^>]*?)\saria-disabled="true"/g, '$1$2');
    if (at_ === steps.length) controls_ = controls_.replace(/(<button[^>]*class="oa-stepper-next")/, '$1 aria-disabled="true"');
  }
  const stepper = `<div class="oa-stepper wa-stepper" data-oa-stepper data-oa-part="stepper"${at_ ? ` data-oa-at="${at_}"` : ''}><p class="oa-stepper-status" role="status" data-oa-ready="${esc(ready)}">${status_}</p>`
    + controls_ + why + `<ol class="oa-stepper-steps" role="list">${items_}</ol></div>`;
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
  const ev = `<ul class="wa-ev">` + steps.map((s, i) => `<li data-oa-part="row${low(s.id)}" data-atlas-kind="Connection" data-atlas-id="${esc(s.id)}" data-sign="${esc(s.sign)}" data-type="${esc(s.type)}" data-delay="${esc(s.delay.key)}" data-grade="${esc(s.grade.key)}">`
    + `<span class="st">${esc(fill(P.step_word, { n: i + 1 }))}</span>${sc(s)}<span class="gr">${F.grade_samples[s.grade.key] || ''} <span class="ws-nb">${s.grade.key === 'documented' ? F.record_square : ''}${esc(s.grade.word)}</span></span>`
    + `<span class="ct wa-stored" data-atlas-field="citation">${stored(s.citation, I)}</span></li>`).join('') + `</ul>`
;
  const recs_line = `<p><a href="/atlas/register?loop=${low(lp.id)}">${count(lp.records.length, `loop:${lp.id}:records`, esc(fill(P.records_line, { n: lp.records.length })))}</a></p>`;
  return sec('Loop', null, null, head, ` aria-labelledby="${pid}-h1"`)
    + bsec('Stepper', `${pid}-s2`, P.stepper_heading, `<p>${esc(P.arithmetic)}</p>`, sec2)
    + bsec('Record', `${pid}-s3`, P.record_heading, `<p>${esc(wd(P, 'record_lede', 'A14'))}</p>`, `<div class="ws-g"><div class="wa-col7">${rec}</div></div>`)
    + bsec('Evidence', `${pid}-s4`, P.evidence_heading, recs_line, `<div class="ws-g"><div class="wa-col8">${ev}</div></div>`);
}

// ---------------------------------------------------------------------------------------------------------------- reform
function view_reform({ pid, P, A, F, panels, spec }) {
  const v = F.view, r = v.reform, I = F.ids;
  need(P, ['status_label', 'problem', 'remedy', 'where_heading', 'where_note', 'touches', 'aims_here', 'grades_heading', 'source_link', 'effects_heading',
    'effects_confidence', 'routes_heading', 'routes_head', 'complements_heading', 'sources_summary'], 'the reform page');
  const band = (A.bands && A.bands[r.band]) || r.band;
  const gw = (g) => `<b>${esc(g.word)}</b>`;
  const status = `<div class="wa-facts${panels.includes('Reform') ? ' oa-surface-charcoal ws-panel' : ''}" data-oa-part="status"><p class="lab">${esc(P.status_label)}</p>`
    + `<p class="wa-small" data-status-date="${esc(r.status.checked)}" data-atlas-reform="${esc(r.id)}">${esc(fill(A.as_of, { date: r.status.checked_words }))}</p>`
    + `<p class="wa-small wa-stored wa-wide48" data-atlas-field="status">${stored(r.status.text, I)}</p>`
    + `<dl><div><dt>${esc(P.problem)}</dt><dd><a href="#${pid}-problem">${gw(r.problem.grade)}</a></dd></div><div><dt>${esc(P.remedy)}</dt><dd><a href="#${pid}-remedy">${gw(r.remedy.grade)}</a></dd></div></dl>`
    + `<p class="wa-cap wa-wide48">${esc(r.band_words || '')}</p></div>`
    + `<div class="wa-narrow48 wa-after"><p class="wa-small wa-stored" data-atlas-field="status">${stored(r.status.text, I)}</p><p class="wa-cap">${esc(r.band_words || '')}</p></div>`;
  const head = `<div class="ws-g wa-head"><div class="wa-op"><p class="ws-kick">${chip('Reform', r.id)}<span class="d" aria-hidden="true">·</span><span class="b">${esc(band)}</span></p>`
    + `<h1 class="ws-h1 wa-t1" id="${pid}-h1">${esc(r.title)}</h1><p class="ws-intro wa-stored" data-atlas-field="summary">${stored(r.summary, I)}</p></div>${status}</div>`;
  // where it acts: the figure step's drawing of the targets, red, with the other reforms' ink tags (Rules 12.5, 21.5)
  const tv = v.targets.filter((t) => 'part' in t);
  const tags = Object.entries(v.tags).filter(([, rs]) => rs.length).map(([t, rs]) => `<li class="wa-tag"><span class="ws-nb">${link_chip('Variable', t, I)}:</span> ${rs.map((x) => chip('Reform', x, { href: PATHS.Reform(x) })).join(' ')} ${esc(rs.length === 1 ? wd(P, 'aims_here_one', 'A12') : P.aims_here)}</li>`).join('');
  const targets_words = tv.map((t) => `${link_chip('Variable', t.id, I)} “${esc(t.title)}”`).join(' and ');
  const note = `<div class="wa-note"><p class="wa-small">${fill_html(P.where_note, { reform: chip('Reform', r.id), targets: targets_words })}</p>`
    + tv.map((t) => `<p class="wa-small">${link_chip('Variable', t.id, I)} <span class="wa-stored" data-atlas-field="increase_means">${stored(t.increase_means, I)}</span></p>`).join('')
    + v.between.filter((c) => !r.targets.includes(c.id)).map((c) => `<p class="wa-small" data-atlas-kind="Connection" data-atlas-id="${esc(c.id)}">${fill_html(wd(P, 'conn_note', 'A12'), {
      conn: link_chip('Connection', c.id, I), name: `<span class="wa-stored" data-atlas-field="name">${esc(c.name)}</span>`, sign: esc(A.signs[c.sign]), delay: esc(A.delays[c.delay.key]),
      grade: `<span class="ws-nb">${c.grade.key === 'documented' ? F.record_square : ''}${esc(c.grade.word)}</span>` })}</p>`).join('')
    + v.loops_named.filter((l) => !l.drawn).map((l) => `<p class="wa-small">${fill_html(P.touches, { loop: link_chip('Loop', l.id, I) })}</p>`).join('') + `</div>`;
  const where = `<div class="ws-g wa-where" data-oa-part="targets"><div class="wa-draw"><h2 class="ws-h3">${esc(P.where_heading)}</h2>`
    + (v.figure ? `<figure class="wa-fig">${v.figure.svg}</figure>` : '') + (tags ? `<ul class="wa-tags">${tags}</ul>` : '') + `</div>${note}</div>`;
  // the two grades apart (Rule 15.12), the contested remedy's two readings side by side (H08), split where the content
  // file says (remedy_split, the sentence of the stored text that opens the second reading)
  // the data lead's R15: the stored text split at the start of the sentence remedy_split names, by the one splitter the
  // kit and the test share (System 1's sentences(), through the figure step), rejoining to the stored text whole
  const sents = r.remedy.sentences;
  const k = (spec.remedy_split || 0) - 1;
  const readings = k > 0 && k < sents.length ? [sents.slice(0, k).join(' '), sents.slice(k).join(' ')] : [r.remedy.text];
  if (readings.some((x) => !x)) throw new Error('remedy_split leaves a reading empty (the specs, section 9)');
  const src_of = v.sources.map((s) => s.id);
  const rhead = (lbl, g, id) => `<div class="wa-gh" id="${id}"><p class="lab">${esc(lbl)}</p><p class="wa-gw">${esc(g.word)}</p><p class="wa-small">${esc(g.gloss)}</p></div>`;
  const reading_src = (i) => (src_of[i + 1] ? ` <a class="wa-srcl" href="#${pid}-source-${low(src_of[i + 1])}">${esc(P.source_link)}</a>` : '');
  const grades = `<div class="ws-g wa-grade">${rhead(P.problem, r.problem.grade, `${pid}-problem`)}<div class="wa-rd">${quote(stored(r.problem.text, I), 'problem')}</div></div>`
    + `<div class="ws-g wa-grade wa-remedy">${rhead(P.remedy, r.remedy.grade, `${pid}-remedy`)}`
    + readings.map((x, i) => `<div class="wa-rd" data-reading="${i + 1}" data-split="${esc(spec.remedy_split || '')}" data-atlas-reform="${esc(r.id)}">${quote(stored(x, I) + reading_src(i), 'remedy')}</div>`).join('') + `</div>`;
  const effects_lede = `<p data-status-date="${esc(r.status.checked)}" data-atlas-reform="${esc(r.id)}">${esc(fill(A.as_of, { date: r.status.checked_words }))}</p>`
    + `<p>${esc(fill(P.effects_confidence, { text: r.effects_confidence }))}</p>`;
  const effects = effect_rows(r, F);
  const routes = route_rows(r, A, I);
  const routes_lede = `<p>${esc(P.complements_heading)}: ` + v.complements.map((c) => `${link_chip('Reform', c.id, I)} “${esc(c.title)}”`).join('; ') + `</p>`;
  const srcs = `<details class="oa-disclosure wa-src"><summary class="oa-disclosure-summary"><span class="oa-disclosure-label">${esc(P.sources_summary)}</span>${CHEV()}</summary>`
    + `<div class="oa-disclosure-body"><ul>` + v.sources.map((s) => `<li id="${pid}-source-${low(s.id)}" class="wa-small">${esc([s.publisher, s.title, s.year].filter(Boolean).join(', '))}${s.url ? `, <span class="ws-nb">${esc(s.url)}</span>` : ''}</li>`).join('')
    + `</ul></div></details>`;
  return sec('Reform', null, null, head + where, ` aria-labelledby="${pid}-h1"`)
    + bsec('Grades', `${pid}-s2`, P.grades_heading, `<p>${esc(wd(P, 'grades_lede', 'A12'))}</p>`, grades, ' data-oa-part="grades"')
    + bsec('Effects', `${pid}-s3`, P.effects_heading, effects_lede, `<div class="ws-g"><div class="wa-col8">${effects}</div></div>`, ' data-oa-part="effects"')
    + bsec('Routes', `${pid}-s4`, P.routes_heading, routes_lede, `<div class="ws-g"><div class="wa-col8">${routes}</div></div>`, ' data-oa-part="routes"')
    + sec('Sources', null, null, `<div class="ws-g"><div class="wa-col8">${srcs}</div></div>`);
}

// ---------------------------------------------------------------------------------------------------------------- tables
// Rule 18.10's table, chapter 18's classes and roles, so a container can restyle it as cards and keep its semantics
const th = (x, cls = '') => `<th class="oa-table-th oa-table-th--plain${cls ? ' ' + cls : ''}" role="columnheader" scope="col">${x}</th>`;
const td = (x, label, cls = '') => `<td class="oa-table-td${cls ? ' ' + cls : ''}" role="cell"${label ? ` data-k="${esc(label)}"` : ''}>${x}</td>`;
const table = (cls, head, rows, extra = '') => `<table class="oa-table-grid ${cls}" role="table"${extra}><thead class="oa-table-thead" role="rowgroup"><tr class="oa-table-row" role="row">${head}</tr></thead>`
  + `<tbody role="rowgroup">${rows}</tbody></table>`;
const GRADES = ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis'];

// ---------------------------------------------------------------------------------------------------------------- register
function sign_mark(s, F) { return s.sign === 'none' ? (F.view.marks_authority || '') : ''; }
function view_register({ pid, P, A, F, panels, spec }) {
  const v = F.view, I = F.ids, S = v.sheet;
  const gw = (g) => esc(A.grades[g] || g);
  const ih = P.index_head || [];
  const head = th(esc(wd(ih, 0, 'A13.index_head'))) + [1, 2, 3, 4, 5].map((i) => th(esc(wd(ih, i, 'A13.index_head')), 'n')).join('')
    + GRADES.map((g) => th(`<span class="wa-gs">${F.grade_samples[g]}</span>${g === 'documented' ? `<span class="ws-nb">${F.record_square}${gw(g)}</span>` : gw(g)}`, 'n g')).join('');
  const cnt = (n, key) => count(n, key, String(n));
  const rows = v.rows.map((r) => `<tr class="oa-table-row" role="row"><th class="oa-table-th wa-rh" role="rowheader" scope="row">`
    + (r.domain ? `${link_chip('Domain', r.id, I)} ${esc(r.title)}` : esc(r.title)) + `</th>`
    + td(cnt(r.variables, `sheet:${r.id}:variables`), ih[1], 'n') + td(cnt(r.connections, `sheet:${r.id}:connections`), ih[2], 'n')
    + td(cnt(r.loops, `sheet:${r.id}:loops`), ih[3], 'n') + td(cnt(r.reforms, `sheet:${r.id}:reforms`), ih[4], 'n')
    + td(r.issues == null ? count(0, `sheet:${r.id}:issues`, esc(wd(P, 'none_filed', 'A13'))) : cnt(r.issues, `sheet:${r.id}:issues`), ih[5], 'n')
    + GRADES.map((g) => td(cnt(r.grades[g], `sheet:${r.id}:grade:${g}`), A.grades[g], 'n')).join('') + `</tr>`).join('');
  const W_ = v.whole;
  const whole = `<tr class="oa-table-row wa-whole" role="row"><th class="oa-table-th wa-rh" role="rowheader" scope="row">${esc(wd(P, 'whole', 'A13'))}</th>`
    + td(cnt(W_.variables, 'atlas:variables'), ih[1], 'n') + td(cnt(W_.connections, 'atlas:connections'), ih[2], 'n')
    + td(cnt(W_.loops, 'atlas:loops-numbered'), ih[3], 'n') + td(cnt(W_.reforms, 'atlas:reforms-active'), ih[4], 'n')
    + td(fill_html(wd(P, 'whole_issues', 'A13'), { n: cnt(W_.issues, 'atlas:issues'), retired: esc(nword(W_.retired)) }), ih[5], 'n')
    + GRADES.map((g) => td(cnt(W_.grades[g], `atlas:grade:${g}`), A.grades[g], 'n')).join('') + `</tr>`;
  const key = `<ul class="wa-gkey${panels.includes('Index') ? ' oa-surface-charcoal ws-panel' : ''}">` + GRADES.map((g) => `<li>${F.grade_samples[g]} <span class="ws-nb">${g === 'documented' ? F.record_square : ''}${gw(g)}</span></li>`).join('') + `</ul>`;
  const index = `<div class="ws-g wa-head"><div class="wa-op"><h1 class="ws-h1 wa-t1" id="${pid}-h1">${esc(wd(P, 'h1', 'A13'))}</h1><p class="ws-intro">${esc(wd(P, 'intro', 'A13'))}</p></div></div>`
    + `<div class="ws-g"><div class="wa-col12 wa-tablewrap" data-oa-part="index">${key}`
    + table(`wa-index${panels.includes('Index') ? ' wa-headon' : ''}`, head, rows + whole) + `<p class="wa-cap">${esc(wd(P, 'whole_note', 'A13'))}</p></div></div>`;
  // the open sheet: its band, its variables, its connections, one line each with its own address (Rule 21.9)
  const band = `<div class="wa-band${panels.includes('Sheet') ? ' oa-surface-charcoal ws-panel' : ''}"><h2 class="ws-h2 wa-bh" id="${pid}-s2">${S.domain ? link_chip('Domain', S.id, I) + ' ' : ''}${esc(S.title)}</h2>`
    + (S.question ? `<p class="lab">${esc(wd(P, 'sheet_question_label', 'A13'))}</p><p class="ws-intro wa-stored" data-atlas-field="everyday_question">${esc(S.question)}</p>` : '') + `</div>`;
  const vars = `<h3 class="ws-h3">${esc(wd(P, 'variables_heading', 'A13'))}</h3><ul class="wa-vars">` + S.variables.map((x) => `<li id="${pid === 'site' ? '' : pid + '-'}variable-${low(x.id)}" data-atlas-kind="Variable" data-atlas-id="${esc(x.id)}">`
    + `${chip('Variable', x.id)} <b>${esc(x.title)}</b><span class="wa-small wa-stored" data-atlas-field="increase_means">${stored(x.increase_means, I)}</span></li>`).join('') + `</ul>`;
  const ch = P.conn_head || [];
  const chead = [0, 1, 2, 3, 4, 5, 6].map((i) => th(esc(wd(ch, i, 'A13.conn_head')))).join('');
  const crow = (c) => `<tr class="oa-table-row" role="row" id="${pid === 'site' ? '' : pid + '-'}register-${low(c.id)}" data-oa-part="row${low(c.id)}" data-atlas-kind="Connection" data-atlas-id="${esc(c.id)}" data-sign="${esc(c.sign)}" data-type="${esc(c.type)}" data-delay="${esc(c.delay.key)}" data-grade="${esc(c.grade.key)}">`
    + `<th class="oa-table-th wa-rh" role="rowheader" scope="row">${chip('Connection', c.id, { href: `#${pid === 'site' ? '' : pid + '-'}register-${low(c.id)}`, evidence: true })}</th>`
    + td(`${link_chip('Variable', c.from, I)} ${esc(c.from_title)} <span class="wa-to">${esc(wd(P, 'to', 'A13'))}</span> ${link_chip('Variable', c.to, I)} ${esc(c.to_title)}`, ch[1])
    + td(`${F.sign_samples[c.sign] || ''} ${esc(A.signs[c.sign])}`, ch[2])
    + td(esc(A.types ? A.types[c.type] || c.type : c.type), ch[3])
    + td(`${F.tick_samples[c.delay.key] || ''} ${esc(A.delays[c.delay.key])}`, ch[4])
    + td(`<span class="wa-gs">${F.grade_samples[c.grade.key]}</span> <span class="ws-nb">${c.grade.key === 'documented' ? F.record_square : ''}${esc(c.grade.word)}</span>`, ch[5])
    + td(`<span class="wa-stored" data-atlas-field="citation">${stored(c.citation, I)}</span>`, ch[6]) + `</tr>`;
  const conns = `<h3 class="ws-h3">${esc(wd(P, 'connections_heading', 'A13'))}</h3>` + table('wa-conns', chead, S.connections.map(crow).join(''));
  const sheet = `<div class="ws-g"><div class="wa-col12" data-oa-part="sheet">${band}<div class="wa-col8in">${vars}</div>${conns}</div></div>`;
  // what the atlas set aside: the rejected option under its stored title (DD-11C-1) and the reviewed connections (Rule 21.10)
  const rej = S.rejected.map((r) => {
    const label = /^Rejected option/.test(r.title) ? '' : `<p class="lab">${esc(wd(P, 'rejected_heading', 'A13'))}</p>`;
    const tg = (r.targets || []).map((t) => (I[t] && I[t].kinds.includes('Variable') ? link_chip('Variable', t, I) : link_chip('Connection', t, I)));
    const tl = tg.length < 2 ? tg.join('') : tg.slice(0, -1).join(', ') + ' and ' + tg[tg.length - 1];
    return `<div class="wa-rej" data-oa-part="rejected">${label}<h3 class="ws-h3">${link_chip('Reform', r.id, I)} ${esc(r.title)}</h3>`
      + (tg.length ? `<p class="wa-small">${fill_html(wd(P, 'rejected_targets', 'A13'), { targets: tl })}</p>` : '')
      + (r.status && r.status.checked ? `<p class="wa-small" data-status-date="${esc(r.status.checked)}" data-atlas-reform="${esc(r.id)}">${esc(fill(A.as_of, { date: r.status.checked_words }))}</p>` : '')
      + effect_rows(r, F)
      + `<dl class="wa-dl"><div><dt>${esc(wd(P, 'problem', 'A13'))}</dt><dd><b>${esc(r.problem.grade.word)}</b>, ${esc(r.problem.grade.gloss)}</dd></div>`
      + `<div><dt>${esc(wd(P, 'remedy', 'A13'))}</dt><dd><b>${esc(r.remedy.grade.word)}</b>, ${esc(r.remedy.grade.gloss)}. ${esc(wd(P, 'rejected_grade', 'A13'))}.</dd></div></dl>`
      + quote(stored(r.remedy.text, I), 'remedy') + route_rows(r, A, I) + `</div>`;
  }).join('');
  const reviewed = S.reviewed.length ? `<div class="wa-rev" data-oa-part="rejected"><h3 class="ws-h3">${esc(wd(P, 'reviewed_heading', 'A13'))}</h3><ul class="wa-revl">`
    + S.reviewed.map((x) => `<li><p class="wa-small">${esc(fill(wd(P, 'reviewed_word', 'A13'), { id: x.id }))}: ${link_chip('Variable', x.from, I)} ${esc(x.from_title)} ${esc(wd(P, 'to', 'A13'))} ${link_chip('Variable', x.to, I)} ${esc(x.to_title)}</p>`
      + quote(stored(x.reason, I), 'reason') + `</li>`).join('') + `</ul></div>` : '';
  const set_aside = rej || reviewed ? bsec('Rejected', `${pid}-s3`, wd(P, 'rejected_section', 'A13'), `<p>${esc(wd(P, 'rejected_lede', 'A13'))}</p>`, `<div class="ws-g"><div class="wa-col8">${rej}${reviewed}</div></div>`) : '';
  // its issue records behind chapter 18's filter bar (Rule 21.11): one chip a variable, each with its count
  const fsrc = fs.readFileSync(path.join(CODE, 'c-18-filter-bar.html'), 'utf8');
  const fbtn = sprite_icons(fsrc.match(/<button\s+type="button"\s+class="oa-filters-toggle"[\s\S]*?<\/button>/)[0]).replace(/\s*\n\s*/g, ' ')
    .replace('aria-controls="oa-filters-sheet"', `aria-controls="${pid}-fsheet"`).replace('aria-expanded="false"', `aria-expanded="${spec.filters_open ? 'true' : 'false'}"`)
    .replace(/>Filters, 0 on</, `>${esc(fill(wd(P, 'filters_on', 'A13'), { n: S.filter.length }))}<`);
  const fcheck = sprite_icons(fsrc.match(/<svg\s+class="oa-filters-check"[\s\S]*?<\/svg>/)[0]).replace(/\s*\n\s*/g, ' ');
  const chips_ = S.variables.map((x) => `<button type="button" class="oa-filters-chip" aria-pressed="${S.filter.includes(x.id)}" data-oa-filter="${esc(x.id)}" data-atlas-filter="${esc(x.id)}">${fcheck}`
    + `<span class="oa-filters-word">${chip('Variable', x.id)} ${esc(x.title)} ${count(S.filter_counts[x.id], `records-naming:${S.id}:${x.id}`, `(${S.filter_counts[x.id]})`)}</span></button>`).join('');
  const shown = S.records.filter((r) => r.shown).length;
  const recs = S.records.map((r) => `<li class="oa-filters-result" data-oa-var="${esc(r.nodes.join(' '))}" id="${pid}-issue-${low(r.id)}"${r.shown ? '' : ' hidden'}>`
    + `${chip('Issue', r.id)} <span class="wa-stored" data-atlas-field="title">${esc(r.title)}</span> <span class="wa-rg">${esc(r.grade.word)}</span></li>`).join('');
  const filters = `<div class="oa-filters wa-filters" data-oa-filters><div class="oa-filters-bar">${fbtn}<button type="button" class="oa-filters-clear"${S.filter.length ? '' : ' hidden'}>${esc(wd(P, 'filters_clear', 'A13'))}</button></div>`
    + `<div class="oa-filters-sheet" id="${pid}-fsheet"${spec.filters_open ? '' : ' hidden'}><div class="oa-filters-chips" role="group" aria-label="${esc(wd(P, 'filters', 'A13'))}" data-oa-group="var">${chips_}</div></div>`
    + `<p class="oa-filters-status" role="status" data-oa-noun="${esc(wd(P, 'records_noun', 'A13'))}" data-oa-none="${esc(wd(P, 'records_none', 'A13'))}">`
    + fill_html(wd(P, 'showing', 'A13'), { n: count(shown, `records-shown:${S.id}`, String(shown)), total: count(S.records.length, `sheet:${S.id}:issues`, String(S.records.length)) })
    + `</p><ul class="oa-filters-results wa-recl">${recs}</ul></div>`;
  const records = S.records.length ? bsec('Records', `${pid}-s4`, wd(P, 'records_heading', 'A13'), `<p>${esc(wd(P, 'records_lede', 'A13'))}</p>`, `<div class="ws-g"><div class="wa-col8">${filters}</div></div>`, ' data-oa-part="records"') : '';
  return sec('Index', null, null, index, ` aria-labelledby="${pid}-h1"`) + `<section class="wa-sec" data-oa-section="Sheet" aria-labelledby="${pid}-s2">${sheet}</section>` + set_aside + records;
}

// ---------------------------------------------------------------------------------------------------------------- loop index
function view_loop_index({ pid, P, A, F, panels }) {
  const v = F.view, I = F.ids;
  const h = P.head || [];
  const head = [0, 1, 2, 3, 4, 5].map((i) => th(esc(wd(h, i, 'A15.head')), i === 2 || i === 3 ? 'n' : '')).join('');
  const GKEYS = Object.keys(A.grades).sort((a, b) => b.length - a.length);
  // R18: the display word capitalized at the field's start and after a semicolon, lowercase elsewhere
  const grade_html = (g) => esc(g).replace(new RegExp(`(?<![\\w-])(${GKEYS.map((k) => k.replace(/[-_]/g, (c) => '\\' + c)).join('|')})(?![\\w-])`, 'g'),
    (m, k, at, all) => { const w = A.grades[m] || m; return at === 0 || /;\s*$/.test(all.slice(0, at)) ? esc(w) : esc(w.toLowerCase()); })
    .replace(/\b([A-Z]{1,2}\d+[a-z]?)\b/g, (m) => (I[m] && I[m].kinds.includes('Variable') ? link_chip('Variable', m, I) : m));
  const group = (gr, i) => {
    const word = gr.type === 'R' ? wd(P, 'reinforcing', 'A15') : wd(P, 'balancing', 'A15');
    const rows = gr.loops.map((l) => `<tr class="oa-table-row" role="row"><th class="oa-table-th wa-rh" role="rowheader" scope="row">${link_chip('Loop', l.id, I)}</th>`
      + td(`<span class="wa-stored" data-atlas-field="title">${esc(l.title)}</span>`, h[1])
      + td(l.conceptual ? esc(wd(P, 'no_chain', 'A15')) : count(l.steps, `loop:${l.id}:steps`, String(l.steps)), h[2], 'n')
      + td(l.conceptual ? esc(wd(P, 'no_chain', 'A15')) : count(l.minus, `loop:${l.id}:minus`, String(l.minus)), h[3], 'n')
      + td(`<span class="wa-stored" data-atlas-field="closure">${esc(l.closure)}</span>`, h[4])
      + td(`<span class="wa-grade-words" data-grade-text="${esc(l.evidence)}">${grade_html(l.evidence)}</span>`, h[5]) + `</tr>`).join('');
    const on = i === 0 && panels.includes('Reinforcing');
    const h2 = `${word} (${gr.loops.length})`;
    return bsec(i === 0 ? 'Reinforcing' : 'Balancing', `${pid}-g${i}`, h2, `<p>${esc(wd(P, i === 0 ? 'reinforcing_lede' : 'balancing_lede', 'A15'))}</p>`,
      `<div class="ws-g"><div class="wa-col12 wa-tablewrap">${table('wa-lix', head, rows)}</div>` + (i === 1 ? `<p class="wa-cap wa-col8">${stored(wd(P, 'titles_note', 'A15'), I)}</p>` : '') + `</div>`);
  };
  const top = `<div class="ws-g wa-head"><div class="wa-op"><h1 class="ws-h1 wa-t1" id="${pid}-h1">${esc(wd(P, 'h1', 'A15'))}</h1><p class="ws-intro">${esc(wd(P, 'intro', 'A15'))}</p></div></div>`;
  return top + v.groups.map(group).join('');
}

// ---------------------------------------------------------------------------------------------------------------- how to read
function view_how_to_read({ pid, P, A, F }) {
  const M = F.view.marks;
  const rows = P.rows || [];
  const cell = (k) => ({ sign_up: M.sign_up, sign_down: M.sign_down, authority: M.authority, record_square: M.record_square, hollow: M.hollow, red: M.red,
    ticks_S: M.ticks.S, ticks_M: M.ticks.M, ticks_L: M.ticks.L, ...Object.fromEntries(GRADES.map((g) => [`grade_${g}`, M.grades[g] + (g === 'documented' ? M.record_square : '')])),
    chip: chip('Loop', 'R18'), chip_link: chip('Loop', 'R18', { href: PATHS.Loop('R18') }) }[k] || '');
  const G = P.groups || {}, MK = P.marks || {};
  const LAYOUT = { signs: ['raises', 'lowers', 'type', 'authority'], grades: [...GRADES, 'record_square'], delay: ['S', 'M', 'L'], loops: ['hollow', 'red', 'tag', 'weakest'], every: ['chip', 'pressed'] };
  const CELL = { raises: 'sign_up', lowers: 'sign_down', S: 'ticks_S', M: 'ticks_M', L: 'ticks_L', ...Object.fromEntries(GRADES.map((g) => [g, `grade_${g}`])) };
  const nm_of = (k) => (MK[k] || [k])[0];
  const extra_cells = { type: M.grades['well-supported'], weakest: `<span class="wa-mkc">${M.grades.plausible}<span class="wa-mkw">${esc(nm_of('weakest').toLowerCase())}</span></span>`,
    tag: `${chip('Reform', 'R-48')}`, pressed: `<span class="oa-toggle wa-q wa-qs wa-qon" aria-hidden="true">${CHECK()}<span class="oa-toggle-label">${esc(nm_of('pressed'))}</span></span>`,
    documented: M.grades.documented };
  const sign_note = F.view.sign_note ? `<p class="wa-small wa-stored" data-atlas-field="glossary">${esc(F.view.sign_note)}</p>` : '';
  const groups = Object.entries(LAYOUT).map(([gk, keys], i) => `<div class="ws-g"><h2 class="ws-h2" id="${pid}-m${i}">${esc(wd(G, gk, 'A16.groups'))}</h2></div>` + (`<div class="ws-g"><ul class="wa-marks wa-col12">`
    + keys.map((k) => { const [nm, mean] = MK[k] || [`⟦${k}⟧`, '']; if (!MK[k]) MISSING.add(`A16.marks.${k}`);
      return `<li><span class="wa-mk">${extra_cells[k] || cell(CELL[k] || k)}</span><span><b>${k === 'documented' ? M.record_square : ''}${esc(nm)}</b><span class="wa-small">${stored(mean, F.ids)}</span>${k === 'lowers' ? sign_note : ''}</span></li>`; }).join('') + `</ul></div>`)).join('');
  return `<section class="wa-sec" data-oa-section="Marks" aria-labelledby="${pid}-h1"><div class="wa-hband wa-hband--read oa-surface-charcoal ws-panel"><div class="ws-g"><h1 class="ws-h1 wa-hh" id="${pid}-h1">${esc(wd(P, 'h1', 'A16'))}</h1>`
    + `<p class="ws-p wa-hi">${esc(wd(P, 'intro', 'A16'))}</p></div></div>${groups}</section>`;
}

// ---------------------------------------------------------------------------------------------------------------- home
function home_box(p_, v, P, A, lit_on, open) {
  const [name, question] = (A.parts && A.parts[p_.id]) || [p_.id, null];
  const lit = v.lit.length ? (v.lit.includes(p_.id) ? 'true' : 'false') : null;
  const pills = open ? `<ul class="wa-pills">` + p_.variables.map((x) => `<li class="wa-pill" data-atlas-kind="Variable" data-atlas-id="${esc(x)}" style="min-height:${v.pills[x].h}px">${esc(v.pills[x].title)}</li>`).join('') + `</ul>` : '';
  return `<p class="nm">${esc(name)}</p>` + (question ? `<p class="q">${esc(question)}</p>` : '') + `<p class="mt wa-stored" data-atlas-field="title">${esc(p_.title)}</p>`
    // the lit line in every box, shown where the pressed question lights it, so a question pressed on the working page
    // names its parts in words as the drawn state does, and each box's height is measured with it (requests 4, 27)
    + `<p class="lt">${esc(wd(P, 'lit', 'A11'))}</p>` + pills
    + `<p class="ct">${count(p_.variables.length, `part-variables:${p_.id}`, esc(fill(wd(P, 'variables', 'A11'), { n: p_.variables.length })))}`
    + ` ${p_.inside ? count(p_.inside, `part-inside:${p_.id}`, esc(fill(wd(P, 'inside', 'A11'), { n: p_.inside }))) : count(0, `part-inside:${p_.id}`, esc(wd(P, 'inside_none', 'A11')))}</p>`;
}
function view_home({ pid, P, A, F, panels, spec, frame }) {
  const v = F.view, I = F.ids;
  const lit_of = (id) => (v.lit.length ? ` data-lit="${v.lit.includes(id)}"` : '');
  const intro = fill_html(wd(P, 'intro', 'A11'), {
    variables: count(F.counts.variables, 'atlas:variables', String(F.counts.variables)), connections: count(F.counts.connections, 'atlas:connections', String(F.counts.connections)),
    loops: count(F.counts.loops, 'atlas:loops', String(F.counts.loops)), reforms: count(F.counts.reforms, 'atlas:reforms', String(F.counts.reforms)),
    issues: count(F.counts.issues, 'atlas:issues', String(F.counts.issues)) });
  const tsrc = fs.readFileSync(path.join(CODE, 'c-18-toggle.html'), 'utf8');
  const tcheck = sprite_icons(tsrc.match(/<svg\s+class="oa-toggle-check"[\s\S]*?<\/svg>/)[0]).replace(/\s*\n\s*/g, ' ');
  const sw = `<button type="button" class="oa-toggle wa-switch" aria-pressed="${v.every_variable}">${tcheck}<span class="oa-toggle-label">${esc(wd(P, 'switch', 'A11'))}</span></button>`;
  const band = `<div class="wa-hband${panels.includes('System') ? ' oa-surface-charcoal ws-panel' : ''}"><div class="ws-g"><h1 class="ws-h1 wa-hh" id="${pid}-h1">${esc(wd(P, 'h1', 'A11'))}</h1>`
    + `<p class="ws-p wa-hi wa-wide64">${intro}</p><div class="wa-hs">${sw}</div></div></div><div class="ws-g wa-narrow64 wa-hi2"><p class="ws-p">${intro}</p></div>`;
  // the drawing (specs 12.2): HTML boxes over the figure step's arrows, closed and open; the switch shows one
  // every variable shown (A17): the open drawing alone, shown whatever the switch's place in the page (a crop to the
  // drawing carries no switch)
  const draw = (D, open) => `<div class="wa-sys${open ? ' wa-sys--open' : ''}${open && v.every_variable ? ' wa-sys--only' : ''}" style="height:${D.h}px" aria-hidden="true">${D.svg}`
    + v.parts.map((p_) => { const b = D.boxes[p_.id]; return `<div class="wa-box${p_.id === 'X' ? ' wa-box--band' : ''}" data-part="${p_.id}"${lit_of(p_.id)} style="left:${b.x}px;top:${b.y}px;width:${b.w}px;height:${b.h}px">${home_box(p_, v, P, A, v.lit, open)}</div>`; }).join('') + `</div>`;
  const names = (k) => ((A.parts && A.parts[k]) || [k])[0];
  // the text equivalent and the phone form (R7): each part a card, its outgoing flows one line each, the main one first
  const cards = v.parts.map((p_) => {
    const out = v.flows.filter((f) => f.from === p_.id).sort((a, b) => b.main - a.main);
    return `<li class="wa-card" data-part="${p_.id}"${lit_of(p_.id)}>${home_box(p_, v, P, A, v.lit, v.every_variable)}<ul class="wa-fl">`
      + out.map((f) => `<li${f.main ? ' class="b"' : ''}>${fill_html(wd(P, 'flow_line', 'A11'), { n: count(f.count, `flow:${f.from}>${f.to}`, String(f.count)), part: esc(names(f.to)) })}</li>`).join('') + `</ul></li>`;
  }).join('');
  const key = `<p class="wa-key"><span class="wa-ks mc"></span>${esc(wd(P, 'key_main', 'A11'))} <span class="wa-ks of"></span>${esc(wd(P, 'key_other', 'A11'))} ${esc(wd(P, 'key_counts', 'A11'))}</p>`;
  const drawing = `<div class="ws-g"><div class="wa-col12 wa-sysw" role="group" aria-label="${esc(wd(P, 'drawing_label', 'A11'))}" data-oa-part="drawing">`
    + `<div class="wa-wide">${v.every_variable ? draw(v.drawing_open, true) : draw(v.drawing, false) + draw(v.drawing_open, true)}</div>`
    + `<ol class="wa-plist">${cards}</ol>${key}</div></div>`;
  // the questions under their hubs (Rule 21.3): toggles, one pressed at a time, the parts each lights in data-parts
  const pressed = v.pressed;
  const say_parts = (q) => { const ps_ = q.parts.map(names); return ps_.length < 2 ? ps_.join('') : ps_.slice(0, -1).join(', ') + ' and ' + ps_[ps_.length - 1]; };
  const hubs = `<div class="wa-hubs" data-oa-part="questions">` + v.hubs.map((h) => `<div class="wa-hub"><p class="lab">${esc(h.title)}</p><div class="wa-qs" role="group" aria-label="${esc(h.title)}">`
    + h.questions.map((q) => `<button type="button" class="oa-toggle wa-q" aria-pressed="${q.id === pressed}" data-pathway="${esc(q.id)}" data-parts="${esc(q.parts.join(' '))}"`
      + ` data-say="${esc(fill(wd(P, 'status', 'A11'), { parts: say_parts(q) }))}">${tcheck}<span class="oa-toggle-label wa-stored" data-atlas-field="question">${esc(q.question)}</span></button>`).join('')
    + `</div></div>`).join('') + `</div>`;
  const pq = v.hubs.flatMap((h) => h.questions).find((q) => q.id === pressed);
  const status = `<p class="wa-small wa-status" role="status">${frame && pq ? esc(fill(wd(P, 'status', 'A11'), { parts: say_parts(pq) })) : ''}</p>`;
  let answer = '';
  if (v.answer) {
    let txt = esc(v.answer.text).replace(/'/g, '’');
    const discs = [];
    for (const f of v.answer.figures) {
      const id = `${pid}-claim-${low(f.claim)}`;
      txt = txt.replace(esc(f.text), `${esc(f.text)} <a class="oa-chip oa-chip--link wa-claim" href="#${id}" data-atlas-kind="Claim" data-atlas-id="${esc(f.claim)}" data-evidence-href="#${id}">Claim <span class="oa-chip-id">${esc(f.claim)}</span></a>`);
      const r = f.record;
      discs.push(`<details class="oa-disclosure wa-cl" id="${id}"${v.claim_open ? ' open' : ''}><summary class="oa-disclosure-summary"><span class="oa-disclosure-label">${chip('Claim', f.claim)} ${esc(wd(P, 'claim_summary', 'A11'))}</span>${CHEV()}</summary>`
        + `<div class="oa-disclosure-body"><p class="wa-small wa-stored" data-atlas-field="claim">${esc(r.claim)}</p><dl class="wa-dl">`
        + [['grade', `<b>${esc(r.grade.word)}</b>, ${esc(r.grade.gloss)}`], ['population', esc(r.population)], ['jurisdiction', esc(r.jurisdiction)], ['period', esc(r.period)], ['limitation', esc(r.limitation)],
          ['sources', r.sources.map((s_) => esc([s_.publisher, s_.title, s_.year].filter(Boolean).join(', '))).join('; ')]]
          .map(([k, val]) => `<div><dt>${esc(wd(P.claim_labels || {}, k, 'A11.claim_labels'))}</dt><dd>${val}</dd></div>`).join('') + `</dl></div></details>`);
    }
    answer = `<div class="wa-answer" data-oa-part="answer"><p class="lab">${esc(wd(P, 'answer_label', 'A11'))}</p><p class="ws-p wa-stored" data-atlas-field="short_answer">${txt}</p>${discs.join('')}</div>`;
  }
  return `<section class="wa-sec" data-oa-section="System" aria-labelledby="${pid}-h1">${band}${drawing}</section>`
    + bsec('Questions', `${pid}-s2`, wd(P, 'questions_heading', 'A11'), `<p>${esc(wd(P, 'questions_lede', 'A11'))}</p>`, `<div class="ws-g"><div class="wa-col12">${hubs}${status}</div><div class="wa-col8">${answer}</div></div>`);
}

// the atlas's own script, beside chapter 18's: one question pressed at a time, the parts it lights and the line that names
// them on press (Rule 21.3); the switch that opens every box (Rule 21.2); a claim's chip opening its record (Rule 21.7)
export const atlas_js = () => `(function () {
  document.querySelectorAll('.ws.wa').forEach(function (page) {
    var qs = page.querySelectorAll('.wa-q');
    var status = page.querySelector('.wa-status');
    qs.forEach(function (q) {
      q.addEventListener('click', function () {
        var on = q.getAttribute('aria-pressed') !== 'true';
        qs.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        q.setAttribute('aria-pressed', String(on));
        var parts = on ? q.getAttribute('data-parts').split(' ') : [];
        page.querySelectorAll('[data-part]').forEach(function (b) {
          if (b.closest('.wa-loc')) return;
          if (on) b.setAttribute('data-lit', String(parts.indexOf(b.getAttribute('data-part')) >= 0)); else b.removeAttribute('data-lit');
        });
        if (status) status.textContent = on ? q.getAttribute('data-say') : '';
      });
    });
    var sw = page.querySelector('.wa-switch');
    if (sw) sw.addEventListener('click', function () { sw.setAttribute('aria-pressed', String(sw.getAttribute('aria-pressed') !== 'true')); });
    page.querySelectorAll('a.wa-claim').forEach(function (a) {
      a.addEventListener('click', function () { var d = page.querySelector(a.getAttribute('href')); if (d) d.open = true; });
    });
  });
})();`;

const VIEWS = { loop: view_loop, reform: view_reform, register: view_register, 'loop-index': view_loop_index, 'how-to-read': view_how_to_read, home: view_home };

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
${W} .wa-ticks line,.wa-sym.wa-ticks line{stroke:var(--oa-color-graphic-essential);stroke-width:2px}
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
${W} .wa-fv:not(.wa-fv--on){display:none}
${[1, 2, 3, 4, 5].map((k) => `${W} .ws-in:has(.wa-choose .oa-choice-item:nth-child(${k}) .oa-choice-input:checked) .wa-fv{display:none}${W} .ws-in:has(.wa-choose .oa-choice-item:nth-child(${k}) .oa-choice-input:checked) .wa-fv:nth-child(${k}){display:block}`).join('')}
${W} .wa-acts{margin-top:8px !important}
${W} .wa-panels .wa-panel{display:none}
${[1, 2, 3, 4, 5].map((k) => `${W} .wa-choose:has(.oa-choice-item:nth-child(${k}) .oa-choice-input:checked) .wa-panel:nth-child(${k})`).join(',')}{display:block}
@media print{${W} .wa-panels .wa-panel{display:block}}
${W} .wa-panels{padding-top:16px;border-top:2px solid var(--oa-color-border-strong)}
${W} .wa-panel .lab{margin-top:24px !important}
${W} .wa-ef,${W} .wa-rt{list-style:none;margin:0;padding:0;${type_css('body-small')}}
${W} .wa-ef li,${W} .wa-rt li{display:flex;flex-wrap:wrap;align-items:center;column-gap:12px;min-height:var(--oa-size-target-touch);padding:8px 0;border-bottom:1px solid var(--oa-color-border-hairline)}
${W} .wa-ef .f{flex:0 0 12em;font-weight:var(--oa-font-weight-semibold)}
${W} .wa-ef .pp .j,.wa-sym.pp .j{stroke:var(--oa-color-graphic-essential)}
/* the data lead's R14 (d): a red target's case is Charcoal in both themes, the edge on Newsprint, lost in the dark ground */
${W} .sv .rt .ak-case,.wa-sym.sv .rt .ak-case{stroke:var(--oa-color-graphic-essential-on-newsprint)}
/* specs 8.1: the stepper's four buttons in one row from 48em, 8 px apart, over chapter 18's layout (AL-22's order) */
${W} .wa-stepper .oa-stepper-controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
${W} .wa-stepper .oa-stepper-controls>button{width:auto;min-width:0}
${at(BP.tablet, `${W} .wa-stepper .oa-stepper-controls{grid-template-columns:repeat(4,minmax(0,1fr))}`)}
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
/* specs 14.1: the section band */
${W} .wa-sband{display:flex;flex-direction:column;justify-content:center;min-height:112px;padding:24px;margin-top:80px;margin-bottom:32px}
${at(BP.tablet, `${W} .wa-sband{padding:32px}`)}
${at(BP.desktop, `${W} .wa-sband{min-height:128px}`)}
${W} .wa-sband .ws-h2{margin:0 !important;color:var(--oa-color-text-primary)}
${W} .wa-lede{${type_css('body-small')};color:var(--oa-color-text-secondary);margin-top:8px}
${W} .wa-lede>*+*{margin-top:4px !important}
${W} .wa-bsec .wa-sband{grid-column:1/-1}
/* specs 14.2: a block printed twice, in its panel from a width and after it below, the hidden one display:none */
${under(BP.tablet, `${W} .wa-wide48{display:none}`)}${at(BP.tablet, `${W} .wa-narrow48{display:none}`)}
${under(BP.desktop, `${W} .wa-wide64{display:none}`)}${at(BP.desktop, `${W} .wa-narrow64{display:none}`)}
${W} .wa-after{margin-top:16px}${W} .wa-after>*+*{margin-top:8px !important}
${W} .wa-hi2{margin-top:24px}
${under(BP.tablet, `${W} .wa-facts dl>div{grid-template-columns:minmax(0,1fr) minmax(0,1fr);padding:2px 0;border-bottom:0}${W} .wa-head>.wa-facts{padding:16px 24px}`)}
${at(BP.desktop, `${W} .wa-index thead tr{height:88px}${W} .wa-index thead .wa-gs{margin:8px 0}`)}
${W} .wa-hband--read{padding-block:32px}
${at(BP.desktop, `${W} .wa-hband--read{min-height:160px}${W} .wa-hband--read .wa-hh{grid-column:1/-1}${W} .wa-hband--read .wa-hi{grid-column:1/9}`)}
/* tables (Rule 18.10; specs 10 and 11): chapter 18's grid, its head row on Charcoal where the content file turns it on,
   restyled as one card a row under 48em with each cell's label from data-k */
${W} .wa-tablewrap{min-width:0}
${W} .wa-col12{grid-column:1/-1;min-width:0}
${W} .oa-table-grid{width:100%;border-collapse:collapse;${type_css('body-small')}}
${W} .oa-table-grid .oa-table-th,${W} .oa-table-grid .oa-table-td{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--oa-color-border-hairline)}
${W} .oa-table-grid thead .oa-table-th{${type_css('data-label')};vertical-align:bottom;border-bottom:2px solid var(--oa-color-border-strong)}
${W} .oa-table-grid .n{text-align:right;font-variant-numeric:tabular-nums}
${at(BP.tablet, `${W} .oa-table-grid{table-layout:fixed}
 ${W} .wa-index th:nth-child(1){width:20%}${W} .wa-index thead th:nth-child(n+2){width:8%}
 ${[11, 26, 9, 8, 11, 12, 23].map((w_, i) => `${W} .wa-conns thead th:nth-child(${i + 1}){width:${w_}%}`).join('')}
 ${[9, 31, 7, 8, 20, 25].map((w_, i) => `${W} .wa-lix thead th:nth-child(${i + 1}){width:${w_}%}`).join('')}`)}
${W} .oa-table-grid .g{min-width:0;overflow-wrap:normal}
${W} .oa-table-grid .oa-chip{white-space:nowrap}
${W} .wa-index thead .g{padding-inline:6px}
${W} .oa-table-grid .wa-rh{position:static;width:auto;height:auto;overflow:visible;clip-path:none;white-space:normal;text-align:left}
${W} .wa-gs{display:inline-flex;align-items:center;gap:4px}
${W} thead .wa-gs{display:flex;margin-bottom:8px;justify-content:flex-end}
${W} .wa-headon thead tr{background:var(--oa-color-surface-charcoal)}
${W} .wa-headon thead .oa-table-th{color:var(--oa-color-text-primary-on-charcoal);border-bottom:0}
${W} .wa-headon thead :is(.ln,.rs){--oa-color-graphic-essential:var(--oa-color-graphic-essential-on-charcoal)}
${W} .wa-whole>*{font-weight:var(--oa-font-weight-semibold);border-top:2px solid var(--oa-color-border-strong)}
${W} .wa-gkey{display:none;list-style:none;margin:0 0 16px;padding:24px;${type_css('data-label')}}
${W} .wa-gkey li{display:flex;align-items:center;gap:8px}
${under(BP.tablet, `${W} .oa-table-grid,${W} .oa-table-grid tbody,${W} .oa-table-grid tr,${W} .oa-table-grid th,${W} .oa-table-grid td{display:block;width:auto}
 ${W} .oa-table-grid thead{display:none}${W} .oa-table-grid tr{padding:16px 0;border-bottom:1px solid var(--oa-color-border-hairline)}
 ${W} .oa-table-grid .oa-table-th,${W} .oa-table-grid .oa-table-td{padding:2px 0;border:0;text-align:left;white-space:normal;min-width:0}
 ${W} .oa-table-grid td[data-k]::before{content:attr(data-k) ": ";font-weight:var(--oa-font-weight-semibold)}
 ${W} .wa-gkey{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 16px}${W} .wa-gkey li{flex-wrap:wrap;min-width:0}`)}
${W} .wa-band{padding:24px;margin-top:80px}
${at(BP.tablet, `${W} .wa-band{padding:32px}`)}
${W} .wa-band .ws-h2.wa-bh{margin:0 0 16px !important}
${W} .wa-vars{list-style:none;margin:16px 0 32px;padding:0}
${W} .wa-vars li{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:12px 0;border-bottom:1px solid var(--oa-color-border-hairline)}
${W} .wa-vars .wa-small{flex:0 0 100%}
${W} .wa-col8in{max-width:866.7px;margin-top:32px}
${W} .wa-tagm .dm{fill:var(--oa-color-surface);stroke:var(--oa-color-graphic-essential);stroke-width:2px}
${W} .wa-tagm,${W} .wa-tickm{display:inline-block;vertical-align:middle}
${W} .wa-rej,${W} .wa-rev{padding-top:16px;border-top:2px solid var(--oa-color-border-strong);margin-top:24px}
${W} .wa-rej>*+*,${W} .wa-rev>*+*{margin-top:16px !important}
${W} .wa-dl{margin:0;${type_css('body-small')}}
${W} .wa-dl>div{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,3fr);gap:12px;padding:8px 0;border-bottom:1px solid var(--oa-color-border-hairline)}
${W} .wa-dl dt{font-weight:var(--oa-font-weight-semibold)}${W} .wa-dl dd{margin:0}
${W} .wa-revl{list-style:none;margin:0;padding:0}${W} .wa-revl>li+li{margin-top:24px}
${W} .wa-filters{margin-top:16px}
${W} .wa-recl{list-style:none;margin:16px 0 0;padding:0}
${W} .wa-recl li{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;min-height:var(--oa-size-target-touch);padding:8px 0;border-bottom:1px solid var(--oa-color-border-hairline);${type_css('body-small')}}
${W} .wa-recl li[hidden]{display:none}
${W} .wa-rg{${type_css('data-label')};margin-left:auto}
/* How to read (specs 11.2) */
${W} .wa-marks{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);column-gap:var(--g)}
${at(BP.desktop, `${W} .wa-marks{grid-template-columns:repeat(2,minmax(0,1fr))}`)}
${W} .wa-marks li{display:grid;grid-template-columns:120px minmax(0,1fr);gap:16px;align-items:center;min-height:64px;padding:8px 0;border-bottom:1px solid var(--oa-color-border-hairline)}
${W} .wa-marks b{display:block;${type_css('ui')};font-weight:var(--oa-font-weight-semibold)}
${W} .wa-mk{display:flex;align-items:center;justify-content:center;width:120px;min-height:48px;overflow:hidden}
${W} .wa-mkc{display:flex;flex-direction:column;align-items:center;gap:2px}${W} .wa-mkw{${type_css('caption')}}
${W} .ln .dm,.wa-sym.ln .dm{fill:var(--oa-color-surface);stroke:var(--oa-color-graphic-essential);stroke-width:2px}
${W} .wa-qs{min-height:0;padding:4px 8px}
/* the home (specs 12) */
${W} .wa-hband{padding-block:24px;box-shadow:inset 0 1px 0 var(--oa-color-border-hairline-on-charcoal)}
${W} .wa-hband .ws-g{row-gap:16px;align-items:start}
${W} .wa-hh{${type_css('h3')};margin:0}
${W} .wa-hi{margin:0}
${at(BP.desktop, `${W} .wa-hh{grid-column:1/5}${W} .wa-hi{grid-column:5/11}${W} .wa-hs{grid-column:11/13;justify-self:end}`)}
.ws.wa:is([data-atlas-view="home"],[data-atlas-view="how-to-read"]) .ws-main{padding-top:0}
${W} .wa-sysw{margin-top:24px}
${W} .wa-wide{display:none}
${at(75, `${W} .wa-wide{display:block}${W} .wa-plist{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}`)}
${W} .wa-sys{position:relative;width:1312px}
${W} .wa-sysw:has(.wa-switch[aria-pressed="true"]) .wa-sys:not(.wa-sys--open),${W} .wa-sys--open{display:none}
${W} .wa-sysw:has(.wa-switch[aria-pressed="true"]) .wa-sys--open{display:block}
${W} .ws-in:has(.wa-switch[aria-pressed="true"]) .wa-sys:not(.wa-sys--open){display:none}
${W} .ws-in:has(.wa-switch[aria-pressed="true"]) .wa-sys--open{display:block}
${W} .wa-sys--only{display:block}
${W} .wa-flows{position:absolute;left:0;top:0}
${W} .wa-flows .ln,.wa-sym.wa-flows .ln{fill:none;stroke-width:2px}
${W} .wa-flows .mc .ln,${W} .wa-flows .ln.mc,.wa-sym.wa-flows .mc .ln,.wa-sym.wa-flows .ln.mc{stroke:var(--oa-color-graphic-essential)}${W} .wa-flows .mc .hd,.wa-sym.wa-flows .mc .hd{fill:var(--oa-color-graphic-essential)}
${W} .wa-flows .of .ln,${W} .wa-flows .ln.of,.wa-sym.wa-flows .of .ln,.wa-sym.wa-flows .ln.of{stroke:var(--oa-color-graphic-subtle)}${W} .wa-flows .of .hd,.wa-sym.wa-flows .of .hd{fill:var(--oa-color-graphic-subtle)}
${W} .wa-flows .cut,.wa-sym.wa-flows .cut{fill:var(--oa-color-surface)}
${W} .wa-flows text,.wa-sym.wa-flows text{${type_css('data-label')};font-variant-numeric:tabular-nums;fill:var(--oa-color-text-primary)}
${W} .wa-flows text.b,.wa-sym.wa-flows text.b{font-weight:var(--oa-font-weight-bold)}
${W} .wa-box{position:absolute;box-sizing:border-box;padding:12px 16px;border:1px solid var(--oa-color-graphic-essential);background:var(--oa-color-surface);display:flex;flex-direction:column;gap:2px}
${W} .wa-box .lt{margin-top:4px !important}${W} .wa-box .ct{margin-top:auto !important;padding-top:4px}
${W} .wa-box:is([data-part="EC"],[data-part="TC"]){display:grid;grid-template-columns:minmax(0,1fr) auto;grid-auto-flow:dense;column-gap:16px;align-content:start}
${W} .wa-box:is([data-part="EC"],[data-part="TC"])>:is(.nm,.q,.mt){grid-column:1}
${W} .wa-box:is([data-part="EC"],[data-part="TC"])>:is(.lt,.ct){grid-column:2;text-align:right;margin:0 !important;padding:0}
${W} .wa-box:is([data-part="EC"],[data-part="TC"])>.ct{grid-row:2}
${W} .wa-box:is([data-part="EC"],[data-part="TC"])>.wa-pills{grid-column:1/-1}
${W} .wa-sys--open .wa-box{padding-inline:12px}
${W} .wa-box--band{flex-direction:row;align-items:center;gap:16px;padding-block:8px}
${W} .wa-box .nm,${W} .wa-card .nm{${type_css('h4')};margin:0}
${W} .wa-box .q{${type_css('caption')}}${W} .wa-card .q{${type_css('body-small')}}
${W} .wa-box .mt,${W} .wa-card .mt{${type_css('caption')};color:var(--oa-color-text-secondary)}
${W} .wa-box .lt,${W} .wa-card .lt{${type_css('data-label')};font-weight:var(--oa-font-weight-semibold)}
${W} .wa-box .ct,${W} .wa-card .ct{${type_css('data-label')};margin-top:auto !important}
${W} .wa-box--band .ct{margin:0 0 0 auto !important}
${W} [data-lit="false"]{border-color:var(--oa-color-state-muted-mark)}
${W} [data-lit="false"] :is(.nm,.lt){font-weight:var(--oa-font-weight-regular)}
${W} :is(.wa-box,.wa-card):not([data-lit="true"]) .lt{display:none}
${W} .wa-pills{list-style:none;margin:8px 0;padding:0;display:flex;flex-direction:column;gap:8px}
${W} .wa-box--band .wa-pills{flex-direction:row;margin:0}
${W} [data-part="EC"] .wa-pills,${W} [data-part="TC"] .wa-pills{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
${W} [data-part="TC"] .wa-pills{grid-template-columns:repeat(2,minmax(0,1fr))}
${W} .wa-pill{display:flex;align-items:center;justify-content:center;text-align:center;padding:0 8px;border:2px solid var(--oa-color-graphic-essential);border-radius:999px;${type_css('body-small')};font-weight:var(--oa-font-weight-semibold)}
${W} .wa-key{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;margin-top:16px !important;${type_css('caption')};color:var(--oa-color-text-secondary)}
${W} .wa-ks{display:inline-block;width:40px;height:2px;vertical-align:middle;margin-right:-8px}
${W} .wa-ks.mc{background:var(--oa-color-graphic-essential)}${W} .wa-ks.of{background:var(--oa-color-graphic-subtle)}
${W} .wa-plist{list-style:none;margin:0;padding:0;display:grid;gap:12px}
${W} .wa-card{padding:16px;border:1px solid var(--oa-color-graphic-essential);display:flex;flex-direction:column;gap:4px}
${W} .wa-fl{list-style:none;margin:8px 0 0;padding:0;${type_css('data-label')};font-weight:var(--oa-font-weight-regular)}
${W} .wa-fl .b{font-weight:var(--oa-font-weight-bold)}
${W} .wa-hubs{display:grid;grid-template-columns:minmax(0,1fr);gap:24px}
${at(BP.desktop, `${W} .wa-hubs{grid-template-columns:repeat(5,minmax(0,1fr))}`)}
${W} .wa-qs{display:flex;flex-direction:column;gap:8px}
${W} .wa-q{width:100%;justify-content:flex-start;text-align:left;min-height:var(--oa-size-target-touch);padding:8px 12px;${type_css('body-small')}}
/* the pressed look is chapter 18's own (the check, bold words, a 2 px edge); How to read's sample draws the same look */
${W} .wa-qon{border-width:var(--oa-border-width-rule);font-weight:var(--oa-font-weight-bold)}
${W} .wa-qon .oa-toggle-check{display:block}
${W} .wa-status{margin-top:16px !important;min-height:1lh}
${W} .wa-answer{margin-top:32px;padding-top:16px;border-top:2px solid var(--oa-color-border-strong)}
${W} .wa-answer>*+*{margin-top:12px !important}
${fig_css}
`;
}

// ---------------------------------------------------------------------------------------------------------------- render
export async function render(spec) {
  const AWd = atlas_words();
  // a state of a page (contract C9: "state", "of") takes the words of the application it is a state of
  const wid = spec.of || spec.id;
  const pw = AWd[wid];
  if (!pw) throw new Error(`the atlas page words hold no entry for ${wid} (contract C9)`);
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
    const main = fn({ pid, P: pw.page, A, F, panels, spec, width, frame: !!theme_for });
    const inner = `<a class="ws-skip" href="#${pid}-main">${esc(site.skip)}</a>${head}`
      + title_bar({ pid, A, M, current: pw.current_view, cur_val: record_page ? 'true' : 'page', open })
      + (pw.crumbs ? breadcrumb({ A, crumbs: pw.crumbs, own, loc }) : '')
      + `<main id="${pid}-main" class="ws-main" tabindex="-1">${main}</main>`
      + footer(site).replace(/\{pid\}/g, pid);
    const style = vh ? ` style="--ws-vh:${vh}px"` : '';
    return `<div class="ws wa" id="${pid}"${theme_for ? ` data-oa-theme="${theme}"` : ''}${style} data-oa-application="${esc(spec.id)}"`
      + ` data-atlas-view="${esc(spec.view)}"${spec.record ? ` data-atlas-record="${esc(spec.record)}"` : ''}${spec.chosen_reform ? ` data-atlas-chosen="${esc(spec.chosen_reform)}"` : ''} data-atlas-model="${esc(M.sha256)}"><div class="ws-in">${inner}</div></div>`;
  };
  const comp = ['id-chip', 'disclosure', 'loop-stepper', 'choice', 'toggle', 'filter-bar', 'table'].map((c) => component_css(c)).join('\n');
  const syms = [...UTILITY_SPRITE, 'oa-sym-u-chevron-24px', 'oa-sym-u-play-24px', 'oa-sym-u-pause-24px', 'oa-sym-u-reset-24px', 'oa-sym-u-arrow-24px'];
  const js = (n) => fs.readFileSync(path.join(CODE, `c-18-${n}.js`), 'utf8');
  const own_css = comp + '\n' + atlas_css(F.figure_css);
  return {
    id: spec.id, type, page: spec.view, part: 'page', title: fill(pw.title, { title: F.record_title || '' }), words_from: AWd.__from,
    // the working page's style: the website's, then chapter 18's components and the atlas's own rules
    css: site_css() + '\n' + masthead_css() + '\n' + switch_css() + '\n' + own_css,
    // in the guide the website's style is already in the head (plates/web-site.css); the atlas plate carries its own
    plate_css: own_css, styles: ['web-site'],
    export_css: res_switch_css(), kit_css: '', sprite: sprite([...new Set(syms)]),
    body, widths: spec.widths, views: spec.views,
    scripts: { head: switch_head_js(), tail: [masthead_js(), switch_js(), close_on_widen_js(NAV_BP), js('disclosure'), js('loop-stepper'), js('filter-bar'), atlas_js()].join('\n') },
    // contract C4 and C9: the plate's words are chapter 21's entry for this page and chapter 20's site words
    words_records: [{ generator: GEN, id: wid }, { generator: SITE_GEN, id: 'A06:site' }],
    atlas: { model: M.sha256, view: spec.view, record: spec.record || null },
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}
