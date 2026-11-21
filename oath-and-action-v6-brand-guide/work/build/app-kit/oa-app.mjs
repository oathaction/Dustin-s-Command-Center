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
import { KIT, ROOT, EXPORTS, PLATE_CSS, esc, export_page, font_css, frame, missing_tokens, plate, today, tokens_css } from './lib.mjs';

const require = createRequire(import.meta.url);
const SCRATCH = '/tmp/claude-0/-home-user-Dustin-s-Command-Center/127ebfa4-7663-587b-a8ae-9ad439f7784c/scratchpad/c10/engineer/app-out';
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');

function args(argv) {
  const o = { _: [], out: SCRATCH, exports: EXPORTS, date: today(), export: true };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--all') o.all = true;
    else if (a === '--out') o.out = path.resolve(argv[++i]);
    else if (a === '--exports') o.exports = path.resolve(argv[++i]);
    else if (a === '--date') o.date = argv[++i];
    else if (a === '--no-export') o.export = false;
    else o._.push(a);
  }
  return o;
}

function specs(o) {
  const dir = path.join(KIT, 'specs');
  const all = fs.readdirSync(dir).filter((f) => /^a\d+-.*\.json$/.test(f)).sort();
  const pick = o.all || !o._.length ? all : all.filter((f) => o._.some((x) => f.toLowerCase().startsWith(x.toLowerCase())));
  return pick.map((f) => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')));
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
  document.querySelectorAll('[data-red]').forEach((e) => { const r = e.getBoundingClientRect(); if (r.width && getComputedStyle(e).display !== 'none') out.reds.push(e.getAttribute('data-red')); });
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
  for (let i = 0; i < 8; i++) {
    await p.keyboard.press('Tab');
    order.push(await p.evaluate(() => { const a = document.activeElement; if (!a || a === document.body) return null; const st = getComputedStyle(a); const f = a.matches('input') ? getComputedStyle(a.nextElementSibling || a) : st;
      return { tag: a.tagName.toLowerCase(), name: (a.getAttribute('aria-label') || a.value || a.textContent || '').trim().slice(0, 40), ring: f.outlineStyle !== 'none' && parseFloat(f.outlineWidth) >= 2 }; }));
  }
  r.tab_order = order;
  r.headline_lines = await p.evaluate(() => { const h = document.querySelector('.wa-h1'); const rg = document.createRange(); rg.selectNodeContents(h); const ys = new Set([...rg.getClientRects()].map((x) => Math.round(x.top))); return { lines: ys.size, text: h.textContent }; });
  r.headline_breaks = await p.evaluate(() => { const t = document.querySelector('.wa-h1').firstChild;
    const rg = document.createRange(); const words = t.textContent.split(' '); let pos = 0; const out = [];
    for (const w of words) { rg.setStart(t, pos); rg.setEnd(t, pos + w.length); const y = Math.round(rg.getBoundingClientRect().top); if (!out.length || out[out.length - 1].y !== y) out.push({ y, words: [w] }); else out[out.length - 1].words.push(w); pos += w.length + 1; }
    return out.map((l) => l.words.join(' ')); });
  return r;
}

async function main() {
  const o = args(process.argv.slice(2));
  const { chromium } = require('playwright');
  fs.mkdirSync(o.out, { recursive: true });
  if (o.export) fs.mkdirSync(o.exports, { recursive: true });
  const manifest = { written: new Date().toISOString(), by: 'work/build/app-kit/oa-app.mjs', specs: 'work/research/20261121_Platform-Specifications.json', files: [] };
  const plates = [];
  const extra_page = { sprite: [], kit_css: null };
  const browser = await chromium.launch();
  const fonts = font_css(), tokens = tokens_css();
  try {
    for (const spec of specs(o)) {
      const R = await renderer(spec.type);
      const r = await R.render(spec);
      const dir = path.join(o.out, spec.id.toLowerCase());
      fs.mkdirSync(dir, { recursive: true });
      const facts = { id: spec.id, type: spec.type, views: [] };
      const miss = missing_tokens((r.css || '') + (r.html || '') + (r.page ? r.page({}) : ''), (r.fig && r.fig.css) || '');
      facts.missing_tokens = miss;
      if (miss.length) console.log(`  ~ ${spec.id}: tokens not in tokens.css: ${miss.join(', ')}`);
      const stem = (n) => `${o.date}_${n}`;
      if (spec.type === 'social-post' || spec.type === 'report-page') {
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
            manifest.files.push({ file, spec: spec.id, platform: ex.platform, format: 'png', theme: ex.theme, ...(ex.proof ? { expect: { width: r.w, height: r.h }, note: 'proof of the sheet at 96 ppi' } : {}) });
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
            f.width = wv.w; f.theme = t; f.checked = await p.evaluate(() => (document.querySelector('.oa-theme-input:checked') || {}).value);
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
        const fr = [];
        for (const wv of r.widths) for (const t of r.themes) {
          const pid = `a02-${wv.w}-${t}`;
          const body = r.page({ pid, theme: t, theme_for: pid, group: `oa-theme-${pid}` });
          fr.push(frame({ w: wv.w, h: heights[wv.w], html: body, alt: `${r.alt} At ${wv.w} px, ${t === 'light' ? 'on Newsprint' : 'in the dark mode'}.` }));
        }
        plates.push({ id: spec.id, html: plate({ id: 'a02', head: r.plate.head, line: r.plate.line, css: r.css, frames: fr }) });
      }
      fs.writeFileSync(path.join(dir, 'facts.json'), JSON.stringify(facts, null, 1));
      console.log(`${spec.id} ${spec.type}: ${facts.views.length} view(s)${facts.missing_tokens.length ? ', ' + facts.missing_tokens.length + ' unknown token(s)' : ''}`);
    }
  } finally {
    await browser.close();
  }
  if (o.export && manifest.files.length) {
    const mf = path.join(o.exports, `${o.date}_Phase-4-Exports-Manifest.json`);
    fs.writeFileSync(mf, JSON.stringify(manifest, null, 1));
    console.log(`wrote ${manifest.files.length} exports and ${path.relative(ROOT, mf)}`);
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
