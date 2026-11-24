#!/usr/bin/env node
// The application kit's one command (DR-297, chat 10). Draws each application from its content file at build time into
// static markup, with the guide's own fonts and tokens, and writes its exports, its plate and its checks' inputs.
//
//   node work/build/app-kit/oa-app.mjs build [ID...] [--all] [--out DIR] [--exports DIR] [--date YYYYMMDD] [--no-export]
//   (OUT defaults to $TMPDIR/oa-app-out; the exports' date to each content file's export_date, else today; --date overrides)
//
// For each content file (specs/<id>-*.json, or --all):
//   1. the renderer for its type (renderers/<type>.mjs) draws it at true size;
//   2. a standalone export page per view goes to OUT/<id>/ (scratch by default);
//   3. Chromium captures each export into EXPORTS (work/build/exports/phase-4/ by default) with a dated, descriptive name:
//      a PNG at exact pixels, a full-page PNG per width and theme, a PDF at the sheet's size with its trim and bleed boxes
//      (pypdf, after Chromium); a manifest, <date>_Phase-4-Exports-Manifest.json, lists each with its platform row;
//   4. the page's own facts for the checks go to OUT/<id>/facts.json: every word's box, size and colors, every mark's box,
//      the reds, a web page's height per width and its axe, keyboard, theme and reflow results;
//   5. its plate (the drawing at true size in a frame that scales it, with its overlay) goes to OUT/<id>/plate.html, and a
//      measurement page, OUT/measure.html, holds every plate on a page like the guide's.
// A renderer that exports build() (chat 12b: video-frame, A21) does steps 2 to 5 itself and hands back its plates.
// Then run tools/export_checks.py on OUT for the pixel checks, and check-dimensions.py on EXPORTS.
// It never writes into the repository except the exports folder.
import fs from 'fs';
import os from 'os';
import path from 'path';
import { spawnSync } from 'child_process';
import { createRequire } from 'module';
import { KIT, ROOT, EXPORTS, PLATES, PLATE_CSS, atlas_symbolize, esc, export_page, font_css, frame, identity_sprite, missing_tokens, plate, sha256, symbolize, today, tokens_css, track, untrack } from './lib.mjs';
import { words } from './renderers/web-site.mjs';

const require = createRequire(import.meta.url);
// PR-S3 (chat 12): the default output folder sits under the session's own temporary folder (TMPDIR), never an old chat's
// scratch; OA_APP_OUT or --out still name it
const SCRATCH = process.env.OA_APP_OUT || path.join(process.env.TMPDIR || os.tmpdir(), 'oa-app-out');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');

function args(argv) {
  const o = { _: [], out: SCRATCH, exports: EXPORTS, plates: PLATES, date: today(), export: true };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--all') o.all = true;
    else if (a === '--out') o.out = path.resolve(argv[++i]);
    else if (a === '--exports') o.exports = path.resolve(argv[++i]);
    else if (a === '--date') { o.date = argv[++i]; o.date_set = true; }
    else if (a === '--no-export') o.export = false;
    else if (a === '--plates') o.plates = path.resolve(argv[++i]);
    else if (a === '--no-plates') o.plates = null;
    else if (a === '--spec-dir') o.spec_dir = path.resolve(argv[++i]);
    else o._.push(a);
  }
  return o;
}

function specs(o) {
  const dir = o.spec_dir || path.join(KIT, 'specs');
  const all = fs.readdirSync(dir).filter((f) => /^a\d+-.*\.json$/.test(f)).sort();
  const pick = o.all || !o._.length ? all : all.filter((f) => o._.some((x) => f.toLowerCase().startsWith(x.toLowerCase())));
  return pick.map((f) => Object.defineProperty(JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')), '__dir', { value: dir, enumerable: false }));
}

async function renderer(t) { return import(path.join(KIT, 'renderers', `${t}.mjs`)); }

// what a page tells the checks: words (each text node's boxes, its size, ink and nearest painted background), marks
// (each svg's box), the reds, and the live box. Runs in the page.
function page_facts() {
  const out = { words: [], marks: [], reds: [], doc_h: document.documentElement.scrollHeight, doc_w: document.documentElement.scrollWidth };
  const bg = (el) => { for (let e = el; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor; if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') return c; } return 'rgb(255, 255, 255)'; };
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || el.closest('[hidden], script, style, .wa-skip, details:not([open]) > :not(summary)')) continue;
    // text kept for a screen reader alone (clipped to nothing, as the kit's and the guide's visually hidden class does)
    let clipped = false;
    for (let e = el; e && e !== document.body; e = e.parentElement) { const c = getComputedStyle(e); if ((c.clip && c.clip !== 'auto') || (c.clipPath && c.clipPath !== 'none' && /inset\(50%/.test(c.clipPath)) || (c.position === 'absolute' && parseFloat(c.width) <= 1 && parseFloat(c.height) <= 1)) { clipped = true; break; } }
    if (clipped) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const rects = [...r.getClientRects()].filter((x) => x.width > 0.5 && x.height > 0.5).map((x) => [x.left + scrollX, x.top + scrollY, x.width, x.height]);
    if (!rects.length) continue;
    out.words.push({ text: n.textContent.trim().slice(0, 60), size: parseFloat(cs.fontSize), weight: cs.fontWeight, color: cs.color, bg: bg(el), rects, tag: el.tagName.toLowerCase(), cls: String(el.className || '').slice(0, 40) });
  }
  document.querySelectorAll('svg').forEach((s) => {
    if (s.closest('.oa-sprite, defs, symbol')) return;
    const r = s.getBoundingClientRect();
    if (r.width < 1 || r.height < 1 || getComputedStyle(s).display === 'none') return;
    out.marks.push({ cls: String(s.getAttribute('class') || ''), red: s.getAttribute('data-red'), rect: [r.left + scrollX, r.top + scrollY, r.width, r.height] });
  });
  out.red_marks = [];
  document.querySelectorAll('[data-red]').forEach((e) => { const r = e.getBoundingClientRect(); if (r.width && getComputedStyle(e).display !== 'none') { out.reds.push(e.getAttribute('data-red'));
    out.red_marks.push({ red: e.getAttribute('data-red'), job: e.getAttribute('data-red-job') || '', rect: [Math.round(r.left + scrollX), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)] }); } });
  // chat 11 (contract C5): each section's top, from data-oa-section, and each element painted Charcoal or Prussian, the
  // outermost of nested ones, on the page (tools/screen_shares.py keeps those of 1 percent of a screen or more as panels)
  // chat 11c (the data lead's R15): the lines each of a contested remedy's two readings takes, for the atlas test's report
  out.readings = [...document.querySelectorAll('[data-reading]')].map((e) => { const r = document.createRange(); r.selectNodeContents(e);
    return { n: e.getAttribute('data-reading'), reform: e.getAttribute('data-atlas-reform'), top: Math.round(e.getBoundingClientRect().top + scrollY),
      lines: new Set([...r.getClientRects()].filter((x) => x.height > 4 && x.width > 1).map((x) => Math.round(x.top))).size }; });
  // chat 11c (the data lead's request 15): each table row's head on a shown table, and whether a reader sees it, for T1
  out.rowheads = [...document.querySelectorAll('[role="rowheader"]')].filter((e) => { const t = e.closest('table'); const tr = e.closest('tr'); return t && t.getClientRects().length && (!tr || tr.getClientRects().length) && getComputedStyle(t).display !== 'none' && !t.closest('[hidden]'); })
    .map((e) => { const r = e.getBoundingClientRect(); const c = getComputedStyle(e);
      return { text: e.textContent.trim().replace(/\s+/g, ' ').slice(0, 60), shown: r.width > 2 && r.height > 2 && !/inset\(50%/.test(c.clipPath || '') && c.visibility !== 'hidden' }; });
  // chat 12b (the data lead's item 1): each chip's words against its own content box, for the atlas test's T14; a
  // visually hidden word (clipped to 1 px) is no part of what a reader sees
  out.chips = [...document.querySelectorAll('.oa-chip')].filter((e) => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden').map((e) => {
    const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
    const left = r.left + parseFloat(cs.borderLeftWidth) + parseFloat(cs.paddingLeft), right = r.right - parseFloat(cs.borderRightWidth) - parseFloat(cs.paddingRight);
    let x0 = Infinity, x1 = -Infinity;
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      if (!n.textContent.trim()) continue;
      const pr = n.parentElement.getBoundingClientRect(); if (pr.width <= 1 || pr.height <= 1) continue;
      const g = document.createRange(); g.selectNodeContents(n);
      for (const q of g.getClientRects()) { if (q.width < 0.5) continue; x0 = Math.min(x0, q.left); x1 = Math.max(x1, q.right); }
    }
    if (!isFinite(x0)) return null;
    return { text: e.textContent.trim().replace(/\s+/g, ' ').slice(0, 40), box: +r.width.toFixed(2), inner: +(right - left).toFixed(2),
      over: +Math.max(x1 - right, left - x0).toFixed(2), at: [Math.round(r.left + scrollX), Math.round(r.top + scrollY)] };
  }).filter(Boolean);
  out.sections = [...document.querySelectorAll('[data-oa-section]')].map((e) => ({ name: e.getAttribute('data-oa-section'), top: Math.round(e.getBoundingClientRect().top + scrollY) }));
  const DARK = { 'rgb(18, 18, 18)': 'charcoal', 'rgb(31, 45, 90)': 'prussian' };
  const darkOf = (e) => DARK[getComputedStyle(e).backgroundColor];
  out.dark = [];
  document.querySelectorAll('body *').forEach((e) => {
    const k = darkOf(e);
    if (!k) return;
    for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) if (darkOf(p)) return;
    const r = e.getBoundingClientRect();
    if (r.width < 1 || r.height < 1 || r.bottom + scrollY <= 0 || getComputedStyle(e).visibility === 'hidden') return;
    const sec = e.closest('[data-oa-section]');
    out.dark.push({ color: k, tag: e.tagName.toLowerCase(), cls: String(e.getAttribute('class') || '').slice(0, 40), section: sec ? sec.getAttribute('data-oa-section') : null, rect: [Math.round(r.left + scrollX), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)] });
  });
  return out;
}

async function web_checks(p, url, vw, vh) {
  // axe (the guide check's library, from work/build/node_modules), keyboard order, the theme kept on reload, reflow
  const r = {};
  await p.addScriptTag({ path: AXE });
  const ax = await p.evaluate(async () => { const x = await axe.run(document, { resultTypes: ['violations'] }); return x.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, first: v.nodes[0] && v.nodes[0].target.join(' ') })); });
  r.axe_violations = ax;
  const order = [];
  await p.evaluate(() => { document.activeElement && document.activeElement.blur(); window.scrollTo(0, 0); });
  for (let i = 0; i < (r.tabs || 12); i++) {
    await p.keyboard.press('Tab');
    order.push(await p.evaluate(() => { const a = document.activeElement; if (!a || a === document.body) return null; const st = getComputedStyle(a); const f = a.matches('input') ? getComputedStyle(a.nextElementSibling || a) : st;
      return { tag: a.tagName.toLowerCase(), name: (a.getAttribute('aria-label') || a.value || a.textContent || '').trim().slice(0, 40), ring: f.outlineStyle !== 'none' && parseFloat(f.outlineWidth) >= 2 }; }));
  }
  r.tab_order = order;
  if (!(await p.evaluate(() => !!document.querySelector('.wa-h1')))) return r;
  r.headline_lines = await p.evaluate(() => { const h = document.querySelector('.wa-h1'); const rg = document.createRange(); rg.selectNodeContents(h); const ys = new Set([...rg.getClientRects()].map((x) => Math.round(x.top))); return { lines: ys.size, text: h.textContent }; });
  r.headline_breaks = await p.evaluate(() => { const t = document.querySelector('.wa-h1').firstChild;
    const rg = document.createRange(); const words = t.textContent.split(' '); let pos = 0; const out = [];
    for (const w of words) { rg.setStart(t, pos); rg.setEnd(t, pos + w.length); const y = Math.round(rg.getBoundingClientRect().top); if (!out.length || out[out.length - 1].y !== y) out.push({ y, words: [w] }); else out[out.length - 1].words.push(w); pos += w.length + 1; }
    return out.map((l) => l.words.join(' ')); });
  return r;
}

// A frame is a picture, so it carries only what its width and window can show (bytes; no pixel moves): a closed
// disclosure keeps its summary alone, an element the page sets display:none goes, and a one-window view drops everything
// that starts below the window (limit). Runs in the page; returns the root's markup.
function PRUNE(arg) {
  // chat 11c: arg is the limit, or { limit, careful }; a careful prune (the atlas pages) keeps an element below the window
  // whose parent lays its children out as a grid, flex row or table and starts inside the window, since taking one child
  // out of such a parent can move its siblings above the window
  const limit = typeof arg === 'object' && arg ? arg.limit : arg;
  const careful = typeof arg === 'object' && arg ? arg.careful : false;
  const flowing = (el) => { const d = getComputedStyle(el).display; return /grid|flex|table/.test(d); };
  const root = document.querySelector('.ws');
  const out = [];
  const kept = [];   // a careful prune keeps an element whole, its descendants too
  const html = (e) => !(e instanceof SVGElement) || e.ownerSVGElement === null;
  for (const e of root.querySelectorAll('*')) {
    if (!html(e) || out.some((x) => x.contains(e)) || kept.some((x) => x.contains(e))) continue;
    const d = e.parentElement && e.parentElement.closest('details:not([open])');
    if (d && e.parentElement === d && e.tagName !== 'SUMMARY') { out.push(e); continue; }
    // a drawing switched by screen resolution (the end mark's fit and master, a 1x and 2x pair) stays: the guide shows one
    // or the other by the reader's screen, and this page renders at 1x only
    if (getComputedStyle(e).display === 'none' && !e.closest('.ws-end, [class*="oa-at-"]')) { out.push(e); continue; }
    // 22:07 call: a visually hidden word list stays while its holder starts inside the window, so a tracker the window
    // shows keeps its steps' states in words (A-5); it draws nothing
    const vh = e.closest('.vh');
    if (vh && vh.parentElement && vh.parentElement.getBoundingClientRect().top + scrollY < limit) continue;
    // CR-13 (chat 12): a held run of words (.ws-nw) is text, as it was before it was held; taking it out of a paragraph
    // that starts inside the window would reflow the lines the window shows
    if (e.classList.contains('ws-nw')) continue;
    if (limit && e.getBoundingClientRect().top + scrollY >= limit) {
      const par = e.parentElement;
      if (careful && par && flowing(par) && par.getBoundingClientRect().top + scrollY < limit) { kept.push(e); continue; }
      out.push(e);
    }
  }
  // chat 12: a one-window view keeps its page's ground to the window's last row: if taking out what starts below the window
  // would leave the page shorter than the window (A06 390-dark-screen, once CR-16 moved the page up 6 px), the page keeps
  // the window's height
  const h0 = root.getBoundingClientRect().height;
  out.forEach((e) => e.remove());
  if (limit && root.getBoundingClientRect().height < Math.min(h0, limit)) root.style.minHeight = `${Math.ceil(Math.min(h0, limit))}px`;
  return { removed: out.length, html: root.outerHTML };
}

// A style sheet's text as a tree of rules, comments out: { tree: [{ prelude, body | children, sel }], selectors }; each
// style rule's selector is numbered in the order it appears, for css_rebuild
function css_rules(css) {
  const text = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const selectors = [];
  let i = 0;
  const block = () => {   // from just after '{' to its matching '}', returns the body text
    let depth = 1, start = i, q = null;
    for (; i < text.length; i++) {
      const c = text[i];
      if (q) { if (c === q && text[i - 1] !== '\\') q = null; continue; }
      if (c === '"' || c === "'") q = c;
      else if (c === '{') depth++;
      else if (c === '}') { depth--; if (!depth) { const b = text.slice(start, i); i++; return b; } }
    }
    throw new Error('css_rules: an unclosed block');
  };
  const list = (end) => {
    const out = [];
    while (i < text.length) {
      while (i < text.length && /\s/.test(text[i])) i++;
      if (i >= text.length || text[i] === '}') { if (text[i] === '}') i++; break; }
      const open = text.indexOf('{', i), semi = text.indexOf(';', i);
      if (semi >= 0 && (open < 0 || semi < open)) { out.push({ prelude: text.slice(i, semi + 1), statement: true }); i = semi + 1; continue; }
      const prelude = text.slice(i, open).trim();
      i = open + 1;
      if (/^@(media|container|supports|layer|scope|document)\b/.test(prelude)) out.push({ prelude, children: list() });
      else if (prelude.startsWith('@')) out.push({ prelude, body: block() });
      else { out.push({ prelude, body: block(), sel: selectors.length }); selectors.push(prelude); }
    }
    return out;
  };
  return { tree: list(), selectors };
}
function css_rebuild(tree, flags) {
  return tree.map((r) => {
    if (r.statement) return r.prelude;
    if (r.children) { const inner = css_rebuild(r.children, flags); return inner ? `${r.prelude}{${inner}}` : ''; }
    if (r.sel !== undefined && !flags[r.sel]) return '';
    return `${r.prelude}{${r.body}}`;
  }).filter(Boolean).join('\n');
}

// chat 11c (DD11C-Q7, the C1 and D4-152 way): the atlas-page style placed in the guide's head serves pictures only, so it
// keeps a rule when its selector, with its hover and focus states read as plain, matches an element in some atlas plate's
// frame, and drops the rest; grouping rules keep their kept rules. Every frame of every atlas plate is captured at its true
// size with the full style and with the pruned one, and the two must match pixel for pixel, or the full style stays.
async function prune_atlas_css(browser, o, fonts, tokens, sprite_) {
  const full_f = path.join(o.out, 'atlas-page.full.css');
  const css_f = path.join(o.plates, 'atlas-page.css');
  // the style the renderer wrote this build is the full one; a later build of some atlas plates writes it whole again
  const full = fs.readFileSync(css_f, 'utf8');
  fs.writeFileSync(full_f, full);
  const plates_ = fs.readdirSync(o.plates).filter((f) => /^a\d+\.json$/.test(f)).map((f) => JSON.parse(fs.readFileSync(path.join(o.plates, f), 'utf8')))
    .filter((x) => x.type === 'atlas-page');
  const syms = Object.assign({}, ...plates_.map((x) => x.symbols || {}));
  // PR-M2 (chat 12): a build into a fresh plates folder takes the website's style from the kit's own plates
  const web_f = fs.existsSync(path.join(o.plates, 'web-site.css')) ? path.join(o.plates, 'web-site.css') : path.join(PLATES, 'web-site.css');
  const web = fs.readFileSync(web_f, 'utf8');
  const frames = plates_.flatMap((x) => x.views.map((v) => ({ id: `${x.id} ${v.key}`, w: v.w, html: v.html })));
  const page = (css) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><style>${fonts}</style><style>${tokens}</style><style>${PLATE_CSS}</style>`
    + `<style>${web}</style><style id="atlas">${css}</style><style>body{margin:0;background:var(--oa-color-surface)}.f{display:block}</style></head><body>${sprite_}${identity_sprite(syms)}`
    + frames.map((f, i) => `<div class="f" id="f${i}" style="width:${f.w}px">${f.html}</div>`).join('') + `</body></html>`;
  const pf = path.join(o.out, 'atlas-css-prune.html');
  fs.writeFileSync(pf, page(full));
  const pg = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await pg.goto('file://' + pf, { waitUntil: 'load' });
  await pg.evaluate(() => document.fonts.ready);
  // the rules are cut from the style's own text, never rebuilt from the CSSOM, whose serialization drops a shorthand set
  // by a variable when a longhand follows it (it did: chapter 18's filter status lost its font); each style rule's
  // selector is judged in the page
  const parsed = css_rules(full);
  const flags = await pg.evaluate((sels) => {
    const plain = (sel) => sel.replace(/::?(hover|focus-visible|focus-within|focus|active|visited|before|after|marker|placeholder|-webkit-[a-z-]+)(\([^)]*\))?/g, '');
    return sels.map((sel) => sel.split(',').some((x) => { const q = plain(x).trim() || '*'; try { return !!document.querySelector(q); } catch (e) { return true; } }));
  }, parsed.selectors);
  const pruned = { css: css_rebuild(parsed.tree, flags), kept: flags.filter(Boolean).length, dropped: flags.filter((x) => !x).length };
  const shots = async () => { const out = []; for (let i = 0; i < frames.length; i++) out.push(await pg.locator(`#f${i}`).screenshot()); return out; };
  const a = await shots();
  await pg.evaluate((css) => { document.getElementById('atlas').textContent = css; }, pruned.css);
  await pg.evaluate(() => document.fonts.ready);
  const b = await shots();
  await pg.close();
  fs.writeFileSync(path.join(o.out, 'atlas-page.pruned.css'), pruned.css);
  const diff = frames.filter((f, i) => Buffer.compare(a[i], b[i]) !== 0).map((f) => f.id);
  if (diff.length) {
    console.log(`  ~ atlas style: pruning changed ${diff.length} frame(s) (${diff.slice(0, 4).join(', ')}); the full style stays`);
    return;
  }
  fs.writeFileSync(css_f, pruned.css);
  for (const x of plates_) {
    // each atlas plate's record of its style's bytes, for the build's report and the next reader
    const f = path.join(o.plates, `${x.id.toLowerCase()}.json`);
    const d = JSON.parse(fs.readFileSync(f, 'utf8'));
    d.css_pruned = { full: Buffer.byteLength(full), placed: Buffer.byteLength(pruned.css), rules_kept: pruned.kept, rules_dropped: pruned.dropped, frames_same: frames.length };
    fs.writeFileSync(f, JSON.stringify(d, null, 1));
  }
  console.log(`atlas style: ${Buffer.byteLength(full).toLocaleString('en-US')} bytes to ${Buffer.byteLength(pruned.css).toLocaleString('en-US')}, ${pruned.kept} rules kept and ${pruned.dropped} dropped; ${frames.length} of ${frames.length} frames the same`);
}

// chat 11c: a kit module and every module it imports by a relative path, followed through their imports
function imports_of(rel, seen = new Set()) {
  if (seen.has(rel)) return seen;
  seen.add(rel);
  const src = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  for (const m of src.matchAll(/^import\s[^;]*?\sfrom\s+'(\.{1,2}\/[^']+\.mjs)'/gm)) imports_of(path.relative(ROOT, path.resolve(path.dirname(path.join(ROOT, rel)), m[1])), seen);
  return seen;
}

const PREV_PLATE = {};   // PR-S1: each plate's time and atlas test record before this build rewrote it
// Contract C4: the plate the guide build places for a data-oa-app placeholder, with every input's hash so the build can tell
// a stale drawing. The renderer type's style goes beside it once (plates/<type>.css), for the page's head.
function write_plate(dir, gp, read, R, spec) {
  fs.mkdirSync(dir, { recursive: true });
  // the kit's own code, every renderer included (renderers import each other), and, for an application with a chart, the
  // chart kit's code and the forms its charts draw: modules load by import, which the read record does not see
  // chat 11c: the renderer's own module and the modules it imports, followed through their imports, so an edit to one
  // renderer stales only the plates drawn by the renderers that load it (chapter 20's plates never read atlas-page.mjs)
  const code = ['work/build/app-kit/oa-app.mjs', ...imports_of(`work/build/app-kit/renderers/${spec.type}.mjs`)];
  const charts = Object.keys(spec.charts || {});
  if (charts.length) {
    const ck = path.join(ROOT, 'work/build/chart-kit');
    code.push(...fs.readdirSync(ck).filter((f) => /\.(m?js|css)$|^words\.json$/.test(f)).map((f) => `work/build/chart-kit/${f}`));
    for (const c of charts) {
      const form = JSON.parse(fs.readFileSync(path.join(ck, 'specs', `${c}.json`), 'utf8')).form;
      if (form && fs.existsSync(path.join(ck, 'forms', `${form}.js`))) code.push(`work/build/chart-kit/forms/${form}.js`);
    }
  }
  if (R.code_inputs) code.push(...R.code_inputs(spec));
  const specdir = spec.__dir || path.join(KIT, 'specs');
  const specfile = fs.readdirSync(specdir).find((f) => f.toLowerCase().startsWith(spec.id.toLowerCase() + '-'));
  const inputs = {};
  // contract C4: the words a plate takes from the chapter generator are checked by their own hash (words_hash), so an edit
  // to another page's words leaves this plate fresh; the generator file itself is no input
  const GEN = 'work/build/scripts/phase-4/phase4_ch20_build.py';
  const GENS = [GEN, 'work/build/scripts/phase-4/phase4_ch21_build.py', 'work/build/scripts/phase-4/phase4_ch16_build.py'];
  const hash_of = (generator, ids) => {
    const wh = spawnSync('python3', ['-I', path.join(KIT, 'tools/app_plates.py'), '--words-hash', ids, '--generator', generator], { encoding: 'utf8', cwd: ROOT });
    if (wh.status !== 0 || !wh.stdout.trim()) throw new Error(`words hash for ${ids} in ${generator}: ${(wh.stderr || wh.stdout).trim()}`);
    return { generator, id: ids, sha256: wh.stdout.trim() };
  };
  let words_rec = null;
  if (gp.words_records) {
    // chat 11c (contract C9): an atlas page's words are chapter 21's entry for it and chapter 20's site words; a record
    // whose generator is not written yet (stand-in words, a provisional plate) is left out
    for (const g of GENS) read.delete(g);
    words_rec = gp.words_records.filter((w) => fs.existsSync(path.join(ROOT, w.generator))).map((w) => hash_of(w.generator, w.id));
  } else if (read.has(GEN) && spec.words_file) {
    // PR-M2 (chat 12): a page with its own words file prints none of the generator's entries but the site's, so its words
    // record is the site's page (A07) and its words file is one of its inputs
    read.delete(GEN);
    words_rec = hash_of(GEN, 'A07');
  } else if (read.has(GEN)) {
    read.delete(GEN);
    // the entries the plate prints: its own, and for the favicon plate's tab the home page's title too
    words_rec = hash_of(GEN, spec.type === 'favicon-set' ? `${spec.id},A06` : spec.id);
  }
  for (const rel of [...new Set([...code, path.relative(ROOT, path.join(specdir, specfile)), ...read])].sort()) {
    if (fs.existsSync(path.join(ROOT, rel)) && fs.statSync(path.join(ROOT, rel)).isFile()) inputs[rel] = sha256(rel);
  }
  const css_file = `${gp.type}.css`;
  fs.writeFileSync(path.join(dir, css_file), gp.css);
  const out = { id: spec.id, type: gp.type, title: gp.title || spec.title || null, css: css_file,
    ...(gp.words_from && !String(gp.words_from).startsWith('work/') ? { provisional_words: gp.words_from } : {}), written: new Date().toISOString(), by: 'work/build/app-kit/oa-app.mjs',
    ...(gp.switch_words ? { switch_words: gp.switch_words } : {}),
    ...(words_rec ? { words: words_rec } : {}),
    ...(gp.styles ? { styles: gp.styles } : {}),
    ...(gp.atlas ? { atlas: gp.atlas } : {}),
    ...(gp.symbols && Object.keys(gp.symbols).length ? { symbols: gp.symbols } : {}),
    views: gp.views.map(({ key, w, h, theme, alt, screens, contrast, html }) => ({ key, w, h, theme, alt, ...(screens ? { screens } : {}), ...(contrast ? { contrast } : {}), html })), inputs };
  // PR-S1 (chat 12): a plate keeps its time while what it holds is the same, so a rerun of a run order is a clean git diff;
  // the atlas test's record (added after the drawing) is kept aside for the same comparison below
  const pfile = path.join(dir, `${spec.id.toLowerCase()}.json`);
  let prev = null;
  try { prev = JSON.parse(fs.readFileSync(pfile, 'utf8')); } catch (e) { prev = null; }
  if (prev) {
    PREV_PLATE[spec.id] = { written: prev.written, atlas_test: prev.atlas_test || null };
    const { written: _w1, atlas_test: _a1, ...was } = prev;
    const { written: _w2, ...now } = out;
    if (prev.written && JSON.stringify(was) === JSON.stringify(now)) out.written = prev.written;
  }
  fs.writeFileSync(pfile, JSON.stringify(out, null, 1));
  console.log(`  plate ${spec.id}: ${gp.views.length} frame(s), ${Object.keys(inputs).length} inputs -> ${path.relative(ROOT, path.join(dir, spec.id.toLowerCase() + '.json'))}`);
}

async function main() {
  const o = args(process.argv.slice(2));
  const { chromium } = require('playwright');
  fs.mkdirSync(o.out, { recursive: true });
  if (o.export) fs.mkdirSync(o.exports, { recursive: true });
  const manifest = { written: new Date().toISOString(), by: 'work/build/app-kit/oa-app.mjs', specs: 'work/research/20261121_Platform-Specifications.json', files: [] };
  const plates = [], guide_plates = [];
  const extra_page = { sprite: [], kit_css: null };
  const browser = await chromium.launch();
  const fonts = font_css(), tokens = tokens_css();
  try {
    for (const spec of specs(o)) {
      const R = await renderer(spec.type);
      const reads = track();   // contract C4: every file read while this application is drawn
      let r = await R.render(spec);
      const dir = path.join(o.out, spec.id.toLowerCase());
      fs.mkdirSync(dir, { recursive: true });
      const facts = { id: spec.id, type: spec.type, views: [] };
      const miss = missing_tokens((r.css || '') + (r.html || '') + (typeof r.page === 'function' ? r.page({}) : '') + (r.body ? r.body({ pid: 'x', theme: 'light' }) : ''),
        ((r.fig && r.fig.css) || '') + (r.kit_css || ''));
      facts.missing_tokens = miss;
      if (miss.length) console.log(`  ~ ${spec.id}: tokens not in tokens.css: ${miss.join(', ')}`);
      // PR-S2 (chat 12): a content file names its exports' date (export_date), so a run order needs no --date to reproduce
      // them; --date still overrides it, and a content file with none takes today's
      const stem = (n) => `${o.date_set ? o.date : (spec.export_date || o.date)}_${n}`;
      if (typeof R.build === 'function') {
        // chat 12b (A21, contract W-C4): a renderer that captures its own exports, runs its own checks and writes its own
        // plate views (renderers/video-frame.mjs); a frame with a fault places no plate, and the build exits 1
        const out = await R.build({ r, spec, o, browser, dir, facts, manifest, stem, fonts, tokens });
        plates.push(...(out.plates || []));
        if (out.kit_css) extra_page.kit_css = extra_page.kit_css || out.kit_css;
        if (out.sprite) extra_page.sprite.push(out.sprite);
        if (out.faults && out.faults.length) {
          console.log(`  ~ ${spec.id}: ${out.faults.length} fault(s); no plate placed`);
          out.faults.slice(0, 20).forEach((x) => console.log('    ' + x));
          process.exitCode = 1;
        } else if (spec.guide && out.guide) guide_plates.push({ spec, ...out.guide });
      } else if (spec.type === 'social-post' || spec.type === 'report-page' || spec.type === 'share-image') {
        const html = export_page({ title: r.title || spec.plate_head, w: r.w, h: r.h, html: r.html, css: r.css, page: r.print || null });
        const pf = path.join(dir, 'export.html');
        fs.writeFileSync(pf, html);
        const p = await browser.newPage({ viewport: { width: r.w, height: r.h }, deviceScaleFactor: 1 });
        await p.goto('file://' + pf, { waitUntil: 'load' });
        await p.evaluate(() => document.fonts.ready);
        const f = await p.evaluate(page_facts);
        f.live = r.live; f.floor_px = r.floor_px; f.sign_off = r.sign_off || null; f.w = r.w; f.h = r.h;
        for (const ex of r.exports) {
          if (!o.export) continue;
          if (ex.kind === 'png') {
            const file = stem(ex.name) + '.png';
            await p.screenshot({ path: path.join(o.exports, file), clip: { x: 0, y: 0, width: r.w, height: r.h } });
            manifest.files.push({ file, spec: spec.id, platform: ex.platform, format: 'png', theme: ex.theme, size: `${r.w.toLocaleString('en-US')} by ${r.h.toLocaleString('en-US')} px`, ...(ex.proof ? { expect: { width: r.w, height: r.h }, note: 'proof of the sheet at 96 ppi' } : {}), ...(r.meta ? { meta: r.meta } : {}) });
            f.png = file;
          } else if (ex.kind === 'pdf') {
            const file = stem(ex.name) + '.pdf';
            await p.emulateMedia({ media: 'print' });
            await p.pdf({ path: path.join(o.exports, file), width: `${r.print.width_in}in`, height: `${r.print.height_in}in`, printBackground: true, tagged: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
            await p.emulateMedia({ media: 'screen' });
            const fx = spawnSync('python3', ['-I', path.join(KIT, 'tools/pdf_boxes.py'), path.join(o.exports, file), String(r.print.bleed_pt), spec.title || ''], { encoding: 'utf8' });
            if (fx.status !== 0) console.log('  ~ pdf boxes: ' + (fx.stderr || fx.stdout).trim());
            manifest.files.push({ file, spec: spec.id, platform: ex.platform, format: 'pdf', theme: ex.theme });
            f.pdf = file;
          }
        }
        facts.views.push(f);
        await p.close();
        // the plate: the drawing in its frame with its overlay; the social post adds the size a phone's feed shows it
        const fr = [frame({ w: r.w, h: r.h, html: r.html, alt: r.alt, layers: r.layers })];
        if (r.plate.feed_px) fr.push(frame({ w: r.w, h: r.h, html: r.html, alt: r.alt + ' Shown at the 390 px width a phone’s feed gives it.', cls: 'oa-app-feed' }));
        plates.push({ id: spec.id, html: plate({ id: spec.id.toLowerCase(), head: r.plate.head, line: r.plate.line, css: r.css, frames: fr }) });
        // contract C4: a still drawn for the guide, one view at its true size
        if (spec.guide) {
          const key = `${r.w}-${r.exports[0].theme || 'light'}`;
          const alt = r.alt || spec.alt;   // W6: the share preview's alt is the generator's words (r.alt)
          guide_plates.push({ spec, type: spec.type, css: r.css, views: [{ key, w: r.w, h: r.h, theme: r.exports[0].theme || 'light', alt,
            html: frame({ w: r.w, h: r.h, html: r.html, alt, layers: r.layers, page: { id: spec.id, key, type: spec.type } }) }] });
        }
      } else if (spec.type === 'favicon-set') {
        // contract C6: the SVG favicon as written, the ICO from three PNGs the kit draws at 16, 32 and 48 px on a clear
        // ground, and the three app icons at their rows' sizes
        const views = [];
        for (const ex of r.exports) {
          const pid = `${spec.id.toLowerCase()}-${ex.name.toLowerCase()}`;
          if (ex.kind === 'svg') {
            const file = stem(ex.name) + '.svg';
            if (o.export) { fs.writeFileSync(path.join(o.exports, file), ex.text); manifest.files.push({ file, spec: spec.id, platform: ex.platform, format: 'svg', serve_as: ex.serve_as, size: '16 by 16 px drawing, at any size' }); }
            facts.views.push({ svg: file, kind: 'svg' });
          } else if (ex.kind === 'ico') {
            const parts = [];
            for (const px of ex.sizes) {
              const pf = path.join(dir, `ico-${px}.html`);
              fs.writeFileSync(pf, `<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}</style></head><body>${ex.html_at(px)}</body></html>`);
              const p = await browser.newPage({ viewport: { width: px, height: px }, deviceScaleFactor: 1 });
              await p.goto('file://' + pf, { waitUntil: 'load' });
              const png = path.join(dir, `ico-${px}.png`);
              await p.screenshot({ path: png, clip: { x: 0, y: 0, width: px, height: px }, omitBackground: true });
              await p.close();
              parts.push(png);
            }
            const file = stem(ex.name) + '.ico';
            if (o.export) {
              const ic = spawnSync('python3', ['-I', path.join(KIT, 'tools/ico.py'), path.join(o.exports, file), ...parts], { encoding: 'utf8' });
              if (ic.status !== 0) throw new Error('ico: ' + (ic.stderr || ic.stdout));
              manifest.files.push({ file, spec: spec.id, platform: ex.platform, format: 'ico', serve_as: ex.serve_as, sizes: ex.sizes, size: '16, 32 and 48 px' });
            }
            facts.views.push({ ico: file, kind: 'ico', parts: parts.map((x) => path.basename(x)) });
          } else {
            const html = export_page({ title: spec.plate_head, w: ex.w, h: ex.h, html: ex.html, css: ex.css, fonts: false });
            const pf = path.join(dir, `${ex.name}.html`);
            fs.writeFileSync(pf, html);
            const p = await browser.newPage({ viewport: { width: ex.w, height: ex.h }, deviceScaleFactor: 1 });
            await p.goto('file://' + pf, { waitUntil: 'load' });
            const file = stem(ex.name) + '.png';
            if (o.export) { await p.screenshot({ path: path.join(o.exports, file), clip: { x: 0, y: 0, width: ex.w, height: ex.h } }); manifest.files.push({ file, spec: spec.id, platform: ex.platform, format: 'png', serve_as: ex.serve_as, theme: 'light', size: `${ex.w} by ${ex.h} px` }); }
            facts.views.push({ png: file, kind: 'app-icon', w: ex.w, h: ex.h, b: ex.b, safe: ex.platform === 'website.manifest_512' ? r.safe_512 : null });
            await p.close();
            if (spec.guide) {
              const key = `${ex.w}`;
              const ICON = { 'apple-touch-icon.png': 'The Apple touch icon', 'icon-192.png': 'The web app manifest icon', 'icon-512-maskable.png': 'The maskable web app manifest icon' };
              const alt = `${String(spec.alt).replace(/\.?$/, '.')} ${ICON[ex.serve_as] || 'The icon'}, ${ex.w} by ${ex.h} px.`;
              views.push({ key, w: ex.w, h: ex.h, theme: 'light', alt, html: frame({ w: ex.w, h: ex.h, html: ex.html, alt, page: { id: spec.id, key, type: spec.type } }) });
            }
          }
        }
        if (spec.guide) {
          // the guide's views (spec 9, R9): the favicon drawn in currentColor from the token (a frame takes no literal color),
          // on a light and a dark tab showing the home page's title as a tab does; the ICO's three sizes at their own
          // pixels; the three tiles, the 512 with its safe circle as an overlay a reader switches on (contract C3)
          const fav = (px) => r.svg.replace(/<title[\s\S]*?<\/title>|<desc[\s\S]*?<\/desc>/g, '').replace(/\s(role|aria-labelledby)="[^"]*"/g, '')
            .replace('<svg ', '<svg aria-hidden="true" focusable="false" ').replace(/\swidth="16" height="16"/, ` width="${px}" height="${px}"`).replace(/fill="#[0-9A-Fa-f]{6}"/, 'fill="currentColor"');
          let tab_title = 'Oath & Action';
          try { tab_title = (words().A06 || {}).title || tab_title; } catch (e) { /* the content file's words */ }
          const vs = [];
          for (const g of ['light', 'dark']) {
            const key = `tab-${g}`;
            const alt = `${spec.alt} The favicon at 16 px on a ${g === 'light' ? 'light' : 'dark'} browser tab beside the page’s title.`;
            vs.push({ key, w: 240, h: 40, theme: g, alt, html: frame({ w: 240, h: 40, alt, page: { id: spec.id, key, type: spec.type },
              html: `<div class="fi-tab fi-tab--${g}">${fav(16)}<span>${esc(tab_title)}</span></div>` }) });
          }
          vs.push({ key: 'ico', w: 128, h: 48, theme: 'light', alt: `${spec.alt} The favicon.ico file’s three images at their own pixels: 16, 32 and 48 px.`,
            html: frame({ w: 128, h: 48, alt: `${spec.alt} The favicon.ico file’s three images at their own pixels: 16, 32 and 48 px.`, page: { id: spec.id, key: 'ico', type: spec.type },
              html: `<div class="fi-ico">${fav(16)}${fav(32)}${fav(48)}</div>` }) });
          for (const v of views) {
            if (v.key === '512') {
              const c = r.safe_512;
              v.html = frame({ w: v.w, h: v.h, alt: v.alt, page: { id: spec.id, key: v.key, type: spec.type }, html: r.exports.find((x) => x.w === 512).html,
                layers: [{ kind: 'circle', cx: c.cx, cy: c.cy, r: c.r, sw: 2, label: 'Safe circle, 40 percent', lx: 16, ly: 16, x: 0, y: 0, w: 0, h: 0 }] });
            }
            vs.push(v);
          }
          const tile_css = r.exports.filter((x) => x.css).map((x) => x.css).join('');
          guide_plates.push({ spec, type: spec.type, views: vs, switch_words: spec.plate_switch || 'Show the safe areas',
            css: tile_css + '.fi-tab{display:flex;align-items:center;gap:8px;width:240px;height:40px;padding:0 12px;box-sizing:border-box;font:var(--oa-type-ui-font-weight) 13px/1 var(--oa-type-ui-font-family);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
              + '.fi-tab span{overflow:hidden;text-overflow:ellipsis}.fi-tab svg{flex:none;display:block}'
              + '.fi-tab--light{background:var(--oa-color-surface-white);color:var(--oa-color-text-primary-on-white)}.fi-tab--light svg{color:var(--oa-color-identity-signature-on-white)}'
              + '.fi-tab--dark{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal)}.fi-tab--dark svg{color:var(--oa-color-identity-signature-on-charcoal)}'
              + '.fi-ico{display:flex;align-items:flex-end;gap:16px;height:48px}.fi-ico svg{display:block;color:var(--oa-color-identity-signature)}' });
        }
      } else if (spec.type === 'web-site' || spec.type === 'atlas-page') {
        // chat 11: the website's pages (A04 to A08). The working page goes to the exports as HTML; each width and theme is
        // captured from it as a full-length PNG with the page's facts and its web checks; the menu's open states are
        // captured by pressing Menu; each guide frame is measured on its own markup at its width.
        const kit_css = r.kit_css || '';
        const head_of = (title, theme) => `<!doctype html>
<html lang="en"${theme ? ` data-oa-theme="${theme}"` : ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>${esc(title)}</title>
<script>${r.scripts.head}</script>
<style>${fonts}</style>
<style>${tokens}</style>
<style>${kit_css}</style>
<style>html,body{margin:0;padding:0}body{background:var(--oa-color-surface)}${r.css}${r.export_css || ''}</style>
${r.head_links || ''}
</head>
`;
        const page_html = (theme, fig_w = null) => head_of(r.title, theme) + `<body>${r.sprite}${r.body({ pid: 'site', theme: theme || 'device', fig_w }).replace(/id="site-main"/g, 'id="main"').replace(/href="#site-main"/g, 'href="#main"')}<script>${r.scripts.tail}</script></body>
</html>
`;
        // chat 11c (the data lead's requests 4 and 27): the atlas home's boxes grow to hold their words. The page is drawn
        // once, each box's height read at 1440 px with its height freed and every line it can show shown, in both forms,
        // and the figure step draws again with those heights as each row's floor
        if (spec.type === 'atlas-page' && /class="wa-sys/.test(r.body({ pid: 'site', theme: 'light' })) && !spec.box_need) {
          const mf = path.join(dir, 'measure-boxes.html');
          fs.writeFileSync(mf, page_html('light', 1440));
          const p = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
          await p.goto('file://' + mf, { waitUntil: 'load' });
          await p.evaluate(() => document.fonts.ready);
          spec.box_need = await p.evaluate(() => {
            const out = {};
            for (const sys of document.querySelectorAll('.wa-sys')) {
              const form = sys.classList.contains('wa-sys--open') ? 'open' : 'closed';
              sys.style.display = 'block';
              out[form] = {};
              for (const b of sys.querySelectorAll('.wa-box')) {
                b.style.height = 'auto';
                b.querySelectorAll('.lt').forEach((x) => { x.style.display = 'block'; });
                out[form][b.dataset.part] = Math.ceil(b.getBoundingClientRect().height);
              }
            }
            return out;
          });
          await p.close();
          fs.unlinkSync(mf);
          console.log(`  ${spec.id}: boxes measured ${JSON.stringify(spec.box_need)}`);
          r = await R.render(spec);
        }
        // chat 11c (contract C9): a content file marked "state" is a page in one state for a rule plate; it draws its frames
        // and its facts and writes no export, since its page is the export of the application it is a state of
        const exp = o.export && !spec.state;
        if (r.part === 'page') {
          const file = stem(spec.export_name) + '.html';
          const html = page_html(null);
          fs.writeFileSync(path.join(dir, 'export.html'), html);
          if (exp) { fs.writeFileSync(path.join(o.exports, file), html); manifest.files.push({ file, spec: spec.id, platform: 'website.page_1440', format: 'html', width: 1440, size: 'the working page, at any width', note: 'the working page; every width and theme is captured from it' }); }
          facts.page_html = file;
        }
        const heights = {};
        const needs = new Set((spec.views || []).map((k) => k.split('-').slice(0, 2).join('-')));
        if (r.part === 'page') {
          for (const wv of r.widths) for (const t of ['light', 'dark']) {
            if (!needs.has(`${wv.w}-${t}`) && !(spec.capture || []).includes(`${wv.w}-${t}`)) continue;
            const pf = path.join(dir, `export-${wv.w}-${t}.html`);
            fs.writeFileSync(pf, page_html(t, wv.w));
            const p = await browser.newPage({ viewport: { width: wv.w, height: wv.vh }, deviceScaleFactor: 1 });
            await p.goto('file://' + pf, { waitUntil: 'load' });
            await p.evaluate(() => document.fonts.ready);
            const f = await p.evaluate(page_facts);
            f.width = wv.w; f.vh = wv.vh; f.theme = t; f.checked = await p.evaluate(() => [...document.querySelectorAll('.oa-theme-input:checked')].map((x) => x.value));
            if (exp) {
              const file = stem(`${spec.export_name}-${wv.w}-${t === 'light' ? 'Light' : 'Dark'}`) + '.png';
              await p.screenshot({ path: path.join(o.exports, file), fullPage: true });
              const ph = await p.evaluate(() => document.documentElement.scrollHeight);
              manifest.files.push({ file, spec: spec.id, platform: wv.platform, format: 'png', theme: t, size: `${wv.w.toLocaleString('en-US')} by ${ph.toLocaleString('en-US')} px` });
              f.png = file;
            }
            f.checks = await web_checks(p, pf, wv.w, wv.vh);
            if (wv.w === 1440) {
              const other = t === 'light' ? 'dark' : 'light';
              await p.click(`.oa-site-switch-bar .oa-theme-input[value="${other}"]`, { force: true });
              await p.reload({ waitUntil: 'load' });
              f.checks.theme_after_reload = { chose: other, root: await p.evaluate(() => document.documentElement.getAttribute('data-oa-theme')), stored: await p.evaluate(() => { try { return localStorage.getItem('oa-theme'); } catch (e) { return 'unreadable'; } }),
                checked: await p.evaluate(() => [...document.querySelectorAll('.oa-theme-input:checked')].map((x) => x.value)) };
              await p.evaluate(() => { try { localStorage.removeItem('oa-theme'); } catch (e) {} });
            }
            facts.views.push(f);
            await p.close();
          }
          // R6 (the design director's request): each full-length view's screens by contract C5, for the plate's JSON
          if (exp) {
            const items = facts.views.filter((v) => v.png && v.vh).map((v) => ({ key: `${v.width}-${v.theme}`, png: path.join(o.exports, v.png), vh: v.vh, sections: v.sections, dark: v.dark, theme: v.theme, width: v.width }));
            const bi = path.join(dir, 'screens-in.json'), bo = path.join(dir, 'screens-out.json');
            fs.writeFileSync(bi, JSON.stringify(items));
            const sr = spawnSync('python3', ['-I', path.join(KIT, 'tools/screen_shares.py'), '--batch', bi, bo], { encoding: 'utf8' });
            if (sr.status !== 0) throw new Error('screens: ' + (sr.stderr || sr.stdout));
            JSON.parse(fs.readFileSync(bo, 'utf8')).forEach((scr, i) => {
              facts.screens = facts.screens || {};
              facts.screens[items[i].key] = scr.map((x) => ({ name: x.screen === 'first screen' ? 'first' : x.screen, newsprint: x.newsprint, dark: x.dark,
                red: Math.round(x.red * 10) / 10, panels: x.panels, panels_box: x.panels_box, judged: x.judged, faults: x.faults }));
            });
          }
          for (const [vw, zoom] of [[320, 1], [1024, 2]]) {
            const p = await browser.newPage({ viewport: { width: vw, height: 900 } });
            await p.goto('file://' + path.join(dir, 'export.html'), { waitUntil: 'load' });
            if (zoom !== 1) await p.addStyleTag({ content: 'html{font-size:200%}' });
            await p.evaluate(() => document.fonts.ready);
            facts[`reflow_${vw}_${zoom * 100}`] = await p.evaluate(() => ({ scroll_w: document.documentElement.scrollWidth, win_w: innerWidth,
              wider: [...document.querySelectorAll('.ws *')].filter((e) => e.getBoundingClientRect().right > innerWidth + 1 && !e.closest('.oac-art,.oac-tw,.ws-skip,dialog')).slice(0, 5).map((e) => e.tagName.toLowerCase() + '.' + String(e.className).slice(0, 24)) }));
            await p.close();
          }
        } else if (r.part === 'masthead' && o.export) {
          // the menu open, from the working article page: Menu pressed, one window captured
          const pf = path.join(dir, 'menu.html');
          for (const key of spec.views.filter((k) => k.endsWith('-open'))) {
            const [w, t] = key.split('-');
            const wv = r.widths.find((x) => String(x.w) === w);
            fs.writeFileSync(pf, page_html(t));
            const p = await browser.newPage({ viewport: { width: wv.w, height: wv.vh }, deviceScaleFactor: 1 });
            await p.goto('file://' + pf, { waitUntil: 'load' });
            await p.evaluate(() => document.fonts.ready);
            await p.click('.oa-masthead-menu');
            await p.mouse.move(1, wv.vh - 2);   // the pointer off every control, so no hover style shows in the capture
            const st = await p.evaluate(() => ({ open: document.querySelector('dialog').open, expanded: document.querySelector('.oa-masthead-menu').getAttribute('aria-expanded'), focus: (document.activeElement.textContent || '').trim().slice(0, 40) }));
            const file = stem(`${spec.export_name}-Open-${w}-${t === 'light' ? 'Light' : 'Dark'}`) + '.png';
            await p.screenshot({ path: path.join(o.exports, file) });
            manifest.files.push({ file, spec: spec.id, platform: wv.platform, format: 'png', theme: t, size: `${wv.w} by ${wv.vh} px`, note: 'the menu open, one window' });
            await p.keyboard.press('Escape');
            await p.waitForFunction(() => !document.querySelector('dialog').open);
            await p.waitForTimeout(50);
            st.after_escape = await p.evaluate(() => ({ open: document.querySelector('dialog').open, expanded: document.querySelector('.oa-masthead-menu').getAttribute('aria-expanded'), focus: document.activeElement.className }));
            facts.views.push({ key, png: file, menu: st });
            await p.close();
          }
        }
        // the guide's frames, each measured on its own markup at its width
        const views = [];
        const plate_symbols = {};
        const mp = path.join(dir, 'measure-frame.html');
        for (const key of spec.views || []) {
          // chat 11c (contract C9): a key may add the open state and a crop to a part, <w>-<theme>[-open][-<part>]
          const [w, t, ...rest] = key.split('-');
          const open_ = rest.includes('open');
          const crop = rest.find((x) => x !== 'open' && x !== 'screen') || null;
          const kind = rest.includes('screen') ? 'screen' : open_ && !crop ? 'open' : crop ? 'crop' : undefined;
          const wv = r.widths.find((x) => String(x.w) === w);
          const pid = `${spec.id.toLowerCase()}-${key}`;
          const part = r.part === 'footer' ? 'footer' : r.part === 'masthead' ? 'masthead' : 'page';
          const html = r.body({ pid, theme: t, theme_for: pid, part, width: wv.w, vh: wv.vh, open: open_ });
          // a crop's page takes the frame's theme on its root too, so a crop that ends on a fraction of a pixel shows the
          // frame's own ground there before and after pruning (chapter 20's frames, which are no crops, keep their page)
          fs.writeFileSync(mp, head_of(spec.id, crop ? t : null) + `<body>${r.sprite}${html}</body></html>`);
          const p = await browser.newPage({ viewport: { width: wv.w, height: wv.vh }, deviceScaleFactor: 1 });
          await p.goto('file://' + mp, { waitUntil: 'load' });
          await p.evaluate(() => document.fonts.ready);
          const full = await p.evaluate(() => Math.ceil(document.querySelector('.ws').getBoundingClientRect().height));
          // a crop runs from its part's top to its foot; the part "top" runs from the page's top to 16 px into main (specs 4)
          let y0 = 0, h = kind === 'screen' || kind === 'open' ? wv.vh : full, box_exact = 0, part_x = null;
          if (crop) {
            const box = await p.evaluate((name) => {
              if (name === 'top') { const m = document.querySelector('.ws main'); return m ? { top: 0, bottom: Math.ceil(m.getBoundingClientRect().top + scrollY + 16) } : null; }
              // CD-S2 (chat 12, atlas specs 15.2): the part is the union of every element carrying its name
              const es = [...document.querySelectorAll(`.ws [data-oa-part="${name}"]`)];
              if (!es.length) return null;
              const rs = es.map((x) => x.getBoundingClientRect());
              const b = { top: Math.min(...rs.map((r) => r.top)), bottom: Math.max(...rs.map((r) => r.bottom)),
                left: Math.min(...rs.map((r) => r.left)), right: Math.max(...rs.map((r) => r.right)) };
              // chat 11c: a crop holds the part's whole pixel rows, so no sliver of what sits above or below it shows
              return { top: Math.ceil(b.top + scrollY - 0.001), bottom: Math.floor(b.bottom + scrollY + 0.001), exact: b.top + scrollY,
                left: Math.max(0, Math.floor(b.left)), right: Math.min(innerWidth, Math.ceil(b.right)) };
            }, crop);
            if (!box) throw new Error(`${spec.id} ${key}: the page marks no data-oa-part="${crop}" (contract C9)`);
            y0 = box.top; h = box.bottom - box.top; box_exact = box.exact;
            if (crop !== 'top') part_x = { x: box.left, width: box.right - box.left };
          }
          if (y0 + h > wv.vh) await p.setViewportSize({ width: wv.w, height: Math.max(wv.vh, y0 + h) });
          // a frame is a picture, so it carries only what its width and window can show (bytes; no pixel moves): a closed
          // disclosure keeps its summary alone, an element the page sets display:none goes, and a one-window view drops
          // everything that starts below the window. The page is captured before and after, and the two must match.
          const before = await p.screenshot({ clip: { x: 0, y: y0, width: wv.w, height: h } });
          // DD11C-Q6: a crop is its part; the part's own columns are what the part-alone drawing must match
          const before_part = part_x ? await p.screenshot({ clip: { ...part_x, y: y0, height: h } }) : null;
          const lim = kind === 'screen' ? wv.vh : crop ? y0 + h : 0;
          const pruned = await p.evaluate(PRUNE, spec.type === 'atlas-page' ? { limit: lim, careful: true } : lim);
          let after = await p.screenshot({ clip: { x: 0, y: y0, width: wv.w, height: h } });
          const same = Buffer.compare(before, after) === 0;
          if (!same) throw new Error(`${spec.id} ${key}: pruning what the frame cannot show changed its pixels`);
          // chat 11c (DD11C-Q6): a crop to a part carries the part's own subtree, its ancestors up to the page's root and,
          // in a table, the head row that sets its columns; every other branch goes. The page is drawn again so, and the
          // part's pixels at its new place must equal its pixels in the whole page, or the crop keeps the clipped page.
          if (crop && crop !== 'top') {
            // two ways to set the part alone: at the place its top had in the page, to the fraction of a pixel (a dashed
            // line's edge pixels follow its place on the page), else moved up with its top's fraction kept (a list whose
            // rows round alike only near the top); the first whose part draws the same pixels is the frame
            const tried = [];
            let done = false;
            for (const mode of ['place', 'fraction']) {
              await p.goto('file://' + mp, { waitUntil: 'load' });
              await p.evaluate(() => document.fonts.ready);
              const nb = await p.evaluate(({ name, exact, mode }) => {
                // CD-S2 (chat 12): every element carrying the part's name stays, with its ancestors
                const parts_ = [...document.querySelectorAll(`.ws [data-oa-part="${name}"]`)];
                const root = document.querySelector('.ws');
                const keep = new Set();
                for (const p0 of parts_) for (let x = p0; x && x !== root; x = x.parentElement) keep.add(x);
                // a sibling in a grid or flex row stays as an empty box of its own tag, classes and height, so the part keeps its
                // column and its row (a grid places by order); a table's other rows go, its head row stays
                const TABLE = new Set(['TABLE', 'THEAD', 'TBODY', 'TFOOT', 'TR']);
                const boxes = [], rows_kept = [];
                const done_parents = new Set();
                for (const n of keep) {
                  const parent = n.parentElement;
                  if (!parent || done_parents.has(parent)) continue;
                  done_parents.add(parent);
                  const pd = getComputedStyle(parent).display;
                  const laid = /grid|flex/.test(pd);
                  for (const sib of [...parent.children]) {
                    if (keep.has(sib)) continue;
                    if (parent.tagName === 'TABLE' && (sib.tagName === 'THEAD' || sib.tagName === 'COLGROUP')) continue;
                    // the rows either side of a row stay, emptied, at their heights: a collapsed border is shared between two
                    // rows, so the row keeps the border it had (alone, it would take the head's rule and grow half a pixel)
                    if (sib.tagName === 'TR' && (keep.has(sib.nextElementSibling) || keep.has(sib.previousElementSibling))) {
                      const hh = sib.getBoundingClientRect().height;
                      const tr = document.createElement('tr');
                      if (sib.getAttribute('class')) tr.setAttribute('class', sib.getAttribute('class'));
                      for (const c of sib.children) { const x = document.createElement(c.tagName.toLowerCase()); if (c.getAttribute('class')) x.setAttribute('class', c.getAttribute('class')); tr.appendChild(x); }
                      tr.setAttribute('style', `height:${Math.round(hh * 1000) / 1000}px`);
                      rows_kept.push([sib, tr]);
                      continue;
                    }
                    const cs = getComputedStyle(sib);
                    if (laid && !TABLE.has(parent.tagName) && cs.display !== 'none' && cs.position !== 'absolute' && cs.position !== 'fixed') {
                      const bb = sib.getBoundingClientRect();
                      boxes.push([sib, Math.round(bb.height * 1000) / 1000, /flex/.test(pd) ? Math.round(bb.width * 1000) / 1000 : null]);
                    } else sib.remove();
                  }
                }
                for (const [sib, tr] of rows_kept) sib.replaceWith(tr);
                for (const [sib, hh, ww] of boxes) {
                  const e = document.createElement(sib.tagName.toLowerCase());
                  if (sib.getAttribute('class')) e.setAttribute('class', sib.getAttribute('class'));
                  e.setAttribute('style', `height:${hh}px;min-height:0;box-sizing:border-box;padding:0;border:0;overflow:hidden;visibility:hidden${ww != null ? `;width:${ww}px;flex:none` : ''}`);
                  sib.replaceWith(e);
                }
                const t1 = Math.min(...parts_.map((x) => x.getBoundingClientRect().top)) + scrollY;
                const shift = mode === 'place' ? exact - t1 : (((exact % 1) - (t1 % 1)) % 1 + 1) % 1;
                if (shift > 0.001) document.querySelector('.ws-in').style.paddingTop = `${shift.toFixed(3)}px`;
                return {};
              }, { name: crop, exact: box_exact, mode });
              const sub = await p.evaluate(PRUNE, 0);
              // the part-alone page drawn afresh from its markup, as the frame will be, so the proof reads what the frame shows
              await p.evaluate((html) => { const ws = document.querySelector('.ws'); const t = document.createElement('template'); t.innerHTML = html; ws.replaceWith(t.content.firstElementChild); }, sub.html);
              await p.evaluate(() => document.fonts.ready);
              Object.assign(nb, await p.evaluate((name) => { const rs = [...document.querySelectorAll(`.ws [data-oa-part="${name}"]`)].map((x) => x.getBoundingClientRect());
                const b = { top: Math.min(...rs.map((r) => r.top)), bottom: Math.max(...rs.map((r) => r.bottom)) };
                return { top: Math.ceil(b.top + scrollY - 0.001), bottom: Math.floor(b.bottom + scrollY + 0.001) }; }, crop));
              if (nb.bottom - nb.top !== h) { tried.push(`${mode}: the part alone is ${nb.bottom - nb.top} px tall, in the page ${h}`); continue; }
              const mine = await p.screenshot({ clip: { x: 0, y: nb.top, width: wv.w, height: h } });
              const mine_part = await p.screenshot({ clip: { ...part_x, y: nb.top, height: h } });
              if (Buffer.compare(before_part, mine_part) !== 0) {
                tried.push(`${mode}: the part alone did not draw the same pixels`);
                // the two pictures, for a reader to see where they part (the kit's output folder only)
                fs.writeFileSync(path.join(dir, `crop-${key}-${mode}-page.png`), before);
                fs.writeFileSync(path.join(dir, `crop-${key}-${mode}-part.png`), mine);
                continue;
              }
              facts.subtree = facts.subtree || {};
              facts.subtree[key] = { bytes_clipped: Buffer.byteLength(pruned.html), bytes_subtree: Buffer.byteLength(sub.html), top_before: y0, top_after: nb.top, mode,
                part_columns: part_x.width === wv.w ? 'the whole width' : `${part_x.x} to ${part_x.x + part_x.width} px; beside it the frame shows the page's ground`,
                band_same: Buffer.compare(before, mine) === 0 };
              pruned.html = sub.html; pruned.removed += sub.removed;
              y0 = nb.top;
              after = mine;
              done = true;
              break;
            }
            if (!done) {
              facts.subtree = facts.subtree || {};
              facts.subtree[key] = { kept_clipped: tried.join('; ') };
              await p.goto('file://' + mp, { waitUntil: 'load' });
              await p.evaluate(() => document.fonts.ready);
              await p.evaluate(PRUNE, { limit: y0 + h, careful: true });
            }
          }
          // step 4: each identity master by <use> of one symbol the page carries once; captured again, it must match
          const sym = symbolize(pruned.html);
          await p.evaluate(({ html, sprite_ }) => { const ws = document.querySelector('.ws'); ws.insertAdjacentHTML('beforebegin', sprite_); const t = document.createElement('template'); t.innerHTML = html; ws.replaceWith(t.content.firstElementChild); }, { html: sym.html, sprite_: identity_sprite(sym.symbols) });
          await p.evaluate(() => document.fonts.ready);
          const again = await p.screenshot({ clip: { x: 0, y: y0, width: wv.w, height: h } });
          const same2 = Buffer.compare(after, again) === 0;
          if (!same2) { fs.writeFileSync(path.join(dir, `id-${key}-after.png`), after); fs.writeFileSync(path.join(dir, `id-${key}-again.png`), again); }
          if (!same2) throw new Error(`${spec.id} ${key}: drawing the identity masters by <use> changed the frame's pixels`);
          // chat 11c (round 2, weight step c): an atlas frame's repeated drawings by <use> of one symbol each, group by group
          // (a group is the drawings sharing one class list); a group whose symbols move a pixel stays drawn inline
          let atl = null;
          if (spec.type === 'atlas-page') {
            const trial = async (skip) => {
              const a = atlas_symbolize(sym.html, skip);
              if (!Object.keys(a.symbols).length) return { a, same: true };
              await p.evaluate(({ html, sprite_ }) => { document.querySelectorAll('svg[data-oa-app-kit="identity"]').forEach((x) => x.remove()); const ws = document.querySelector('.ws'); ws.insertAdjacentHTML('beforebegin', sprite_); const t = document.createElement('template'); t.innerHTML = html; ws.replaceWith(t.content.firstElementChild); },
                { html: a.html, sprite_: identity_sprite({ ...sym.symbols, ...a.symbols }) });
              await p.evaluate(() => document.fonts.ready);
              const shot = await p.screenshot({ clip: { x: 0, y: y0, width: wv.w, height: h } });
              return { a, same: Buffer.compare(after, shot) === 0 };
            };
            let t1 = await trial(new Set());
            const kept_inline = [];
            if (!t1.same) {
              const all = Object.keys(t1.a.groups);
              for (const g of all) { const r1 = await trial(new Set(all.filter((x) => x !== g))); if (!r1.same) kept_inline.push(g); }
              t1 = await trial(new Set(kept_inline));
              if (!t1.same) { kept_inline.push(...Object.keys(t1.a.groups)); t1 = null; }
            }
            if (t1 && Object.keys(t1.a.symbols).length) atl = { ...t1.a, kept_inline };
            else atl = { html: sym.html, symbols: {}, groups: {}, kept_inline };
          }
          // CD-S2 (chat 12, atlas specs 15.2, DD12-C1): a crop to a part is cut on both axes: the part's box plus 24 px of the
          // page each side, clipped to the page; the frame is that box (the part itself was proved above, pixel for pixel)
          const page_h = await p.evaluate(() => Math.ceil(document.querySelector('.ws').getBoundingClientRect().bottom + scrollY));
          await p.close();
          let fx = 0, fw = wv.w, fy = y0, fh = h, pad_foot = 0;
          if (crop && crop !== 'top' && part_x) {
            // chat 12b (Engineer A's request 2, DD12b-R2): 24 px of the page under the part even where the part ends its
            // part-alone page (A18's sheettop); the crop's wrapper carries the page's ground, by its theme's surface class,
            // that far below the page's foot
            pad_foot = Math.max(0, Math.ceil(y0 + h + 24 - Math.max(page_h, y0 + h)));
            fy = Math.max(0, y0 - 24); fh = y0 + h + 24 - fy;
            fx = Math.max(0, part_x.x - 24); fw = Math.min(wv.w, part_x.x + part_x.width + 24) - fx;
          }
          facts.pruned = facts.pruned || {};
          facts.pruned[key] = { removed: pruned.removed, bytes_before: Buffer.byteLength(html), bytes_after: Buffer.byteLength(pruned.html), bytes_symbolized: Buffer.byteLength(sym.html), pixels_same: same && same2,
            ...(atl ? { bytes_atlas_symbols: Buffer.byteLength(atl.html), atlas_symbol_groups: atl.groups, atlas_kept_inline: atl.kept_inline } : {}) };
          if (atl) { sym.html = atl.html; Object.assign(sym.symbols, atl.symbols); }
          Object.assign(plate_symbols, sym.symbols);
          // a crop draws the page moved up by its part's top, inside a frame as tall as the part
          // (CD-S2: and moved left by the box's left edge, the page kept at its own width so it lays out as before)
          const frame_html = fy || fw !== wv.w || pad_foot ? `<div class="oa-app-crop${pad_foot ? ` oa-surface-${t === 'dark' ? 'charcoal' : 'newsprint'}` : ''}" style="margin-top:-${fy}px${fw !== wv.w ? `;margin-left:-${fx}px;width:${wv.w}px` : ''}${pad_foot ? `;padding-bottom:${pad_foot}px` : ''}">${sym.html}</div>` : sym.html;
          // W6 and ED11-4: the application's words end in a period, then the view's own sentence
          const alt = r.view_alt ? r.view_alt(key) : `${String(spec.alt).replace(/\.?$/, '.')} At ${w} px, ${t === 'light' ? 'in the light theme' : 'in the dark theme'}${kind === 'open' ? ', the menu open' : kind === 'screen' ? ', its first screen' : ''}.`;
          // chat 11c (Rule 21.15): an atlas page's full-length view carries the contrast measured on its capture's pixels,
          // for Rule 21.15's ratio table (tools/atlas_contrast.py)
          let contrast = null;
          const cap = spec.type === 'atlas-page' && !kind && facts.views.find((x) => x.width === wv.w && x.theme === t && x.png);
          if (cap && o.export) {
            const ac = spawnSync('python3', ['-I', path.join(KIT, 'tools/atlas_contrast.py'), path.join(o.exports, cap.png), t], { encoding: 'utf8' });
            if (ac.status !== 0) throw new Error('atlas contrast: ' + (ac.stderr || ac.stdout));
            contrast = JSON.parse(ac.stdout);
          }
          views.push({ key, w: fw, h: fh, theme: t, alt, ...(fw !== wv.w ? { page_w: wv.w, box: { x: fx, y: fy } } : {}),
            ...(facts.screens && facts.screens[key] ? { screens: facts.screens[key] } : {}), ...(contrast ? { contrast } : {}),
            html: frame({ w: fw, h: fh, html: frame_html, alt, page: { id: spec.id, key, type: spec.type } }) });
          heights[key] = fh;
        }
        facts.frame_heights = heights;
        // chat 11c: an atlas plate carries only its own rules (r.plate_css) and names the website's style it stands on
        if (spec.guide) guide_plates.push({ spec, type: spec.type, css: r.plate_css || r.css, views, words_from: r.words_from, title: r.title, symbols: plate_symbols,
          ...(r.styles ? { styles: r.styles } : {}), ...(r.atlas ? { atlas: r.atlas } : {}), ...(r.words_records ? { words_records: r.words_records } : {}) });
        plates.push({ id: spec.id, html: plate({ id: spec.id.toLowerCase(), head: r.plate.head, line: r.plate.line, css: r.css, frames: views.map((v) => v.html) }) });
        extra_page.kit_css = extra_page.kit_css || kit_css;
        extra_page.sprite.push(r.sprite);
      } else if (spec.type === 'web-page') {
        extra_page.sprite.push(r.sprite);
        extra_page.kit_css = r.fig.css;
        facts.chart_faults = r.fig.faults;
        const heights = {};
        for (const wv of r.widths) {
          for (const t of r.themes) {
            const body = r.page({ theme: t });
            const html = `<!doctype html>
<html lang="en" data-oa-theme="${t}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>${esc(spec.title)}</title>
<script>${R.switch_head_js()}</script>
<style>${fonts}</style>
<style>${tokens}</style>
<style>${r.fig.css}</style>
<style>html,body{margin:0;padding:0}body{background:var(--oa-color-surface)}${r.css}</style>
</head>
<body>${r.sprite}${body}<script>${R.switch_js()}</script></body>
</html>
`;
            const pf = path.join(dir, `export-${wv.w}-${t}.html`);
            fs.writeFileSync(pf, html);
            const p = await browser.newPage({ viewport: { width: wv.w, height: wv.vh }, deviceScaleFactor: 1 });
            await p.goto('file://' + pf, { waitUntil: 'load' });
            await p.evaluate(() => document.fonts.ready);
            const f = await p.evaluate(page_facts);
            f.width = wv.w; f.vh = wv.vh; f.theme = t; f.checked = await p.evaluate(() => (document.querySelector('.oa-theme-input:checked') || {}).value);
            heights[wv.w] = f.doc_h;
            const ex = r.exports.find((x) => x.viewport[0] === wv.w && x.theme === t);
            if (o.export) {
              const file = stem(ex.name) + '.png';
              await p.screenshot({ path: path.join(o.exports, file), fullPage: true });
              manifest.files.push({ file, spec: spec.id, platform: ex.platform, format: 'png', theme: t });
              f.png = file;
            }
            f.checks = await web_checks(p, pf, wv.w, wv.vh);
            // the theme kept after a reload: choose Dark (or Light), reload, read the root
            if (wv.w === 1440) {
              const other = t === 'light' ? 'dark' : 'light';
              await p.click(`.oa-theme-input[value="${other}"]`, { force: true });
              await p.reload({ waitUntil: 'load' });
              f.checks.theme_after_reload = { chose: other, root: await p.evaluate(() => document.documentElement.getAttribute('data-oa-theme')), stored: await p.evaluate(() => { try { return localStorage.getItem('oa-theme'); } catch (e) { return 'unreadable'; } }) };
              await p.evaluate(() => { try { localStorage.removeItem('oa-theme'); } catch (e) {} });
            }
            facts.views.push(f);
            await p.close();
          }
        }
        // reflow at 320 px and text at 200 percent at 1440: nothing wider than the window
        for (const [vw, zoom] of [[320, 1], [1440, 2]]) {
          const p = await browser.newPage({ viewport: { width: vw, height: 900 } });
          await p.goto('file://' + path.join(dir, 'export-1440-light.html'), { waitUntil: 'load' });
          if (zoom !== 1) await p.addStyleTag({ content: 'html{font-size:200%}' });
          await p.evaluate(() => document.fonts.ready);
          facts[`reflow_${vw}_${zoom * 100}`] = await p.evaluate(() => ({ scroll_w: document.documentElement.scrollWidth, win_w: innerWidth,
            wider: [...document.querySelectorAll('.wa *')].filter((e) => e.getBoundingClientRect().right > innerWidth + 1 && !e.closest('.oac-art,.oac-table-wrap,.wa-skip')).slice(0, 5).map((e) => e.tagName.toLowerCase() + '.' + String(e.className).slice(0, 20)) }));
          await p.close();
        }
        // the plate: one frame per width, Light and Dark side by side, each its own page at its width (container queries
        // and cqi type), the switch inside each frame setting that frame
        const fr = [], views = [];
        for (const wv of r.widths) for (const t of r.themes) {
          const key = `${wv.w}-${t}`;
          const pid = `${spec.id.toLowerCase()}-${key}`;
          const body = r.page({ pid, theme: t, theme_for: pid, group: `oa-theme-${pid}` });
          const alt = (r.view_alt ? r.view_alt(wv, t) : null) || `${r.alt} At ${wv.w} px, ${t === 'light' ? 'in the light theme' : 'in the dark mode'}.`;
          const html = frame({ w: wv.w, h: heights[wv.w], html: body, alt, page: { id: spec.id, key, type: spec.type } });
          fr.push(html);
          views.push({ key, w: wv.w, h: heights[wv.w], theme: t, alt, html });
        }
        plates.push({ id: spec.id, html: plate({ id: spec.id.toLowerCase(), head: r.plate.head, line: r.plate.line, css: r.css, frames: fr }) });
        if (spec.guide) guide_plates.push({ spec, type: spec.type, css: r.css, views });   // contract C4: a plate for the guide
      }
      const read = untrack();
      const gp = guide_plates.find((x) => x.spec === spec);
      if (gp && o.plates) write_plate(o.plates, gp, read, R, spec);
      fs.writeFileSync(path.join(dir, 'facts.json'), JSON.stringify(facts, null, 1));
      console.log(`${spec.id} ${spec.type}: ${facts.views.length} view(s)${facts.missing_tokens.length ? ', ' + facts.missing_tokens.length + ' unknown token(s)' : ''}`);
    }
    // chat 11c (DD11C-Q7): the atlas plates' style in the guide holds only the rules some drawn frame uses
    if (o.plates && specs(o).some((x) => x.type === 'atlas-page')) await prune_atlas_css(browser, o, fonts, tokens, extra_page.sprite.join(''));
  } finally {
    await browser.close();
  }
  if (o.export && manifest.files.length) {
    // chat 11: one manifest for the folder; a build of some applications replaces their entries and keeps the others'.
    // chat 11c: the manifest keeps the date it was first written (CLAUDE.md; D4-231), whatever --date the exports take
    const built = new Set(manifest.files.map((f) => f.spec));
    let prev = null;
    const olds = fs.readdirSync(o.exports).filter((f) => /^\d{8}_Phase-4-Exports-Manifest\.json$/.test(f)).sort();
    const mf = path.join(o.exports, olds.length ? olds[0] : `${o.date}_Phase-4-Exports-Manifest.json`);
    if (olds.length) prev = JSON.parse(fs.readFileSync(path.join(o.exports, olds[olds.length - 1]), 'utf8'));
    if (prev) manifest.files = prev.files.filter((f) => !built.has(f.spec)).concat(manifest.files);
    // PR-S1 (chat 12): entries in spec order (each spec's files in the order the kit wrote them), and the manifest keeps its
    // time while the list is the same, so a rerun of a run order leaves it untouched
    const by_spec = (a) => Number(String(a.spec).replace(/\D/g, '')) || 0;
    manifest.files = manifest.files.map((f, i) => [f, i]).sort((a, b) => by_spec(a[0]) - by_spec(b[0]) || a[1] - b[1]).map(([f]) => f);
    if (prev && JSON.stringify(prev.files) === JSON.stringify(manifest.files)) manifest.written = prev.written;
    for (const f of olds) if (path.join(o.exports, f) !== mf) fs.unlinkSync(path.join(o.exports, f));
    fs.writeFileSync(mf, JSON.stringify(manifest, null, 1));
    console.log(`wrote ${manifest.files.length} exports and ${path.relative(ROOT, mf)}`);
  }
  // chat 11c (contract C9, Rule 21.16): the atlas test on every atlas page this build drew, its working page and its plate's
  // frames, and its self-test; each atlas plate carries its result, which the strict guide build reads, and a FAIL stops
  // this build (exit 1) once every file is written
  const atlas_ids = specs(o).filter((x) => x.type === 'atlas-page').map((x) => x.id);
  if (atlas_ids.length && o.plates) {
    const T = path.join(KIT, 'tools/atlas_test.py');
    const rep = path.join(o.out, 'atlas-test.json');
    const run = spawnSync('python3', ['-I', T, o.out, '--plates', o.plates, '--json', rep, '--ids', ...atlas_ids], { encoding: 'utf8', cwd: ROOT, maxBuffer: 64 * 1024 * 1024 });
    const st = spawnSync('python3', ['-I', T, '--self-test', o.out, '--plates', o.plates], { encoding: 'utf8', cwd: ROOT, maxBuffer: 64 * 1024 * 1024 });
    const lines = (run.stdout || '').split('\n').filter((x) => /^(PASS|FAIL) T\d+ /.test(x));
    const self = /self-test: PASS/.test(st.stdout || '') ? 'PASS' : 'FAIL';
    const when = new Date().toISOString();
    // PR-S1 (chat 12): a plate whose drawing and result are both unchanged keeps the time its test last ran, and so does the
    // report when every plate kept its time and the lines are the same; any change takes this run's time
    let all_kept = true;
    for (const id of atlas_ids) {
      const pf = path.join(o.plates, `${id.toLowerCase()}.json`);
      if (!fs.existsSync(pf)) continue;
      const mine = lines.filter((x) => x.split(' ')[2] === id);
      const fails = mine.filter((x) => x.startsWith('FAIL'));
      const pl = JSON.parse(fs.readFileSync(pf, 'utf8'));
      const rec = { ran: when, pass: mine.length - fails.length, fail: fails.length, first_fail: fails[0] || null, self_test: self,
        self_test_misses: (st.stdout || '').split('\n').filter((x) => x.startsWith('FAIL')).slice(0, 20) };
      const was = PREV_PLATE[id];
      const same = was && was.atlas_test && was.written === pl.written
        && JSON.stringify({ ...was.atlas_test, ran: null }) === JSON.stringify({ ...rec, ran: null });
      if (same) rec.ran = was.atlas_test.ran; else all_kept = false;
      pl.atlas_test = rec;
      fs.writeFileSync(pf, JSON.stringify(pl, null, 1));
    }
    // the report for Rule 21.16's plate: every line of the last run, beside the plates
    const repf = path.join(o.plates, 'atlas-test.json');
    let old_rep = null;
    try { old_rep = JSON.parse(fs.readFileSync(repf, 'utf8')); } catch (e) { old_rep = null; }
    const rep_rec = { ran: when, by: 'work/build/app-kit/tools/atlas_test.py', ids: atlas_ids, self_test: self, lines };
    if (all_kept && old_rep && JSON.stringify({ ...old_rep, ran: null }) === JSON.stringify({ ...rep_rec, ran: null })) rep_rec.ran = old_rep.ran;
    fs.writeFileSync(repf, JSON.stringify(rep_rec, null, 1));
    const nf = lines.filter((x) => x.startsWith('FAIL')).length;
    console.log(`atlas test: ${lines.length - nf} PASS, ${nf} FAIL; self-test ${self}`);
    lines.filter((x) => x.startsWith('FAIL')).slice(0, 12).forEach((x) => console.log('  ' + x));
    if (nf || self !== 'PASS') process.exitCode = 1;
  }
  // the measurement page: a page like the guide's, which already carries the fonts, tokens.css, the chart kit's style and
  // the sprite; each plate sits in a frame of the guide's kind, and its bytes are counted alone
  for (const pl of plates) fs.writeFileSync(path.join(o.out, pl.id.toLowerCase(), 'plate.html'), pl.html);
  const page = `<!doctype html>
<html lang="en" data-oa-theme="light">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Application kit: measurement page (studio)</title>
<style id="oa-fonts">${fonts}</style>
<style id="oa-tokens">${tokens}</style>
<style id="kit-css">${extra_page.kit_css || ''}</style>
<style id="plate-css">${PLATE_CSS}
body{margin:0;background:var(--oa-color-surface);color:var(--oa-color-text-primary);font:var(--oa-type-body-font-weight) var(--oa-type-body-font-size)/var(--oa-type-body-line-height) var(--oa-type-body-font-family)}
body>main{max-width:1120px;margin:0 auto;padding:32px 16px}</style>
</head>
<body><div id="sprite">${extra_page.sprite.join('')}</div><main>
${plates.map((pl) => `<section class="measure" data-plate="${pl.id}">${pl.html}</section>`).join('\n')}
</main></body></html>
`;
  fs.writeFileSync(path.join(o.out, 'measure.html'), page);
  const bytes = Object.fromEntries(plates.map((pl) => [pl.id, Buffer.byteLength(pl.html)]));
  const shared = { plate_css: Buffer.byteLength(PLATE_CSS), sprite: Buffer.byteLength(extra_page.sprite.join('')), kit_css: Buffer.byteLength(extra_page.kit_css || '') };
  fs.writeFileSync(path.join(o.out, 'measure.json'), JSON.stringify({ plates: bytes, shared, page: Buffer.byteLength(page) }, null, 1));
  console.log('plates: ' + Object.entries(bytes).map(([k, v]) => `${k} ${v.toLocaleString('en-US')} bytes`).join('; ') + `; shared plate style ${shared.plate_css.toLocaleString('en-US')}, sprite ${shared.sprite.toLocaleString('en-US')}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
