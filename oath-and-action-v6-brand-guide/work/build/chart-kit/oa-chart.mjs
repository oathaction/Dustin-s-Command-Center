#!/usr/bin/env node
// The chart kit's one command (contract C3). Builds a chart from its spec and data file, runs its checks, and writes the
// exports and captures.
//
//   node work/build/chart-kit/oa-chart.mjs build <ID|spec path>... [--all] [--widths 1440,390] [--grounds newsprint,charcoal]
//                                          [--out DIR] [--no-png] [--date YYYYMMDD] [--specs DIR]
//   node work/build/chart-kit/oa-chart.mjs check <ID|spec path>... [--all]
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
  const o = { _: [], widths: [1440, 390], grounds: ['newsprint', 'charcoal'], out: SCRATCH, png: true, date: null, specs: path.join(KIT, 'specs') };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--all') o.all = true;
    else if (a === '--widths') o.widths = argv[++i].split(',').map(Number);
    else if (a === '--grounds') o.grounds = argv[++i].split(',');
    else if (a === '--out') o.out = path.resolve(argv[++i]);
    else if (a === '--no-png') o.png = false;
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

export const GUIDE_WIDTHS = [656, 558, 358, 296, 256];
export function guide_widths(spec) {
  return /^s-13-/i.test(String(spec.id)) ? GUIDE_WIDTHS.concat([243, 224]) : GUIDE_WIDTHS;
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
OAChart.words = OAChart_words;</script>
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
    out.items[it.key || spec.id] = { html, faults: res.faults, id: spec.id, form: spec.form, tier: spec.tier,
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
