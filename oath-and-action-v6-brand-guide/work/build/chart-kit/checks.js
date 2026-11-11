// The chart kit's checks (contract C3a), for Node: the CLI (oa-chart.mjs) and guide_build.py through it run them on every
// spec and drawing. Each check returns a list of faults; an empty list passes. The self-test plants one fault of each kind.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '../../..');
const DATA = path.join(ROOT, 'work/build/data');
const V7_PATH = path.join(ROOT, 'work/extract/atlas-v7-data.json');
const FAMILIES = ['comparison', 'shift-and-swing', 'change-over-time', 'composition', 'distribution-and-density', 'correlation',
  'uncertainty-and-estimates', 'proportion-and-overlap', 'gauges-and-indicators', 'behavior', 'structure', 'relationships', 'flow',
  'maps', 'tables-and-plain-words', 'infographics'];
const TIERS = ['core', 'extended', 'reference', 'avoid'];
const EVIDENCE = ['finding', 'association', 'estimate', 'illustration'];
const REQUIRED = ['kit', 'id', 'form', 'family', 'tier', 'reader_question', 'evidence', 'evidence_label', 'title', 'measure_line',
  'source_line', 'illustrative', 'alt', 'table', 'phone', 'domain', 'states', 'encode'];
const DOMAINS = Array.from({ length: 10 }, (_, i) => 'D' + String(i + 1).padStart(2, '0')).concat(['all']);
// The retired disclosure (DR-100, D2-1756): any copy of its words fails
const DISCLOSURE = /Yes on 3|Veterans for All Voters|Ranked Choice Melrose|\bDisclosure:/i;
// Words and codes that never reach a reader, as guide_check.js lists them (D2-253): decision codes, studio words, internal names
const STUDIO = [[/\b(?:DR|D1|D2|D3|G1)-\d+/, 'a decision code'], [/\bMaster Brief\b/, 'an internal document'], [/\bPhase\b/, 'a studio word'],
  [/\bGates?\b/, 'a studio word'], [/\b[Bb]oards?[\s\u00a0]+(?:\d+|[A-F])\b/, 'a studio word'], [/\bthe studio\b/i, 'a studio word'],
  [/\bV5\b/, 'an internal edition name'], [/\bAtlas V7/, 'an internal document; the guide says "Oath & Action\u2019s systems atlas"']];
const COLOR_LITERAL = /#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b|\brgba?\(|\bhsla?\(|\boklch\(|\blab\(/;
// V7's grade words for a claim or connection (Gate 1, M1 and M2) and the grades a causal verb needs (H08, Rule 13.2)
const V7_GRADES = ['documented', 'well-supported', 'well supported', 'plausible', 'plausible_contested', 'contested', 'hypothesis',
  'official statistic', 'official results', 'secondary compilation', 'conditional directions, no forecast', 'mixed'];
const CAUSAL = /\b(caus(?:e|es|ed|ing)|dr(?:ive|ives|ove|iving)|leads? to|led to|rais(?:e|es|ed)|lower(?:s|ed)?|cut(?:s)?|boost(?:s|ed)?|because of)\b/i;
const WEAK = ['plausible', 'plausible_contested', 'contested', 'hypothesis'];
const PRUSSIAN = '#1F2D5A';
const RED = '#E63946';
const KEY_LIGHTNESS_MARGIN = 10;   // CIE L* between any two key entries told apart by fill alone

let V7 = null;
function v7() {
  if (V7) return V7;
  const d = JSON.parse(fs.readFileSync(V7_PATH, 'utf8'));
  const ids = new Map();
  const add = (k, type) => { if (k) ids.set(k, type); };
  Object.keys(d.nodes).forEach(k => add(k, 'Variable'));
  Object.keys(d.links).forEach(k => add(k, 'Connection'));
  Object.keys(d.loops).forEach(k => add(k, 'Loop'));
  Object.keys(d.reforms).forEach(k => add(k, 'Reform'));
  Object.keys(d.issues).forEach(k => add(k, 'Issue'));
  d.pathways.forEach(p => add(p.id, 'Pathway'));
  d.repairLog.rows.forEach(r => add(r.id, 'Repair log'));
  Object.keys(d.deliveryLog).forEach(k => add(k, 'Delivery log'));
  d.domains.forEach(x => add(x.id, 'Domain'));
  d.overlays.forEach(x => add(x.id, 'Overlay'));
  V7 = { data: d, ids, snapshot: d.meta.snapshot };
  return V7;
}

function strings(node, out, where) {
  out = out || [];
  where = where || '';
  if (typeof node === 'string') out.push([where, node]);
  else if (Array.isArray(node)) node.forEach((x, i) => strings(x, out, where + '[' + i + ']'));
  else if (node && typeof node === 'object') Object.keys(node).forEach(k => strings(node[k], out, where ? where + '.' + k : k));
  return out;
}

// ---------------------------------------------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------------------------------------------
function load_dataset(name, dir) {
  dir = dir || DATA;
  const mp = path.join(dir, name + '.meta.json');
  if (!fs.existsSync(mp)) return { fault: `dataset ${name}: no sidecar ${path.relative(ROOT, mp)}` };
  const meta = JSON.parse(fs.readFileSync(mp, 'utf8'));
  const fp = path.join(dir, meta.file || '');
  if (!fs.existsSync(fp)) return { fault: `dataset ${name}: no data file ${meta.file}` };
  const text = fs.readFileSync(fp, 'utf8');
  return { meta, text, file: meta.file, json: fp.endsWith('.json') };
}

function rows_of(K, ds) {
  const raw = ds.json ? JSON.parse(ds.text).rows : K.parse_csv(ds.text);
  return K.type_rows(raw, ds.meta.columns);
}

// ---------------------------------------------------------------------------------------------------------------
// The spec against the contract, its data, its words and V7
// ---------------------------------------------------------------------------------------------------------------
function check_spec(K, spec, opts) {
  opts = opts || {};
  const f = [];
  const datasets = [];
  for (const k of REQUIRED) if (spec[k] === undefined || spec[k] === null || spec[k] === '') f.push(`spec: "${k}" is missing`);
  if (spec.dataset === undefined && spec.data === undefined) f.push('spec: "dataset" is missing');
  if (spec.kit !== 1) f.push(`spec: "kit" must be 1 (contract 1), not ${JSON.stringify(spec.kit)}`);
  if (spec.form && !K.forms[spec.form]) f.push(`spec: form "${spec.form}" is not registered`);
  if (spec.family && FAMILIES.indexOf(spec.family) < 0) f.push(`spec: family "${spec.family}" is not one of the coverage plan's 16`);
  if (spec.tier && TIERS.indexOf(spec.tier) < 0) f.push(`spec: tier "${spec.tier}" is not core, extended, reference or avoid`);
  if (spec.evidence && EVIDENCE.indexOf(spec.evidence) < 0) f.push(`spec: evidence "${spec.evidence}" is not finding, association, estimate or illustration`);
  if (spec.phone && ['same', 'differs'].indexOf(spec.phone) < 0) f.push('spec: phone is "same" or "differs"');
  if (spec.phone === 'differs' && !spec.phone_note) f.push('spec: a phone drawing that differs needs "phone_note"');
  if (spec.domain && DOMAINS.indexOf(spec.domain) < 0) f.push(`spec: domain "${spec.domain}" is not D01 to D10 or all`);
  if (spec.states && (!Array.isArray(spec.states) || spec.states.some(s => !/^[A-Z]{2}$/.test(s)))) f.push('spec: states is a list of USPS codes');
  if (spec.illustrative !== false && (typeof spec.illustrative !== 'string' || !spec.illustrative.trim())) f.push('spec: illustrative is false or the printed label, such as "Illustrative data"');
  if (spec.source_line && !/^Source: /.test(spec.source_line)) f.push('spec: source_line starts "Source: "');
  if (spec.title && /^\s*[a-z]/.test(spec.title)) f.push('spec: the title starts with a capital');
  // words
  for (const [where, s] of strings(spec)) {
    if (where.indexOf('notes_internal') === 0) continue;
    if (/—/.test(s)) f.push(`words: an em dash in ${where}`);
    if (/‑/.test(s)) f.push(`words: U+2011 in ${where}; IDs take an ASCII hyphen (D2-975)`);
    if (DISCLOSURE.test(s)) f.push(`words: the retired disclosure in ${where} (DR-100, D2-1756)`);
    if (COLOR_LITERAL.test(s)) f.push(`words: a literal color in ${where}; color comes from oa.chart tokens only`);
    if (!/^(?:form|family|tier|dataset|encode|where|sort|formats|scale|artboard|phone$|phone_note|reader_question|domain|states|v7|kit|id$|failure|show|data\b|table\.columns\[\d+\]\.(?:field|format)|table\.pivot\.(?:row|column|value|format))/.test(where)) {
      for (const [re, what] of STUDIO) if (re.test(s)) { f.push(`words: ${what} in ${where} ("${(s.match(re) || [''])[0]}")`); break; }
    }
  }
  // data
  const names = spec.dataset === undefined ? [] : (Array.isArray(spec.dataset) ? spec.dataset : [spec.dataset]);
  let rows = null, first = null;
  if (spec.data) {
    if (!spec.illustrative) f.push('spec: inline "data" is only for invented data, with the Illustrative label');
    rows = K.type_rows(spec.data.rows || [], spec.data.columns || {});
    first = { meta: { kind: 'illustrative', columns: spec.data.columns || {}, printed_source_line: spec.source_line } };
  }
  names.forEach((n, i) => {
    const ds = load_dataset(n, opts.data_dir);
    if (ds.fault) { f.push(ds.fault); return; }
    datasets.push(ds);
    if (i === 0) { first = ds; rows = rows_of(K, ds); }
    if (DISCLOSURE.test(JSON.stringify(ds.meta)) || ds.meta.required_text) f.push(`dataset ${n}: its sidecar carries the retired disclosure (DR-100)`);
    if (ds.meta.kind === 'illustrative' && !spec.illustrative) f.push(`dataset ${n} is invented; the spec prints the Illustrative label`);
  });
  let sel = rows ? K.select(spec, rows) : [];
  if (rows && !sel.length) f.push('data: no rows left after "where"');
  if (first && spec.where) for (const k of Object.keys(spec.where)) if (!(k in (first.meta.columns || {}))) f.push(`where: column ${k} is not in the data`);
  if (first) {
    const cols = first.meta.columns || {};
    const fields = [];
    const enc = spec.encode || {};
    Object.keys(enc).forEach(k => { const v = enc[k]; (Array.isArray(v) ? v : [v]).forEach(x => { if (typeof x === 'string' && k !== 'of') fields.push([k, x]); }); });
    for (const [k, x] of fields) if (!(x in cols)) f.push(`encode.${k}: column "${x}" is not in ${first.file || 'the data'}`);
    const tb = spec.table || {};
    (tb.columns || []).forEach(c => { if (!(c.field in cols)) f.push(`table: column "${c.field}" is not in the data`); });
    if (tb.pivot) ['row', 'column', 'value'].forEach(k => { if (!(tb.pivot[k] in cols)) f.push(`table.pivot.${k}: "${tb.pivot[k]}" is not in the data`); });
    if (!tb.columns || !tb.columns.length) f.push('table: no columns; every chart carries its table equivalent');
    // the source line against the sidecar (H04)
    if (datasets.length === 1) {
      const m = datasets[0].meta;
      const ok = [m.printed_source_line].concat(Object.values(m.source_line_variants || {}));
      if (ok.indexOf(spec.source_line) < 0) f.push(`source: the source line differs from ${datasets[0].file}'s printed_source_line (or its variants)`);
    } else if (datasets.length > 1) {
      // each dataset's publisher appears: any one of its "; " parts, whole or after its last comma, with "United States" read as "U.S."
      const norm = x => String(x).replace(/United States/g, 'U.S.').trim();
      const line = norm(spec.source_line);
      datasets.forEach(d => {
        const parts = String(d.meta.publisher).split(';').map(norm);
        const ok = parts.every(p => line.indexOf(p) >= 0 || line.indexOf(p.split(',').slice(-1)[0].trim()) >= 0);
        if (!ok) f.push(`source: the source line does not name ${d.meta.publisher}`);
      });
    }
  }
  // V7: the values a chart draws from the atlas carry the grade and every ID in its chip
  const usesV7 = datasets.some(d => d.meta.kind === 'v7' || /^v7-/.test(d.file || ''));
  if (usesV7 && !spec.v7) f.push('v7: a chart of Atlas V7 data names "v7": {grade, ids, snapshot}');
  const V = v7();
  if (spec.v7) {
    if (spec.v7.snapshot && spec.v7.snapshot !== V.snapshot) f.push(`v7: snapshot ${spec.v7.snapshot} is not V7's ${V.snapshot}`);
    if (spec.v7.grade && V7_GRADES.indexOf(String(spec.v7.grade).toLowerCase()) < 0) f.push(`v7: grade "${spec.v7.grade}" is not one of V7's grade words`);
    (spec.v7.ids || []).forEach(id => { if (!V.ids.has(id)) f.push(`v7: ID ${id} is not in Atlas V7`); });
    if (spec.v7.grade && WEAK.indexOf(String(spec.v7.grade).toLowerCase()) >= 0 && CAUSAL.test(spec.title || '')) f.push(`v7: the title uses a causal verb a ${spec.v7.grade} grade does not allow (H08, Rule 13.2)`);
  }
  if (spec.evidence === 'association' && CAUSAL.test(spec.title || '')) f.push('words: an association titled with a causal verb (H08, Rule 13.2)');
  const listed = new Set((spec.v7 && spec.v7.ids) || []);
  const prose = ['title', 'reading_guide', 'measure_line', 'alt'].map(k => [k, spec[k]]).concat((spec.notes || []).map((n, i) => ['notes[' + i + ']', n]));
  for (const [where, s] of prose) {
    if (typeof s !== 'string') continue;
    const re = /(^|[^A-Za-z0-9-])([A-Z]{1,3}-?\d{1,4}[a-z]?)(?![A-Za-z0-9])/g;
    let m;
    while ((m = re.exec(s))) {
      const id = m[2];
      if (!V.ids.has(id)) continue;
      if (!listed.has(id)) f.push(`v7: ${id} in ${where} is an atlas ID not listed in v7.ids, so it would print bare (H11)`);
      const type = V.ids.get(id);
      void type;   // the kit's chip adds the type word where the words before the ID lack it (E7, H11)
    }
  }
  // the table equivalent's rows against the data rows
  if (rows && spec.table) {
    const t = K.table_rows(spec, sel);
    const cells = t.pivot ? Object.keys(t.cell).length : t.rows.length;
    if (cells !== sel.length) f.push(`table: ${cells} table rows or cells for ${sel.length} data rows`);
  }
  return { faults: f, rows: sel, datasets };
}

// ---------------------------------------------------------------------------------------------------------------
// The drawing: the layout guard's results, the chart check and the key's lightness
// ---------------------------------------------------------------------------------------------------------------
function hex_to_lab_l(hex) {
  const m = /^#?([0-9a-f]{6})$/i.exec(String(hex).trim());
  if (!m) return null;
  const n = parseInt(m[1], 16);
  const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const y = 0.2126 * lin(n >> 16 & 255) + 0.7152 * lin(n >> 8 & 255) + 0.0722 * lin(n & 255);
  return y > 0.008856 ? 116 * Math.cbrt(y) - 16 : 903.3 * y;
}
function role_color(role, tok) {
  // the hex a color role resolves to on a ground, from tokens.css's surface block (the same map kit.css reads)
  const names = {
    subject: 'chart-color-subject', context: 'chart-color-context', secondary: 'chart-color-secondary', label: 'chart-color-label',
    baseline: 'chart-color-baseline', gridline: 'chart-color-gridline', point: 'chart-color-point', band: 'chart-color-band', track: 'chart-color-track',
    'light-fill': 'chart-color-light-fill', land: 'chart-color-land', party: 'chart-color-party-mark', leader: 'chart-color-leader',
    'cat-1': 'chart-color-categorical-fill-group1', 'cat-2': 'chart-color-categorical-fill-group2',
    'cat-3': 'chart-color-categorical-fill-group3', 'cat-4': 'chart-color-categorical-fill-group4', ghost: 'chart-color-ghost',
    'on-cat-1': 'chart-color-categorical-label-group1', 'on-cat-2': 'chart-color-categorical-label-group2',
    'on-cat-3': 'chart-color-categorical-label-group3', 'beside-cat-4': 'chart-color-categorical-label-beside-group4',
  };
  for (let i = 1; i <= 5; i++) { names['seq-' + i] = 'chart-color-sequential-fill-step' + i; names['div-' + i] = 'chart-color-diverging-fill-step' + i; }
  for (let i = 1; i <= 4; i++) names['mag-' + i] = 'chart-color-magnitude-fill-step' + i;
  const n = names[role];
  if (!n) return null;
  for (const x of [].concat(n)) { const v = tok['--oa-' + x]; if (v && /^#[0-9a-f]{6}$/i.test(v.trim())) return v.trim().toUpperCase(); }
  return null;
}

function check_drawing(spec, d, tok, where) {
  const f = [];
  const at = where ? ` (${where})` : '';
  d.guard.forEach(g => f.push('layout guard: ' + g + at));
  d.warnings.forEach(w => f.push('form: ' + w + at));
  const W = d.width, H = d.height;
  for (const m of d.marks) {
    const key = (m.data && (m.data.key || m.data['key'])) || m.kind;
    if (m.x < -1 || m.y < -1 || m.x + m.w > W + 1 || m.y + m.h > H + 1) f.push(`chart: mark ${key} outside its drawing${at}`);
    if (m.kind === 'bar' && m.zero !== undefined) {
      const ok = m.axis === 'x' ? (Math.abs(m.x - m.zero) < 0.6 || Math.abs(m.x + m.w - m.zero) < 0.6)
        : (Math.abs(m.y - m.zero) < 0.6 || Math.abs(m.y + m.h - m.zero) < 0.6);
      if (!ok) f.push(`chart: bar ${key} does not start on its zero line${at}`);
    }
    if (m.kind === 'bar' && m.zero === undefined) f.push(`chart: bar ${key} names no zero line${at}`);
    if (m.area_of) {
      const want = m.area_of.value > 0 ? Math.sqrt(m.area_of.value / m.area_of.max_value) * m.area_of.max_radius : 0;
      if (Math.abs(want - m.r) > 0.5) f.push(`chart: circle ${key} is not sized by area (radius ${m.r.toFixed(2)}, area rule gives ${want.toFixed(2)})${at}`);
    }
  }
  // group 4's label sits beside its hatch or on a halo of the ground, never on the fill (labelBeside, D3-84 fix pass)
  for (const m of d.marks.filter(x => x.fill === 'cat-4')) {
    for (const t of d.texts || []) {
      if (t.halo) continue;
      const cx = t.x + t.w / 2, cy = t.y + t.h / 2;
      if (cx > m.x && cx < m.x + m.w && cy > m.y && cy < m.y + m.h) f.push(`chart: "${String(t.words).slice(0, 30)}" is set on group 4's hatch; set it beside the hatch or on a halo${at}`);
    }
  }
  const color = m => role_color(m.fill || m.stroke, tok);
  const party = d.marks.filter(m => m.data && m.data.party);
  for (const m of party) {
    const c = color(m);
    if (c === RED || c === PRUSSIAN) f.push(`chart: a party mark in ${c === RED ? 'Pillar Red' : 'Prussian'} (DR-48)${at}`);
  }
  const reds = d.marks.filter(m => color(m) === RED);
  if (reds.length > 1) f.push(`chart: ${reds.length} working reds in one view (Rule 05.3)${at}`);
  for (const r of reds) {
    for (const m of d.marks) {
      if (m === r || color(m) !== PRUSSIAN) continue;
      if (r.x <= m.x + m.w + 1 && m.x <= r.x + r.w + 1 && r.y <= m.y + m.h + 1 && m.y <= r.y + r.h + 1) f.push(`chart: red touches Prussian${at}`);
    }
  }
  for (const key of d.keys || []) {
    const plain = key.filter(e => !e.pattern && !e.direct);
    for (let i = 0; i < plain.length; i++) for (let j = i + 1; j < plain.length; j++) {
      const a = hex_to_lab_l(role_color(plain[i].fill, tok)), b = hex_to_lab_l(role_color(plain[j].fill, tok));
      if (a === null || b === null) { f.push(`key: ${plain[i].fill} or ${plain[j].fill} has no resolved color${at}`); continue; }
      if (Math.abs(a - b) < KEY_LIGHTNESS_MARGIN) f.push(`key: ${plain[i].fill} and ${plain[j].fill} differ by ${Math.abs(a - b).toFixed(1)} in lightness, under ${KEY_LIGHTNESS_MARGIN}, with no pattern or direct label${at}`);
    }
  }
  if (spec.failure && spec.failure.exempt) {
    const ex = spec.failure.exempt;
    return f.filter(x => !ex.some(e => x.indexOf(e) >= 0));
  }
  return f;
}

function check_csv(K, csv_text, rows, ds_meta) {
  // the CSV export against the rows the chart draws: same count, same columns, same values
  const back = K.type_rows(K.parse_csv(csv_text), ds_meta.columns);
  const f = [];
  if (back.length !== rows.length) f.push(`csv: ${back.length} rows exported for ${rows.length} drawn`);
  const cols = Object.keys(ds_meta.columns);
  for (let i = 0; i < Math.min(back.length, rows.length); i++) {
    for (const c of cols) {
      const a = back[i][c], b = rows[i][c];
      if (!(a === b || (a === null && (b === null || b === undefined)) || (typeof a === 'number' && Math.abs(a - b) < 1e-9))) { f.push(`csv: row ${i + 1} column ${c} reads ${a} for ${b}`); break; }
    }
  }
  return f;
}

function to_csv(rows, columns) {
  const q = v => { if (v === null || v === undefined) return ''; const s = String(v); return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  return [columns.join(',')].concat(rows.map(r => columns.map(c => q(r[c])).join(','))).join('\n') + '\n';
}

function id_types() {
  // the type word each chip carries (H11): Variable, Connection, Loop, Reform, Issue
  const out = {};
  for (const [k, t] of v7().ids) if (['Variable', 'Connection', 'Loop', 'Reform', 'Issue'].indexOf(t) >= 0) out[k] = t;
  return out;
}

module.exports = { id_types, check_spec, check_drawing, check_csv, to_csv, load_dataset, rows_of, v7, role_color, hex_to_lab_l, strings,
  FAMILIES, TIERS, EVIDENCE, DISCLOSURE, KEY_LIGHTNESS_MARGIN, ROOT, DATA };
