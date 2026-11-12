#!/usr/bin/env node
// The chart kit's one command (contract C3). Builds a chart from its spec and data file, runs its checks, and writes the
// exports and captures.
//
//   node work/build/chart-kit/oa-chart.mjs build <ID|spec path>... [--all] [--widths 1440,390] [--grounds newsprint,charcoal]
//                                          [--out DIR] [--no-png] [--date YYYYMMDD] [--specs DIR]
//   node work/build/chart-kit/oa-chart.mjs check <ID|spec path>... [--all]
//   build and check also draw every whole width from 256 px (224 for a rule plate) to 723 px on Newsprint, the sweep
//   (AX S1); --no-sweep leaves it out
//   node work/build/chart-kit/oa-chart.mjs fragments --in LIST.json --out OUT.json     (guide_build.py's hook)
//   node work/build/chart-kit/oa-chart.mjs figure <spec path> --svg DESK.svg [--phone-svg PHONE.svg] [--id FID] [--out FILE]
//                                          a drawing made outside the kit, set in the kit's figure (ED-E9, round 1 fix pass)
//   node work/build/chart-kit/oa-chart.mjs self-test
//
// It never reads source/ or writes into the repository unless --out names a folder there.
import fs from 'fs';
import path from 'path';
import zlib from 'zlib';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import { minify } from './tools/minify.mjs';

const require = createRequire(import.meta.url);
const KIT = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(KIT, '../../..');
const SCRATCH = '/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/engineer/kit-out';
const TOKENS_CSS = path.join(ROOT, 'work/build/tokens/tokens.css');
const FONTS = path.join(ROOT, 'work/build/assets/fonts');

export function load_kit() {
  require(path.join(KIT, 'metrics.js'));
  require(path.join(KIT, 'kit.js'));
  require(path.join(KIT, 'parts.js'));
  require(path.join(KIT, 'geo.js'));
  for (const f of fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js')).sort()) require(path.join(KIT, 'forms', f));
  const K = globalThis.OAChart;
  K.words = JSON.parse(fs.readFileSync(path.join(KIT, 'words.json'), 'utf8'));
  return K;
}
const K = load_kit();
const C = require(path.join(KIT, 'checks.js'));
K.id_types = C.id_types();
const CSS = fs.readFileSync(TOKENS_CSS, 'utf8');
export const TOK = { newsprint: K.tokens_from_css(CSS, 'newsprint'), charcoal: K.tokens_from_css(CSS, 'charcoal') };

// page width -> the width the figure's drawing gets (the page's gutters: 16 px under 600, 32 px from 600)
export function container(page, spec) {
  const t = K.token_reader(TOK.newsprint);
  const art = K.artboard(spec, t);
  const gutter = page < 600 ? 16 : 32;
  return Math.min(art, page - 2 * gutter);
}

function args(argv) {
  const o = { _: [], widths: [1440, 390], grounds: ['newsprint', 'charcoal'], out: SCRATCH, png: true, date: null, specs: path.join(KIT, 'specs'), sweep: true };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--all') o.all = true;
    else if (a === '--widths') o.widths = argv[++i].split(',').map(Number);
    else if (a === '--grounds') o.grounds = argv[++i].split(',');
    else if (a === '--out') o.out = path.resolve(argv[++i]);
    else if (a === '--no-png') o.png = false;
    else if (a === '--no-sweep') o.sweep = false;
    else if (a === '--sweep') o.sweep = true;
    else if (a === '--png') o.png = true;
    else if (a === '--date') o.date = argv[++i];
    else if (a === '--specs') o.specs = path.resolve(argv[++i]);
    else if (a === '--in') o.in = argv[++i];
    else if (a === '--svg') o.svg = argv[++i];
    else if (a === '--phone-svg') o.phone_svg = argv[++i];
    else if (a === '--id') o.id = argv[++i];
    else o._.push(a);
  }
  if (!o.date) { const d = new Date(); o.date = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`; }
  return o;
}

export function spec_path(x, dir) {
  if (/\.json$/.test(x)) return path.resolve(x);
  return path.join(dir || path.join(KIT, 'specs'), x.toLowerCase() + '.json');
}

function title_case(s) {
  return String(s).replace(/[^A-Za-z0-9 ]+/g, ' ').trim().split(/\s+/).map(w => w[0].toUpperCase() + w.slice(1)).join('-');
}
export function file_stem(spec, date) {
  const form = (K.forms[spec.form] && K.forms[spec.form].name) || spec.form.replace(/-/g, ' ');
  return `${date}_${spec.id.toUpperCase()}-${title_case(form)}`;
}

// The rows of a spec's second and later datasets, by name, every row (a form filters them itself)
export function extra_rows(chk) {
  const out = {};
  (chk.datasets || []).slice(1).forEach(ds => { out[ds.file.replace(/\.(csv|json)$/, '')] = C.rows_of(K, ds); });
  return out;
}
// R-B11 (round 1): a spec's second and later datasets ride in the island only for a form that reads them (c.extra, or
// extra: true in its registration); S05's gap-margin file went to the page for nothing
export function reads_extra(form) {
  const def = K.forms[form];
  return !!def && (def.extra === true || /\bc\.extra\b/.test(String(def.draw)));
}
function extra_island(res) {
  const out = {};
  if (!res.spec_form || !reads_extra(res.spec_form)) return out;
  (res.datasets || []).slice(1).forEach(ds => {
    const cols = Object.keys(ds.meta.columns), ct = {};
    cols.forEach(c => { ct[c] = { type: ds.meta.columns[c].type }; });
    out[ds.file.replace(/\.(csv|json)$/, '')] = { columns: ct, csv: C.to_csv(C.rows_of(K, ds), cols) };
  });
  return out;
}

// access N2 (second pass): every width the strict build draws a chart at, measured in Chromium at 1440, 1024, 390, 360 and
// 320 px: an entry's chart at 720, 558, 326, 296 and 256 (326 was not checked); a rule plate's at 675, 639, 510, 474, 325,
// 294, 264, 243 and 224, its stage padded inside the plate (chapters 13 and 14)
export const GUIDE_WIDTHS = [656, 558, 358, 326, 296, 256];
export const PLATE_WIDTHS = [675, 639, 510, 474, 325, 294, 264, 243, 224];
export function guide_widths(spec) {
  return /^s-1[34]-(?!s\d)/i.test(String(spec.id)) ? GUIDE_WIDTHS.concat(PLATE_WIDTHS) : GUIDE_WIDTHS;
}

// AX S1 (round 2 fix pass, D3-904): the guide draws an entry's chart at any whole width from 256 px (a 320 px screen at
// 400 percent zoom) to 723 px, and a rule plate's from 224 px; the six columns above miss widths a phone or tablet gives
// (329 px at a 393 px phone, 560 px at a 768 px tablet). The sweep draws every whole width in that range on Newsprint and
// runs the drawing checks on each; one fault at many widths prints once, with the widths it holds at.
export const SWEEP_MAX = 723;
export function sweep_range(spec) {
  const hi = Math.min(SWEEP_MAX, K.artboard(spec, K.token_reader(TOK.newsprint)));
  return [Math.min(...guide_widths(spec)), hi];
}
function span_list(ws) {
  // 329, 330, 331, 560 -> "329 to 331, 560"
  const out = [];
  for (let i = 0; i < ws.length; i++) {
    let j = i;
    while (j + 1 < ws.length && ws[j + 1] === ws[j] + 1) j++;
    out.push(j > i ? `${ws[i]} to ${ws[j]}` : String(ws[i]));
    i = j;
  }
  return out.join(', ');
}
export function sweep_faults(spec, rows, extra) {
  const [lo, hi] = sweep_range(spec), seen = new Map(), skip = new Set(GUIDE_WIDTHS.concat(PLATE_WIDTHS));
  for (let w = lo; w <= hi; w++) {
    if (skip.has(w)) continue;   // checked already, with the guide's columns
    let f;
    try {
      const d = K.draw(spec, rows, { width: w, ground: 'newsprint', tokens: TOK.newsprint, extra });
      f = C.check_drawing(spec, d, TOK.newsprint, '');
    } catch (e) { f = [`draw: ${e.message}`]; }
    for (const x of f) {
      // one fault at many widths is one fault: its words with the figures read as one
      const k = x.replace(/-?\d+(?:\.\d+)?/g, '#');
      if (!seen.has(k)) seen.set(k, { first: x, ws: [] });
      const ws = seen.get(k).ws;
      if (ws[ws.length - 1] !== w) ws.push(w);
    }
  }
  return [...seen.values()].map(v => `sweep: ${v.first.replace(/ \(\)$/, '')} (at ${v.ws.length} of the widths from ${lo} to ${hi} px: ${span_list(v.ws)})`);
}

// One spec, checked and drawn in Node at every width and ground
export function run_spec(spec, o) {
  const res = { id: spec.id, faults: [], drawings: [], spec_path: o.spec_path, spec_form: spec.form };
  let chk;
  try { chk = C.check_spec(K, spec, o); } catch (e) { res.faults.push('spec: ' + e.message); return res; }
  res.faults.push(...chk.faults);
  res.rows = chk.rows;
  res.datasets = chk.datasets;
  if (!K.forms[spec.form] || !chk.rows || !chk.rows.length) return res;
  for (const g of o.grounds) for (const w of o.widths) {
    const cw = container(w, spec);
    let d;
    try { d = K.draw(spec, chk.rows, { width: cw, ground: g, tokens: TOK[g], extra: extra_rows(chk) }); } catch (e) { res.faults.push(`draw at ${w} on ${g}: ${e.message}`); continue; }
    const where = `${g} ${w}`;
    res.faults.push(...C.check_drawing(spec, d, TOK[g], where));
    res.drawings.push({ ground: g, page: w, width: d.width, height: d.height, svg: d.svg, bytes: Buffer.byteLength(d.svg) });
  }
  if (!o.no_narrow) {
    // every column width the guide and zoom give a chart (D3-93), checked and never exported: 656 px (200 percent text at
    // 1440), 558 (1024), 358 (390), 296 (360) and 256 (320 px reflow); chapter 13's narrower plates add 243 and 224
    for (const w of guide_widths(spec)) {
      if (w > K.artboard(spec, K.token_reader(TOK.newsprint))) continue;
      try {
        const d = K.draw(spec, chk.rows, { width: w, ground: 'newsprint', tokens: TOK.newsprint, extra: extra_rows(chk) });
        res.faults.push(...C.check_drawing(spec, d, TOK.newsprint, `a ${w} px guide column`));
      } catch (e) { res.faults.push(`draw at a ${w} px guide column: ${e.message}`); }
    }
    // the sweep (AX S1): every other whole width an entry or plate can draw at; build and check run it unless --no-sweep
    if (o.sweep) res.faults.push(...sweep_faults(spec, chk.rows, extra_rows(chk)));
  }
  return res;
}

function font_css() {
  const fam = { 'Inter': ['inter/20261111_Inter-Latin.woff2', 'inter/20261111_Inter-Latin-Ext.woff2'], 'Inter Tight': ['inter-tight/20261111_Inter-Tight-Latin.woff2', 'inter-tight/20261111_Inter-Tight-Latin-Ext.woff2'] };
  return Object.entries(fam).map(([f, files]) => files.map(x => `@font-face{font-family:"${f}";src:url(data:font/woff2;base64,${fs.readFileSync(path.join(FONTS, x)).toString('base64')}) format("woff2");font-weight:100 900;font-display:block}`).join('\n')).join('\n');
}

export function used_columns(spec, columns) {
  // the columns a spec names anywhere (encode, table, pivot, where, sort, formats, a label's {placeholder}): load-trim keeps only these
  const names = new Set(Object.keys(columns));
  const used = new Set();
  const visit = (v, key) => {
    if (typeof v === 'string') {
      if (names.has(v)) used.add(v);
      for (const m of v.matchAll(/\{([a-z0-9_]+)\}/g)) if (names.has(m[1])) used.add(m[1]);
    } else if (Array.isArray(v)) v.forEach(x => visit(x));
    else if (v && typeof v === 'object') for (const k of Object.keys(v)) { if (names.has(k) && key !== 'labels') used.add(k); visit(v[k], k); }
  };
  ['encode', 'table', 'where', 'sort', 'formats', 'labels', 'annotations'].forEach(k => visit(spec[k], k));
  return Object.keys(columns).filter(c => used.has(c));
}

// The keys a page needs to draw: no words the figure already prints (method load-table)
const DRAW_KEYS = ['kit', 'id', 'form', 'artboard', 'encode', 'labels', 'annotations', 'formats', 'scale', 'table', 'phone'];
export function draw_spec(spec) {
  const out = {};
  DRAW_KEYS.forEach(k => { if (spec[k] !== undefined) out[k] = spec[k]; });
  if (out.table) out.table = Object.assign({}, out.table, { caption: undefined });
  if (spec.form === 'social-data-card') ['evidence_label', 'title', 'source_line'].forEach(k => { out[k] = spec[k]; });
  return out;
}
export function table_fields(spec) {
  const tb = spec.table || {};
  if (tb.pivot) return [].concat(tb.pivot.row, [tb.pivot.column, tb.pivot.value]);
  return (tb.columns || []).map(c => c.field);
}
export function island_table(spec, rows, columns, extra) {
  // method load-table: the drawing spec, the types of the columns it uses, and as CSV only the used columns the table lacks
  const used = used_columns(spec, columns), inTable = new Set(table_fields(spec));
  const missing = used.filter(c => !inTable.has(c));
  const ctypes = {};
  used.concat([...inTable]).forEach(c => { if (columns[c]) ctypes[c] = { type: columns[c].type }; });
  const payload = { mode: 'table', spec: draw_spec(spec), columns: ctypes };
  if (extra && Object.keys(extra).length) payload.extra = extra;
  if (missing.length) payload.csv = C.to_csv(rows, missing);
  const carry = K.lean_carry(spec, rows, columns);
  if (Object.keys(carry).length) payload.carry = carry;
  return island_element(payload);
}

// The island carried compressed (DR-238): its JSON deflated (raw, level 9) and written as base64 in a data block the
// browser never runs, <script type="text/plain" data-oa-chart-data="deflate">. The kit inflates it at load (K.island);
// only the script reads it, so a reader with scripts off loses nothing. Each island is inflated again here by the kit's
// own inflater and must give back its JSON, or the build stops.
export function island_element(payload) {
  const json = JSON.stringify(payload);
  const z = zlib.deflateRawSync(Buffer.from(json, 'utf8'), { level: 9, memLevel: 9 }).toString('base64');
  if (K.island_text(z, 'deflate') !== json) throw new Error('the kit could not inflate a data island back to its JSON');
  return '<script type="text/plain" data-oa-chart-data="deflate">' + z + '</script>';
}

export function island(spec, rows, columns, trim) {
  // the data a page draws from: the spec, the column types and the rows as CSV (the lightest text form); trim keeps
  // only the columns the spec names
  const cols = trim ? used_columns(spec, columns) : Object.keys(columns);
  const ctypes = {};
  cols.forEach(c => { ctypes[c] = { type: columns[c].type }; });
  const lean = Object.assign({}, spec);
  delete lean.notes_internal;
  const payload = { spec: trim ? lean : spec, columns: trim ? ctypes : columns, csv: C.to_csv(rows, cols) };
  return island_element(payload);
}

// The kit as a page carries it: minified by tools/minify.mjs (every comment and needless space dropped, nothing renamed),
// so the same code runs in the page and in Node; tools/kit_snapshot.mjs proves the drawings identical (weight pass).
// strip() is the round 0 pilot's lighter pass, kept for comparison.
export function strip(js) {
  return js.replace(/^\s*\/\*[\s\S]*?\*\/\s*$/gm, '').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('//')).join('\n');
}
export function kit_parts() {
  const forms = fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js')).sort();
  const core = ['metrics.js', 'kit.js', 'parts.js'].map(f => minify(fs.readFileSync(path.join(KIT, f), 'utf8'))).join('');
  return { core, geo: minify(fs.readFileSync(path.join(KIT, 'geo.js'), 'utf8')), forms: Object.fromEntries(forms.map(f => [f, minify(fs.readFileSync(path.join(KIT, 'forms', f), 'utf8'))])),
    css: fs.readFileSync(path.join(KIT, 'kit.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '').split('\n').map(l => l.trim()).filter(Boolean).join('\n') };
}
export function kit_scripts() {
  const k = kit_parts();
  return [k.core, k.geo].concat(Object.values(k.forms)).join('').replace(/<\/script/gi, '<\\/script');
}
export function kit_scripts_full() {
  const forms = fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js')).sort().map(f => fs.readFileSync(path.join(KIT, 'forms', f), 'utf8'));
  return [fs.readFileSync(path.join(KIT, 'metrics.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'kit.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'parts.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'geo.js'), 'utf8')].concat(forms).join('\n').replace(/<\/script/gi, '<\\/script');
}

function page_html(specs) {
  // specs: [{spec, rows, columns, grounds, extra}]
  // a plain page: tokens.css, kit.css, the kit and its forms, and each figure with its data island (DR-235)
  const body = specs.map(({ spec, rows, columns, grounds, extra }) => grounds.map(g => `<section class="oa-surface-${g} oac-ground" data-ground="${g}">
${(f => f.slice(0, f.lastIndexOf('</figure>')) + island_table(spec, rows, columns, extra) + '</figure>')(K.figure(spec, rows, { id: `oac-${spec.id.toLowerCase()}-${g}`, lean_table: true, types: columns }))}
</section>`).join('\n')).join('\n');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chart kit build</title><style>${font_css()}</style><style>${CSS}</style><style>${fs.readFileSync(path.join(KIT, 'kit.css'), 'utf8')}</style>
<style>body{margin:0}.oac-ground{padding:32px 32px 40px}@media (max-width:599px){.oac-ground{padding:24px 16px 32px}}.oac-fig[data-wide]{max-width:var(--oa-chart-artboard-wide)}</style>
</head><body>
${body}
<script>OAChart_words=${JSON.stringify(K.words)};</script>
<script>${kit_scripts()}
OAChart.words = OAChart_words;
OAChart.lookup_in_place = false;   // the build page shows each lookup's still drawing, which its PNG export and captures are made from</script>
</body></html>`;
}

function png_size(buf) { return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }; }

async function captures(items, o) {
  const { chromium } = require('/opt/node-tools/node_modules/playwright');
  const browser = await chromium.launch();
  try {
    for (const it of items) {
      const { spec, res } = it;
      const dir = path.join(o.out, spec.id.toLowerCase());
      const html = page_html([{ spec, rows: res.rows, columns: res.datasets.length ? res.datasets[0].meta.columns : (spec.data || {}).columns, grounds: o.grounds, extra: extra_island(res) }]);
      const page_file = path.join(dir, spec.id.toLowerCase() + '.html');
      fs.writeFileSync(page_file, html);
      const stem = file_stem(spec, o.date);
      for (const w of o.widths) {
        for (const dpr of [1, 2]) {
          const ctx = await browser.newContext({ viewport: { width: w, height: 1000 }, deviceScaleFactor: dpr });
          const p = await ctx.newPage();
          const errors = [];
          p.on('pageerror', e => errors.push(String(e)));
          await p.goto('file://' + page_file);
          await p.evaluate(() => document.fonts.ready);
          // charts draw as they near the screen (D3-97); a check draws them all first
          await p.evaluate(() => window.OAChart && OAChart.draw_all && OAChart.draw_all());
          await p.waitForFunction(() => Array.from(document.querySelectorAll('figure.oac-fig')).every(f => f.getAttribute('data-oa-drawn') || f.getAttribute('data-oa-error')), null, { timeout: 15000 });
          errors.forEach(e => res.faults.push(`page error at ${w}: ${e}`));
          for (const g of o.grounds) {
            const fid = `#oac-${spec.id.toLowerCase()}-${g}`;
            const node = res.drawings.find(d => d.ground === g && d.page === w);
            const info = await p.evaluate(({ fid, node_svg, title, alt, fonts_note }) => {
              const f = document.querySelector(fid);
              const err = f.getAttribute('data-oa-error');
              const svg = f.querySelector('svg.oac-svg');
              const tb = f.querySelector('table.oac-table');
              const out = { err, rows: tb && tb.hasAttribute('data-oa-lean') ? (tb.querySelector('tbody th[scope=row]') && tb.querySelectorAll('thead th').length > 1 && tb.querySelectorAll('tbody td[data-x]').length + tb.querySelectorAll('tbody td').length !== tb.querySelectorAll('tbody tr').length * (tb.querySelectorAll('thead th').length - 1) ? 0 : 0) : f.querySelectorAll('[data-oa-row]').length };
              if (tb && tb.hasAttribute('data-oa-lean')) out.rows = (isl => window.OAChart.rows_from_table(tb, isl.spec, isl))(window.OAChart.island(f.querySelector('script[data-oa-chart-data]'))).length;
              if (!svg) return out;
              const clone = svg.cloneNode(true);
              clone.removeAttribute('aria-describedby');
              const ser = new XMLSerializer();
              const a = ser.serializeToString(clone);
              const b = node_svg ? ser.serializeToString(new DOMParser().parseFromString(node_svg, 'image/svg+xml').documentElement) : null;
              const norm = x => x ? x.replace(/ aria-labelledby="[^"]*"/g, '').replace(/<title>.*?<\/title>|<desc>.*?<\/desc>/gs, '').replace(/<style>.*?<\/style>/gs, '').replace(/ oac-u-[a-z0-9-]+/g, '').replace(/<pattern id="[^"]*-fc-[^"]*".*?<\/pattern>/gs, '').replace(/<defs><\/defs>/g, '').replace(/oac-[a-z0-9-]*?-(\d+)-([a-z0-9]+)/g, 'U-$1-$2') : x;
              out.parity = norm(a) === norm(b);
              out.width = svg.getAttribute('width');
              // the standalone export: computed colors and type written on each element, no classes, title and desc kept
              const ex = svg.cloneNode(true);
              const src = svg.querySelectorAll('*'), dst = ex.querySelectorAll('*');
              const props = ['fill', 'stroke', 'stroke-width', 'stroke-dasharray', 'stroke-linejoin', 'stroke-linecap', 'paint-order', 'font-family', 'font-weight', 'font-size', 'letter-spacing', 'font-variant-numeric', 'opacity'];
              for (let i = 0; i < src.length; i++) {
                if (/^(title|desc|tspan|defs|pattern)$/i.test(src[i].tagName) && !/^tspan$/i.test(src[i].tagName)) continue;
                const cs = getComputedStyle(src[i]);
                for (const pr of props) {
                  let v = cs.getPropertyValue(pr);
                  if (!v || v === 'normal' && pr !== 'font-weight') continue;
                  if (pr === 'font-family') v = v.replace(/"/g, "'");
                  dst[i].setAttribute(pr, v);
                }
                dst[i].removeAttribute('class');
              }
              ex.removeAttribute('class');
              // a standalone file names itself: the spec's title and alt as the SVG's title and desc
              const NS = 'http://www.w3.org/2000/svg';
              if (!ex.querySelector(':scope > desc') && alt) { const d = document.createElementNS(NS, 'desc'); d.textContent = alt; ex.insertBefore(d, ex.firstChild); }
              if (!ex.querySelector(':scope > title') && title) { const t = document.createElementNS(NS, 'title'); t.textContent = title; ex.insertBefore(t, ex.firstChild); }
              // the file names its fonts and says they are needed (D3-102, access S9); embedding them waits for Phase 5's package
              const dd = ex.querySelector(':scope > desc');
              if (dd && fonts_note) dd.textContent = dd.textContent + ' ' + fonts_note;
              ex.setAttribute('data-fonts', 'Inter, Inter Tight');
              ex.querySelectorAll('style').forEach(st => st.remove());
              ex.removeAttribute('aria-describedby');
              ex.removeAttribute('aria-labelledby');
              ex.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
              const bg = getComputedStyle(f.closest('.oac-ground')).backgroundColor;
              const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
              rect.setAttribute('width', '100%'); rect.setAttribute('height', '100%'); rect.setAttribute('fill', bg);
              const firstMark = ex.querySelector(':scope > :not(title):not(desc):not(defs)');
              ex.insertBefore(rect, firstMark);
              out.export = '<?xml version="1.0" encoding="UTF-8"?>\n' + ser.serializeToString(ex);
              out.bg = bg;
              const back = new DOMParser().parseFromString(out.export, 'image/svg+xml');
              out.export_ok = !back.querySelector('parsererror') && !!back.querySelector('svg > title') && !!back.querySelector('svg > desc') && out.export.indexOf('var(') < 0 && out.export.indexOf(' class=') < 0;
              return out;
            }, { fid, node_svg: node ? node.svg : null, title: spec.title, alt: spec.alt, fonts_note: K.words.export_fonts });
            if (info.err) { res.faults.push(`page: ${g} ${w}: ${info.err}`); continue; }
            if (dpr === 1) {
              if (!info.parity) res.faults.push(`parity: the page's drawing at ${w} on ${g} differs from the Node drawing the exports use`);
              const t = K.table_rows(spec, res.rows);
              const want = t.pivot ? Object.keys(t.cell).length : t.rows.length;
              if (info.rows !== want) res.faults.push(`table: the page shows ${info.rows} table rows or cells for ${want} data rows (${g} ${w})`);
              if (!info.export_ok) res.faults.push(`svg export: not standalone or no title and desc (${g} ${w})`);
              fs.writeFileSync(path.join(dir, `${stem}-${title_case(g)}-${w}.svg`), info.export);
              const fig = await p.$(fid);
              await fig.screenshot({ path: path.join(dir, `${spec.id.toLowerCase()}-${g}-${w}.png`) });
              await p.addStyleTag({ content: 'html{filter:grayscale(1)}' });
              await fig.screenshot({ path: path.join(dir, `${spec.id.toLowerCase()}-${g}-${w}-grayscale.png`) });
              await p.addStyleTag({ content: 'html{filter:none}' });
            } else {
              const svgEl = await p.$(fid + ' svg.oac-svg');
              const pf = path.join(dir, `${stem}-${title_case(g)}-${w}.png`);
              await svgEl.screenshot({ path: pf, omitBackground: false });
              const sz = png_size(fs.readFileSync(pf));
              const want = { w: 2 * node.width, h: 2 * node.height };
              if (sz.w !== want.w || sz.h !== want.h) res.faults.push(`png: ${path.basename(pf)} is ${sz.w} by ${sz.h}, expected ${want.w} by ${want.h}`);
            }
          }
          await ctx.close();
        }
      }
    }
  } finally {
    await browser.close();
  }
}

async function build(o, check_only) {
  let paths = o._.map(x => spec_path(x, o.specs));
  if (o.all) paths = fs.readdirSync(o.specs).filter(f => /^s\d+\.json$/.test(f)).sort().map(f => path.join(o.specs, f));
  if (!paths.length) { console.error('name a spec, or --all'); return 2; }
  const items = [];
  let bad = 0;
  for (const p of paths) {
    let spec;
    try { spec = JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { console.log(`FAIL ${path.basename(p)}: ${e.message}`); bad++; continue; }
    const res = run_spec(spec, Object.assign({}, o, { spec_path: p }));
    items.push({ spec, res, p });
  }
  if (!check_only) {
    for (const { spec, res } of items) {
      const dir = path.join(o.out, spec.id.toLowerCase());
      fs.mkdirSync(dir, { recursive: true });
      if (res.rows && res.datasets.length) {
        const cols = Object.keys(res.datasets[0].meta.columns);
        const csv = C.to_csv(res.rows, cols);
        const cf = path.join(dir, `${file_stem(spec, o.date)}.csv`);
        fs.writeFileSync(cf, csv);
        res.faults.push(...C.check_csv(K, fs.readFileSync(cf, 'utf8'), res.rows, res.datasets[0].meta));
      }
    }
    if (o.png) {
      await captures(items.filter(i => i.res.drawings.length), o);
      // the grayscale proofs are exact gray (R = G = B), so one 8-bit channel holds the same pixels at half the bytes (E24)
      const { spawnSync } = require('child_process');
      const dirs = items.map(i => path.join(o.out, i.spec.id.toLowerCase()));
      const py = "import sys,glob\nfrom PIL import Image\nfor d in sys.argv[1:]:\n    for f in glob.glob(d+'/*-grayscale.png'):\n        im=Image.open(f)\n        if im.mode!='L': im.convert('L').save(f, optimize=True)";
      const r = spawnSync('python3', ['-I', '-c', py, ...dirs], { encoding: 'utf8' });
      if (r.status !== 0) console.log('grayscale proofs stay RGB: ' + (r.stderr || '').slice(0, 200));
    }
  }
  for (const { spec, res } of items) {
    const summary = { id: spec.id, form: spec.form, spec: path.relative(ROOT, res.spec_path), rows: res.rows ? res.rows.length : 0,
      drawings: res.drawings.map(d => ({ ground: d.ground, page: d.page, width: d.width, height: d.height, svg_bytes: d.bytes })), faults: res.faults };
    if (!check_only) fs.writeFileSync(path.join(o.out, spec.id.toLowerCase(), `${spec.id.toLowerCase()}-check.json`), JSON.stringify(summary, null, 1));
    console.log(`${res.faults.length ? 'FAIL' : 'PASS'} ${spec.id} ${spec.form}: ${summary.rows} rows, ${res.drawings.length} drawings, ${res.faults.length} faults`);
    res.faults.slice(0, 40).forEach(f => console.log('  - ' + f));
    if (res.faults.length) bad++;
  }
  // say where the files went, so a reader who does not code can find them (editor's read, K7)
  if (!check_only) console.log(`wrote: ${o.out}, one folder per spec (its pages, SVG, PNG and CSV exports, captures and check file)`);
  return bad ? 1 : 0;
}

export const GUIDE_NOTE_FAULTS = [/^layout: a /, /^chart: Pillar Red covers /];
// guide_build.py's hook: draw each listed spec for the page, by the chosen method, and return the fragments and faults
async function fragments(o) {
  const list = JSON.parse(fs.readFileSync(o.in, 'utf8'));
  const kp = kit_parts();
  const out = { kit_js: kit_scripts(), kit_css: kp.css, words: K.words, items: {},
    kit_sizes: { core: Buffer.byteLength(kp.core), geo: Buffer.byteLength(kp.geo), css: Buffer.byteLength(kp.css), forms: Object.fromEntries(Object.entries(kp.forms).map(([k, v]) => [k, Buffer.byteLength(v)])),
      registered: Object.keys(K.forms).length } };
  for (const it of list.items) {
    const spec = JSON.parse(fs.readFileSync(it.spec, 'utf8'));
    if (it.phone_view) spec.phone_view = true;   // D3-487: the build asks for the phone drawing beside an entry's chart
    const res = run_spec(spec, { grounds: [it.ground || 'newsprint'], widths: it.widths || [1440, 390], spec_path: it.spec });
    const columns = res.datasets && res.datasets.length ? res.datasets[0].meta.columns : (spec.data || {}).columns || {};
    const fid = it.fid || ('oac-' + spec.id.toLowerCase());
    let html;
    if (!res.rows || !res.rows.length) html = '';
    else if (list.method === 'lean') {
      // lean inline SVG: the desktop drawing, and a phone drawing that the page's CSS switches to under 480 px
      const desk = res.drawings.find(d => d.page >= 600), ph = res.drawings.find(d => d.page < 600);
      let svg = desk ? desk.svg.replace('class="oac-svg"', 'class="oac-svg oac-desk"') : '';
      if (ph) svg += ph.svg.replace('class="oac-svg"', 'class="oac-svg oac-phone"');
      html = K.figure(spec, res.rows, { id: fid, svg, art_attrs: ' data-oa-lean', guide: true });
    } else if (list.method === 'load-table') {
      html = K.figure(spec, res.rows, { id: fid, lean_table: true, types: columns, guide: true });
      html = html.slice(0, html.lastIndexOf('</figure>')) + island_table(spec, res.rows, columns, extra_island(res)) + '</figure>';
    } else {
      const isl = island(spec, res.rows, columns, list.method === 'load-trim');
      html = K.figure(spec, res.rows, { id: fid, guide: true });
      html = html.slice(0, html.lastIndexOf('</figure>')) + isl + '</figure>';
    }
    // round 2 fix pass: the drawing checks this pass added (words crossed or half covered, AX S2; red past Rule 05.1's
    // share, CD A-M2) fail the kit's build and check, the gate every owner runs on a spec; the guide build lists them as
    // notes, so one owner's spec does not stop another's strict build while the owners clear them (the sweep's way too)
    const kit_gate = f => GUIDE_NOTE_FAULTS.some(re => re.test(f));
    out.items[it.key || spec.id] = { html, faults: res.faults.filter(f => !kit_gate(f)), notes: res.faults.filter(kit_gate), id: spec.id, form: spec.form, tier: spec.tier,
      svg_bytes: res.drawings.map(d => d.bytes), rows: res.rows ? res.rows.length : 0 };
  }
  fs.writeFileSync(o.out, JSON.stringify(out));
  return 0;
}

async function self_test() {
  // plant one fault of each kind; the checks must catch every one
  const base = JSON.parse(fs.readFileSync(path.join(KIT, 'fixtures/specs/s14.json'), 'utf8'));
  const cases = [
    ['an em dash', s => { s.title += ' — and more'; }, 'em dash'],
    ['U+2011 in an ID', s => { s.notes = ['Loop R‑10']; }, 'U+2011'],
    ['the retired disclosure', s => { s.notes = ['Disclosure: the editor works with Yes on 3.']; }, 'disclosure'],
    ['a literal color', s => { s.labels = Object.assign({}, s.labels, { average: '#E63946 line' }); }, 'literal color'],
    ['a studio word in printed words', s => { s.notes = ['As Board 1 decided.']; }, 'studio word'],
    ['the atlas by its studio name', s => { s.measure_line = 'From Atlas V7.'; }, 'internal document'],
    ['a source line that differs from the sidecar', s => { s.source_line = 'Source: somewhere else.'; }, 'source line differs'],
    ['a table that drops a row', s => { s.where = { month: ['2022-01', '2022-02'] }; s.table.columns = [{ field: 'month', label: 'Month', format: 'month' }]; s.table.pivot = { row: 'month', column: 'status', value: 'change_thousands', format: 'signed-thousands' }; }, null],
    ['a missing table', s => { s.table = { caption: 'x', columns: [] }; }, 'no columns'],
    ['an unknown form', s => { s.form = 'pie-of-pies'; }, 'not registered'],
    ['a bare atlas ID', s => { s.notes = ['As Loop R10 shows.']; }, 'not listed in v7.ids'],
    ['a causal verb on a plausible grade', s => { s.v7 = { grade: 'plausible', ids: [], snapshot: '2026-10-15' }; s.title = 'Tariffs caused the drop in jobs.'; }, 'causal verb'],
    ['an association titled as a cause', s => { s.evidence = 'association'; s.title = 'Rates drove the change.'; }, 'causal verb'],
    ['a typography replacement whose words hold what it finds (D3-519)', s => { s.typography = { curl_quotes: true, replace: [['Act', 'Acts']] }; }, 'second pass'],
    ['a spec with no Illustrative label on invented data', s => { s.data = { columns: { month: { type: 'month', description: 'm' } }, rows: [{ month: '2022-01' }] }; delete s.dataset; s.illustrative = false; }, 'Illustrative'],
  ];
  let bad = 0;
  for (const [name, fn, want] of cases) {
    const s = JSON.parse(JSON.stringify(base));
    fn(s);
    let r;
    try { r = run_spec(s, { grounds: ['newsprint'], widths: [1440] }); } catch (e) { r = { faults: ['threw: ' + e.message] }; }
    const hit = want ? r.faults.some(f => f.indexOf(want) >= 0) : r.faults.length > 0;
    if (name === 'a table that drops a row') {
      // a pivot whose cells fall short of the rows: two rows, one status column, so both cells exist; drop one by hand
      const t = K.table_rows(s, r.rows || []);
      const ok = (t.pivot ? Object.keys(t.cell).length : t.rows.length) === (r.rows || []).length;
      console.log(`${ok ? 'pass' : 'FAIL'} table rows equal data rows on a clean pivot`);
      if (!ok) bad++;
      continue;
    }
    console.log(`${hit ? 'caught' : 'MISSED'} ${name}${hit ? '' : ': ' + JSON.stringify(r.faults.slice(0, 3))}`);
    if (!hit) bad++;
  }
  // drawing faults, planted in a drawing result
  const s = JSON.parse(JSON.stringify(base));
  const r = run_spec(s, { grounds: ['newsprint'], widths: [1440] });
  if (r.faults.length) { console.log('FAIL the clean fixture has faults: ' + r.faults.slice(0, 5).join('; ')); bad++; }
  const d0 = K.draw(s, r.rows, { width: 720, ground: 'newsprint', tokens: TOK.newsprint });
  const plant = [
    ['a bar off its zero line', d => { const m = d.marks.find(x => x.kind === 'bar'); m.y -= 3; m.h -= 0; m.zero = m.zero; m.y = m.zero - m.h - 3; }, 'zero line'],
    ['a mark outside its drawing', d => { d.marks[0].x = d.width + 20; }, 'outside its drawing'],
    ['text outside the artboard', d => { d.guard = K.guard({ texts: [{ x: d.width - 5, y: 10, w: 40, h: 16, size: 15, words: 'spill' }] }, d.width, d.height); }, 'outside the artboard'],
    ['two texts overlapping', d => { d.guard = K.guard({ texts: [{ x: 10, y: 10, w: 40, h: 16, size: 15, words: 'a' }, { x: 20, y: 12, w: 40, h: 16, size: 15, words: 'b' }] }, d.width, d.height); }, 'overlap'],
    ['text under 13 px', d => { d.guard = K.guard({ texts: [{ x: 10, y: 10, w: 40, h: 12, size: 11, words: 'tiny' }] }, d.width, d.height); }, 'under 13 px'],
    ['a party mark in red', d => { d.marks.push({ kind: 'rect', x: 1, y: 1, w: 2, h: 2, fill: 'point', data: { party: 'Republican' } }); }, 'party mark'],
    ['two working reds', d => { d.marks.push({ kind: 'circle', x: 1, y: 1, w: 2, h: 2, fill: 'point', data: {} }, { kind: 'circle', x: 50, y: 50, w: 2, h: 2, fill: 'point', data: {} }); }, 'working reds'],
    ['red touching Prussian', d => { d.marks.push({ kind: 'circle', x: 10, y: 10, w: 4, h: 4, fill: 'point', data: {} }, { kind: 'rect', x: 13, y: 10, w: 10, h: 10, fill: 'cat-3', data: {} }); }, 'touches Prussian'],
    ['a label on group 4\'s hatch', d => { d.marks.push({ kind: 'rect', x: 0, y: 0, w: 200, h: 40, fill: 'cat-4', data: {} }); d.texts = (d.texts || []).concat([{ x: 10, y: 10, w: 60, h: 16, size: 15, words: 'Group four' }]); }, 'group 4\'s hatch'],
    ['a circle sized by radius', d => { d.marks.push({ kind: 'circle', x: 0, y: 0, w: 20, h: 20, r: 10, data: {}, area_of: { value: 25, max_value: 100, max_radius: 40 } }); }, 'sized by area'],
    ['a key told apart by lightness alone, too close', d => { d.keys = [[{ fill: 'subject' }, { fill: 'cat-1' }]]; }, 'lightness'],
    ['a leader line through a label', d => { d.guard = K.guard({ texts: [{ x: 10, y: 10, w: 60, h: 16, size: 15, words: 'label' }], leaders: [{ x1: 0, y1: 18, x2: 100, y2: 18 }] }, d.width, d.height); }, 'leader line crosses'],
    ['a label in the ink of its mark in forced colors', d => { d.marks.push({ kind: 'rect', x: 0, y: 0, w: 200, h: 40, fill: 'subject', data: {} }); d.texts = (d.texts || []).concat([{ x: 10, y: 10, w: 60, h: 16, size: 15, words: 'Inked', fill: 'label' }]); }, 'forced colors'],
    ['ordered steps too close to their neighbors', d => { d.keys = [[{ fill: 'seq-2', ordered: true, outline: true }, { fill: 'seq-2', ordered: true, outline: true }]]; }, 'neighbors'],
    // round 1 fix pass: a shape the reader reads no value from, drawn far under the drawing (CD RM1, K-S2)
    ['a zero line drawn under its drawing', d => { d.ink.push({ kind: 'line', x: 30, y: d.height + 189, w: 600, h: 0, role: 'baseline' }); }, 'drawn outside its drawing'],
    // access S2: a row's two dots on each other while its values differ by a third
    ['two dots of one row drawn on each other', d => { d.marks.push({ kind: 'circle', x: 100, y: 50, w: 10, h: 10, r: 5, row: 'r1', data: { value: 60 } }, { kind: 'circle', x: 102, y: 50, w: 10, h: 10, r: 5, row: 'r1', data: { value: 90 } }); }, 'closer than a dot'],
  ];
  for (const [name, fn, want] of plant) {
    const d = JSON.parse(JSON.stringify(d0));
    fn(d);
    const f = C.check_drawing(s, d, TOK.newsprint, 'self-test');
    const hit = f.some(x => x.indexOf(want) >= 0);
    console.log(`${hit ? 'caught' : 'MISSED'} ${name}${hit ? '' : ': ' + JSON.stringify(f.slice(0, 3))}`);
    if (!hit) bad++;
  }
  // access S1 (round 1 fix pass): a source line whose period leaves out a year the chart draws fails, and a sidecar's
  // template, filled with the years drawn, prints and passes. A copy of the fixture's data in a scratch folder carries a
  // line for 2026 alone and a template.
  {
    const td = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'oa-kit-span-'));
    const DATA = path.join(ROOT, 'work/build/data');
    const meta = JSON.parse(fs.readFileSync(path.join(DATA, base.dataset + '.meta.json'), 'utf8'));
    fs.copyFileSync(path.join(DATA, meta.file), path.join(td, meta.file));
    const one = 'Source: a fixture publisher, all nonfarm employees, 2026, United States. Retrieved November 6, 2026.';
    meta.printed_source_line = one; meta.source_line_variants = {};
    meta.source_line_templates = { span: 'Source: a fixture publisher, all nonfarm employees, {from} to {to}, United States. Retrieved November 6, 2026.' };
    fs.writeFileSync(path.join(td, base.dataset + '.meta.json'), JSON.stringify(meta));
    const s1 = JSON.parse(JSON.stringify(base)); delete s1.source_line;
    const r1 = run_spec(s1, { grounds: ['newsprint'], widths: [1440], data_dir: td, no_narrow: true });
    const c1 = r1.faults.some(x => x.indexOf('but the chart draws 2022 to 2026') >= 0);
    console.log(`${c1 ? 'caught' : 'MISSED'} a source line for 2026 under a chart of 2022 to 2026${c1 ? '' : ': ' + JSON.stringify(r1.faults.slice(0, 2))}`);
    if (!c1) bad++;
    const s2 = JSON.parse(JSON.stringify(base)); delete s2.source_line; s2.source_line_template = 'span';
    const r2 = run_spec(s2, { grounds: ['newsprint'], widths: [1440], data_dir: td, no_narrow: true });
    const ok2 = !r2.faults.some(x => /^source:/.test(x)) && s2.source_line === 'Source: a fixture publisher, all nonfarm employees, 2022 to 2026, United States. Retrieved November 6, 2026.';
    console.log(`${ok2 ? 'pass' : 'FAIL'} a template filled with the years drawn prints and passes${ok2 ? '' : ': ' + JSON.stringify([s2.source_line].concat(r2.faults.slice(0, 2)))}`);
    if (!ok2) bad++;
    fs.rmSync(td, { recursive: true, force: true });
  }
  // round 1 fix pass (CD RM1): a line chart on a scale that starts above zero draws no zero line, and a dumbbell's small
  // change (two dots touching on a value a hundredth apart) is no fault
  {
    const ln = { kit: 1, id: 'T01', form: 'line-event-notes', family: 'change-over-time', tier: 'core', reader_question: 'q', evidence: 'illustration', evidence_label: 'Illustration',
      title: 'A line.', measure_line: 'm', source_line: 'Source: invented for the self-test.', illustrative: 'Illustrative data', alt: 'a', phone: 'same', domain: 'all', states: [], encode: { x: 'year', y: 'v' }, scale: { y: [30, 80] },
      table: { caption: 'c', columns: [{ field: 'year', label: 'Year', format: 'year', row_header: true }, { field: 'v', label: 'Value', format: 'number:1' }] },
      data: { columns: { year: { type: 'year', description: 'y' }, v: { type: 'number', description: 'v' } }, rows: [{ year: 2001, v: 40 }, { year: 2002, v: 55 }, { year: 2003, v: 70 }] } };
    const rl = run_spec(ln, { grounds: ['newsprint'], widths: [1440, 390] });
    const okl = rl.drawings.length === 2 && !rl.faults.length;   // the shape check would fail a zero line drawn under the plot
    console.log(`${okl ? 'pass' : 'FAIL'} a line chart on a scale from 30 draws no zero line${okl ? '' : ': ' + JSON.stringify(rl.faults.slice(0, 2))}`);
    if (!okl) bad++;
    const d1 = JSON.parse(JSON.stringify(d0));
    d1.marks.push({ kind: 'circle', x: 100, y: 50, w: 10, h: 10, r: 5, row: 'r2', data: { value: 74.5 } }, { kind: 'circle', x: 101, y: 50, w: 10, h: 10, r: 5, row: 'r2', data: { value: 74.7 } });
    const f1 = C.check_drawing(s, d1, TOK.newsprint, 'self-test');
    const okd = !f1.some(x => x.indexOf('closer than a dot') >= 0);
    console.log(`${okd ? 'pass' : 'FAIL'} a dumbbell row whose small change draws its dots touching is left alone`);
    if (!okd) bad++;
  }
  // the compressed island (DR-238): the kit's inflater gives back what zlib deflates, in every block type and level, and
  // refuses data that is not deflate
  {
    const samples = [Buffer.alloc(0), Buffer.from('a'), Buffer.from(JSON.stringify(base)), Buffer.from('é—“chart”−'.repeat(300)),
      require('crypto').randomBytes(70000), Buffer.from(Array.from({ length: 90000 }, (_, i) => (i * 7919) % 251))];
    const opts = [0, 1, 6, 9].map(level => ({ level })).concat([{ level: 9, strategy: zlib.constants.Z_FIXED }, { level: 9, strategy: zlib.constants.Z_HUFFMAN_ONLY },
      { level: 9, strategy: zlib.constants.Z_RLE }, { level: 9, memLevel: 9 }]);
    let n = 0, miss = 0;
    for (const b of samples) for (const op of opts) {
      n++;
      const got = Buffer.from(K.inflate(zlib.deflateRawSync(b, op)));
      if (!got.equals(b)) miss++;
    }
    console.log(`${miss ? 'FAIL' : 'pass'} the kit's inflater gives back ${n - miss} of ${n} deflated samples (stored, fixed and dynamic blocks)`);
    if (miss) bad++;
    const isl = island_element({ mode: 'table', spec: draw_spec(base) });
    const z = isl.match(/>([^<]*)</)[1];
    const back = JSON.parse(K.island_text(z, 'deflate'));
    const ok = JSON.stringify(back) === JSON.stringify({ mode: 'table', spec: draw_spec(base) }) && /^<script type="text\/plain" data-oa-chart-data="deflate">[A-Za-z0-9+/=]+<\/script>$/.test(isl);
    console.log(`${ok ? 'pass' : 'FAIL'} a compressed island reads back as its JSON`);
    if (!ok) bad++;
    const bytes = zlib.deflateRawSync(Buffer.from(JSON.stringify(base)));
    const cut = bytes.subarray(0, bytes.length >> 1), flip = Buffer.from(bytes); flip[0] |= 6;
    for (const [name, data] of [['a cut island', cut], ['an island with a bad block type', flip]]) {
      let threw = false;
      try { K.inflate(data); } catch (e) { threw = /^inflate: /.test(e.message); }
      console.log(`${threw ? 'caught' : 'MISSED'} ${name}`);
      if (!threw) bad++;
    }
  }
  // second pass (D3-614): a point alone names itself (ED-E12), sort takes an order of values (A12), and a word drawn on a
  // GrayText mark takes Canvas in forced colors
  {
    const cx = { ground: 'newsprint', t: () => 1 };
    const one = K.parts.named_fill(cx, undefined, 'k', null, 'B'), both = K.parts.named_fill(cx, ['B'], 'k', null, 'B'), none = K.parts.named_fill(cx, undefined, 'k');
    const ok1 = one({ k: 'A' }) === 'light-fill' && one({ k: 'B' }) === 'point' && both({ k: 'A' }) === 'light-fill' && both({ k: 'B' }) === 'point' && none({ k: 'A' }) === 'subject';
    console.log(`${ok1 ? 'pass' : 'FAIL'} labels.point alone gives every other mark the light fill; with labels.named too, the same`);
    if (!ok1) bad++;
    const sel = K.select({ sort: [{ field: 'g', values: ['b', 'a'] }] }, [{ g: 'a', n: 1 }, { g: 'c', n: 2 }, { g: 'b', n: 3 }, { g: 'a', n: 4 }]).map(r => r.n).join(',');
    const ok2 = sel === '3,1,4,2';
    console.log(`${ok2 ? 'pass' : 'FAIL'} sort by an order of values keeps each value's rows in data order, unlisted values last (${sel})`);
    if (!ok2) bad++;
    const c3 = new K.Ctx({ id: 'T', labels: {}, encode: {} }, [], { width: 300, ground: 'newsprint', t: K.token_reader(TOK.newsprint), uid: 't' });
    c3.rect(0, 0, 100, 40, { fill: 'seq-3', data: { key: 'x' } });
    const tb = c3.text(50, 25, 'PA', { anchor: 'middle' }), tc = c3.text(200, 25, 'OH', { anchor: 'middle' });
    const ok3 = tb.on_gray && !tc.on_gray && /oac-fc-on-gray/.test(c3._els[1]) && !/oac-fc-on-gray/.test(c3._els[2]);
    console.log(`${ok3 ? 'pass' : 'FAIL'} a word on a GrayText mark is marked to take Canvas in forced colors, one beside it is not`);
    if (!ok3) bad++;
  }
  // round 2 (R2-5, contract R2-C2): the shared interval, whisker, band and stack parts, and the interval form's checks (R2-C1)
  {
    const P = K.parts, T = K.token_reader(TOK.newsprint);
    const mk = enc => new K.Ctx({ id: 'T', labels: {}, encode: enc }, [], { width: 400, ground: 'newsprint', t: T, uid: 't2' });
    const ivm = P.interval_of(mk({ category: 'k', value: 'v', margin: 'm' })), ivl = P.interval_of(mk({ category: 'k', y: 'v', low: 'a', high: 'b' }));
    const a = ivm({ v: 82, m: 0.4 }), b = ivm({ v: 77, m: 2.5 }), l = ivl({ v: 5, a: 3, b: 8 });
    const ok1 = a.lo === 81.6 && a.hi === 82.4 && l.lo === 3 && l.hi === 8 && l.m === 2.5 && ivm.differs({ v: 82, m: 0.4 }, { v: 77, m: 2.5 }) && !ivm.differs({ v: 82, m: 0.4 }, { v: 80, m: 2.5 }) && b.m === 2.5;
    console.log(`${ok1 ? 'pass' : 'FAIL'} interval_of reads a margin or two ends, and differs() tests the margin of the difference`);
    if (!ok1) bad++;
    const cw = mk({});
    const wb = P.whisker(cw, 300, 100, 40, { key: 'AK', low: 81, high: 96 });
    const ln = cw._els.filter(e => /^<line/.test(e));
    const ok2 = ln.length === 1 && /oac-s-context/.test(ln[0]) && /stroke-width="2"/.test(ln[0]) && wb.x === 100 && wb.w === 200 &&
      cw.marks.filter(m => m.kind === 'datum').map(m => m.data.field + '@' + m.x).join(',') === 'low@100,high@300' && !cw.marks.some(m => m.kind === 'line');
    console.log(`${ok2 ? 'pass' : 'FAIL'} whisker draws one 2 px context line with no mark and records its two ends`);
    if (!ok2) bad++;
    const cb = mk({});
    const pts = [[0, 50, 60], [10, 48, 62], [20, null, 60], [30, 40, 70], [40, 42, 66], [50, 45, 65], [60, 44, 64]].map((p, i) => ({ x: p[0], y0: p[1], y1: p[2], key: 'y' + i, low: i, high: i + 1, break: i === 5 }));
    const br = P.band(cb, pts, { fill: 'band', edge: false });
    const paths = cb._els.filter(e => /^<path/.test(e));
    const ok3 = JSON.stringify(br.runs) === '[[0,1],[3,4],[5,6]]' && paths.length === 3 && paths.every(p => /oac-f-band/.test(p)) && br.top === 40 && br.bottom === 70 &&
      cb.marks.filter(m => m.kind === 'datum').length === 12 && !cb.marks.some(m => m.kind === 'path');
    // RF-2 (round 2 fix pass): by default each run also draws its two edges, 1 px in the context ink
    const cbe = mk({}); P.band(cbe, pts, { fill: 'band' });
    const pe = cbe._els.filter(e => /^<path/.test(e));
    const ok3e = pe.length === 9 && pe.filter(p => /oac-s-context/.test(p) && /stroke-width="1"/.test(p) && /oac-f-none/.test(p)).length === 6;
    console.log(`${ok3e ? 'pass' : 'FAIL'} band draws its two edges in the context ink at 1 px by default (RF-2)`);
    if (!ok3e) bad++;
    const cb1 = mk({}); P.band(cb1, [{ x: 5, y0: 10, y1: 20 }, { x: 6, y0: NaN, y1: 1 }], {});
    const ok3b = cb1._els.length === 1 && /^<line/.test(cb1._els[0]);
    console.log(`${ok3 && ok3b ? 'pass' : 'FAIL'} band draws one path a run, breaks at a gap and at break: true, records each end, and draws a lone point as a whisker`);
    if (!(ok3 && ok3b)) bad++;
    const rs = [{ k: 'A', o: 60, r: 40, t: 100 }, { k: 'B', o: 30, r: 10, t: 50 }, { k: 'C', o: null, r: 25, t: 25 }];
    const z = P.stack(rs, ['o', 'r']), ex = P.stack(rs, ['o', 'r'], { offset: 'expand', total: 't' }), ce = P.stack(rs, ['o', 'r'], { offset: 'center', center_at: 'r' });
    const py = P.stack([{ m: 5, w: 6 }], ['m', 'w'], { negative: ['m'] });
    const ok4 = z[0].segs[1].start === 60 && z[0].segs[1].end === 100 && z.hi === 100 && z.lo === 0 && z[2].segs[0].missing && z[2].segs[0].start === z[2].segs[0].end &&
      ex[1].segs[0].end === 60 && ex[1].segs[1].end === 80 && Math.abs(ce[0].segs[0].start + 60) < 1e-9 && ce[0].segs[1].start === 0 && ce[0].segs[1].end === 40 && ce.lo === -75 &&
      py[0].segs[0].start === -5 && py[0].segs[0].end === 0 && py[0].segs[1].start === 0 && py[0].segs[1].end === 6;
    const wd = P.wide([{ a: 1, s: 'male', v: 3 }, { a: 1, s: 'female', v: 4 }, { a: 2, s: 'male', v: 5 }], 'a', 's', 'v');
    const ok4b = wd.length === 2 && wd[0].male === 3 && wd[0].female === 4 && wd[1].male === 5 && wd.series.join() === 'male,female';
    console.log(`${ok4 && ok4b ? 'pass' : 'FAIL'} stack gives each segment's start and end (zero, a pyramid's negative side, shares, a midline), an empty cell no length; wide pivots long rows`);
    if (!(ok4 && ok4b)) bad++;
    // the interval form's checks, on a form registered for the test only
    if (!K.forms['t-interval']) K.register_chart({ form: 't-interval', family: 'uncertainty-and-estimates', interval: true,
      encode: { category: 'text', value: 'number', low: 'number?', high: 'number?', margin: 'number?' }, draw: c => { c.height(10); } });
    const iv = { kit: 1, id: 'T02', form: 't-interval', family: 'uncertainty-and-estimates', tier: 'core', reader_question: 'q', evidence: 'estimate', evidence_label: 'Estimate',
      title: 'Two estimates.', measure_line: 'A share, with its 90 percent margin of error', source_line: 'Source: invented for the self-test.', illustrative: 'Illustrative data', alt: 'a', phone: 'same', domain: 'all', states: [],
      encode: { category: 'k', value: 'v', margin: 'm' },
      table: { caption: 'c', columns: [{ field: 'k', label: 'Name', format: 'text', row_header: true }, { field: 'v', label: 'Share', format: 'number:1' }, { field: 'm', label: 'Margin', format: 'number:1' }] },
      data: { columns: { k: { type: 'text', description: 'k' }, v: { type: 'number', description: 'v' }, m: { type: 'number', description: 'm' }, lo: { type: 'number', description: 'lo' }, hi: { type: 'number', description: 'hi' } },
        rows: [{ k: 'A', v: 82, m: 0.4, lo: 81.6, hi: 82.4 }, { k: 'B', v: 77, m: 2.5, lo: 74.5, hi: 79.5 }] } };
    const ri = run_spec(JSON.parse(JSON.stringify(iv)), { grounds: ['newsprint'], widths: [1440], no_narrow: true });
    const ok5 = !ri.faults.some(x => /^interval:/.test(x));
    // ED-E17: the level's words held together by no-break spaces read as the level
    const nb = JSON.parse(JSON.stringify(iv)); nb.measure_line = 'A share, with its 90\u00a0percent margin\u00a0of\u00a0error';
    const rn = run_spec(nb, { grounds: ['newsprint'], widths: [1440], no_narrow: true });
    const ok5b = !rn.faults.some(x => /^interval:/.test(x));
    console.log(`${ok5b ? 'pass' : 'FAIL'} a level held together by no-break spaces ("90\u00a0percent margin\u00a0of\u00a0error") passes the level check${ok5b ? '' : ': ' + JSON.stringify(rn.faults.slice(0, 3))}`);
    if (!ok5b) bad++;
    console.log(`${ok5 ? 'pass' : 'FAIL'} an interval spec with its names, level and table passes the interval checks${ok5 ? '' : ': ' + JSON.stringify(ri.faults.slice(0, 3))}`);
    if (!ok5) bad++;
    const icases = [
      ['an interval form given both a margin and two ends', s => { s.encode.low = 'lo'; s.encode.high = 'hi'; }, 'together, or "margin" alone'],
      ['an interval that does not hold its estimate', s => { s.encode = { category: 'k', value: 'v', low: 'lo', high: 'hi' }; s.data.rows[1].hi = 76; s.table.columns.push({ field: 'lo', label: 'Low', format: 'number:1' }, { field: 'hi', label: 'High', format: 'number:1' }); }, 'does not hold its estimate'],
      ['an interval form whose measure line names no level', s => { s.measure_line = 'A share, with its margin of error'; }, 'names the interval\'s level'],
      ['an interval form whose table leaves the margin out', s => { s.table.columns.pop(); }, 'table equivalent prints the interval'],
    ];
    for (const [name, fn, want] of icases) {
      const s2 = JSON.parse(JSON.stringify(iv)); fn(s2);
      const r2 = run_spec(s2, { grounds: ['newsprint'], widths: [1440], no_narrow: true });
      const hit = r2.faults.some(x => x.indexOf(want) >= 0);
      console.log(`${hit ? 'caught' : 'MISSED'} ${name}${hit ? '' : ': ' + JSON.stringify(r2.faults.slice(0, 3))}`);
      if (!hit) bad++;
    }
    // ruling (b): the total line dashed 5 and 3 in the text's ink, the total point an open ring in it
    {
      const ct = mk({});
      P.total_line(ct, 0, 50, 300, 50); P.total_ring(ct, 40, 40, 6.5, { data: { key: 'US', field: 'v', value: 1 } });
      const okt = /oac-s-label/.test(ct._els[0]) && /stroke-dasharray="5 3"/.test(ct._els[0]) && /stroke-width="2"/.test(ct._els[0]) && /oac-f-surface/.test(ct._els[1]) &&
        /oac-s-label/.test(ct._els[2]) && ct.marks.length === 1 && ct.marks[0].data.key === 'US';
      console.log(`${okt ? 'pass' : 'FAIL'} total_line draws the dashed total in the text's ink, total_ring an open ring`);
      if (!okt) bad++;
    }
    // labels in small areas (fit_label) and labels beside points that keep clear of each other (place_labels)
    {
      const cf = mk({});
      const inside = (t, b) => t.x >= b.x - 0.01 && t.x + t.w <= b.x + b.w + 0.01 && t.y >= b.y - 0.01 && t.y + t.h <= b.y + b.h + 0.01;
      const b1 = { x: 0, y: 0, w: 200, h: 60 }, b2 = { x: 220, y: 0, w: 40, h: 18 }, b3 = { x: 0, y: 80, w: 160, h: 60 };
      const t1 = P.fit_label(cf, b1, 'National Defense'), n0 = cf._els.length, t2 = P.fit_label(cf, b2, 'Social Security'), t3 = P.fit_label(cf, b3, 'Veterans Benefits and Services', { fill: 'label-on-subject' });
      const ok7 = t1 && inside(t1, b1) && t1.size === cf.size('label') && t2 === null && cf._els.length === n0 + 1 && t3 && inside(t3, b3) && /<tspan/.test(cf._els[cf._els.length - 1]) && /oac-f-label-on-subject/.test(cf._els[cf._els.length - 1]);
      console.log(`${ok7 ? 'pass' : 'FAIL'} fit_label sets words inside an area on one or two lines, and draws nothing where they do not fit`);
      if (!ok7) bad++;
      const cp = mk({});
      const pts = [{ x: 100, y: 100, r: 6.5, words: 'Massachusetts' }, { x: 112, y: 104, r: 6.5, words: 'Connecticut' }, { x: 104, y: 92, r: 6.5, words: 'New Jersey' }, { x: 395, y: 150, r: 6.5, words: 'Hawaii' },
        { x: 106, y: 98, r: 6.5, words: 'Rhode Island' }, { x: 98, y: 108, r: 6.5, words: 'New York' }, { x: 110, y: 96, r: 6.5, words: 'Maryland' }, { x: 102, y: 102, r: 6.5, words: 'Delaware' }];
      pts.forEach(p => cp.circle(p.x, p.y, p.r, { fill: 'subject', data: { key: p.words } }));
      const pl = P.place_labels(cp, pts, { top: 0, bottom: 260 });
      const g = K.guard(cp, 400, 260);
      const hw = pl.placed.find(x => x.item.words === 'Hawaii');
      const ok8 = pl.placed.length >= 5 && pl.placed.length + pl.unplaced.length === pts.length && !g.length && hw && hw.box.x + hw.box.w <= 395 &&
        pl.placed.every(x => pts.every(q => q === x.item || !(x.box.x < q.x + q.r && q.x - q.r < x.box.x + x.box.w && x.box.y < q.y + q.r && q.y - q.r < x.box.y + x.box.h)));
      const cp2 = mk({}); const pl2 = P.place_labels(cp2, pts, { top: 0, bottom: 260, leaders: false });
      const ok8b = pl2.placed.length < pl.placed.length || pl2.unplaced.length > 0;
      console.log(`${ok8 && ok8b ? 'pass' : 'FAIL'} place_labels keeps labels clear of each other, of other dots and of the edge, uses leaders past the first ring, and returns those it cannot place (${pl.placed.length} of ${pts.length} placed; ${pl2.placed.length} without leaders)${ok8 ? '' : ': ' + JSON.stringify(g.slice(0, 2))}`);
      if (!(ok8 && ok8b)) bad++;
    }
    // R2-2: a derived table names its sources and method, and the line printed names each public source's publisher
    {
      const td = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'oa-kit-derived-'));
      const DATA = path.join(ROOT, 'work/build/data');
      const meta = JSON.parse(fs.readFileSync(path.join(DATA, base.dataset + '.meta.json'), 'utf8'));
      const pub = Object.assign({}, meta, { file: 'oa-test-public.csv', kind: 'public', publisher: 'U.S. Bureau of Labor Statistics' });
      fs.copyFileSync(path.join(DATA, meta.file), path.join(td, 'oa-test-public.csv'));
      fs.copyFileSync(path.join(DATA, meta.file), path.join(td, 'oa-test-derived.csv'));
      fs.writeFileSync(path.join(td, 'oa-test-public.meta.json'), JSON.stringify(pub));
      const der = Object.assign({}, meta, { file: 'oa-test-derived.csv', kind: 'derived', derived_from: ['oa-test-public.csv'], derivation: 'Bins of the monthly change, each month counted once.',
        printed_source_line: 'Source: U.S. Bureau of Labor Statistics, all nonfarm employees, monthly change, 2022 to 2026. Retrieved November 6, 2026.', source_line_variants: {
          bare: 'Source: a fixture table, 2022 to 2026. Retrieved November 6, 2026.' }, source_line_templates: {} });
      const run_d = (m, line) => {
        fs.writeFileSync(path.join(td, 'oa-test-derived.meta.json'), JSON.stringify(m));
        const s3 = JSON.parse(JSON.stringify(base)); s3.dataset = 'oa-test-derived'; delete s3.source_line; if (line) s3.source_line = line;
        return run_spec(s3, { grounds: ['newsprint'], widths: [1440], data_dir: td, no_narrow: true }).faults;
      };
      const f1 = run_d(der), f2 = run_d(der, der.source_line_variants.bare), f3 = run_d(Object.assign({}, der, { derivation: '' }));
      const okd = !f1.some(x => /R2-2/.test(x)), c2 = f2.some(x => /does not name U\.S\. Bureau of Labor Statistics/.test(x)), c3 = f3.some(x => /names derived_from and derivation/.test(x));
      console.log(`${okd ? 'pass' : 'FAIL'} a derived table whose line names its source's publisher passes${okd ? '' : ': ' + JSON.stringify(f1.filter(x => /R2-2/.test(x)))}`);
      console.log(`${c2 ? 'caught' : 'MISSED'} a derived table's line that leaves out its source's publisher${c2 ? '' : ': ' + JSON.stringify(f2.slice(0, 3))}`);
      console.log(`${c3 ? 'caught' : 'MISSED'} a derived table with no derivation${c3 ? '' : ': ' + JSON.stringify(f3.slice(0, 3))}`);
      if (!okd) bad++; if (!c2) bad++; if (!c3) bad++;
      fs.rmSync(td, { recursive: true, force: true });
    }
    // ED-E15 and ruling (c): marks the title names together share the red as one job; two jobs still fail. G2: the opt-in edge
    {
      const nf = P.named_fill({ ground: 'newsprint', t: () => 1 }, undefined, 'k', null, ['62', '65']);
      const okn = nf({ k: '62' }) === 'point' && nf({ k: '65' }) === 'point' && nf({ k: '40' }) === 'light-fill' && nf.job({ k: '65' }).job === 'point' && !nf.job({ k: '40' }).job &&
        nf.edge({ k: '40' }).stroke === 'context' && !nf.edge({ k: '62' }).stroke;
      const d1 = JSON.parse(JSON.stringify(d0)), d2 = JSON.parse(JSON.stringify(d0));
      d1.marks.push({ kind: 'rect', x: 1, y: 1, w: 2, h: 2, fill: 'point', data: {}, job: 'point' }, { kind: 'rect', x: 50, y: 50, w: 2, h: 2, fill: 'point', data: {}, job: 'point' });
      d2.marks.push({ kind: 'rect', x: 1, y: 1, w: 2, h: 2, fill: 'point', data: {}, job: 'point' }, { kind: 'rect', x: 50, y: 50, w: 2, h: 2, fill: 'point', data: {}, job: 'other' });
      const f1 = C.check_drawing(s, d1, TOK.newsprint, 'self-test'), f2 = C.check_drawing(s, d2, TOK.newsprint, 'self-test');
      const cj = mk({}); const gj = cj.group({ job: 'point' }); cj.circle(5, 5, 2, { fill: 'point' }); gj.end(); cj.circle(9, 9, 2, { fill: 'point', job: 'point' });
      const okj = !f1.some(x => /working reds/.test(x)) && f2.some(x => /2 working reds/.test(x)) && cj.marks.every(m => m.job === 'point') && /<g data-oa-job="point">/.test(cj._els[0]) && /data-oa-job="point"/.test(cj._els[1]);
      console.log(`${okn && okj ? 'pass' : 'FAIL'} a list of points shares the red as one job (marks in a job group or with job count once); two jobs still fail; the light fill's opt-in edge`);
      if (!(okn && okj)) bad++;
    }
    // second run: RB-G1 (decimal rounding), A-E2 (billions from millions), RB-G3 (a list of reaches), A-E3 (a second block in
    // fit_label), A-E1 (the fill under a word on a filled path)
    {
      const F = K.fmt, M = K.minus;
      const ok1 = F(12.35, 'number:1') === '12.4' && F(-12.35, 'number:1') === M + '12.4' && F(12.34999, 'number:1') === '12.3' && F(1.005, 'number:2') === '1.01' &&
        F(2.5, 'integer') === '3' && F(0.05, 'signed:1') === '+0.1' && F(173250000000, 'billions:1') === '173.3 billion' && F(1.0005, 'thousands') === '1,001' &&
        F(12.25, 'percent:1') === '12.3%' && F(0.1 + 0.2, 'number:16') === F(0.30000000000000004, 'number:16') && F(51.2, 'thousands') === '51,200';
      console.log(`${ok1 ? 'pass' : 'FAIL'} numbers round half away from zero on their decimal value (12.35 to 12.4, 1.005 to 1.01, 2.5 to 3)`);
      if (!ok1) bad++;
      const ok2 = F(36104000, 'billions-from-millions:1') === '36,104.0 billion' && F(36104000, 'billions-value-from-millions:1') === '36,104.0' &&
        K.unformat('36,104.0 billion', { format: 'billions-from-millions:1' }) === '36104000' && K.unformat('36,104.0', { format: 'billions-value-from-millions:1' }) === '36104000';
      console.log(`${ok2 ? 'pass' : 'FAIL'} billions-from-millions prints a column held in millions in billions and reads back`);
      if (!ok2) bad++;
      const crowd = [{ x: 200, y: 100, r: 6.5, words: 'Alpha' }, { x: 204, y: 100, r: 6.5, words: 'Bravo' }, { x: 208, y: 100, r: 6.5, words: 'Charlie' }, { x: 202, y: 104, r: 6.5, words: 'Delta' },
        { x: 206, y: 96, r: 6.5, words: 'Echo' }, { x: 210, y: 102, r: 6.5, words: 'Foxtrot' }, { x: 198, y: 98, r: 6.5, words: 'Golf' }, { x: 204, y: 106, r: 6.5, words: 'Hotel' },
        { x: 207, y: 94, r: 6.5, words: 'India' }, { x: 201, y: 101, r: 6.5, words: 'Juliet' }];
      const ra = mk({}); crowd.forEach(p => ra.circle(p.x, p.y, p.r, { fill: 'subject' })); const one = P.place_labels(ra, crowd, { top: 0, bottom: 300 });
      const rb = mk({}); crowd.forEach(p => rb.circle(p.x, p.y, p.r, { fill: 'subject' })); const many = P.place_labels(rb, crowd, { top: 0, bottom: 300, reach: [14, 40, 80] });
      const ok3 = many.placed.length > one.placed.length && !K.guard(rb, 400, 300).length;
      console.log(`${ok3 ? 'pass' : 'FAIL'} place_labels tries a list of reaches in order (${one.placed.length} placed with one, ${many.placed.length} with three)`);
      if (!ok3) bad++;
      const cs = mk({}), tile = { x: 0, y: 0, w: 150, h: 46 };
      const ts = P.fit_label(cs, tile, 'Social Security', { sub: '$1.6 trillion, 22 percent', pad: [5, 3] });
      const tn = P.fit_label(mk({}), { x: 0, y: 0, w: 150, h: 26 }, 'Social Security', { sub: '$1.6 trillion, 22 percent', pad: [5, 3] });
      const ok4 = ts && ts.sub && ts.sub.size === 13 && ts.sub.y >= ts.y + ts.h && ts.sub.y + ts.sub.h <= tile.y + tile.h + 0.01 && !K.guard(cs, 400, 100).length && tn === null;
      console.log(`${ok4 ? 'pass' : 'FAIL'} fit_label sets a second, smaller block under the words where both fit, and nothing where they do not`);
      if (!ok4) bad++;
      const cfp = mk({});
      cfp.path('M0,0L200,0L200,40L0,40Z', { fill: 'seq-3', mark: false });
      const wt = cfp.text(100, 25, 'On the band', { anchor: 'middle' });
      const ok5 = cfp.fill_under(100, 20) === 'seq-3' && wt.on_gray && cfp.fill_under(100, 60) === null;
      const dp = { marks: [], ink: [{ kind: 'path', x: 0, y: 0, w: 200, h: 40, fill: 'cat-1', poly: [[[0, 0], [200, 0], [200, 40], [0, 40]]] }], texts: [{ x: 60, y: 10, w: 80, h: 15, words: 'Inked', fill: 'label' }], fc: K.FC, fc_on_dark: K.FC_ON_DARK, keys: [], width: 400, height: 100 };
      const dq = JSON.parse(JSON.stringify(dp)); dq.texts[0].fill = 'on-cat-1';
      const fa = C.check_drawing(s, Object.assign({}, d0, dp, { guard: [] }), TOK.newsprint, 'self-test'), fb = C.check_drawing(s, Object.assign({}, d0, dq, { guard: [] }), TOK.newsprint, 'self-test');
      const ok6 = fa.some(x => /prints in CanvasText on a mark in CanvasText/.test(x)) && !fb.some(x => /forced colors/.test(x));
      console.log(`${ok5 && ok6 ? 'pass' : 'FAIL'} a word on a filled path reads that path's fill, in the kit and in the forced-colors check`);
      if (!(ok5 && ok6)) bad++;
    }
    // RS-S3: a drawing reports its arrangement, the phone one under 480 px or where the form says so
    const da = K.draw(s, r.rows, { width: 720, ground: 'newsprint', tokens: TOK.newsprint }), dp = K.draw(s, r.rows, { width: 358, ground: 'newsprint', tokens: TOK.newsprint });
    const ca = mk({}); ca.arrange('phone');
    const ok6 = da.arrangement === 'desk' && dp.arrangement === 'phone' && ca._arr === 'phone';
    console.log(`${ok6 ? 'pass' : 'FAIL'} a drawing reports its arrangement (desk at 720 px, phone at 358 px, phone where a form says so)`);
    if (!ok6) bad++;
  }
  // D3-519: typography sets curly quotes and its replacements once, and a second pass changes nothing
  {
    const sp = { typography: { curl_quotes: true, replace: [['Act,2026', 'Act, 2026']] } };
    const once = K.typeset(sp, "the 'big three' PBMs, \"Act,2026\""), twice = K.typeset(sp, once);
    const okt = once === 'the \u2018big three\u2019 PBMs, \u201cAct, 2026\u201d' && twice === once && K.typeset({}, "it's") === "it's";
    console.log(`${okt ? 'pass' : 'FAIL'} typography curls quotes and replaces once, and a second pass changes nothing`);
    if (!okt) bad++;
  }
  // round 2 fix pass: the checks and parts this pass added, each planted or tried on a form registered for the test only
  {
    const T2 = K.token_reader(TOK.newsprint);
    const mk = enc => new K.Ctx({ id: 'T', labels: {}, encode: enc }, [], { width: 400, ground: 'newsprint', t: T2, uid: 't3' });
    const iv = { kit: 1, id: 'T08', form: 't-interval', family: 'uncertainty-and-estimates', tier: 'core', reader_question: 'q', evidence: 'estimate', evidence_label: 'Estimate',
      title: 'Two estimates.', measure_line: 'A share, with its 90 percent margin of error', source_line: 'Source: invented for the self-test.', illustrative: 'Illustrative data', alt: 'a', phone: 'same', domain: 'all', states: [],
      encode: { category: 'k', value: 'v', margin: 'm' },
      table: { caption: 'c', columns: [{ field: 'k', label: 'Name', format: 'text' }, { field: 'v', label: 'Share', format: 'number:1' }, { field: 'm', label: 'Margin', format: 'number:1' }] },
      data: { columns: { k: { type: 'text', description: 'k' }, v: { type: 'number', description: 'v' }, m: { type: 'number', description: 'm' } }, rows: [{ k: 'A', v: 82, m: 0.4 }, { k: 'B', v: 77, m: 2.5 }] } };
    if (!K.forms['t-interval']) K.register_chart({ form: 't-interval', family: 'uncertainty-and-estimates', interval: true,
      encode: { category: 'text', value: 'number', low: 'number?', high: 'number?', margin: 'number?' }, draw: c => { c.height(10); } });
    const say = (ok, words) => { console.log(`${ok ? 'caught' : 'MISSED'} ${words}`); if (!ok) bad++; };
    const pass = (ok, words) => { console.log(`${ok ? 'pass' : 'FAIL'} ${words}`); if (!ok) bad++; };
    const base2 = { kit: 1, id: 'T09', family: 'comparison', tier: 'core', reader_question: 'q', evidence: 'illustration', evidence_label: 'Illustration',
      title: 'A test.', measure_line: 'Invented values', source_line: 'Source: invented for the self-test.', illustrative: 'Illustrative data', alt: 'a', phone: 'same', domain: 'all', states: [],
      encode: { category: 'k', value: 'v' }, table: { caption: 'c', columns: [{ field: 'k', label: 'Name', format: 'text' }, { field: 'v', label: 'Value', format: 'number:1' }] },
      data: { columns: { k: { type: 'text', description: 'k' }, v: { type: 'number', description: 'v' } }, rows: [{ k: 'A', v: 1 }, { k: 'B', v: 2 }] } };
    const reg = (form, draw, extra) => { K.forms[form] = undefined; K.register_chart(Object.assign({ form, family: 'comparison', encode: { category: 'text', value: 'number' }, draw }, extra || {})); };
    const faults = (form, w) => C.check_drawing(base2, K.draw(Object.assign({}, base2, { form }), base2.data.rows, { width: w || 720, ground: 'newsprint', tokens: TOK.newsprint }), TOK.newsprint, 't');
    // CD A-M2: red past 5 percent of the drawing
    reg('t-red', c => { c.rect(0, 0, 200, 100, { fill: 'point', data: { key: 'A' } }); c.rect(0, 100, 720, 100, { fill: 'light-fill', data: { key: 'B' } }); c.height(200); });
    reg('t-red-ok', c => { c.rect(0, 0, 40, 100, { fill: 'point', data: { key: 'A' } }); c.rect(0, 100, 720, 100, { fill: 'light-fill', data: { key: 'B' } }); c.height(200); });
    say(faults('t-red').some(f => /Pillar Red covers 13\.8 percent/.test(f)), 'red over 5 percent of a drawing (13.8 percent, CD A-M2)');
    pass(!faults('t-red-ok').some(f => /Pillar Red/.test(f)), 'red under 5 percent passes (2.8 percent)');
    // AX M1: a band under 3 to 1 with no edge, and with its default edge
    reg('t-band', c => { K.parts.band(c, [{ x: 10, y0: 40, y1: 60 }, { x: 300, y0: 30, y1: 70 }], { fill: 'mag-1', edge: false }); c.height(100); });
    reg('t-band-ok', c => { K.parts.band(c, [{ x: 10, y0: 40, y1: 60 }, { x: 300, y0: 30, y1: 70 }], { fill: 'mag-1' }); c.height(100); });
    say(faults('t-band').some(f => /band: a band in mag-1 measures 1\.1\d to 1/.test(f)), 'a band at 1.16 to 1 with no edge (AX M1, D3-903)');
    pass(!faults('t-band-ok').some(f => /^band:/.test(f)), 'a band with its default context edge passes (RF-2)');
    // call 9: an interval form whose intervals hide behind their dots at this width
    reg('t-ivw', c => { [0, 1, 2].forEach(i => { K.parts.whisker(c, 100, 100 + (c.width < 400 ? 12 : 60), 20 + 30 * i, { key: 'k' + i, low: 1, high: 2 }); c.circle(100 + (c.width < 400 ? 6 : 30), 20 + 30 * i, 6.5, { fill: 'subject', data: { key: 'k' + i, field: 'v', value: 1.5 } }); }); c.height(100); }, { interval: true });
    say(faults('t-ivw', 358).some(f => /middle row's interval spans 12\.0 px, under the 23\.0 px/.test(f)), 'an interval form whose plot hides its intervals behind their dots (call 9, D3-899)');
    pass(!faults('t-ivw', 720).some(f => /^interval:/.test(f)), 'the same form with room for its intervals passes');
    // AX S2, BC S1: a data line drawn after a word, a dot half under a word, a quiet line cleared by a knockout, a strike
    reg('t-cross', c => { c.text(100, 50, 'Crossed words', { role: 'label' }); c.line(80, 45, 300, 45, { stroke: 'subject', width: 2, mark: false }); c.height(100); });
    reg('t-under', c => { c.circle(100, 50, 8, { fill: 'subject', data: { key: 'A' } }); c.text(104, 54, 'Covered words', { role: 'label' }); c.height(100); });
    reg('t-quiet', c => { c.line(0, 45, 400, 45, { stroke: 'gridline', width: 1, mark: false }); c.text(100, 50, '-48.0', { role: 'label' }); c.height(100); });
    reg('t-strike', c => { c.text(100, 50, '2', { role: 'label' }); c.line(96, 54, 112, 38, { stroke: 'subject', width: 2, mark: false, strike: true }); c.height(100); });
    say(faults('t-cross').some(f => /a line in subject runs through "Crossed words", drawn after the words/.test(f)), 'a data line drawn through a word (AX S2)');
    say(faults('t-under').some(f => /a circle in subject sits half under "Covered words"/.test(f)), 'a dot half under a word (AX S2)');
    const dq = K.draw(Object.assign({}, base2, { form: 't-quiet' }), base2.data.rows, { width: 720, ground: 'newsprint', tokens: TOK.newsprint });
    pass(/<rect x="[\d.]+" y="[\d.]+" width="[\d.]+" height="[\d.]+" class="oac-f-surface"\/><text/.test(dq.svg) && dq.svg.indexOf('\u0002') < 0 && dq.svg.indexOf('\u0003') < 0 && !C.check_drawing(base2, dq, TOK.newsprint, 't').some(f => /^layout:/.test(f)),
      'a gridline through a word is cut by a knockout of the ground behind it, and the drawing passes (BC S1)');
    const dn = K.draw(Object.assign({}, base2, { form: 't-red-ok' }), base2.data.rows, { width: 720, ground: 'newsprint', tokens: TOK.newsprint });
    pass(dn.svg.indexOf('oac-f-surface') < 0 && dn.svg.indexOf('\u0002') < 0, 'a drawing with nothing to clear draws no knockout and keeps no marker');
    pass(!faults('t-strike').some(f => /^layout:/.test(f)), 'a stroke marked strike: true runs through its word and passes');
    // clear_label, row_name, row_value
    { const c = mk({}); c.line(0, 45, 400, 45, { stroke: 'subject', width: 2, mark: false }); const tb = K.parts.clear_label(c, 100, 50, 'On a line', { role: 'label' });
      pass(!!tb.knock && /class="oac-f-surface"/.test(c._els[c._els.length - 2]) && /oac-halo/.test(c._els[c._els.length - 1]), 'clear_label sets a knockout of the ground and the words on its halo (BC S1, BC S7)'); }
    { const c = mk({}); const a = K.parts.row_name(c, 0, 20, 'Alaska', {}), b = K.parts.row_name(c, 0, 40, 'Florida', { named: true }), v = K.parts.row_value(c, 300, 40, '35.5%', { named: true });
      pass(/oac-w4/.test(c._els[0]) && /oac-w7/.test(c._els[1]) && /oac-w7/.test(c._els[2]) && /text-anchor="end"/.test(c._els[2]) && /oac-tnum/.test(c._els[2]), 'row names and values set at 400, the named row at 700 (BC S8, call 11)'); }
    // the sweep: a fault at one off-column width is found and printed once with its widths
    reg('t-sweep', c => { c.text(c.width === 333 || c.width === 334 ? c.width - 10 : 0, 20, 'Spill', { role: 'label' }); c.height(40); });
    const sf = sweep_faults(Object.assign({}, base2, { form: 't-sweep' }), base2.data.rows, {});
    say(sf.length === 1 && /sweep: layout guard: text outside the artboard: "Spill".*at 2 of the widths from 256 to 720 px: 333 to 334\)$/.test(sf[0]), 'a fault at 333 and 334 px only, which the six guide columns miss (the sweep, AX S1)');
    // AX S8: a margin in another unit, a check-only column, a line for another measure
    { const s8 = JSON.parse(JSON.stringify(iv));
      s8.data.columns.v.unit = 'percent'; s8.data.columns.m.unit = 'households'; s8.data.columns.m2 = { type: 'number', description: 'm2', unit: 'percentage points' };
      s8.data.rows.forEach(r => { r.m2 = 0.5; });
      const f8 = C.check_spec(K, JSON.parse(JSON.stringify(s8)), {}).faults;
      say(f8.some(x => /the margin "m" is in households and the value "v" in percent/.test(x)), 'a margin in households beside a value in percent (AX S8)');
      s8.encode.margin = 'm2'; s8.table.columns[2].field = 'm2';
      pass(!C.check_spec(K, JSON.parse(JSON.stringify(s8)), {}).faults.some(x => /AX S8/.test(x)), 'a margin in percentage points beside a percent passes');
      const s9 = JSON.parse(JSON.stringify(base2)); s9.data.columns.v.unit = 'percent';
      const td9 = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'oa-s8-'));
      fs.writeFileSync(path.join(td9, 't9.csv'), 'k,v,w,x\nA,1,2,3\nB,2,3,4\n');
      fs.writeFileSync(path.join(td9, 't9.meta.json'), JSON.stringify({ file: 't9.csv', kind: 'public', publisher: 'Test', printed_source_line: 'Source: Test, the v measure.', source_line_variants: { w: 'Source: Test, the w measure.' },
        source_line_columns: { printed_source_line: ['v'], w: ['w'] }, check_only_columns: ['x'], columns: { k: { type: 'text' }, v: { type: 'number' }, w: { type: 'number' }, x: { type: 'number' } } }));
      const s10 = Object.assign({}, base2, { dataset: 't9', encode: { category: 'k', value: 'w' }, table: { caption: 'c', columns: [{ field: 'k', label: 'Name' }, { field: 'w', label: 'W' }] } }); delete s10.data; delete s10.source_line; s10.illustrative = false;
      const f10 = C.check_spec(K, JSON.parse(JSON.stringify(s10)), { data_dir: td9 }).faults;
      say(f10.some(x => /source line printed \(the sidecar's printed_source_line\) covers v, and the chart prints w; print its source_line_variants "w"/.test(x)), 'a source line for another measure than the chart draws (AX S8)');
      const s11 = Object.assign({}, s10, { source_line: 'Source: Test, the w measure.', table: { caption: 'c', columns: [{ field: 'k', label: 'Name' }, { field: 'w', label: 'W' }, { field: 'x', label: 'X' }] } });
      say(C.check_spec(K, JSON.parse(JSON.stringify(s11)), { data_dir: td9 }).faults.some(x => /"x" is in its sidecar's check_only_columns/.test(x)), 'a check-only column printed in the table (AX S8)');
      fs.rmSync(td9, { recursive: true, force: true }); }
    // BC S12, RB-G5, RB-G6, AX S3, RB-G4
    { const t = K.typeset({ typography: { nbsp: true } }, 'On November 3, 2026, from 2017 to 2022.');
      pass(t === 'On November\u00a03, 2026, from 2017\u00a0to\u00a02022.' && K.typeset({ typography: { nbsp: true } }, t) === t && K.fmt('2026-10-15', 'date') === 'October 15, 2026', 'typography.nbsp holds a date and a span of years together, a second pass changes nothing, and dates still format (BC S12)'); }
    { const c = mk({}); const a = c.text(0, 30, 'At least 17', { role: 'big', weight: 800, open: true }), b = c.text(0, 80, 'At least 17', { role: 'big', weight: 800 });
      pass(/oac-t-open/.test(c._els[0]) && !/oac-t-open/.test(c._els[1]) && Math.abs(a.w - b.w - 2 * K.OPEN_WORD_SPACE * a.size) < 1e-6, 'a big figure that holds words opens its tracking where asked, and is measured so (BC S12)'); }
    { const sp = { id: 'T', table: { columns: [{ field: 'age', label: 'Age', format: 'integer', words: { '100': '100 and over' } }], pivot: { row: 'age', column: 's', value: 'n', format: 'integer' } } };
      const rows = [{ age: 99, s: 'M', n: 5 }, { age: 100, s: 'M', n: 7 }];
      const h = K.table_html(sp, rows, { lean: true, types: { age: { type: 'integer' }, s: { type: 'text' }, n: { type: 'integer' } } });
      pass(/<th scope="row" class="t" data-v="100">100 and over<\/th>/.test(h) && />99<\/th>/.test(h), "a pivot's row header prints its column's words and keeps the stored value for the read-back (RB-G5)"); }
    { const c = mk({}); K.parts.key(c, [{ label: 'Band', fill: 'mag-1', edge: 'context' }], 0, 20, 300);
      pass(c._els.some(e => /oac-f-mag-1/.test(e)) && c._els.some(e => /oac-s-context/.test(e) && /stroke-width="1"/.test(e)), 'a key swatch takes a 1 px edge (RB-G6)'); }
    { const c = mk({}); c.rect(0, 0, 50, 20, { fill: 'context', fc: 'total', data: { key: 'All' } });
      pass(/class="oac-f-context oac-fc-total"/.test(c._els[0]) && c.marks[0].fc === 'total', "a total takes its own forced-colors class (AX S3)"); }
    { // every place beside the point is taken, so the label needs a leader; a square path round the point at 20 px stops each
      const items = [{ x: 200, y: 100, r: 4, words: 'Named' }], avoid = [{ x: 170, y: 70, w: 60, h: 60 }];
      const sq = [[[180, 80], [220, 80], [220, 120], [180, 120], [180, 80]]];
      const c1 = mk({}), free = K.parts.place_labels(c1, items, { avoid, reach: [40] });
      const c2 = mk({}), blocked = K.parts.place_labels(c2, items, { avoid, reach: [40], paths: sq });
      pass(free.placed.length === 1 && blocked.unplaced.length === 1, 'place_labels draws a leader where it may and none across a path it is given (RB-G4)'); }
  }
  // the words inside kit.js equal words.json
  const wj = Object.assign({}, K.words); delete wj.about;
  const same = JSON.stringify(wj) === JSON.stringify(K.WORDS);
  console.log(`${same ? 'pass' : 'FAIL'} the words carried in kit.js equal words.json`);
  if (!same) bad++;
  // the CSV check
  const cols = Object.keys(r.datasets[0].meta.columns);
  const csv = C.to_csv(r.rows.slice(1), cols);
  const cf = C.check_csv(K, csv, r.rows, r.datasets[0].meta);
  console.log(`${cf.length ? 'caught' : 'MISSED'} a CSV export short of a row`);
  if (!cf.length) bad++;
  console.log(bad ? `self-test: ${bad} missed` : 'self-test: every planted fault caught');
  return bad ? 1 : 0;
}

// ED-E9 (round 1 fix pass): a drawing a script makes outside the kit, until a kit form draws it (Rule 14.9's intervals),
// set inside the kit's own figure, so the plate prints the kit's anatomy, its bold "Source:", the credit and the table
// from the spec, as every kit chart does. The spec passes the kit's word and data checks; the drawing takes the kit's role
// classes only (the sketch format, R1-C1: no literal color, no style attribute or element, text at 13 px or more). The
// figure is static: no island, nothing redraws, and its description names the drawing.
export function static_figure(spec, desk, phone, fid) {
  const faults = [];
  const one = (svg, which) => {
    svg = String(svg || '').trim();
    if (!/^<svg\b[^>]*>[\s\S]*<\/svg>$/.test(svg)) { faults.push(`${which}: the file is not one <svg> element`); return ''; }
    if (!/^<svg\b[^>]*\bclass="[^"]*\boac-svg\b/.test(svg)) faults.push(`${which}: the <svg> needs class="oac-svg", so kit.css colors it on both grounds and in forced colors`);
    if (/\sstyle="|<style\b/.test(svg)) faults.push(`${which}: a style attribute or element; color and type come from the kit's role classes`);
    if (/(?:fill|stroke)="#|(?:fill|stroke)="rgb|font-family=/.test(svg)) faults.push(`${which}: a literal color or font name; use the kit's role classes (oac-f-*, oac-s-*, oac-t)`);
    for (const m of svg.matchAll(/font-size="([\d.]+)"/g)) if (+m[1] < 13) { faults.push(`${which}: text at ${m[1]} px; nothing under 13 px`); break; }
    if (/\u2014/.test(svg)) faults.push(`${which}: an em dash`);
    const w = /^<svg\b[^>]*\bwidth="([\d.]+)"/.exec(svg);
    if (!w) faults.push(`${which}: the <svg> needs its width in px, its true size`);
    return svg.replace(/^<svg\b/, `<svg role="img" aria-labelledby="${fid}-alt"`).replace(/\srole="img"(?=[^>]*role="img")/, '');
  };
  let svg = one(desk, 'the drawing');
  let art = '';
  if (phone) { svg = svg.replace('class="oac-svg', 'class="oac-svg oac-desk') + one(phone, 'the phone drawing').replace('class="oac-svg', 'class="oac-svg oac-phone'); art = ' data-oa-lean'; }
  const html = K.figure(spec, spec._rows || [], { id: fid, svg, art_attrs: art + ' data-oa-static', guide: true })
    .replace('<figure class="oac-fig"', '<figure class="oac-fig" data-oa-static');
  return { html, faults };
}
async function figure_cmd(o) {
  const sp = o._[0] ? spec_path(o._[0], o.specs) : null;
  if (!sp || !o.svg) { console.error('usage: oa-chart.mjs figure <spec path> --svg DESK.svg [--phone-svg PHONE.svg] [--id FID] [--out FILE]'); return 2; }
  const spec = JSON.parse(fs.readFileSync(sp, 'utf8'));
  let chk;
  try { chk = C.check_spec(K, spec, { spec_path: sp }); } catch (e) { console.error('FAIL spec: ' + e.message); return 1; }
  const fid = o.id || ('oac-' + String(spec.id).toLowerCase());
  const r = static_figure(Object.assign({}, spec, { _rows: chk.rows || [] }), fs.readFileSync(o.svg, 'utf8'), o.phone_svg ? fs.readFileSync(o.phone_svg, 'utf8') : null, fid);
  const faults = chk.faults.concat(r.faults);
  if (o.out && o.out !== SCRATCH) fs.writeFileSync(o.out, r.html + '\n'); else process.stdout.write(r.html + '\n');
  for (const f of faults) console.error('  - ' + f);
  console.error(`${faults.length ? 'FAIL' : 'PASS'} ${spec.id} static figure: ${(chk.rows || []).length} rows, ${faults.length} faults`);
  return faults.length ? 1 : 0;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const [cmd, ...rest] = process.argv.slice(2);
  const o = args(rest);
  let code = 2;
  if (cmd === 'build') code = await build(o, false);
  else if (cmd === 'check') code = await build(o, true);
  else if (cmd === 'fragments') code = await fragments(o);
  else if (cmd === 'figure') code = await figure_cmd(o);
  else if (cmd === 'self-test') code = await self_test();
  else console.error('usage: oa-chart.mjs build|check|fragments|figure|self-test ...');
  process.exit(code);
}
