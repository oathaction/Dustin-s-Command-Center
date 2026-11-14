#!/usr/bin/env node
// The chart kit's one command (contract C3). Builds a chart from its spec and data file, runs its checks, and writes the
// exports and captures.
//
//   node work/build/chart-kit/oa-chart.mjs build <ID|spec path>... [--all] [--widths 1440,390] [--grounds newsprint,charcoal]
//                                          [--out DIR] [--no-png] [--date YYYYMMDD] [--specs DIR]
//   node work/build/chart-kit/oa-chart.mjs check <ID|spec path>... [--all]
//   build and check take --data DIR: a folder of data files and sidecars read before work/build/data/ (AX-S6), for a
//   derived file kept outside the repository
//   build and check also draw every whole width from 256 px (224 for a rule plate) to the widest the guide gives the chart
//   (720 px for a reading chart, 869 for a wide one) on Newsprint, the sweep (AX S1, N1); --no-sweep leaves it out
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

const FORM_FILES = {};
export function load_kit() {
  require(path.join(KIT, 'metrics.js'));
  require(path.join(KIT, 'kit.js'));
  require(path.join(KIT, 'kit-build.js'));   // the builder's half: figure, tables, words (call 10); never on the guide's page
  require(path.join(KIT, 'parts.js'));
  require(path.join(KIT, 'geo.js'));
  // R4-3 (round 4): which forms each file registers, so the page leaves out a file whose forms all build HTML (no draw)
  for (const f of fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js')).sort()) {
    const before = new Set(Object.keys(globalThis.OAChart.forms));
    require(path.join(KIT, 'forms', f));
    FORM_FILES[f] = Object.keys(globalThis.OAChart.forms).filter(k => !before.has(k));
  }
  const K = globalThis.OAChart;
  K.words = JSON.parse(fs.readFileSync(path.join(KIT, 'words.json'), 'utf8'));
  return K;
}
const K = load_kit();
const C = require(path.join(KIT, 'checks.js'));
K.id_types = C.id_types();
const CSS = fs.readFileSync(TOKENS_CSS, 'utf8');
export const TOK = { newsprint: K.tokens_from_css(CSS, 'newsprint'), charcoal: K.tokens_from_css(CSS, 'charcoal') };
K.default_tokens = TOK;   // R4-3: a card's h.mark drawn for a caller that passes no tokens (the snapshot tool) reads these

// page width -> the width the figure's drawing gets (the page's gutters: 16 px under 600, 32 px from 600)
export function container(page, spec) {
  const t = K.token_reader(TOK.newsprint);
  const art = K.artboard(spec, t);
  const gutter = page < 600 ? 16 : 32;
  // C-M2: a staged drawing (spec.stage) keeps its one width wherever the column gives it a desk drawing
  return K.draw_width(spec, Math.min(art, page - 2 * gutter));
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
    else if (a === '--data') o.data_dir = path.resolve(argv[++i]);   // AX-S6: read before work/build/data/
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
  (chk.datasets || []).slice(1).forEach(ds => { if (!ds.geo) out[ds.file.replace(/\.(csv|json)$/, '')] = C.rows_of(K, ds); });
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
    if (ds.geo) return;   // R3-2: the shapes ride once in geo.js, never in a chart's island
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
// round 5 (R5-1): a maker's spec placed at a rule's plate (S96 at Rule 14.142) sets "plate": "rule", so the kit draws it at
// the rule plates' columns and sweeps it from 224 px, as the guide gives it
export function guide_widths(spec) {
  return /^s-1[34]-(?!s\d)/i.test(String(spec.id)) || spec.plate === 'rule' ? GUIDE_WIDTHS.concat(PLATE_WIDTHS) : GUIDE_WIDTHS;
}

// AX S1 (round 2 fix pass, D3-904): the guide draws an entry's chart at any whole width from 256 px (a 320 px screen at
// 400 percent zoom) to 869 px (SWEEP_MAX below), and a rule plate's from 224 px; the six columns above miss widths a phone or tablet gives
// (329 px at a 393 px phone, 560 px at a 768 px tablet). The sweep draws every whole width in that range on Newsprint and
// runs the drawing checks on each; one fault at many widths prints once, with the widths it holds at.
// N1 (access second pass): the widest drawing the guide's own layout gives a chart, measured in Chromium on the strict
// page at every whole window width from 320 to 1920 px and at 2,200 to 3,840: 869 px for a wide chart (720 for a reading
// one, its artboard); the narrowest is 256 for an entry and 224 for a rule plate
export const SWEEP_MAX = 869;
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
  // N1 (access second pass): skip only the columns this spec was already checked at; an entry is never checked at a
  // plate's columns (510 px is a 574 px window), so those stay in its sweep
  const [lo, hi] = sweep_range(spec), seen = new Map(), skip = new Set(guide_widths(spec).map(w => K.draw_width(spec, w)));
  for (let w0 = lo; w0 <= hi; w0++) {
    // C-M2: a staged spec draws its stage at every desk column, so the sweep reads it once and every phone width
    const w = K.draw_width(spec, w0);
    if (skip.has(w)) continue;   // checked already, at this spec's own guide columns
    skip.add(w);
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
  const res = { id: spec.id, faults: [], warnings: [], drawings: [], spec_path: o.spec_path, spec_form: spec.form };
  let chk;
  try { chk = C.check_spec(K, spec, o); } catch (e) { res.faults.push('spec: ' + e.message); return res; }
  res.faults.push(...chk.faults);
  res.warnings.push(...(chk.warnings || []));
  // AX-S6 (round 3 fix pass): a map form that sets a national figure beside the map (a labels key that starts "nation")
  // warns where the spec sets none, since entries 14.115 to 14.120 ask for it
  const fdef = K.forms[spec.form];
  if (fdef && fdef.family === 'maps') {
    const nl = (fdef.labels || []).filter(l => /^nation/.test(l));
    if (nl.length && !nl.some(l => (spec.labels || {})[l] !== undefined)) res.warnings.push(`map: the form prints a national figure beside the map (labels.${nl.join(' or labels.')}) and this spec sets none; entries 14.115 to 14.120 ask for it: print it, or say in a note why the data holds no national row and ask the research lead for one (AX-S6)`);
  }
  // C-M2 (round 3 fix pass): a stage is one desk width, from the phone's limit to the artboard
  if (spec.stage !== undefined) {
    const art = K.artboard(spec, K.token_reader(TOK.newsprint));
    if (!(typeof spec.stage === 'number' && spec.stage >= K.PHONE_MAX && spec.stage <= art)) res.faults.push(`stage: ${JSON.stringify(spec.stage)} is not a width in px from ${K.PHONE_MAX} to the artboard's ${art} (C-M2)`);
  }
  // DR-261 (round 4): stage_min, a floor, is a width in px from the phone's limit to the artboard, and never beside stage
  if (spec.stage_min !== undefined) {
    const art = K.artboard(spec, K.token_reader(TOK.newsprint));
    if (!(typeof spec.stage_min === 'number' && spec.stage_min >= K.PHONE_MAX && spec.stage_min <= art)) res.faults.push(`stage_min: ${JSON.stringify(spec.stage_min)} is not a width in px from ${K.PHONE_MAX} to the artboard's ${art} (DR-261)`);
    if (spec.stage !== undefined) res.faults.push('stage_min: a spec sets stage (one width) or stage_min (a floor), never both (DR-261)');
  }
  res.rows = chk.rows;
  res.datasets = chk.datasets;
  if (!K.forms[spec.form] || !chk.rows || !chk.rows.length) return res;
  // R4-4 (round 4): a social card's crops, each drawn at its true size and checked there (the 36 px floor, the crop's height);
  // no column width, narrow width or sweep applies, since a card never reflows
  if (spec.card !== undefined) {
    const cr = spec.card && spec.card.crops;
    if (!Array.isArray(cr) || !cr.length || cr.some(x => !Array.isArray(x) || x.length !== 2 || x.some(v => !Number.isInteger(v) || v < 480 || v > 2160)))
      res.faults.push('card: crops is a list of [width, height] in whole px from 480 to 2160, such as [[1080, 1350], [1080, 1080]] (R4-4, DR-268)');
    else {
      for (const g of o.grounds) for (const c of cr) {
        let d;
        try { d = K.draw(spec, chk.rows, { width: c[0], crop: c, ground: g, tokens: TOK[g], extra: extra_rows(chk) }); } catch (e) { res.faults.push(`draw ${c[0]} by ${c[1]} on ${g}: ${e.message}`); continue; }
        res.faults.push(...C.check_drawing(spec, d, TOK[g], `${g} ${c[0]} by ${c[1]}`));
        res.drawings.push({ ground: g, page: c[0], crop: `${c[0]}x${c[1]}`, width: d.width, height: d.height, svg: d.svg, bytes: Buffer.byteLength(d.svg) });
      }
    }
    return res;
  }
  // R4-3 (round 4): a card form builds its HTML in Node; the checks read that HTML (check_html) and every mark h.mark drew;
  // its sizes, overflow, overlap and reading order are read in the browser by build (card_checks)
  if (K.is_card(spec)) {
    res.cards = {};
    (o.grounds && o.grounds.length ? o.grounds : ['newsprint']).forEach((g, gi) => {
      let hc;
      try { hc = K.html_card(spec, chk.rows, { ground: g, tokens: TOK[g] }); } catch (e) { res.faults.push(`html on ${g}: ${e.message}`); return; }
      res.cards[g] = K.hold(spec, hc.html);   // as the figure prints it, held phrases in .oac-nw (IM-E1)
      if (!gi) res.faults.push(...C.check_html(spec, res.cards[g], chk.rows));
      hc.marks.forEach((d, i) => {
        res.faults.push(...C.check_drawing({ kit: 1, id: spec.id, form: spec.form }, d, TOK[g], `${g}, mark ${i + 1}`));
        if (d.fluid && d.texts.length) res.faults.push(`html: mark ${i + 1} scales to its box (fluid) and holds words ("${d.texts[0].words.slice(0, 30)}"); set them as HTML beside it (IM-E7)`);
      });
    });
    return res;
  }
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
    for (const w of [...new Set(guide_widths(spec).map(x => K.draw_width(spec, x)))]) {
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
// typography rides along (round 3 fix pass): c.text sets a drawing's words through it, so a page without it drew S81's key
// without its no-break spaces and failed parity
const DRAW_KEYS = ['kit', 'id', 'form', 'artboard', 'stage', 'stage_min', 'card', 'encode', 'labels', 'annotations', 'formats', 'scale', 'table', 'phone', 'typography'];
export function draw_spec(spec) {
  const out = {};
  DRAW_KEYS.forEach(k => { if (spec[k] !== undefined) out[k] = spec[k]; });
  if (out.table) out.table = Object.assign({}, out.table, { caption: undefined });
  if (out.card) out.card = { crops: out.card.crops };   // R4-4: the page draws the crops; the post's words print in the figure
  if (spec.form === 'social-data-card' || spec.card) ['evidence_label', 'title', 'grade_line', 'source_line'].forEach(k => { if (spec[k] !== undefined) out[k] = spec[k]; });   // IM-E8: the grade line too
  return out;
}
export function typography_draws(spec, rows, extra) {
  if (!spec.typography || !K.forms[spec.form] || !rows || !rows.length) return false;
  const bare = Object.assign({}, spec); delete bare.typography;
  const art = K.artboard(spec, K.token_reader(TOK.newsprint));
  return [art, Math.min(art, 358)].some(w => {
    const o = { width: w, ground: 'newsprint', tokens: TOK.newsprint, extra, uid: 'oac-typo' };
    try { return K.draw(spec, rows, o).svg !== K.draw(bare, rows, o).svg; } catch (e) { return true; }
  });
}
export function table_fields(spec) {
  const tb = spec.table || {};
  if (tb.group) return [];   // R3-3: a grouped table carries no row, so the island carries every column the drawing reads
  if (tb.pivot) return [].concat(tb.pivot.row, [tb.pivot.column, tb.pivot.value]);
  return (tb.columns || []).map(c => c.field);
}
export function island_table(spec, rows, columns, extra) {
  if (K.is_card(spec)) return '';   // R4-3: a card draws nothing on the page, so it carries no island
  // method load-table: the drawing spec, the types of the columns it uses, and as CSV only the used columns the table lacks
  // R3-3: a grouped table prints no row, so the island carries only the columns the drawing reads (its encode, where, sort,
  // formats, labels and annotations), never the table's own; the CSV export still lists every column
  const used = used_columns((spec.table || {}).group ? Object.assign({}, spec, { table: undefined }) : spec, columns), inTable = new Set(table_fields(spec));
  const missing = used.filter(c => !inTable.has(c));
  const ctypes = {};
  used.concat([...inTable]).forEach(c => { if (columns[c]) ctypes[c] = { type: columns[c].type }; });
  const payload = { mode: 'table', spec: draw_spec(spec), columns: ctypes };
  // the island carries typography only where it changes a word the drawing prints, read at the artboard and at 358 px
  // (the phone column), so a spec whose typography reaches only its title, notes and table pays nothing for it
  if (payload.spec.typography && !typography_draws(spec, rows, extra)) delete payload.spec.typography;
  if (extra && Object.keys(extra).length) payload.extra = extra;
  // R3-3 (DL-E1): a column that holds a map layer's geoids, every one in the layer's own order, is not carried; the page
  // reads it back from geo.js, which the page carries once
  const gk = geo_key(spec, rows, missing);
  if (gk) { payload.geo_key = gk; missing.splice(missing.indexOf(gk.field), 1); }
  if (missing.length) payload.csv = C.to_csv(rows, missing);
  const carry = K.lean_carry(spec, rows, columns);
  if (Object.keys(carry).length) payload.carry = carry;
  return island_element(payload);
}

// R3-3: the map layer whose ids a column of the rows holds, in order, every one: {field, layer}, or null
export function geo_key(spec, rows, fields) {
  const G = globalThis.OAChartGeo;
  if (!G || !G.layers || !rows.length) return null;
  const files = [].concat(spec.dataset || []);
  for (const name of Object.keys(G.layers)) {
    if (files.indexOf(G.layers[name].file) < 0) continue;
    const ids = K.geo(name).ids;
    if (ids.length !== rows.length) continue;
    for (const f of fields) if (rows.every((r, i) => String(r[f]) === ids[i])) return { field: f, layer: name };
  }
  return null;
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
// R4-3: a form file whose every form builds HTML at build time (html, no draw) never rides on the page
export function card_file(f) { const ks = FORM_FILES[f]; return !!(ks && ks.length && ks.every(k => K.forms[k] && !K.forms[k].draw)); }
export function kit_parts() {
  const forms = fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js') && !card_file(f)).sort();
  const core = ['metrics.js', 'kit.js', 'parts.js'].map(f => minify(fs.readFileSync(path.join(KIT, f), 'utf8'))).join('');
  return { core, geo: minify(fs.readFileSync(path.join(KIT, 'geo.js'), 'utf8')), forms: Object.fromEntries(forms.map(f => [f, minify(fs.readFileSync(path.join(KIT, 'forms', f), 'utf8'))])),
    css: min_css(fs.readFileSync(path.join(KIT, 'kit.css'), 'utf8')) };
}
// the page's kit.css: comments out, then the white space round { } ; , > and after a colon (round 4 weight: 2,175 bytes less;
// the browser's parse of the two gives the same 204 rules). Safe while no quoted string holds those characters, which the
// self-test checks
export function min_css(t) {
  return t.replace(/\/\*[\s\S]*?\*\//g, '').split('\n').map(l => l.trim()).filter(Boolean).join('\n').replace(/\s*([{};,>])\s*/g, '$1').replace(/:\s+/g, ':').replace(/;}/g, '}');
}
export function kit_scripts() {
  const k = kit_parts();
  return [k.core, k.geo].concat(Object.values(k.forms)).join('').replace(/<\/script/gi, '<\\/script');
}
export function kit_scripts_full() {
  const forms = fs.readdirSync(path.join(KIT, 'forms')).filter(f => f.endsWith('.js')).sort().map(f => fs.readFileSync(path.join(KIT, 'forms', f), 'utf8'));
  return [fs.readFileSync(path.join(KIT, 'metrics.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'kit.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'kit-build.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'parts.js'), 'utf8'), fs.readFileSync(path.join(KIT, 'geo.js'), 'utf8')].concat(forms).join('\n').replace(/<\/script/gi, '<\\/script');
}

// A4-E1 (round 4): the sprite symbols a drawing uses (<use href="#oa-sym-...">), and each symbol as the guide's sprite
// carries it, read from the approved black master (its ink drawn in currentColor), for the kit's own page
export function icons_of(drawings) {
  return [...new Set((drawings || []).flatMap(d => [...String(d.svg || d).matchAll(/href="#(oa-sym-[a-z0-9-]+)"/g)].map(m => m[1])))].sort();
}
const ICON_DIR = path.join(ROOT, 'work/build/assets/civic-line-v6/black');
export function kit_symbol(sid) {
  const id = sid.replace(/^oa-sym-/, '').toUpperCase();
  const f = fs.existsSync(ICON_DIR) && fs.readdirSync(ICON_DIR).find(n => n.includes(`-${id}-`) && /-Black\.svg$/.test(n));
  if (!f) return '';
  const t = fs.readFileSync(path.join(ICON_DIR, f), 'utf8').replace(/<!--[\s\S]*?-->/g, '');
  const root = t.match(/<svg\b[^>]*>/);
  const vb = root[0].match(/viewBox="([^"]+)"/)[1];
  const inner = t.slice(root.index + root[0].length, t.lastIndexOf('</svg>')).replace(/<title>[\s\S]*?<\/title>|<desc>[\s\S]*?<\/desc>/g, '')
    .replace(/\sid="[^"]*"/g, '').replace(/"#121212"/g, '"currentColor"').replace(/>\s+</g, '><').trim();
  return `<symbol id="${sid}" viewBox="${vb}">${inner}</symbol>`;
}
function page_html(specs) {
  // specs: [{spec, rows, columns, grounds, extra}]
  // a plain page: tokens.css, kit.css, the kit and its forms, and each figure with its data island (DR-235)
  const body = specs.map(({ spec, rows, columns, grounds, extra }) => grounds.map(g => `<section class="oa-surface-${g} oac-ground" data-ground="${g}">
${(f => f.slice(0, f.lastIndexOf('</figure>')) + island_table(spec, rows, columns, extra) + '</figure>')(K.figure(spec, rows, { id: `oac-${spec.id.toLowerCase()}-${g}`, lean_table: true, types: columns, ground: g, tokens: TOK[g] }))}
</section>`).join('\n')).join('\n');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chart kit build</title><style>${font_css()}</style><style>${CSS}</style><style>${fs.readFileSync(path.join(KIT, 'kit.css'), 'utf8')}</style>
<style>body{margin:0}.oac-ground{padding:32px 32px 40px}@media (max-width:599px){.oac-ground{padding:24px 16px 32px}}.oac-fig[data-wide]{max-width:var(--oa-chart-artboard-wide)}</style>
</head><body>
${(syms => syms.length ? `<svg hidden aria-hidden="true">${syms.map(kit_symbol).join('')}</svg>` : '')([...new Set(specs.flatMap(x => x.syms || []))])}
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
      const html = page_html([{ spec, rows: res.rows, columns: res.datasets.length ? res.datasets[0].meta.columns : (spec.data || {}).columns, grounds: o.grounds, extra: extra_island(res), syms: icons_of(res.drawings) }]);
      const page_file = path.join(dir, spec.id.toLowerCase() + '.html');
      fs.writeFileSync(page_file, html);
      const stem = file_stem(spec, o.date);
      // R4-4 (round 4): a card's crops show at true size on a 1440 px page, so one pass at 1x gives true-pixel PNGs
      const crops = spec.card && spec.card.crops ? spec.card.crops.map(c => `${c[0]}x${c[1]}`) : [null];
      for (const w of (crops[0] ? [1440] : o.widths)) {
        for (const dpr of (crops[0] ? [1] : [1, 2])) {
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
          for (const g of o.grounds) for (const crop of crops) {
            const fid = `#oac-${spec.id.toLowerCase()}-${g}`, sel = crop ? `[data-oa-crop="${crop}"] svg.oac-svg` : 'svg.oac-svg';
            const node = res.drawings.find(d => d.ground === g && (crop ? d.crop === crop : d.page === w));
            const info = await p.evaluate(({ fid, sel, node_svg, title, alt, fonts_note }) => {
              const f = document.querySelector(fid);
              const err = f.getAttribute('data-oa-error');
              const svg = f.querySelector(sel);
              const tb = f.querySelector('table.oac-table');
              const out = { err, rows: tb && tb.hasAttribute('data-oa-lean') ? (tb.querySelector('tbody th[scope=row]') && tb.querySelectorAll('thead th').length > 1 && tb.querySelectorAll('tbody td[data-x]').length + tb.querySelectorAll('tbody td').length !== tb.querySelectorAll('tbody tr').length * (tb.querySelectorAll('thead th').length - 1) ? 0 : 0) : f.querySelectorAll('[data-oa-row]').length };
              if (tb && tb.hasAttribute('data-oa-lean')) out.rows = (isl => window.OAChart.rows_from_table(tb, isl.spec, isl))(window.OAChart.island(f.querySelector('script[data-oa-chart-data]'))).length;
              // RB3-G2 (round 3): a grouped table's rows come back from the island; the page prints one row a group
              if (tb && tb.hasAttribute('data-oa-group')) {
                out.rows = (isl => window.OAChart.rows_from_table(tb, isl.spec, isl))(window.OAChart.island(f.querySelector('script[data-oa-chart-data]'))).length;
                out.groups = tb.querySelectorAll('tbody tr').length;
              }
              // AX-M1 (round 3 fix pass): a column the page prints empty in every row, read from the page itself
              if (tb) {
                const trs = Array.from(tb.querySelectorAll('tbody tr')), heads = Array.from(tb.querySelectorAll('thead th'));
                out.empty_cols = trs.length ? heads.map((h, i) => trs.every(tr => !tr.children[i] || !tr.children[i].textContent.trim()) ? h.textContent.trim() : null).filter(x => x !== null) : [];
              }
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
                if (/\boac-fc-forced\b/.test(src[i].getAttribute('class') || '')) dst[i].setAttribute('data-oa-fc-forced', '');
                dst[i].removeAttribute('class');
              }
              ex.removeAttribute('class');
              // A4-E1 (round 4): a <use> of the page's sprite draws inline in the standalone file, in the ink the page shows
              const su = svg.querySelectorAll('use'), du = ex.querySelectorAll('use');
              du.forEach((u, i) => {
                const sym = document.getElementById((u.getAttribute('href') || '').slice(1));
                if (!sym) return;
                const n = document.createElementNS('http://www.w3.org/2000/svg', 'svg'), ink = getComputedStyle(su[i]).color;
                ['x', 'y', 'width', 'height'].forEach(a => n.setAttribute(a, u.getAttribute(a)));
                n.setAttribute('viewBox', sym.getAttribute('viewBox'));
                n.innerHTML = sym.innerHTML.replace(/currentColor/g, ink);
                u.replaceWith(n);
              });
              // AX-S1 (round 3 fix pass): a mark drawn for forced colors only (fc 'forced') leaves the standalone file
              ex.querySelectorAll('[data-oa-fc-forced]').forEach(n => n.remove());
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
            }, { fid, sel, node_svg: node ? node.svg : null, title: spec.title, alt: spec.alt, fonts_note: K.words.export_fonts });
            if (info.err) { res.faults.push(`page: ${g} ${w}: ${info.err}`); continue; }
            if (dpr === 1) {
              if (!info.parity) res.faults.push(`parity: the page's drawing at ${w} on ${g} differs from the Node drawing the exports use`);
              const t = K.table_rows(spec, res.rows);
              const want = t.pivot ? Object.keys(t.cell).length : t.rows.length;
              if (info.rows !== want) res.faults.push(`table: the page shows ${info.rows} table rows or cells for ${want} data rows (${g} ${w})`);
              if (t.group && info.groups !== t.groups.length) res.faults.push(`table: the page prints ${info.groups} grouped rows for the data's ${t.groups.length} groups (${g} ${w})`);
              (info.empty_cols || []).forEach(lab => res.faults.push(`table: the page prints the column "${lab}" empty in every row (${g} ${w}, AX-M1)`));
              if (!info.export_ok) res.faults.push(`svg export: not standalone or no title and desc (${g} ${w})`);
              fs.writeFileSync(path.join(dir, `${stem}-${title_case(g)}-${crop || w}.svg`), info.export);
              if (crop) {
                // R4-4: the card's PNG at true pixels, exactly its crop
                const pf = path.join(dir, `${stem}-${crop}-${title_case(g)}.png`);
                await (await p.$(fid + ' ' + sel)).screenshot({ path: pf });
                const sz = png_size(fs.readFileSync(pf)), want = crop.split('x').map(Number);
                if (sz.w !== want[0] || sz.h !== want[1]) res.faults.push(`png: ${path.basename(pf)} is ${sz.w} by ${sz.h}, the card's crop ${want[0]} by ${want[1]}`);
              }
              const fig = await p.$(fid);
              if (crop !== crops[crops.length - 1]) continue;   // the figure's proofs once, after its last crop
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

// R4-3 (round 4): a card form in the browser. On the kit's page, at each page width the build names and, with the sweep, at
// every 8 px column from the narrowest guide column to the widest drawing and at the guide's own columns: every text's
// computed size on the type scale and 13 px or more; no box whose words overflow it or leave the cards' box; no two lines
// of words overlapping; each list's items in visual order (DOM order is reading order); and the page's cards equal to
// Node's (text and elements). Exports: a PNG of the cards' box at true pixels for each page width the build names.
export const CARD_SIZES = ['--oa-chart-type-label', '--oa-chart-type-tick', '--oa-chart-type-note', '--oa-chart-type-title-size', '--oa-chart-type-title-phone-size',
  '--oa-chart-type-measure-size', '--oa-chart-type-eyebrow'];
function card_page_width(col) { return col + 64 >= 600 ? col + 64 : col + 32; }
async function card_captures(items, o) {
  const { chromium } = require('/opt/node-tools/node_modules/playwright');
  const browser = await chromium.launch();
  try {
    for (const { spec, res } of items) {
      const dir = path.join(o.out, spec.id.toLowerCase());
      const columns = res.datasets && res.datasets.length ? res.datasets[0].meta.columns : (spec.data || {}).columns;
      const page_file = path.join(dir, spec.id.toLowerCase() + '.html');
      fs.writeFileSync(page_file, page_html([{ spec, rows: res.rows, columns, grounds: o.grounds, extra: {} }]));
      const stem = file_stem(spec, o.date);
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
      const p = await ctx.newPage();
      const errors = [];
      p.on('pageerror', e => errors.push(String(e)));
      await p.goto('file://' + page_file);
      await p.evaluate(() => document.fonts.ready);
      errors.forEach(e => res.faults.push(`page error: ${e}`));
      const art_max = K.artboard(spec, K.token_reader(TOK.newsprint));
      const cols = new Set(guide_widths(spec).filter(w => w <= art_max));
      if (o.sweep) for (let w = Math.min(...guide_widths(spec)); w <= Math.min(SWEEP_MAX, art_max); w += 8) cols.add(w);
      const pages = [...new Set([...o.widths, ...[...cols].map(card_page_width)])].sort((a, b) => a - b);
      const seen = new Map();
      for (const pw of pages) {
        await p.setViewportSize({ width: pw, height: 1000 });
        const got = await p.evaluate(({ sizes, nodes }) => {
          const out = [], probe = document.createElement('span');
          document.body.append(probe);
          const allowed = sizes.map(v => { probe.style.fontSize = `var(${v})`; return parseFloat(getComputedStyle(probe).fontSize); }).filter(x => x > 0);
          probe.remove();
          document.querySelectorAll('figure.oac-fig[data-oa-html]').forEach(f => {
            const g = f.closest('[data-ground]').getAttribute('data-ground'), art = f.querySelector('[data-oa-html]'), ab = art.getBoundingClientRect();
            const lines = [], say = t => t.replace(/\s+/g, ' ').trim().slice(0, 32);
            const tw = document.createTreeWalker(art, NodeFilter.SHOW_TEXT);
            for (let n = tw.nextNode(); n; n = tw.nextNode()) {
              if (!n.textContent.trim() || n.parentElement.closest('svg')) continue;
              const el = n.parentElement, size = parseFloat(getComputedStyle(el).fontSize);
              if (size < 12.95) out.push(`${g}: words under 13 px (${size} px): "${say(n.textContent)}"`);
              else if (!allowed.some(a => Math.abs(a - size) <= 0.3)) out.push(`${g}: words at ${size} px, off the chart type scale: "${say(n.textContent)}"`);
              const rg = document.createRange();
              rg.selectNodeContents(n);
              for (const rc of rg.getClientRects()) {
                if (rc.width < 0.5 || !n.textContent.trim()) continue;
                lines.push({ n, rc });
                if (rc.left < ab.left - 0.5 || rc.right > ab.right + 0.5) out.push(`${g}: words past the cards' box: "${say(n.textContent)}"`);
              }
            }
            // the innermost box whose words overflow it, once
            const ov = [...art.querySelectorAll('*')].filter(el => !el.closest('svg') && el.clientWidth && el.scrollWidth > el.clientWidth + 1);
            ov.filter(el => !ov.some(d => d !== el && el.contains(d))).forEach(el => out.push(`${g}: a <${el.tagName.toLowerCase()}${el.className ? ' class="' + el.className + '"' : ''}> whose words overflow it: "${say(el.textContent)}"`));
            for (let i = 0; i < lines.length; i++) for (let j = i + 1; j < lines.length; j++) {
              const a = lines[i].rc, b = lines[j].rc;
              if (lines[i].n === lines[j].n) continue;
              if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1) out.push(`${g}: words overlap: "${say(lines[i].n.textContent)}" and "${say(lines[j].n.textContent)}"`);
            }
            art.querySelectorAll('ul, ol').forEach(l => {
              const its = [...l.children].filter(c => c.tagName === 'LI').map(c => c.getBoundingClientRect());
              for (let i = 1; i < its.length; i++) {
                const a = its[i - 1], b = its[i];
                if (!(b.top > a.top + 1 || (Math.abs(b.top - a.top) <= 1 && b.left > a.left))) out.push(`${g}: item ${i + 1} of a list sits before item ${i} on the page; the reading order must be the visual order`);
              }
            });
            const t = document.createElement('template');
            t.innerHTML = nodes[g] || '';
            const shape = r => [...r.querySelectorAll('*')].map(e => e.tagName.toLowerCase() + '.' + (e.getAttribute('class') || '')).join(' ');
            if (t.content.textContent !== art.textContent || shape(t.content) !== shape(art)) out.push(`${g}: parity: the page's cards differ from the Node cards`);
          });
          return out;
        }, { sizes: CARD_SIZES, nodes: res.cards });
        const col = pw - (pw < 600 ? 32 : 64);
        for (const x of got) { const k = x.replace(/-?\d+(\.\d+)?/g, '#'); if (!seen.has(k)) seen.set(k, { first: x, ws: [] }); seen.get(k).ws.push(col); }
        if (o.widths.includes(pw)) for (const g of o.grounds) {
          const fid = `#oac-${spec.id.toLowerCase()}-${g}`;
          const art = await p.$(fid + ' [data-oa-html]'), fig = await p.$(fid);
          const pf = path.join(dir, `${stem}-${title_case(g)}-${pw}.png`);
          await art.screenshot({ path: pf });
          const bb = await art.boundingBox(), sz = png_size(fs.readFileSync(pf));
          if (Math.abs(sz.w - Math.round(bb.width)) > 1 || Math.abs(sz.h - Math.round(bb.height)) > 1) res.faults.push(`png: ${path.basename(pf)} is ${sz.w} by ${sz.h}, the cards' box ${Math.round(bb.width)} by ${Math.round(bb.height)}`);
          await fig.screenshot({ path: path.join(dir, `${spec.id.toLowerCase()}-${g}-${pw}.png`) });
          await p.addStyleTag({ content: 'html{filter:grayscale(1)}' });
          await fig.screenshot({ path: path.join(dir, `${spec.id.toLowerCase()}-${g}-${pw}-grayscale.png`) });
          await p.addStyleTag({ content: 'html{filter:none}' });
        }
      }
      for (const v of seen.values()) { const u = [...new Set(v.ws)].sort((a, b) => a - b); res.faults.push(`cards: ${v.first} (at ${u.length} column width${u.length > 1 ? 's' : ''}: ${span_list(u)})`); }
      await ctx.close();
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
      await card_captures(items.filter(i => i.res.cards && Object.keys(i.res.cards).length), o);
      // the grayscale proofs are exact gray (R = G = B), so one 8-bit channel holds the same pixels at half the bytes (E24)
      const { spawnSync } = require('child_process');
      const dirs = items.map(i => path.join(o.out, i.spec.id.toLowerCase()));
      const py = "import sys,glob\nfrom PIL import Image\nfor d in sys.argv[1:]:\n    for f in glob.glob(d+'/*-grayscale.png'):\n        im=Image.open(f)\n        if im.mode!='L': im.convert('L').save(f, optimize=True)";
      const r = spawnSync('python3', ['-I', '-c', py, ...dirs], { encoding: 'utf8' });
      if (r.status !== 0) console.log('grayscale proofs stay RGB: ' + (r.stderr || '').slice(0, 200));
    }
  }
  for (const { spec, res } of items) {
    let wt = null;
    try { wt = plate_weight(spec, res); } catch (e) { res.warnings.push('weight: not measured: ' + e.message); }
    if (wt && wt.with_frame > wt.ceiling && +String(spec.id).replace(/^S/i, '') >= 65) res.warnings.push(`weight: about ${wt.with_frame.toLocaleString('en-US')} bytes on the page with its frame, past ${wt.ceiling.toLocaleString('en-US')}; no plate from round 3 on (S65 and later) goes past it (D3-1328)`);
    const summary = { id: spec.id, form: spec.form, spec: path.relative(ROOT, res.spec_path), rows: res.rows ? res.rows.length : 0,
      drawings: res.drawings.map(d => ({ ground: d.ground, page: d.page, width: d.width, height: d.height, svg_bytes: d.bytes })), faults: res.faults, warnings: res.warnings, weight: wt };
    if (!check_only) fs.writeFileSync(path.join(o.out, spec.id.toLowerCase(), `${spec.id.toLowerCase()}-check.json`), JSON.stringify(summary, null, 1));
    console.log(`${res.faults.length ? 'FAIL' : 'PASS'} ${spec.id} ${spec.form}: ${summary.rows} rows, ${res.drawings.length} drawings, ${res.faults.length} faults`);
    res.faults.slice(0, 40).forEach(f => console.log('  - ' + f));
    if (wt) console.log(`  weight: ${wt.figure.toLocaleString('en-US')} bytes as the guide places it, about ${wt.with_frame.toLocaleString('en-US')} with its plate's frame; share per plate ${wt.share.toLocaleString('en-US')} (${wt.share_from}), ceiling ${wt.ceiling.toLocaleString('en-US')}`);
    // AX-M2 (round 3 fix pass): a warning prints and is written to the check file; it does not fail the spec
    (res.warnings || []).forEach(x => console.log('  ~ warning: ' + x));
    if (res.faults.length) bad++;
  }
  // say where the files went, so a reader who does not code can find them (editor's read, K7)
  if (!check_only) console.log(`wrote: ${o.out}, one folder per spec (its pages, SVG, PNG and CSV exports, captures and check file)`);
  return bad ? 1 : 0;
}

// AX-S6 (round 3 fix pass): what a spec weighs on the guide's page, measured as guide_build.py's load-table method
// places an entry (the figure with its lean table and its compressed island), with a plate's frame added; the share per
// plate is D3-1328's for round 3's plates, and the guide's strict build prints the current share in its report
// ("chapter 14's share per plate")
export const PLATE_FRAME = 750, PLATE_CEILING = 15000;
// D3-1497 (second pass): the share per plate is the one the last guide build of the guide's own chapters reported, which
// guide_build.py writes to plate-share.json; with no such build yet, D3-1328's 14,106
export function plate_share() {
  try {
    const j = JSON.parse(fs.readFileSync(path.join(KIT, 'plate-share.json'), 'utf8'));
    if (j && j.per_plate > 0) return { bytes: j.per_plate, from: `the guide build of ${String(j.built || '').replace('T', ' ')}`, plates: j.plates_to_come };
  } catch (e) { /* no build has written it */ }
  return { bytes: 14106, from: 'D3-1328, no guide build recorded', plates: null };
}
export const PLATE_SHARE = plate_share().bytes;
export function plate_weight(spec, res) {
  if (!res.rows || !res.rows.length || !K.forms[spec.form]) return null;
  const columns = res.datasets && res.datasets.length ? res.datasets[0].meta.columns : (spec.data || {}).columns || {};
  let html = K.figure(spec, res.rows, { id: 'oac-' + String(spec.id).toLowerCase(), lean_table: true, types: columns, guide: true, ground: 'newsprint', tokens: TOK.newsprint });
  html = html.slice(0, html.lastIndexOf('</figure>')) + island_table(spec, res.rows, columns, extra_island(res)) + '</figure>';
  const fig = Buffer.byteLength(html);
  const sh = plate_share();
  return { figure: fig, with_frame: fig + PLATE_FRAME, share: sh.bytes, share_from: sh.from, ceiling: PLATE_CEILING };
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
      html = K.figure(spec, res.rows, { id: fid, lean_table: true, types: columns, guide: true, ground: it.ground || 'newsprint', tokens: TOK[it.ground || 'newsprint'] });
      html = html.slice(0, html.lastIndexOf('</figure>')) + island_table(spec, res.rows, columns, extra_island(res)) + '</figure>';
    } else {
      const isl = island(spec, res.rows, columns, list.method === 'load-trim');
      html = K.figure(spec, res.rows, { id: fid, guide: true, ground: it.ground || 'newsprint', tokens: TOK[it.ground || 'newsprint'] });
      html = html.slice(0, html.lastIndexOf('</figure>')) + isl + '</figure>';
    }
    // A4-E1 (round 4): the figure names the sprite symbols its drawing uses, so the guide's page carries each once
    const syms = icons_of(res.drawings);
    if (html && syms.length) html = html.replace('<figure class="oac-fig"', `<figure class="oac-fig" data-oa-sym="${syms.join(' ')}"`);
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
    ['a bare atlas claim ID (C-3, round 3)', s => { s.notes = ['As the atlas’s claim CL1516 records.']; }, 'CL1516 in notes[0] is an atlas ID not listed'],
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
    // the fixture is a plain table: since --data (AX-S6) a derived sidecar's sources are found in work/build/data/ after
    // the scratch folder, and the fixture's publisher names none of them
    meta.kind = 'public'; delete meta.derived_from; delete meta.derivation;
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
      // round 3: a boundary file may be among a derived table's sources; its publisher must then be named too
      ['census-cb-2024-counties.geojson', 'census-cb-2024-counties.meta.json'].forEach(f => fs.symlinkSync(path.join(DATA, f), path.join(td, f)));
      const both = 'Source: U.S. Bureau of Labor Statistics, all nonfarm employees, monthly change, 2022 to 2026; county boundaries, U.S. Census Bureau, 2024. Retrieved November 6, 2026.';
      const dg = Object.assign({}, der, { derived_from: ['oa-test-public.csv', 'census-cb-2024-counties.geojson'], source_line_variants: Object.assign({}, der.source_line_variants, { both }) });
      const g1 = run_d(dg, both), g2 = run_d(dg);
      const okg = !g1.some(x => /R2-2|not in the data folder/.test(x)) && g2.some(x => /does not name U\.S\. Census Bureau/.test(x));
      console.log(`${okg ? 'pass' : 'FAIL'} a derived table may name a boundary file among its sources, and its line names the Bureau${okg ? '' : ': ' + JSON.stringify(g1.concat(g2).filter(x => /R2-2|data folder|Census/.test(x)).slice(0, 3))}`);
      if (!okg) bad++;
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
    // RF-25: 7 px dots where a 13 px dot hides the interval; then the margins in words, with every margin and the note
    reg('t-iv7', c => { [0, 1, 2].forEach(i => { K.parts.whisker(c, 100, 118, 20 + 30 * i, { key: 'k' + i, low: 1, high: 2 }); c.circle(109, 20 + 30 * i, 3.5, { fill: 'subject', data: { key: 'k' + i, field: 'v', value: 1.5 } }); }); c.height(100); }, { interval: true });
    pass(!faults('t-iv7', 358).some(f => /^interval:/.test(f)), 'an 18 px interval past a 7 px dot passes (it needs 17 px; RF-25)');
    const words = (all, note) => c => { c.margins_in_words(); [0, 1, 2].forEach(i => { c.circle(100, 20 + 30 * i, 3.5, { fill: 'subject', data: { key: 'k' + i, field: 'v', value: 1.5 } }); if (all || i) c.text(110, 25 + 30 * i, '±0.' + (i + 3), { role: 'label', margin_of: 'k' + i }); }); if (note) c.text(0, 120, 'At this width each margin of error is narrower than its dot.', { role: 'note', margin_note: true, max: 300 }); c.height(140); };
    reg('t-ivw-ok', words(true, true), { interval: true });
    reg('t-ivw-short', words(false, true), { interval: true });
    reg('t-ivw-nonote', words(true, false), { interval: true });
    reg('t-iv-none', c => { [0, 1].forEach(i => c.circle(100, 20 + 30 * i, 6.5, { fill: 'subject', data: { key: 'k' + i, field: 'v', value: 1.5 } })); c.height(80); }, { interval: true });
    pass(!faults('t-ivw-ok', 358).some(f => /^interval:/.test(f)), 'margins in words pass with every margin printed and the note drawn (RF-25)');
    say(faults('t-ivw-short', 358).some(f => /1 row\(s\) print no margin \(k0\)/.test(f)), 'margins in words with one margin missing (RF-25)');
    say(faults('t-ivw-nonote', 358).some(f => /the note saying so is not in the drawing/.test(f)), 'margins in words with no note in the drawing (RF-25)');
    say(faults('t-iv-none', 358).some(f => /no row's interval is drawn at this width/.test(f)), 'an interval form that draws no interval and prints no margin (RF-25)');
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
    // ---- round 3 (R3-5, R3-2): nodes, links, trees, flows, and shapes inside a moved group ----
    const P = K.parts;
    const drawn = (fn, w) => { const nm = 'oa-self-test-r3'; K.register_chart({ form: nm, name: 'T', family: 'structure', encode: {}, labels: [], phone: 'same', draw: fn });
      const sp = { kit: 1, id: 'T3', form: nm, encode: {}, labels: {} }; const d = K.draw(sp, [{}], { width: w || 400, ground: 'newsprint', tokens: TOK.newsprint }); delete K.forms[nm]; return { d, f: C.check_drawing(sp, d, TOK.newsprint, 'self-test') }; };
    { const a = drawn(c => { P.link(c, { x: 10, y: 10, w: 0, h: 0 }, { x: 300, y: 10, w: 0, h: 0 }); c.text(100, 15, 'Under a link'); });
      pass(a.f.some(x => x.indexOf('a link crosses "Under a link"') >= 0), 'R3-5: the layout guard fails a link drawn before a word with no halo'); }
    { const a = drawn(c => { c.text(100, 15, 'Under a link'); P.link(c, { x: 10, y: 10, w: 0, h: 0 }, { x: 300, y: 10, w: 0, h: 0 }); });
      pass(a.f.some(x => x.indexOf('a link crosses') >= 0), 'R3-5: the layout guard fails a link drawn after a word'); }
    { const a = drawn(c => { P.link(c, { x: 10, y: 10, w: 0, h: 0 }, { x: 300, y: 10, w: 0, h: 0 }); P.clear_label(c, 100, 15, 'On a link'); });
      pass(!a.f.length, 'R3-5: words set on a link with clear_label pass' + (a.f.length ? ': ' + a.f[0] : '')); }
    { const a = drawn(c => { const A = P.node(c, { x: 10, y: 10, w: 140, h: 40 }, 'Agency'), B = P.node(c, { x: 200, y: 90, w: 140, h: 40 }, 'Final rule');
      P.link(c, A, B, { shape: 'elbow', dir: 'down', arrow: true }); P.link(c, A, B, { shape: 'arc' }); P.link(c, A, B); });
      pass(!a.f.length, 'R3-5: nodes with straight, elbow and arc links to their edges pass, words drawn after links or not' + (a.f.length ? ': ' + a.f[0] : '')); }
    { const c = mk({}); const r = P.node(c, { x: 0, y: 0, w: 60, h: 24 }, 'Office of Information and Regulatory Affairs'); const sz = P.node_size(c, 'Office of Information and Regulatory Affairs', { max: 200 });
      pass(r === null && c._els.length === 0 && sz && sz.w <= 200 && sz.lines >= 2, 'R3-5: a node too small for its words draws nothing and says so; node_size gives the box it needs'); }
    { // A-E3: a node sized by node_size at a width sets its words on the lines it was sized for, at every width tried
      let bad = 0, tried = 0;
      const words = 'Congress and the Department of Health and Human Services';
      for (let w = 90; w <= 260; w += 1) {
        const c = mk({}), sz = P.node_size(c, words, { max: w, min: w, lines: 8, sub: 'the Secretary', sub_lines: 3 });
        if (!sz) continue;
        tried++;
        const n = P.node(c, { x: 0, y: 0, w: sz.w, h: sz.h }, words, { lines: 8, sub: 'the Secretary', sub_lines: 3 });
        const el = n ? c._els.filter(e => e.indexOf('<text') >= 0)[0] : '';
        if (!n || ((el.match(/<tspan/g) || []).length || 1) !== sz.lines) bad++;
      }
      pass(tried > 100 && !bad, `A-E3: a node set in the box node_size gives draws on the lines it was sized for (${tried} widths, ${bad} short)`); }
    { const items = [{ id: 'r', w: 120, h: 30 }, { id: 'a', parent: 'r', w: 100, h: 30 }, { id: 'b', parent: 'r', w: 160, h: 50 }, { id: 'a1', parent: 'a', w: 90, h: 30 }, { id: 'a2', parent: 'a', w: 90, h: 30 }, { id: 'b1', parent: 'b', w: 90, h: 30 }, { id: 'x', parent: 'nobody', w: 40, h: 30 }];
      const T = P.tree(items, { gap: 10, level: 20 }), N = T.nodes;
      let clash = false; for (let i = 0; i < N.length; i++) for (let j = i + 1; j < N.length; j++) { const p = N[i], q = N[j]; if (p.x < q.x + q.w + 9.99 && q.x < p.x + p.w + 9.99 && p.y < q.y + q.h && q.y < p.y + p.h) clash = true; }
      const mid = Math.abs(T.by.r.cx - (T.by.a.cx + T.by.b.cx) / 2) < 0.01, under = N.every(n => !n.parent || n.y >= T.by[n.parent].y + T.by[n.parent].h + 20 - 0.01);
      const R = P.tree(items.slice(0, 6), { dir: 'right' }), I = P.tree(items.slice(0, 6), { dir: 'indent' });
      pass(!clash && mid && under && T.order.join() === 'r,a,a1,a2,b,b1,x' && T.faults.length === 1 && R.by.a1.x > R.by.a.x && I.order.join() === 'r,a,a1,a2,b,b1' && I.by.a1.x === 40,
        'R3-5: the tree lays siblings apart, centers each parent over its children, reads depth first, and names an unknown parent'); }
    { const F = P.flows([{ from: 'In', to: 'Node', value: 30 }, { from: 'Loan', to: 'Node', value: 10 }, { from: 'Node', to: 'Out', value: 35 }], { max_px: 80 });
      const G = P.flows([{ from: 'In', to: 'Node', value: 30 }, { from: 'Node', to: 'Out', value: 25 }, { from: 'Node', to: 'Cash', value: 5 }], { max_px: 60 });
      pass(F.faults.length === 1 && /Node takes in 40 and sends 35/.test(F.faults[0]) && !G.faults.length && G.links[2].out_at === G.px(25) && Math.abs(G.nodes.Node.size - 60) < 1e-9,
        'R3-5: flows share one unit, stack at each node, and fail a node whose bands do not sum'); }
    { const a = drawn(c => { P.flow_band(c, 10, 10, 300, 60, 20, { fill: 'band', edge: false }); });
      const b = drawn(c => { P.flow_band(c, 10, 10, 300, 60, 20, { fill: 'band' }); });
      pass(a.f.some(x => x.indexOf('band:') >= 0) && !b.f.some(x => x.indexOf('band:') >= 0), 'R3-5: a light flow band with no edge fails 3 to 1, and passes with its edges'); }
    { // R3-3 and C-E1: a grouped table prints one row a group with its counts, and the island reads back to every row
      const sp = { id: 'T', table: { columns: [{ field: 'g', label: 'G' }], group: { by: 'st', sort: 'key', columns: [{ label: 'State', agg: 'key', state_name: true }, { label: 'Seats', agg: 'count' },
        { label: 'Won by A', agg: 'count_eq', field: 'w', value: 'A' }, { label: 'Close', agg: 'count_in', field: 'm', to: 5 }, { label: 'Least', agg: 'min', field: 'm', format: 'number:1' }, { label: 'Closest', agg: 'min_name', field: 'm', name: 'g' }] } } };
      const rows = [{ st: 'MI', g: 'MI-01', w: 'A', m: 3.2 }, { st: 'MI', g: 'MI-02', w: 'B', m: 12 }, { st: 'AL', g: 'AL-01', w: 'A', m: 40 }];
      const h = K.table_html(sp, rows, { lean: true });
      pass(/<tr><th scope="row" class="t">Alabama<\/th><td>1<\/td><td>1<\/td><td>0<\/td><td>40\.0<\/td><td class="t">AL-01<\/td><\/tr><tr><th scope="row" class="t">Michigan<\/th><td>2<\/td><td>1<\/td><td>1<\/td><td>3\.2<\/td><td class="t">MI-01<\/td><\/tr>/.test(h)
        && K.table_rows(sp, rows).rows.length === 3 && K.rows_from_table(null, sp, { csv: 'g,m\nMI-01,3.2\n', columns: { g: { type: 'text' }, m: { type: 'number' } } }).length === 1,
        'R3-3: a grouped table prints a row a group with its counts (count_eq: C-E1) and reads its rows from the island' + (/Alabama/.test(h) ? '' : ': ' + h.slice(0, 200))); }
    { // A-E1 and A-E2: a group of two columns, and a list and a count of the set
      const sp = { id: 'T', table: { columns: [{ field: 'm', label: 'M' }], group: { by: ['ch', 'p'], columns: [{ label: 'Group', agg: 'key', words: { 'Senate, D': 'Senate Democrats' } },
        { label: 'Yes', agg: 'count_eq', field: 'v', value: 'Yea' }, { label: 'Named', agg: 'list', field: 'm' }, { label: 'With a seat', agg: 'count_set', field: 's' }] } } };
      const rows = [{ ch: 'Senate', p: 'D', v: 'Yea', m: 'A', s: '1' }, { ch: 'Senate', p: 'D', v: 'Nay', m: 'B', s: '' }, { ch: 'House', p: 'D', v: 'Yea', m: 'C', s: '2' }];
      const h = K.table_html(sp, rows, { lean: true });
      pass(/>Senate Democrats<\/th><td>1<\/td><td class="t">A; B<\/td><td>1<\/td>/.test(h) && />House, D<\/th><td>1<\/td><td class="t">C<\/td><td>1<\/td>/.test(h),
        'A-E1 and A-E2: a table grouped by two columns, with a list and a count of the set' + (/Senate Democrats/.test(h) ? '' : ': ' + h.slice(0, 300))); }
    { // A-E7: a grouped table's words take the spec's typography
      const sp = { id: 'T', typography: { replace: [['Davis (NC) (NC, ', 'Davis (NC, ']], curl_quotes: true }, table: { columns: [{ field: 'm', label: 'M' }], group: { by: 'p', columns: [{ label: 'Party', agg: 'key' },
        { label: 'Broke', agg: 'list', field: 'm', with: ['st', 'v'] }, { label: 'Seats', agg: 'count' }] } } };
      const h = K.table_html(sp, [{ p: "D's", m: 'Davis (NC)', st: 'NC', v: 'Yea' }], { lean: true });
      pass(/>D’s<\/th><td class="t">Davis \(NC, Yea\)<\/td><td>1<\/td>/.test(h), "A-E7: a grouped table's words take the spec's typography" + (/Davis \(NC, Yea\)/.test(h) ? '' : ': ' + h.slice(0, 300))); }
    { // MA-9: a list column's words, keyed by the group, stand in for its list in that group alone
      const sp = { id: 'T', table: { columns: [{ field: 'c', label: 'C' }], group: { by: 'court', columns: [{ label: 'Court', agg: 'key' },
        { label: 'States', agg: 'list', field: 'st', distinct: true, words: { 'Supreme Court': 'Every state, DC and the territories' } }] } } };
      const h = K.table_html(sp, [{ court: 'Supreme Court', st: 'All' }, { court: 'First Circuit', st: 'ME' }, { court: 'First Circuit', st: 'MA' }], { lean: true });
      pass(/>Supreme Court<\/th><td class="t">Every state, DC and the territories<\/td>/.test(h) && />First Circuit<\/th><td class="t">ME; MA<\/td>/.test(h),
        "MA-9: a column's words keyed by the group stand in for its list in that group alone" + (/Every state/.test(h) ? '' : ': ' + h.slice(0, 300))); }
    { // C-3, C-E6: a claim ID listed in v7.ids prints in its typed chip, once
      pass(K.chips('as CL1516 records', ['CL1516']) === 'as <span class="oa-id" data-oa-id="CL1516">Claim CL1516</span> records' && /claim <span class="oa-id" data-oa-id="CL1516">CL1516</.test(K.chips('the atlas’s claim CL1516', ['CL1516'])),
        "C-3: an atlas claim ID takes its typed chip, its type word printed once"); }
    { // A-E5 and A-E6: a list of the rows that broke from their group, with fields in parentheses, and a distinct list
      const sp = { id: 'T', table: { columns: [{ field: 'm', label: 'M' }], group: { by: 'p', columns: [{ label: 'Party', agg: 'key' },
        { label: 'Broke', agg: 'list', field: 'm', odd: 'v', with: ['st', 'v'] }, { label: 'States', agg: 'list', field: 'st', distinct: true }] } } };
      const rows = [{ p: 'D', m: 'A', st: 'NY', v: 'Nay' }, { p: 'D', m: 'B', st: 'NY', v: 'Nay' }, { p: 'D', m: 'Cuellar', st: 'TX', v: 'Yea' },
        { p: 'I', m: 'K', st: 'ME', v: 'Yea' }, { p: 'I', m: 'S', st: 'VT', v: 'Nay' }];
      const h = K.table_html(sp, rows, { lean: true });
      pass(/>D<\/th><td class="t">Cuellar \(TX, Yea\)<\/td><td class="t">NY; TX<\/td>/.test(h) && />I<\/th><td class="t">K \(ME, Yea\); S \(VT, Nay\)<\/td>/.test(h),
        'A-E5 and A-E6: a list of the rows that broke from their group, with fields, and a distinct list' + (/Cuellar/.test(h) ? '' : ': ' + h.slice(0, 300))); }
    { // maker B's S65: a share held as a fraction prints as a percent and reads back to its stored value
      const sp = { id: 'T', table: { columns: [{ field: 'k', label: 'K', row_header: true }, { field: 's', label: 'Share', format: 'fraction-percent:1' }] } };
      const rows = [{ k: 'a', s: 0.9368 }, { k: 'b', s: 0.5 }];
      const h = K.table_html(sp, rows, { lean: true, types: { k: { type: 'text' }, s: { type: 'number' } } });
      const carry = K.lean_carry(sp, rows, { k: { type: 'text' }, s: { type: 'number' } });
      pass(K.fmt(0.9368, 'fraction-percent:1') === '93.7%' && K.fmt(0.05, 'fraction-percent') === '5%' && K.unformat('93.7%', { format: 'fraction-percent:1' }) === '0.937' && />93\.7%</.test(h) && carry.s && /0\.9368/.test(carry.s),
        'fraction-percent prints a fraction as a percent and the table carries its stored value' + (/93\.7%/.test(h) ? '' : ': ' + h.slice(0, 200))); }
    { // A-E4: a link ending in Rule 15.5's open diamond, its far point on the node's edge and the line stopped at its near point
      const a = drawn(c => { const A = P.node(c, { x: 10, y: 10, w: 140, h: 40 }, 'Commission'), B = P.node(c, { x: 200, y: 120, w: 140, h: 40 }, 'Utility');
        const L = P.link(c, A, B, { shape: 'elbow', arrow: 'diamond' }); c.height(170); c.extra.L = L; });
      const dia = a.d.svg.match(/<path d="M([\d.]+),([\d.]+)L[^"]*Z" class="oac-f-surface oac-s-context"/);
      pass(!a.f.length && !!dia && Math.abs(+dia[2] - 120) < 0.6, 'A-E4: a link ends in an open diamond on its node\'s edge' + (a.f.length ? ': ' + a.f[0] : '')); }
    { // R3-3: a one-column island keeps a row whose value is empty
      const back = K.parse_csv(C.to_csv([{ v: 1 }, { v: null }, { v: 3 }], ['v']));
      pass(back.length === 3 && back[1].v === '', 'R3-3: a one-column CSV keeps its empty cells as rows'); }
    { // round 3: a word on a dark step in that step's label ink passes in forced colors; the plain label ink there fails
      const ok1 = drawn(c => { c.rect(0, 0, 200, 40, { fill: 'seq-5', data: { key: 'a' } }); c.text(10, 26, 'OK', { fill: 'on-seq-5' }); c.rect(0, 50, 200, 40, { fill: 'mag-4', data: { key: 'b' } }); c.circle(100, 70, 4, { fill: 'on-mag-4', mark: false }); });
      const bad = drawn(c => { c.rect(0, 0, 200, 40, { fill: 'seq-5', data: { key: 'a' } }); c.text(10, 26, 'OK', { fill: 'label' }); });
      pass(!ok1.f.length && bad.f.some(x => /forced colors/.test(x)) && C.role_color('on-seq-5', TOK.newsprint) && C.contrast(C.role_color('on-seq-5', TOK.newsprint), C.role_color('seq-5', TOK.newsprint)) >= 4.5,
        "round 3: a step's label ink reads on its step, in forced colors too" + (ok1.f.length ? ': ' + ok1.f[0] : '')); }
    { // R3-2: the layers decode to their features; names sit inside or in the eastern column, none on a dark fill; dots are
      // the same at every call and every width; a place projects inside its county
      const Ls = K.geo('states'), Lc = K.geo('counties'), Lca = K.geo('counties-ca'), code = {};
      Object.keys(globalThis.OAChartGeo.tiles).forEach(k => { code[globalThis.OAChartGeo.tiles[k][2]] = k; });
      let lab = null;
      const a = drawn(c => { const T = P.map_fit(c, Ls, { w: c.width - 44 }); const it = Ls.ids.map((id, i) => ({ id, fill: 'seq-' + (1 + (i % 5)) }));
        P.map_shapes(c, Ls, T, it); P.map_mesh(c, Ls, T, {}); P.map_insets(c, Ls, T);
        lab = P.map_labels(c, Ls, T, it.map(x => ({ id: x.id, words: code[x.id], fill: 'on-' + x.fill }))); c.height(T.h); }, 720);
      const dots = w => { let d = null; drawn(c => { const T = P.map_fit(c, Lc, {}); d = P.map_dots(c, Lc, T, { '06037': 4500000, '36061': 2400000, '99999': 5 }, { per: 10000, seed: 7 }); c.height(T.h); }, w); return d; };
      const d1 = dots(720), d2 = dots(720), d3 = dots(400);
      const ki = Lca.index['06029'], li = K.geo.project(Lca, -118.48261, 35.637098);
      pass(Ls.ids.length === 51 && Lc.ids.length === 3144 && !a.f.length && lab.inside.length + lab.beside.length === 51 && d1.dots === 690 && d2.dots === d1.dots && d3.dots === d1.dots && d1.skipped.join() === '99999'
        && Lca.rings(ki).some(rs => K.in_poly(rs, li[0], li[1])),
        'R3-2: layers decode, names sit inside or in the eastern column, dots repeat at every width, a place lands in its county' + (a.f.length ? ': ' + a.f[0] : '') + (lab ? ` (${lab.inside.length} inside, ${lab.beside.length} beside)` : '')); }
    { // RB3-G1: two bands side by side at one height lie on the ground; a band inside a wider one across and down lies on it
      const side = drawn(c => { P.flow_band(c, 10, 10, 150, 10, 40, { fill: 'light-fill' }); P.flow_band(c, 200, 10, 340, 10, 40, { fill: 'light-fill' }); });
      const held = drawn(c => { P.flow_band(c, 10, 10, 340, 10, 60, { fill: 'light-fill' }); P.flow_band(c, 60, 20, 300, 20, 20, { fill: 'light-fill' }); });
      pass(!side.f.some(x => x.indexOf('band:') >= 0) && held.f.some(x => x.indexOf('light-fill band under it') >= 0), 'RB3-G1: a band lies under another only where the other holds it across as well as down'); }
    { const a = drawn(c => { const g = c.group({ transform: 'translate(0,20) scale(0.5)' }); c.rect(0, 0, 400, 40, { fill: 'point', data: { key: 'x' } }); g.end(); });
      const b = drawn(c => { const g = c.group({ transform: 'translate(0,20) scale(2)' }); c.rect(0, 0, 400, 40, { fill: 'subject', mark: false }); g.end(); });
      const e = drawn(c => { const g = c.group({ transform: 'translate(10,20) scale(0.5)' }); c.line(0, 30, 300, 30, { stroke: 'subject', width: 2 }); g.end(); c.text(40, 40, 'Beside the line'); });
      pass(a.f.some(x => x.indexOf('Pillar Red covers') >= 0) && b.f.some(x => x.indexOf('drawn outside its drawing') >= 0) && e.f.some(x => x.indexOf('runs through "Beside the line"') >= 0) && K.parse_transform('rotate(4)') === null,
        'R3-2: the red share, edge and crossing checks reach shapes inside a moved and scaled group'); }
    // ---- round 3 fix pass ----
    { // ST-M1: first prints text through the column's words; ST-S9: a state_name key sorts by the printed name
      const g1 = K.group_cell({ agg: 'first', field: 'n', words: { '28C': '28C, refund' } }, { key: 'x', rows: [{ n: '28C' }, { n: '22' }] });
      const g2 = K.group_cell({ agg: 'first', field: 'n' }, { key: 'x', rows: [{ n: 'HARRIS VICTORY FUND' }] });
      const sp = { table: { group: { by: 'st', sort: 'key', columns: [{ agg: 'key', state_name: true }] } } };
      const order = K.table_groups(sp, [{ st: 'AK' }, { st: 'AL' }, { st: 'DC' }, { st: 'DE' }]).map(g => g.key).join();
      const sp2 = { table: { group: { by: 'k', sort: 'name', columns: [{ agg: 'key', words: { b: 'Apple', a: 'Pear' } }] } } };
      const order2 = K.table_groups(sp2, [{ k: 'a' }, { k: 'b' }]).map(g => g.key).join();
      pass(g1 === '28C, refund' && g2 === 'HARRIS VICTORY FUND' && order === 'AL,AK,DE,DC' && order2 === 'b,a', 'ST-M1 and ST-S9: first prints text; groups sort by the printed name' + ` (${g1}; ${g2}; ${order}; ${order2})`); }
    { // AX-M1: a printed column empty in every row fails; AX-M2: a words column printing an unmapped value warns, words_pass silences it
      const cols = { k: { type: 'text' }, v: { type: 'number' }, e: { type: 'text' } };
      const mk = (tb) => ({ kit: 1, id: 'T', form: 'ranked-bar', illustrative: 'Illustrative data', data: { columns: cols, rows: [{ k: 'a', v: 1, e: '' }, { k: 'b', v: 2, e: '' }] }, encode: { category: 'k', value: 'v' }, table: tb });
      const r1 = C.check_spec(K, mk({ columns: [{ field: 'k', label: 'K', row_header: true, words: { a: 'Ay' } }, { field: 'e', label: 'Empty' }] }), {});
      const r2 = C.check_spec(K, mk({ columns: [{ field: 'k', label: 'K', row_header: true, words: { a: 'Ay' }, words_pass: true }, { field: 'v', label: 'V' }] }), {});
      const r3 = C.check_spec(K, mk({ columns: [{ field: 'k', label: 'K' }], group: { by: 'k', columns: [{ label: 'K', agg: 'key' }, { label: 'Blank', agg: 'first', field: 'e' }] } }), {});
      pass(r1.faults.some(x => /the column "Empty" prints nothing/.test(x)) && r1.warnings.some(x => /"K" has words and prints 1 stored value they do not map \("b"\)/.test(x))
        && !r2.warnings.length && r3.faults.some(x => /the column "Blank" prints nothing in any of its 2 rows/.test(x)), 'AX-M1 and AX-M2: an empty printed column fails, grouped or not; an unmapped words value warns unless words_pass'); }
    { // call 7: map_labels sets a name at the widest run where the label point has no room
      const ring = [[0, 0], [200, 0], [200, 20], [20, 20], [20, 200], [0, 200], [0, 0]];
      const L = { index: { X: 0 }, labels: [[10, 150, 10]], rings: () => [[ring]], arcs: [], ids: ['X'] };
      const T = { pt: p => p, ox: 0, oy: 0, k: 1, box: [0, 0, 200, 200], x: 0, y: 0, w: 200, h: 200 };
      let res = null, res0 = null;
      drawn(c => { res = P.map_labels(c, L, T, [{ id: 'X', words: 'WIDE NAME', weight: 600 }], { role: 'tick', beside: false, inset: 1 }); });
      drawn(c => { res0 = P.map_labels(c, L, T, [{ id: 'X', words: 'WIDE NAME', weight: 600 }], { role: 'tick', beside: false, inset: 1, widest: false }); });
      const b = res && res.inside[0] && res.inside[0].box;
      pass(!!b && res.inside[0].moved && b.y > 0 && b.y + b.h < 20 && b.x > 20 && res0.unplaced.length === 1, 'call 7: map_labels sets a name at the shape\'s widest run where its label point has no room' + (b ? ` (${Math.round(b.x)}, ${Math.round(b.y)})` : '')); }
    { // BC-S2, RB3F-G1: a band key of three steps draws in the band's fill and reads as widths of one ink
      const a = drawn(c => { c.height(P.width_key(c, 0, 0, 0.2, [10, 50, 100], { band: true, len: 32 }) + 4); });
      pass(!a.f.some(x => /^key/.test(x)) && /oac-f-band/.test(a.d.svg), 'BC-S2: width_key with band draws the band fill, and its steps pass the key check' + (a.f.length ? ': ' + a.f[0] : '')); }
    { // C-M2: a stage draws one desk width; AX-S1: fc classes and the key's forced edge; ST-M2: {data_file}; the island keeps typography
      const st = { artboard: 'wide', stage: 1024 };
      const a = drawn(c => { c.rect(0, 0, 10, 10, { fill: 'land', fc: 'region' }); P.key(c, [{ label: 'Authority', stroke: 'label', forced_edge: true }, { label: 'Not voting', fill: 'light-fill', fc: 'muted' }], 0, 40, 380); c.height(80); });
      pass(K.draw_width(st, 600) === 1024 && K.draw_width(st, 479) === 479 && container(1440, st) === 1024 && container(390, st) === 358
        && /oac-fc-region/.test(a.d.svg) && /oac-fc-forced/.test(a.d.svg) && /oac-fc-muted/.test(a.d.svg) && !a.f.length
        && K.chips('In {data_file}.', []).indexOf(K.fill_words('{data_file}')) > 0 && K.fill_words('{data_file}') === K.word('data_file')
        && draw_spec({ id: 'x', typography: { nbsp: true }, stage: 1024 }).typography.nbsp === true && draw_spec({ id: 'x', stage: 1024 }).stage === 1024,
        'C-M2, AX-S1, ST-M2: a stage keeps its desk width; fc classes and a forced edge print; {data_file} fills; the island keeps stage and typography' + (a.f.length ? ': ' + a.f[0] : '')); }
    { // DR-261 (round 4): stage_min is a floor; D3-1546: the stacked tile forced into a 558 px drawing (board 2's picture at a
      // 1024 px window) fails the cell check, and the real form passes at 558 (gray steps) and at 618 (the stacked tile)
      const fl = { artboard: 'wide', stage_min: 618 };
      const floor = K.draw_width(fl, 558) === 618 && K.draw_width(fl, 723) === 723 && K.draw_width(fl, 479) === 479 && container(1440, fl) === 1024 && container(1024, fl) === 960
        && draw_spec({ id: 'x', stage_min: 618 }).stage_min === 618;
      const s12 = JSON.parse(fs.readFileSync(path.join(KIT, 'specs/s12.json'), 'utf8')), r12 = C.check_spec(K, s12, {}).rows;
      const at = (w) => { const d = K.draw(s12, r12, { width: w, ground: 'newsprint', tokens: TOK.newsprint }); return { n: d.cells.length, f: C.check_drawing(s12, d, TOK.newsprint, 'self-test').filter(x => /cell\(s\)/.test(x)) }; };
      const a558 = at(558), a618 = at(618);
      const real = K.forms['tile-map-shift-arrows'], src = fs.readFileSync(path.join(KIT, 'forms/tile-map-shift-arrows.js'), 'utf8');
      const planted = src.replace('var tight = c.phone || size < AY + hw + 1 || wide + 7 > size;', 'var tight = c.phone;');
      let p558 = { n: 0, f: [] };
      if (planted !== src) { new Function(planted)(); p558 = at(558); }
      K.forms['tile-map-shift-arrows'] = real;
      pass(floor && a558.n === 0 && !a558.f.length && a618.n === 51 && !a618.f.length && p558.n === 51 && p558.f.length === 1 && /51 cell\(s\)/.test(p558.f[0]),
        'DR-261, D3-1546: stage_min is a floor; the stacked tile forced into 558 px fails the cell check (51 tiles), and the real form passes at 558 and 618' + (p558.f.length ? '' : ': not caught')); }
    { // R4-3 (round 4): a card form builds HTML in Node; check_html catches each planted fault; the figure carries no island
      // and no drawing script, and the page bundle leaves a card file out; IM-E1: a held phrase prints inside .oac-nw
      const nm = 'oa-self-test-cards';
      K.register_chart({ form: nm, name: 'T', family: 'infographics', encode: {}, labels: [], phone: 'same', html: h => '<ul class="oac-h-cards" role="list">' + h.rows.map((r, i) =>
        `<li class="oac-h-item"${h.row(i)}><p class="oac-h-name">${h.words(r.k)}</p><dl class="oac-h-fields"><dt class="oac-h-k">Term</dt><dd class="oac-h-v">${h.esc(r.t)}</dd></dl>` +
        h.mark(60, 10, c => { c.rect(0, 0, 6 * r.n, 10, { fill: 'subject', data: { key: r.k, value: r.n } }); }) + '</li>').join('') + '</ul>' });
      const sp = { kit: 1, id: 'T4', form: nm, alt: 'Two cards.', title: 'Two cards on Public Law 119-12.', typography: { hold: ['Public Law 119-12'] }, table: { caption: 'C', columns: [{ field: 'k', label: 'K', format: 'text', row_header: true }] } };
      const rows = [{ k: 'One', t: '8 years', n: 3 }, { k: 'Two', t: '14 years', n: 5 }];
      const hc = K.html_card(sp, rows, { tokens: TOK.newsprint }), good = C.check_html(sp, hc.html, rows);
      const plant = (from, to) => C.check_html(sp, hc.html.replace(from, to), rows);
      const caught = [
        plant(' role="list"', '').some(x => /role="list"/.test(x)),
        plant('oac-h-name', 'oac-h-title').some(x => /class oac-h-title/.test(x)),
        plant(' data-oa-row="1"', '').some(x => /print in no item/.test(x)),
        plant(' data-oa-row="1"', ' data-oa-row="0"').some(x => /printed by two items/.test(x)),
        plant('<p class="oac-h-name">Two</p>', '<h3>Two</h3>').some(x => /<h3> is not a card element/.test(x)),
        plant('>Term</dt><dd class="oac-h-v">14', '>Length</dt><dd class="oac-h-v">14').some(x => /same fields/.test(x)),
        plant('8 years', 'eight years — at most').some(x => /em dash/.test(x)),
        plant('<p class="oac-h-name">One', '<p class="oac-h-name" style="color:red">One').some(x => /attribute style/.test(x))];
      const fig = K.figure(sp, rows, { id: 'oac-t4', tokens: TOK.newsprint }), isl = island_table(sp, rows, {}, {});
      delete K.forms[nm];
      pass(!good.length && hc.marks.length === 2 && caught.every(Boolean) && /data-oa-static data-oa-html data-oa-drawn="html"/.test(fig) && !/oac-noscript/.test(fig) && /<details class="oac-eq" data-role="equivalent"><summary>/.test(fig)
        && /<span class="oac-nw">Public Law 119-12<\/span>/.test(fig) && isl === '' && /aria-hidden="true"/.test(hc.html)
        && K.typeset(sp, 'Public Law 119-12 passed') === 'Public Law 119-12 passed',
        'R4-3, IM-E1: a card form\'s HTML passes clean and check_html catches eight planted faults; the card figure carries no island or scripts-off line, its table folded; a held phrase prints in .oac-nw' + (good.length ? ': ' + good[0] : '') + (caught.every(Boolean) ? '' : ': missed ' + caught.map((x, i) => x ? null : i + 1).filter(Boolean).join(', '))); }
    { // A4-E1 (round 4): a Civic Line drawing by <use> of the sprite, read by the checks as a shape (a word on it is caught);
      // a typed chip with its edge clear of its words; the kit page's symbol from the approved master, one ink
      const a = drawn(c => { P.icon(c, 'CL-050', 0, 0, 48); P.chip(c, 60, 30, 'Variable A2'); c.height(60); });
      const b = drawn(c => { P.icon(c, 'CL-050', 0, 0, 48); c.text(4, 30, 'On the drawing', { role: 'tick' }); c.height(60); });
      const sym = kit_symbol('oa-sym-cl-050');
      pass(!a.f.length && /<use href="#oa-sym-cl-050" x="0" y="0" width="48" height="48" class="oac-icon"/.test(a.d.svg) && a.d.ink.some(q => q.kind === 'icon' && q.w === 48)
        && icons_of([a.d]).join() === 'oa-sym-cl-050' && b.f.length > 0 && /^<symbol id="oa-sym-cl-050" viewBox="0 0 128 128">/.test(sym) && sym.indexOf('currentColor') > 0 && sym.indexOf('#121212') < 0,
        'A4-E1: the icon part draws a <use> of the sprite with a box the checks read (a word on it caught), the chip part draws clean, and the kit page\'s symbol comes from the approved master in one ink' + (a.f.length ? ': ' + a.f[0] : '')); }
    { // R4-4, IM-E5 (round 4): a card's crop is exactly its height with a 36 px floor; c.inner draws S19's dot plot across in
      // rank order, 50 columns, the two named states labeled clear of every dot; outside a card S19 draws as before
      const s19 = JSON.parse(fs.readFileSync(path.join(KIT, 'specs/s19.json'), 'utf8')), r19 = C.check_spec(K, s19, {}).rows;
      K.register_chart({ form: 'oa-self-test-card', name: 'T', family: 'infographics', inner: true, encode: { of: 'form' }, labels: [], phone: 'same',
        draw: c => { c.inner(40, 40, 1000, 36 / 13, { label: 'named', ranks: 'across', height: 220 }); c.height(10); } });
      const sp = Object.assign({}, s19, { form: 'oa-self-test-card', encode: Object.assign({ of: 'dot-plot' }, s19.encode) });
      const d = K.draw(sp, r19, { width: 1080, crop: [1080, 760], ground: 'newsprint', tokens: TOK.newsprint });
      delete K.forms['oa-self-test-card'];
      const dots = d.marks.filter(m => m.kind === 'circle' && m.data && m.data.key !== undefined), xs = dots.map(m => m.x);
      const labs = d.texts.filter(t => /^(Mississippi|Massachusetts) \d+$/.test(t.words));
      const small = d.guard.filter(g => /under 36 px/.test(g)), plain = K.draw(s19, r19, { width: 720, ground: 'newsprint', tokens: TOK.newsprint });
      pass(d.height === 760 && dots.length === 50 && xs.every((x, i) => !i || x > xs[i - 1]) && labs.length === 2 && !d.warnings.length && !small.length && plain.marks.filter(m => m.kind === 'circle').length >= 50,
        'R4-4, IM-E5: a crop is exactly its height; S19 across on a card draws 50 columns in rank order with its two named states and no word under 36 px' + (d.warnings.length ? ': ' + d.warnings[0] : '') + (small.length ? ': ' + small[0] : '')); }
    { // the design director's orphan guard (round 4): with typography.pretty a last line of one word takes the word before it;
      // without the key K.wrap is unchanged
      const t = 'one two three four five six seven eight nine ten eleven twelve', w = K.measure('one two three four five six seven eight nine ten eleven', 13, 400, 'reading') + 2;
      const a = K.wrap(t, 13, w, 400, 'reading'), b = K.wrap(t, 13, w, 400, 'reading', true);
      pass(a.length === 2 && a[1] === 'twelve' && b.length === 2 && b[1] === 'eleven twelve' && K.wrap('two words', 13, 20, 400, 'reading', true).join('|') === K.wrap('two words', 13, 20, 400, 'reading').join('|'),
        'the orphan guard: typography.pretty moves a lone last word\'s neighbour down; without it the lines are as before'); }
    { // board 2 (A1): a table caption's {data_file} fills in the visible caption, the table's name and the summary's hidden words
      const sp = { id: 'T', title: 'A title.', table: { caption: 'Every row is in {data_file}', columns: [{ field: 'k', label: 'Key', format: 'text', row_header: true }] } };
      const fig = [false, true].map(g => K.figure(sp, [{ k: 'A' }], { id: 'oac-t', guide: g }));
      pass(fig.every(h => h.indexOf('{data_file}') < 0 && h.split('Every row is in this chart').length - 1 >= 3),
        'board 2: a table caption\'s {data_file} fills in the caption, the table\'s name and the summary, never printed raw'); }
    { // C-E7: a pivot's text cells take the spec's typography, and the lean table reads them back with no carried value
      const sp = { id: 'T', typography: { replace: [['...', 'No state law']] }, table: { columns: [{ field: 'st', label: 'State', format: 'text', row_header: true }], pivot: { row: 'st', column: 'y', value: 'r', format: 'text' } } };
      const rows = [{ st: 'AL', y: 2020, r: '...' }, { st: 'AL', y: 2024, r: '7.25' }];
      const lean = K.table_html(sp, rows, { lean: true, types: { st: { type: 'text' }, y: { type: 'integer' }, r: { type: 'text' } } }), full = K.table_html(sp, rows);
      pass(/<td>No state law<\/td>/.test(lean) && !/>\.\.\.</.test(lean) && /No state law/.test(full) && !/data-v="\.\.\."/.test(lean), 'C-E7: a pivot\'s text cells take the typography and read back as printed'); }
    { // A-E8: a part drawn from the first rows reads every row as c.all_rows
      let seen = null; K.register_chart({ form: 'oa-self-test-all', name: 'T', family: 'structure', encode: {}, labels: [], phone: 'same', draw: c => { seen = [c.rows.length, (c.all_rows || c.rows).length]; c.height(10); } });
      K.draw({ kit: 1, id: 'T', form: 'oa-self-test-all', encode: {} }, [{}, {}], { width: 300, ground: 'newsprint', tokens: TOK.newsprint, all_rows: [{}, {}, {}, {}, {}] }); delete K.forms['oa-self-test-all'];
      pass(seen && seen[0] === 2 && seen[1] === 5, 'A-E8: a part drawn from its first rows reads every row'); }
    { // AX-S6: a source line's retrieval dates, and --data read before work/build/data/
      const d1 = C.retrieved_dates('Source: X; Y. Retrieved November 12 and 13, 2026. Survey estimates.'), d2 = C.retrieved_dates('Source: X. Retrieved October 30 and November 3, 2026.'), d3 = C.retrieved_dates('Source: X, 2026.');
      const td = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'oa-kit-data-'));
      const m = JSON.parse(fs.readFileSync(path.join(C.DATA, 'census-sahie-county-uninsured.meta.json'), 'utf8')); m.file = 'own-file.csv';
      fs.writeFileSync(path.join(td, 'own-file.csv'), 'a\n1\n'); fs.writeFileSync(path.join(td, 'own-file.meta.json'), JSON.stringify(m));
      const own = C.load_dataset('own-file', td), frozen = C.load_dataset('census-cb-2024-states', td), none = C.load_dataset('no-such-file', td);
      fs.rmSync(td, { recursive: true, force: true });
      pass(d1.join() === '2026-11-12,2026-11-13' && d2.join() === '2026-10-30,2026-11-03' && d3 === null && own.file === 'own-file.csv' && frozen.geo === true && !!none.fault,
        'AX-S6: retrieval dates read from a source line; --data read first, work/build/data/ after'); }
  }
  // round 4: the page's CSS minify is safe only while no quoted string in kit.css (outside comments) holds { } ; , > or ": "
  const qs = (fs.readFileSync(path.join(KIT, 'kit.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '').match(/"[^"]*"|'[^']*'/g) || []).filter(q => /[{};,>]|: /.test(q));
  const mc = min_css('.a > .b , .c { color: red ; }\n@media (x: y) { .d { e: f; } }') === '.a>.b,.c{color:red}@media (x:y){.d{e:f}}';
  console.log(`${!qs.length && mc ? 'pass' : 'FAIL'} the page's kit.css minify keeps every rule (no quoted string it could change${qs.length ? ': ' + qs[0] : ''})`);
  if (qs.length || !mc) bad++;
  // round 5 (the complex examples maker's request 3): a margin column prints where each value stands against the margin, a
  // value equal to it inside, and is never read back
  {
    const mcol = { field: 'v', format: 'margin', words: { below: 'Drop past', above: 'Gain past', within: 'Within' } };
    const got = [-140, -122, 0, 122, 133, null].map((v) => K.cell_text(mcol, { v }, { labels: { margin: { value: 122 } } }));
    const own = K.cell_text(Object.assign({ margin: 50 }, mcol), { v: 60 }, {});
    const ok = JSON.stringify(got) === JSON.stringify(['Drop past', 'Within', 'Within', 'Within', 'Gain past', '']) && own === 'Gain past';
    console.log(`${ok ? 'pass' : 'FAIL'} a margin column: past it below, inside it (its edge included), past it above, an empty value empty; a column's own margin first`);
    if (!ok) bad++;
  }
  // round 5 (the complex examples maker's request 4): S96's band words stand clear of every column, or stay out where the
  // drawing has no clear place (210 px, a 256 px window); planted over the October 2025 column, the guard fails them
  {
    const s96 = JSON.parse(fs.readFileSync(path.join(KIT, 'specs/s96.json'), 'utf8')), c96 = C.check_spec(K, s96, {});
    const lab = s96.labels && s96.labels.margin && s96.labels.margin.label;
    const at = (w) => { const d = K.draw(s96, c96.rows, { width: w, ground: 'charcoal', tokens: TOK.charcoal, extra: extra_rows(c96) }); return { d, t: d.texts.find((x) => x.words === lab), f: C.check_drawing(s96, d, TOK.charcoal, 'self-test').filter((x) => /keeps clear of every mark/.test(x)) }; };
    const narrow = at(210), wide = at(400);
    const col = (wide.d.ink || []).find((b) => b.fill === 'subject' && b.kind === 'rect');
    let caught = false;
    if (wide.t && col) {
      const d2 = Object.assign({}, wide.d, { texts: wide.d.texts.map((x) => x === wide.t ? Object.assign({}, x, { x: col.x - x.w / 2, y: col.y + 2 }) : x) });
      caught = C.check_drawing(s96, d2, TOK.charcoal, 'self-test').some((x) => /keeps clear of every mark/.test(x));
    }
    const ok = !!lab && !narrow.f.length && !wide.f.length && !!wide.t && caught;
    console.log(`${ok ? 'pass' : 'FAIL'} S96's band words clear every column (at 400 px set, at 210 px ${narrow.t ? 'set' : 'left out'}), and planted over the October 2025 column the guard fails them`);
    if (!ok) bad++;
  }
  // round 5 (the design director's DD-E1, DD-E2): S96's named words in one stack under the band, clear of its edges; moved
  // onto the band's lower edge, they fail, halo or not
  {
    const s96 = JSON.parse(fs.readFileSync(path.join(KIT, 'specs/s96.json'), 'utf8')), c96 = C.check_spec(K, s96, {});
    s96.labels = Object.assign({}, s96.labels, { named_stack: true }); s96.scale = { y: [-300, 850] };
    const d = K.draw(s96, c96.rows, { width: 720, ground: 'newsprint', tokens: TOK.newsprint, extra: extra_rows(c96) });
    const name = [].concat((s96.labels.named[0] || {}).text || [])[0], t = d.texts.find((x) => x.words === name);
    const edge = (d.ink || []).filter((b) => b.band_edge).sort((a, b) => b.y - a.y)[0];
    const clean = !C.check_drawing(s96, d, TOK.newsprint, 'self-test').some((x) => /band's edge/.test(x));
    let caught = false;
    if (t && edge) {
      const d2 = Object.assign({}, d, { texts: d.texts.map((x) => x === t ? Object.assign({}, x, { y: edge.y - x.h / 2, x: t.x }) : x) });
      caught = C.check_drawing(s96, d2, TOK.newsprint, 'self-test').some((x) => /band's edge runs through/.test(x));
    }
    const ok = !!t && !!edge && clean && caught;
    console.log(`${ok ? 'pass' : 'FAIL'} S96's named words stacked clear of the band's edges at 720 px, and moved onto the lower edge (halo and all) the guard fails them`);
    if (!ok) bad++;
  }
  // the words inside kit.js equal words.json
  const wj = Object.assign({}, K.words); delete wj.about;
  const same = JSON.stringify(wj) === JSON.stringify(K.WORDS);
  console.log(`${same ? 'pass' : 'FAIL'} the words carried in kit-build.js equal words.json`);
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
