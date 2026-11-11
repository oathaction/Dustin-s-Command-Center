#!/usr/bin/env node
// Sprite check (promotion, November 10, 2026, guide engineer): every symbol the guide's sprite can hold, drawn through
// <use> beside its own file, and the 1x and 2x pattern (DR-179), in Chromium. Promotion C (November 11, 2026): the
// fourth family, the 37 fits in civic-line-v6/fit-24/ (black edition only, D2-1132), and the pattern for all 41 on the
// list of drawings that read at 24 px (DR-136, DR-209).
//
// Usage:
//   node work/build/scripts/phase-2/sprite_check.js [--sprite-root DIR] [--json out.json] [--png DIR]
//
// It asks guide_build.py for every symbol of the four families (--sprite-sheet), then draws, on a Newsprint ground at
// device scale 1 and 2:
//   symbols   each symbol through <use> in an <svg> the size the guide sets it (Civic Line at 48 and 128 px, a fit or
//             utility icon at its own size), beside its file inline in the page at the same size, as the guide drew
//             icons before the sprite. The black edition in the ink, #121212 (a utility icon's currentColor takes it
//             too); for Civic Line and the pillar fits also the red-black edition, with --oa-icon-accent set to that
//             file's red. The 37 fits have no red-black edition (D2-1132). The drawings of one item take turns in one
//             cell, and the screenshots are compared there.
//   pattern   each 24 px drawing of the 41 as specimens write it, <use class="oa-at-1x"> of the fit and <use
//             class="oa-at-2x"> of the master, with the shell's switch: at 1x and 1.5x it must draw the fit's file, at
//             2x the master's file at 24 px, and differ from the other one, so the switch is seen to work.
// A pair matches when no channel of any pixel differs by more than 8 of 255. Exit 0 when every pair matches and the
// pattern switches, 1 otherwise, 2 on misuse. --png writes the turns of any page with a failing pair to DIR (a scratch
// folder, never work/build).
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const TOL = 8;                     // largest channel difference that still counts as the same drawing
const GROUND = '#DCD9D2';          // Newsprint
const INK = '#121212';            // Charcoal, the files' ink; a utility icon's currentColor takes it too
const SHELL_SWITCH = fs.readFileSync(path.join(ROOT, 'work/build/guide/shell/guide-shell.css'), 'utf8').match(/\.oa-at-2x \{ display: none \}\n@media[^\n]+/);

function args() {
  const o = { root: null, json: null, png: null };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--sprite-root') o.root = a[++i];
    else if (a[i] === '--json') o.json = a[++i];
    else if (a[i] === '--png') o.png = a[++i];
    else { console.error(`sprite_check: unknown argument ${a[i]}`); process.exit(2); }
  }
  return o;
}

// The file itself, inline in the page as the guide drew icons before the sprite and as the pixel-fit check draws them:
// its root sized to the cell, its ids given a per-cell prefix so two copies on one page keep their own masks.
let cellNo = 0;
const fileOf = (file, px) => {
  const pre = `c${cellNo++}-`;
  let s = fs.readFileSync(file, 'utf8').replace(/<\?xml[^>]*\?>/, '').replace(/<!--[\s\S]*?-->/g, '');
  s = s.replace(/<svg\b[^>]*>/, (r) => r.replace(/\swidth="[^"]*"/, ` width="${px}"`).replace(/\sheight="[^"]*"/, ` height="${px}"`));
  return s.replace(/\sid="([^"]+)"/g, ` id="${pre}$1"`).replace(/url\(#([^)]+)\)/g, `url(#${pre}$1)`).replace(/href="#([^"]+)"/g, `href="#${pre}$1"`);
};
const useOf = (sid, vb, px, style, cls) => `<svg viewBox="${vb}" width="${px}" height="${px}" aria-hidden="true" focusable="false"${style ? ` style="${style}"` : ''}>${cls || `<use href="#${sid}"/>`}</svg>`;
const firstRed = (file, ink) => {
  const c = [...fs.readFileSync(file, 'utf8').matchAll(/(?:fill|stroke)="(#[0-9A-Fa-f]{6})"/g)].map((m) => m[1].toUpperCase())
    .find((x) => ![ink.toUpperCase(), '#FFFFFF', '#000000'].includes(x));
  return c || null;
};

// Each item lists the drawings that take turns in its cell: the references (the file, or for a pattern the fit's file and
// the master's file), then the test, drawn through the sprite.
function items(sheet) {
  const out = [];
  for (const [sid, s] of Object.entries(sheet.symbols)) {
    const vb = s.symbol.match(/viewBox="([^"]+)"/)[1];
    const sizes = s.family === 'civic-line' ? [48, 128] : [Number(sid.match(/-(\d+)px$/)[1])];
    for (const px of sizes) out.push({ kind: 'symbol', sid, label: s.label, edition: 'black', px, refs: [fileOf(s.file, px)], test: useOf(sid, vb, px) });
    if (s.family === 'utility' || s.family === 'fit-24') continue;   // one color: no red-black edition
    const red = s.family === 'civic-line' ? s.file.replace(/\/black\/([^/]+)-Black\.svg$/, '/red-black/$1-Red-Black.svg') : s.file.replace(/-Black\.svg$/, '-Red-Black.svg');
    if (red === s.file || !fs.existsSync(red)) { out.push({ kind: 'missing', sid, label: s.label, edition: 'red-black', file: red }); continue; }
    const accent = firstRed(red, INK);
    for (const px of sizes) out.push({ kind: 'symbol', sid, label: s.label, edition: 'red-black', px, refs: [fileOf(red, px)], test: useOf(sid, vb, px, `--oa-icon-accent:${accent || INK}`) });
  }
  for (const [sid, s] of Object.entries(sheet.symbols)) {
    const m = sid.match(/^oa-sym-((?:cl|r)-\d+)-24px$/);
    if (!m || !['pillar', 'fit-24'].includes(s.family)) continue;
    const master = sheet.symbols[`oa-sym-${m[1]}`];
    if (!master) { out.push({ kind: 'missing', sid, label: s.label, edition: 'master for 2x screens', file: `oa-sym-${m[1]}` }); continue; }
    out.push({ kind: 'pattern', sid, label: s.label, px: 24, refs: [fileOf(s.file, 24), fileOf(master.file, 24)],
               test: useOf(sid, '0 0 24 24', 24, '', `<use class="oa-at-1x" href="#${sid}"/><use class="oa-at-2x" href="#oa-sym-${m[1]}"/>`) });
  }
  return out;
}

// Chromium's raster of one drawing can differ by a few edge pixels between two places on a page (its tiles), so each
// drawing of an item is drawn in turn in the same cell, and the screenshots compared at the same coordinates.
async function run(browser, list, dpr, sheet, pngDir) {
  const ctx = await browser.newContext({ viewport: { width: 160, height: 800 }, deviceScaleFactor: dpr });
  const page = await ctx.newPage();
  const sprite = `<svg class="oa-sprite" aria-hidden="true" focusable="false" width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden">${Object.values(sheet.symbols).map((s) => s.symbol).join('')}</svg>`;
  const results = [];
  const CH = 30;                                  // items per page
  const live = list.filter((x) => x.kind !== 'missing');
  for (let k = 0; k < live.length; k += CH) {
    const chunk = live.slice(k, k + CH);
    const boxes = []; let y = 0;
    for (const it of chunk) { const w = it.px + 8; boxes.push({ y, w }); y += w + 8; }
    const turns = Math.max(...chunk.map((it) => it.refs.length + 1));
    const shots = [];
    for (let v = 0; v < turns; v++) {
      const cells = chunk.map((it, i) => {
        const all = it.refs.concat([it.test]); const c = all[Math.min(v, all.length - 1)];
        return `<div style="position:absolute;left:0;top:${boxes[i].y}px;width:${boxes[i].w}px;height:${boxes[i].w}px;display:grid;place-items:center;line-height:0;color:${INK}">${c}</div>`;
      }).join('');
      await page.setContent(`<!doctype html><html><head><style>html,body{margin:0;background:${GROUND}}svg{display:block}${SHELL_SWITCH ? SHELL_SWITCH[0] : ''}</style></head><body>${sprite}<div style="position:relative;height:${y}px">${cells}</div></body></html>`);
      shots.push((await page.screenshot({ fullPage: true, animations: 'disabled' })).toString('base64'));
    }
    const diffs = await page.evaluate(async ({ shots, boxes, dpr, n }) => {
      const dec = async (s) => { const im = new Image(); im.src = 'data:image/png;base64,' + s; await im.decode(); const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const g = c.getContext('2d'); g.drawImage(im, 0, 0); return g; };
      const gs = await Promise.all(shots.map(dec));
      const cell = (g, b) => g.getImageData(0, Math.round(b.y * dpr), Math.round(b.w * dpr), Math.round(b.w * dpr)).data;
      const diff = (a, b) => { let max = 0, off = 0; for (let i = 0; i < a.length; i += 4) { let m = 0; for (let j = 0; j < 3; j++) m = Math.max(m, Math.abs(a[i + j] - b[i + j])); if (m > max) max = m; if (m > 8) off++; } return { max, off }; };
      // each reference against the test, which is the last turn the item drew
      return boxes.map((b, i) => { const last = n[i]; const t = cell(gs[last], b); const r = []; for (let v = 0; v < last; v++) r.push(diff(cell(gs[v], b), t)); return r; });
    }, { shots, boxes, dpr, n: chunk.map((it) => it.refs.length) });
    chunk.forEach((it, i) => results.push({ it, d: diffs[i] }));
    if (pngDir && diffs.some((d, i) => chunk[i].kind === 'symbol' && d[0].max > TOL)) shots.forEach((s, v) => fs.writeFileSync(path.join(pngDir, `chunk-${k / CH}-${dpr}x-turn-${v}.png`), Buffer.from(s, 'base64')));
  }
  await ctx.close();
  return results;
}

(async () => {
  const o = args();
  const tmp = fs.mkdtempSync(path.join(process.env.TMPDIR || os.tmpdir(), 'oa-sprite-check-'));
  const sheetPath = path.join(tmp, 'sheet.json');
  try {
    execFileSync('python3', ['-I', path.join(__dirname, 'guide_build.py'), '--sprite-sheet', sheetPath].concat(o.root ? ['--sprite-root', o.root] : []), { stdio: 'pipe' });
  } catch (e) { if (!fs.existsSync(sheetPath)) { console.error(String(e.stdout || e.message)); process.exit(2); } }
  const sheet = JSON.parse(fs.readFileSync(sheetPath, 'utf8'));
  fs.rmSync(tmp, { recursive: true, force: true });
  const list = items(sheet);
  const browser = await chromium.launch();
  const report = { checked: new Date().toISOString(), root: sheet.root, tolerance: TOL, missingFolders: sheet.missing, buildWarnings: sheet.warnings, scales: {}, failures: [] };
  for (const w of sheet.warnings) report.failures.push(`the build reading the families: [${w.where}] ${w.message}`);
  if (o.png) fs.mkdirSync(o.png, { recursive: true });
  for (const dpr of [1, 1.5, 2]) {   // at 1.5 only the pattern, which must still draw the fit there
    const res = await run(browser, dpr === 1.5 ? list.filter((x) => x.kind === 'pattern') : list, dpr, sheet, o.png);
    const by = {};
    for (const r of res.filter((x) => x.it.kind === 'symbol')) {
      const fam = sheet.symbols[r.it.sid].family; const k = `${fam} ${r.it.edition}`;
      by[k] = by[k] || { pairs: 0, largest: 0, pixelsOff: 0 };
      by[k].pairs++; by[k].largest = Math.max(by[k].largest, r.d[0].max); by[k].pixelsOff += r.d[0].off;
      if (r.d[0].max > TOL) report.failures.push(`${dpr}x: ${r.it.label} (${r.it.edition}, ${r.it.px} px) through <use> differs from its file by up to ${r.d[0].max} in ${r.d[0].off} pixel(s)`);
    }
    const pat = res.filter((r) => r.it.kind === 'pattern').map((r) => {
      const [fit, master] = r.d; const want = dpr < 2 ? fit : master; const other = dpr < 2 ? master : fit;
      const ok = want.max <= TOL && other.max > TOL;
      if (!ok) report.failures.push(`${dpr}x: the ${r.it.label} pattern does not draw the ${dpr < 2 ? 'fit' : 'master'} alone (against the fit ${fit.max}, the master ${master.max})`);
      return { icon: r.it.label, draws: dpr < 2 ? 'fit' : 'master', againstFit: fit.max, againstMaster: master.max, ok };
    });
    report.scales[`${dpr}x`] = { families: by, pattern: pat };
  }
  for (const r of list.filter((x) => x.kind === 'missing')) report.failures.push(`${r.label}: no ${r.edition} file (${r.file})`);
  await browser.close();
  report.pass = report.failures.length === 0;
  if (o.json) fs.writeFileSync(o.json, JSON.stringify(report, null, 1));
  const counts = Object.entries(sheet.symbols).reduce((a, [, s]) => (a[s.family] = (a[s.family] || 0) + 1, a), {});
  console.log(`${report.pass ? 'PASS' : 'FAIL'} sprite check: ${Object.entries(counts).map(([f, n]) => `${f} ${n}`).join(', ')} symbols, from ${path.relative(ROOT, sheet.root) || sheet.root}`);
  for (const [s, v] of Object.entries(report.scales)) {
    if (Object.keys(v.families).length) console.log(`  ${s}: ` + Object.entries(v.families).map(([k, x]) => `${k} ${x.pairs} pairs, largest difference ${x.largest}`).join('; '));
    if (v.pattern.length) {
      const span = (k) => `${Math.min(...v.pattern.map((p) => p[k]))} to ${Math.max(...v.pattern.map((p) => p[k]))}`;
      console.log(`  ${s} pattern: ${v.pattern.filter((p) => p.ok).length} of ${v.pattern.length} draw the ${v.pattern[0].draws} alone `
        + `(largest difference against the fit ${span('againstFit')}, against the master ${span('againstMaster')})`);
      for (const p of v.pattern.filter((x) => !x.ok)) console.log(`    WRONG ${p.icon}: against the fit ${p.againstFit}, the master ${p.againstMaster}`);
    }
  }
  for (const f of report.failures.slice(0, 40)) console.log('  - ' + f);
  if (report.failures.length > 40) console.log(`  ... and ${report.failures.length - 40} more`);
  process.exit(report.pass ? 0 : 1);
})();
