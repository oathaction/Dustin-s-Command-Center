#!/usr/bin/env node
// The application kit's one command (DR-297, chat 10). Draws each application from its content file at build time into
// static markup, with the guide's own fonts and tokens, and writes its exports, its plate and its checks' inputs.
//
//   node work/build/app-kit/oa-app.mjs build [ID...] [--all] [--out DIR] [--exports DIR] [--date YYYYMMDD] [--no-export]
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
// Then run tools/export_checks.py on OUT for the pixel checks, and check-dimensions.py on EXPORTS.
// It never writes into the repository except the exports folder.
import fs from 'fs';
import path from 'path';
import { spawnSync } from 'child_process';
import { createRequire } from 'module';
import { KIT, ROOT, EXPORTS, PLATES, PLATE_CSS, esc, export_page, font_css, frame, identity_sprite, missing_tokens, plate, sha256, symbolize, today, tokens_css, track, untrack } from './lib.mjs';
import { words } from './renderers/web-site.mjs';

const require = createRequire(import.meta.url);
const SCRATCH = process.env.OA_APP_OUT || '/tmp/claude-0/-home-user-Dustin-s-Command-Center/ac32a0f7-d562-5d93-9aba-0ef59f7ca891/scratchpad/c11/engineer/app-out';
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');

function args(argv) {
  const o = { _: [], out: SCRATCH, exports: EXPORTS, plates: PLATES, date: today(), export: true };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--all') o.all = true;
    else if (a === '--out') o.out = path.resolve(argv[++i]);
    else if (a === '--exports') o.exports = path.resolve(argv[++i]);
    else if (a === '--date') o.date = argv[++i];
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

// chat 11c: a kit module and every module it imports by a relative path, followed through their imports
function imports_of(rel, seen = new Set()) {
  if (seen.has(rel)) return seen;
  seen.add(rel);
  const src = fs.readFileSync(path.join(ROOT, rel), 'utf8');
  for (const m of src.matchAll(/^import\s[^;]*?\sfrom\s+'(\.{1,2}\/[^']+\.mjs)'/gm)) imports_of(path.relative(ROOT, path.resolve(path.dirname(path.join(ROOT, rel)), m[1])), seen);
  return seen;
}

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
  const GENS = [GEN, 'work/build/scripts/phase-4/phase4_ch21_build.py'];
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
    views: gp.views.map(({ key, w, h, theme, alt, screens, html }) => ({ key, w, h, theme, alt, ...(screens ? { screens } : {}), html })), inputs };
  fs.writeFileSync(path.join(dir, `${spec.id.toLowerCase()}.json`), JSON.stringify(out, null, 1));
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
      const r = await R.render(spec);
      const dir = path.join(o.out, spec.id.toLowerCase());
      fs.mkdirSync(dir, { recursive: true });
      const facts = { id: spec.id, type: spec.type, views: [] };
      const miss = missing_tokens((r.css || '') + (r.html || '') + (typeof r.page === 'function' ? r.page({}) : '') + (r.body ? r.body({ pid: 'x', theme: 'light' }) : ''),
        ((r.fig && r.fig.css) || '') + (r.kit_css || ''));
      facts.missing_tokens = miss;
      if (miss.length) console.log(`  ~ ${spec.id}: tokens not in tokens.css: ${miss.join(', ')}`);
      const stem = (n) => `${o.date}_${n}`;
      if (spec.type === 'social-post' || spec.type === 'report-page' || spec.type === 'share-image') {
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
        if (r.part === 'page') {
          const file = stem(spec.export_name) + '.html';
          const html = page_html(null);
          fs.writeFileSync(path.join(dir, 'export.html'), html);
          if (o.export) { fs.writeFileSync(path.join(o.exports, file), html); manifest.files.push({ file, spec: spec.id, platform: 'website.page_1440', format: 'html', width: 1440, size: 'the working page, at any width', note: 'the working page; every width and theme is captured from it' }); }
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
            if (o.export) {
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
          if (o.export) {
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
          const [w, t, kind] = key.split('-');
          const wv = r.widths.find((x) => String(x.w) === w);
          const pid = `${spec.id.toLowerCase()}-${key}`;
          const part = r.part === 'footer' ? 'footer' : r.part === 'masthead' ? 'masthead' : 'page';
          const html = r.body({ pid, theme: t, theme_for: pid, part, width: wv.w, vh: wv.vh, open: kind === 'open' });
          fs.writeFileSync(mp, head_of(spec.id, null) + `<body>${r.sprite}${html}</body></html>`);
          const p = await browser.newPage({ viewport: { width: wv.w, height: wv.vh }, deviceScaleFactor: 1 });
          await p.goto('file://' + mp, { waitUntil: 'load' });
          await p.evaluate(() => document.fonts.ready);
          const full = await p.evaluate(() => Math.ceil(document.querySelector('.ws').getBoundingClientRect().height));
          const h = kind === 'screen' || kind === 'open' ? wv.vh : full;
          // a frame is a picture, so it carries only what its width and window can show (bytes; no pixel moves): a closed
          // disclosure keeps its summary alone, an element the page sets display:none goes, and a one-window view drops
          // everything that starts below the window. The page is captured before and after, and the two must match.
          const before = await p.screenshot({ clip: { x: 0, y: 0, width: wv.w, height: h } });
          const pruned = await p.evaluate((limit) => {
            const root = document.querySelector('.ws');
            const out = [];
            const html = (e) => !(e instanceof SVGElement) || e.ownerSVGElement === null;
            for (const e of root.querySelectorAll('*')) {
              if (!html(e) || out.some((x) => x.contains(e))) continue;
              const d = e.parentElement && e.parentElement.closest('details:not([open])');
              if (d && e.parentElement === d && e.tagName !== 'SUMMARY') { out.push(e); continue; }
              // a drawing switched by screen resolution (the end mark's fit and master, a 1x and 2x pair) stays: the guide
              // shows one or the other by the reader's screen, and this page renders at 1x only
              if (getComputedStyle(e).display === 'none' && !e.closest('.ws-end, [class*="oa-at-"]')) { out.push(e); continue; }
              // 22:07 call: a visually hidden word list stays while its holder starts inside the window, so a tracker the
              // window shows keeps its steps' states in words (A-5); it draws nothing
              const vh = e.closest('.vh');
              if (vh && vh.parentElement && vh.parentElement.getBoundingClientRect().top + scrollY < limit) continue;
              if (limit && e.getBoundingClientRect().top + scrollY >= limit) out.push(e);
            }
            out.forEach((e) => e.remove());
            return { removed: out.length, html: root.outerHTML };
          }, kind === 'screen' ? wv.vh : 0);
          const after = await p.screenshot({ clip: { x: 0, y: 0, width: wv.w, height: h } });
          const same = Buffer.compare(before, after) === 0;
          if (!same) throw new Error(`${spec.id} ${key}: pruning what the frame cannot show changed its pixels`);
          // step 4: each identity master by <use> of one symbol the page carries once; captured again, it must match
          const sym = symbolize(pruned.html);
          await p.evaluate(({ html, sprite_ }) => { const ws = document.querySelector('.ws'); ws.insertAdjacentHTML('beforebegin', sprite_); const t = document.createElement('template'); t.innerHTML = html; ws.replaceWith(t.content.firstElementChild); }, { html: sym.html, sprite_: identity_sprite(sym.symbols) });
          await p.evaluate(() => document.fonts.ready);
          const again = await p.screenshot({ clip: { x: 0, y: 0, width: wv.w, height: h } });
          await p.close();
          const same2 = Buffer.compare(after, again) === 0;
          if (!same2) throw new Error(`${spec.id} ${key}: drawing the identity masters by <use> changed the frame's pixels`);
          facts.pruned = facts.pruned || {};
          facts.pruned[key] = { removed: pruned.removed, bytes_before: Buffer.byteLength(html), bytes_after: Buffer.byteLength(pruned.html), bytes_symbolized: Buffer.byteLength(sym.html), pixels_same: same && same2 };
          Object.assign(plate_symbols, sym.symbols);
          const frame_html = sym.html;
          // W6 and ED11-4: the application's words end in a period, then the view's own sentence
          const alt = r.view_alt ? r.view_alt(key) : `${String(spec.alt).replace(/\.?$/, '.')} At ${w} px, ${t === 'light' ? 'on Newsprint' : 'in the dark theme'}${kind === 'open' ? ', the menu open' : kind === 'screen' ? ', its first screen' : ''}.`;
          views.push({ key, w: wv.w, h, theme: t, alt, ...(facts.screens && facts.screens[key] ? { screens: facts.screens[key] } : {}),
            html: frame({ w: wv.w, h, html: frame_html, alt, page: { id: spec.id, key, type: spec.type } }) });
          heights[key] = h;
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
          const alt = (r.view_alt ? r.view_alt(wv, t) : null) || `${r.alt} At ${wv.w} px, ${t === 'light' ? 'on Newsprint' : 'in the dark mode'}.`;
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
  } finally {
    await browser.close();
  }
  if (o.export && manifest.files.length) {
    const mf = path.join(o.exports, `${o.date}_Phase-4-Exports-Manifest.json`);
    // chat 11: one manifest for the folder; a build of some applications replaces their entries and keeps the others'
    const built = new Set(manifest.files.map((f) => f.spec));
    let prev = null;
    const olds = fs.readdirSync(o.exports).filter((f) => /^\d{8}_Phase-4-Exports-Manifest\.json$/.test(f)).sort();
    if (olds.length) prev = JSON.parse(fs.readFileSync(path.join(o.exports, olds[olds.length - 1]), 'utf8'));
    if (prev) manifest.files = prev.files.filter((f) => !built.has(f.spec)).concat(manifest.files);
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
    for (const id of atlas_ids) {
      const pf = path.join(o.plates, `${id.toLowerCase()}.json`);
      if (!fs.existsSync(pf)) continue;
      const mine = lines.filter((x) => x.split(' ')[2] === id);
      const fails = mine.filter((x) => x.startsWith('FAIL'));
      const pl = JSON.parse(fs.readFileSync(pf, 'utf8'));
      pl.atlas_test = { ran: when, pass: mine.length - fails.length, fail: fails.length, first_fail: fails[0] || null, self_test: self,
        self_test_misses: (st.stdout || '').split('\n').filter((x) => x.startsWith('FAIL')).slice(0, 20) };
      fs.writeFileSync(pf, JSON.stringify(pl, null, 1));
    }
    // the report for Rule 21.16's plate: every line of the last run, beside the plates
    fs.writeFileSync(path.join(o.plates, 'atlas-test.json'), JSON.stringify({ ran: when, by: 'work/build/app-kit/tools/atlas_test.py', ids: atlas_ids,
      self_test: self, lines }, null, 1));
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
