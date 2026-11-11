#!/usr/bin/env node
// The chart kit's one command (contract C3). Builds a chart from its spec and data file, runs its checks, and writes the
// exports and captures.
//
//   node work/build/chart-kit/oa-chart.mjs build <ID|spec path>... [--all] [--widths 1440,390] [--grounds newsprint,charcoal]
//                                          [--out DIR] [--no-png] [--date YYYYMMDD] [--specs DIR]
//   node work/build/chart-kit/oa-chart.mjs check <ID|spec path>... [--all]
//   node work/build/chart-kit/oa-chart.mjs fragments --in LIST.json --out OUT.json     (guide_build.py's hook)
//   node work/build/chart-kit/oa-chart.mjs self-test
//
// It never reads source/ or writes into the repository unless --out names a folder there.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';

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

// One spec, checked and drawn in Node at every width and ground
export function run_spec(spec, o) {
  const res = { id: spec.id, faults: [], drawings: [], spec_path: o.spec_path };
  let chk;
  try { chk = C.check_spec(K, spec, o); } catch (e) { res.faults.push('spec: ' + e.message); return res; }
  res.faults.push(...chk.faults);
  res.rows = chk.rows;
  res.datasets = chk.datasets;
  if (!K.forms[spec.form] || !chk.rows || !chk.rows.length) return res;
  for (const g of o.grounds) for (const w of o.widths) {
    const cw = container(w, spec);
    let d;
    try { d = K.draw(spec, chk.rows, { width: cw, ground: g, tokens: TOK[g] }); } catch (e) { res.faults.push(`draw at ${w} on ${g}: ${e.message}`); continue; }
    const where = `${g} ${w}`;
    res.faults.push(...C.check_drawing(spec, d, TOK[g], where));
    res.drawings.push({ ground: g, page: w, width: d.width, height: d.height, svg: d.svg, bytes: Buffer.byteLength(d.svg) });
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
export function island_table(spec, rows, columns) {
  // method load-table: the drawing spec, the types of the columns it uses, and as CSV only the used columns the table lacks
  const used = used_columns(spec, columns), inTable = new Set(table_fields(spec));
  const extra = used.filter(c => !inTable.has(c));
  const ctypes = {};
  used.concat([...inTable]).forEach(c => { if (columns[c]) ctypes[c] = { type: columns[c].type }; });
  const payload = { mode: 'table', spec: draw_spec(spec), columns: ctypes };
  if (extra.length) payload.csv = C.to_csv(rows, extra);
  return '<script type="application/json" data-oa-chart-data>' + JSON.stringify(payload).replace(/</g, '\\u003c') + '</script>';
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
  return '<script type="application/json" data-oa-chart-data>' + JSON.stringify(payload).replace(/</g, '\\u003c') + '</script>';
}

// The kit as a page carries it: full-line comments and indentation dropped, nothing else changed (no outside tool, no
// renaming), so the same code runs in the page and in Node. A comment after code on its line stays.
export function strip(js) {
  return js.replace(/^\s*\/\*[\s\S]*?\*\/\s*$/gm, '').split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('//')).join('\n');
}
export function kit_parts() {
  const forms = fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js')).sort();
  const core = ['metrics.js', 'kit.js', 'parts.js'].map(f => strip(fs.readFileSync(path.join(KIT, f), 'utf8'))).join('\n');
  return { core, geo: fs.readFileSync(path.join(KIT, 'geo.js'), 'utf8'), forms: Object.fromEntries(forms.map(f => [f, strip(fs.readFileSync(path.join(KIT, 'forms', f), 'utf8'))])),
    css: fs.readFileSync(path.join(KIT, 'kit.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '').split('\n').map(l => l.trim()).filter(Boolean).join('\n') };
}
export function kit_scripts() {
  const k = kit_parts();
  return [k.core, k.geo].concat(Object.values(k.forms)).join('\n').replace(/<\/script/gi, '<\\/script');
}
export function kit_scripts_full() {
  const forms = fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js')).sort().map(f => fs.readFileSync(path.join(KIT, 'forms', f), 'utf8'));
  return [fs.readFileSync(path.join(KIT, 'metrics.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'kit.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'parts.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'geo.js'), 'utf8')].concat(forms).join('\n').replace(/<\/script/gi, '<\\/script');
}

function page_html(specs) {
  // a plain page: tokens.css, kit.css, the kit and its forms, and each figure with its data island (DR-235)
  const body = specs.map(({ spec, rows, columns, grounds }) => grounds.map(g => `<section class="oa-surface-${g} oac-ground" data-ground="${g}">
${(f => f.slice(0, f.lastIndexOf('</figure>')) + island_table(spec, rows, columns) + '</figure>')(K.figure(spec, rows, { id: `oac-${spec.id.toLowerCase()}-${g}`, lean_table: true, types: columns }))}
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
      const html = page_html([{ spec, rows: res.rows, columns: res.datasets.length ? res.datasets[0].meta.columns : (spec.data || {}).columns, grounds: o.grounds }]);
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
          await p.waitForFunction(() => Array.from(document.querySelectorAll('figure.oac-fig')).every(f => f.getAttribute('data-oa-drawn') || f.getAttribute('data-oa-error')), null, { timeout: 15000 });
          errors.forEach(e => res.faults.push(`page error at ${w}: ${e}`));
          for (const g of o.grounds) {
            const fid = `#oac-${spec.id.toLowerCase()}-${g}`;
            const node = res.drawings.find(d => d.ground === g && d.page === w);
            const info = await p.evaluate(({ fid, node_svg, title, alt }) => {
              const f = document.querySelector(fid);
              const err = f.getAttribute('data-oa-error');
              const svg = f.querySelector('svg.oac-svg');
              const tb = f.querySelector('table.oac-table');
              const out = { err, rows: tb && tb.hasAttribute('data-oa-lean') ? (tb.querySelector('tbody th[scope=row]') && tb.querySelectorAll('thead th').length > 1 && tb.querySelectorAll('tbody td[data-x]').length + tb.querySelectorAll('tbody td').length !== tb.querySelectorAll('tbody tr').length * (tb.querySelectorAll('thead th').length - 1) ? 0 : 0) : f.querySelectorAll('[data-oa-row]').length };
              if (tb && tb.hasAttribute('data-oa-lean')) out.rows = window.OAChart.rows_from_table(tb, JSON.parse(f.querySelector('script[data-oa-chart-data]').textContent).spec, JSON.parse(f.querySelector('script[data-oa-chart-data]').textContent)).length;
              if (!svg) return out;
              const clone = svg.cloneNode(true);
              clone.removeAttribute('aria-describedby');
              const ser = new XMLSerializer();
              const a = ser.serializeToString(clone);
              const b = node_svg ? ser.serializeToString(new DOMParser().parseFromString(node_svg, 'image/svg+xml').documentElement) : null;
              const norm = x => x ? x.replace(/ aria-labelledby="[^"]*"/g, '').replace(/<title>.*?<\/title>|<desc>.*?<\/desc>/gs, '').replace(/oac-[a-z0-9-]*?-(\d+)-([a-z0-9]+)/g, 'U-$1-$2') : x;
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
            }, { fid, node_svg: node ? node.svg : null, title: spec.title, alt: spec.alt });
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
  return bad ? 1 : 0;
}

// guide_build.py's hook: draw each listed spec for the page, by the chosen method, and return the fragments and faults
async function fragments(o) {
  const list = JSON.parse(fs.readFileSync(o.in, 'utf8'));
  const kp = kit_parts();
  const out = { kit_js: kit_scripts(), kit_css: kp.css, words: K.words, items: {},
    kit_sizes: { core: Buffer.byteLength(kp.core), geo: Buffer.byteLength(kp.geo), css: Buffer.byteLength(kp.css), forms: Object.fromEntries(Object.entries(kp.forms).map(([k, v]) => [k, Buffer.byteLength(v)])) } };
  for (const it of list.items) {
    const spec = JSON.parse(fs.readFileSync(it.spec, 'utf8'));
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
      html = K.figure(spec, res.rows, { id: fid, svg, art_attrs: ' data-oa-lean' });
    } else if (list.method === 'load-table') {
      html = K.figure(spec, res.rows, { id: fid, lean_table: true, types: columns });
      html = html.slice(0, html.lastIndexOf('</figure>')) + island_table(spec, res.rows, columns) + '</figure>';
    } else {
      const isl = island(spec, res.rows, columns, list.method === 'load-trim');
      html = K.figure(spec, res.rows, { id: fid });
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
    ['red touching Prussian', d => { d.marks.push({ kind: 'circle', x: 10, y: 10, w: 4, h: 4, fill: 'point', data: {} }, { kind: 'rect', x: 13, y: 10, w: 10, h: 10, fill: 'seq-5', data: {} }); }, 'touches Prussian'],
    ['a circle sized by radius', d => { d.marks.push({ kind: 'circle', x: 0, y: 0, w: 20, h: 20, r: 10, data: {}, area_of: { value: 25, max_value: 100, max_radius: 40 } }); }, 'sized by area'],
    ['a key told apart by lightness alone, too close', d => { d.keys = [[{ fill: 'subject' }, { fill: 'cat-1' }]]; }, 'lightness'],
  ];
  for (const [name, fn, want] of plant) {
    const d = JSON.parse(JSON.stringify(d0));
    fn(d);
    const f = C.check_drawing(s, d, TOK.newsprint, 'self-test');
    const hit = f.some(x => x.indexOf(want) >= 0);
    console.log(`${hit ? 'caught' : 'MISSED'} ${name}${hit ? '' : ': ' + JSON.stringify(f.slice(0, 3))}`);
    if (!hit) bad++;
  }
  // the CSV check
  const cols = Object.keys(r.datasets[0].meta.columns);
  const csv = C.to_csv(r.rows.slice(1), cols);
  const cf = C.check_csv(K, csv, r.rows, r.datasets[0].meta);
  console.log(`${cf.length ? 'caught' : 'MISSED'} a CSV export short of a row`);
  if (!cf.length) bad++;
  console.log(bad ? `self-test: ${bad} missed` : 'self-test: every planted fault caught');
  return bad ? 1 : 0;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const [cmd, ...rest] = process.argv.slice(2);
  const o = args(rest);
  let code = 2;
  if (cmd === 'build') code = await build(o, false);
  else if (cmd === 'check') code = await build(o, true);
  else if (cmd === 'fragments') code = await fragments(o);
  else if (cmd === 'self-test') code = await self_test();
  else console.error('usage: oa-chart.mjs build|check|fragments|self-test ...');
  process.exit(code);
}
