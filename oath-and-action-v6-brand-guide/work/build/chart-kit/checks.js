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
const KEY_LIGHTNESS_MARGIN = 10;   // the smaller of CIE L* and luma x 100 between any two key entries told apart by fill alone
const KEY_ORDERED_MARGIN = 8;     // neighbors on an ordered scale, and its lightest step against the ground (access S5; OKLab 0.08)

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
  // round 3 (the data lead's C-3): the atlas's claims (CL...), so a claim printed in words takes its typed chip
  Object.keys(d.claims || {}).forEach(k => add(k, 'Claim'));
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
// AX-S6 (round 3 fix pass): the dates a source line's "Retrieved ..." clause names, as YYYY-MM-DD, or null where it has
// none: "Retrieved November 12 and 13, 2026" gives 2026-11-12 and 2026-11-13; "Retrieved October 30 and November 13,
// 2026" gives both; a year closes every date before it
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
function retrieved_dates(line) {
  const m = /\bRetrieved\s+(.*?)(?:\.(?:\s|$)|$)/.exec(String(line || '').replace(/\u00a0/g, ' '));
  if (!m) return null;
  const out = [], open = [];
  let mon = null;
  for (const tok of m[1].split(/[\s,]+/)) {
    const mi = MONTHS.indexOf(tok);
    if (mi >= 0) { mon = mi + 1; continue; }
    if (/^\d{4}$/.test(tok)) { open.splice(0).forEach(([mo, dd]) => out.push(`${tok}-${String(mo).padStart(2, '0')}-${String(dd).padStart(2, '0')}`)); continue; }
    if (/^\d{1,2}$/.test(tok) && mon) open.push([mon, +tok]);
  }
  return out;
}
function long_date(iso) { const [y, mo, d] = String(iso).split('-').map(Number); return `${MONTHS[mo - 1]} ${d}, ${y}`; }

function load_dataset(name, dir) {
  // AX-S6 (round 3 fix pass): a data folder of one's own (oa-chart.mjs --data DIR) is read first, then work/build/data/,
  // so a designer's derived file sits beside the frozen files it was derived from without writing into work/build/data/
  if (dir && path.resolve(dir) !== path.resolve(DATA) && !fs.existsSync(path.join(dir, name + '.meta.json'))) dir = DATA;
  dir = dir || DATA;
  const mp = path.join(dir, name + '.meta.json');
  if (!fs.existsSync(mp)) return { fault: `dataset ${name}: no sidecar ${path.relative(ROOT, mp)}` };
  const meta = JSON.parse(fs.readFileSync(mp, 'utf8'));
  const fp = path.join(dir, meta.file || '');
  if (!fs.existsSync(fp)) return { fault: `dataset ${name}: no data file ${meta.file}` };
  // R3-2 (round 3): a boundary file (R1-C7) is read by geo.js, never into a chart's rows or island; the spec names it so
  // the source line credits it and the check can find the layer drawn from it
  if (fp.endsWith('.geojson')) return { meta, text: '', file: meta.file, geo: true };
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
// access S1 (round 1 fix pass): the years a chart draws, read from the time columns it draws (its encode and its table's
// pivot), and the years a source line names as its period, leaving out when it was retrieved, released or revised
function drawn_years(spec, cols, rows) {
  const enc = [];
  Object.values(spec.encode || {}).forEach(v => [].concat(v).forEach(x => { if (typeof x === 'string') enc.push(x); }));
  if (spec.table && spec.table.pivot) enc.push(spec.table.pivot.column, spec.table.pivot.row);
  const tcols = [...new Set(enc)].filter(k => cols[k] && ['year', 'month', 'date'].indexOf(cols[k].type) >= 0);
  const ys = new Set();
  for (const r of rows) for (const k of tcols) { const m = /^(\d{4})/.exec(String(r[k] === null || r[k] === undefined ? '' : r[k])); if (m) ys.add(+m[1]); }
  return ys.size ? { from: Math.min(...ys), to: Math.max(...ys), cols: tcols } : null;
}
function line_years(line) {
  const s = String(line || '')
    .replace(/\b[Rr]etrieved (?:on )?(?:[A-Z][a-z]+ \d{1,2}, )?\d{4}/g, ' ')
    .replace(/\b(?:[A-Z][a-z]+ (?:\d{1,2}, )?)?\d{4},? (?:release|revision|vintage|edition|snapshot)\b/g, ' ')
    .replace(/\b(?:[Rr]elease|[Vv]intage|[Ss]napshot|[Ee]dition|[Rr]evision|[Rr]evised|[Uu]pdated|[Pp]ublished|[Ii]ssued)(?: of| on| dated)? (?:[A-Z][a-z]+ )?(?:\d{1,2}, )?\d{4}/g, ' ')
    .replace(/\bas of (?:[A-Z][a-z]+ )?(?:\d{1,2}, )?\d{4}/g, ' ');
  return [...s.matchAll(/(?<![\d$.,-])(?:1[89]|20)\d{2}(?![\d-])/g)].map(m => +m[0]);
}
function fill_template(t, span) { return String(t).replace(/\{from\}/g, String(span.from)).replace(/\{to\}/g, String(span.to)); }

function check_spec(K, spec, opts) {
  opts = opts || {};
  const f = [];
  const datasets = [];
  const own_line = !!spec.source_line;
  // a chart of one dataset may leave source_line out and print its sidecar's line (D3-102)
  const single = typeof spec.dataset === 'string';
  for (const k of REQUIRED) if ((spec[k] === undefined || spec[k] === null || spec[k] === '') && !(k === 'source_line' && single)) f.push(`spec: "${k}" is missing; contract C2 in work/build/chart-kit/README.md lists every key`);
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
  // D3-519: typography is {curl_quotes: true|false, replace: [[find, put], ...]}; a replacement whose words hold what it finds
  // would change them again on a page that reads its rows back from the table
  if (spec.typography !== undefined) {
    const ty = spec.typography;
    if (!ty || typeof ty !== 'object' || Array.isArray(ty)) f.push('spec: typography is {"curl_quotes": true, "replace": [["find", "put"]]}');
    else {
      if (ty.curl_quotes !== undefined && typeof ty.curl_quotes !== 'boolean') f.push('spec: typography.curl_quotes is true or false');
      if (ty.nbsp !== undefined && typeof ty.nbsp !== 'boolean') f.push('spec: typography.nbsp is true or false');
      (ty.replace || []).forEach((pr, i) => {
        if (!Array.isArray(pr) || pr.length !== 2 || typeof pr[0] !== 'string' || typeof pr[1] !== 'string' || !pr[0]) f.push(`spec: typography.replace[${i}] is a pair of words, ["find", "put"]`);
        else if (pr[1].indexOf(pr[0]) >= 0) f.push(`spec: typography.replace[${i}] puts words that hold what it finds ("${pr[0]}"), so a second pass would change them again`);
      });
    }
  }
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
    if (ds.geo) {
      // a boundary file: geo.js carries a layer drawn from it (tools/geo_build.py), and the chart's own data comes first
      const G = globalThis.OAChartGeo, lay = G && G.layers ? Object.keys(G.layers).filter(k => G.layers[k].file === n) : [];
      if (i === 0) f.push(`dataset ${n}: a boundary file draws a map's shapes; name the chart's data file first`);
      if (!lay.length) f.push(`dataset ${n}: no layer in geo.js is drawn from it; ask the engineer for one (tools/geo_build.py)`);
      datasets.push(ds);
      return;
    }
    datasets.push(ds);
    if (i === 0) { first = ds; rows = rows_of(K, ds); }
    if (i === 0 && single && !spec.source_line) spec.source_line = ds.meta.printed_source_line;
    if (DISCLOSURE.test(JSON.stringify(ds.meta)) || ds.meta.required_text) f.push(`dataset ${n}: its sidecar carries the retired disclosure (DR-100)`);
    if (ds.meta.kind === 'illustrative' && !spec.illustrative) f.push(`dataset ${n} is invented; the spec prints the Illustrative label`);
  });
  let sel = rows ? K.select(spec, rows) : [];
  if (rows && !sel.length) f.push('data: no rows left after "where"');
  if (first && spec.where) for (const k of Object.keys(spec.where)) if (!(k in (first.meta.columns || {}))) f.push(`where: column ${k} is not in the data; its columns are ${Object.keys(first.meta.columns || {}).join(', ')}`);
  // a ranked bar of parts that keeps the total among them (production test S6)
  if (spec.form === 'ranked-bar' && spec.encode && sel.some(r => /^(total|all)\b/i.test(String(r[spec.encode.category])))) f.push(`data: a bar reads "${sel.find(r => /^(total|all)\b/i.test(String(r[spec.encode.category])))[spec.encode.category]}"; a chart of the parts leaves the total out with where: {"${spec.encode.category}": {"not": [...]}}`);
  if (first) {
    const cols = first.meta.columns || {};
    const fields = [];
    const enc = spec.encode || {};
    Object.keys(enc).forEach(k => { const v = enc[k]; (Array.isArray(v) ? v : [v]).forEach(x => { if (typeof x === 'string' && k !== 'of') fields.push([k, x]); }); });
    for (const [k, x] of fields) if (!(x in cols)) f.push(`encode.${k}: column "${x}" is not in ${first.file || 'the data'}; its columns are ${Object.keys(cols).join(', ')}`);
    const tb = spec.table || {};
    (tb.columns || []).forEach(c => { if (!(c.field in cols)) f.push(`table: column "${c.field}" is not in the data`); });
    if (tb.pivot) ['row', 'column', 'value'].forEach(k => { if (!(tb.pivot[k] in cols)) f.push(`table.pivot.${k}: "${tb.pivot[k]}" is not in the data`); });
    // R3-3: a grouped table's columns and the columns it groups by are in the data
    if (tb.group) {
      [].concat(tb.group.by).forEach(b => { if (!(b in cols)) f.push(`table.group.by: "${b}" is not in the data`); });
      (tb.group.columns || []).forEach(c => { if (c.field !== undefined && !(c.field in cols)) f.push(`table.group: column "${c.field}" is not in the data`); });
      if (!(tb.group.columns || []).length) f.push('table.group: no columns; the page prints a row a group');
    }
    if (!tb.columns || !tb.columns.length) f.push('table: no columns; every chart carries its table equivalent');
    // the source line against the sidecar (H04)
    if (datasets.length === 1) {
      const m = datasets[0].meta;
      // access S1: a sidecar's templates ({from} and {to}) fit the line to the years this chart draws; a spec names one
      // with source_line_template and leaves source_line out, or writes the filled line itself
      const span = drawn_years(spec, cols, sel);
      const tpl = m.source_line_templates || {};
      if (spec.source_line_template !== undefined) {
        if (!tpl[spec.source_line_template]) f.push(`source: source_line_template "${spec.source_line_template}" is not one of ${datasets[0].file}'s source_line_templates (${Object.keys(tpl).join(', ') || 'none'})`);
        else if (!span) f.push('source: source_line_template needs a year, month or date column the chart draws, to fill {from} and {to}');
        else if (!own_line) spec.source_line = fill_template(tpl[spec.source_line_template], span);
      }
      const ok = [m.printed_source_line].concat(Object.values(m.source_line_variants || {}), span ? Object.values(tpl).map(t => fill_template(t, span)) : []);
      if (ok.indexOf(spec.source_line) < 0) f.push(`source: the source line differs from ${datasets[0].file}'s printed_source_line and its variants${Object.keys(tpl).length ? ' and templates' : ''}. Leave source_line out to print the sidecar's line, copy one of its variants, name a template with source_line_template, or ask the research lead to add a variant to work/build/data/${datasets[0].file.replace(/\.(csv|json)$/, '')}.meta.json`);
      // access S1: the period the line names holds every year the chart draws (a line for fiscal 2026 under a chart of
      // 2016 and 2026 fails); a line that names no year is not read
      const ly = line_years(spec.source_line);
      if (span && ly.length && (span.from < Math.min(...ly) || span.to > Math.max(...ly))) {
        f.push(`source: the source line names ${Math.min(...ly) === Math.max(...ly) ? Math.min(...ly) : Math.min(...ly) + ' to ' + Math.max(...ly)}, but the chart draws ${span.from === span.to ? span.from : span.from + ' to ' + span.to} (${span.cols.join(', ')}); print a line for the years drawn${Object.keys(tpl).length ? ', such as one of the sidecar\'s source_line_templates' : ': ask the research lead for a variant or a template'}`);
      }
    } else if (datasets.length > 1) {
      // each dataset's publisher appears: any one of its "; " parts, whole or after its last comma, with "United States" read as "U.S."
      const norm = x => String(x).replace(/United States/g, 'U.S.').trim();
      const line = norm(spec.source_line);
      datasets.forEach(d => {
        const parts = String(d.meta.publisher).split(';').map(norm);
        const ok = parts.every(p => line.indexOf(p) >= 0 || line.indexOf(p.split(',').slice(-1)[0].trim()) >= 0);
        if (!ok) f.push(`source: the source line does not name ${d.meta.publisher}`);
      });
      // AX-S6 (round 3 fix pass): a line written for two or more datasets that says when they were retrieved names each
      // one's date, as its sidecar's date_retrieved gives it ("Retrieved November 12 and 13, 2026"); an atlas dataset prints
      // its snapshot instead, and a line with no "Retrieved" (an atlas chart's) is not read
      const got = retrieved_dates(spec.source_line);
      if (got !== null) datasets.forEach(d => {
        const want = d.meta.date_retrieved;
        if (d.meta.kind === 'v7' || /^v7-/.test(d.file || '') || !/^\d{4}-\d{2}-\d{2}$/.test(String(want || ''))) return;
        if (got.indexOf(want) < 0) f.push(`source: the source line's retrieval dates (${got.map(long_date).join(', ') || 'none read'}) leave out ${d.file}'s ${long_date(want)} (its sidecar's date_retrieved)`);
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
  // R2-2 (contract R2-C4): a derived table names what it was derived from and how, and the line a chart prints names the
  // publisher of each public or secondary file it was derived from
  datasets.forEach(ds => {
    const m = ds.meta;
    if (m.kind !== 'derived') return;
    const from = Array.isArray(m.derived_from) ? m.derived_from : (m.derived_from ? [m.derived_from] : []);
    if (!from.length || !m.derivation) { f.push(`dataset ${ds.file}: a derived table's sidecar names derived_from and derivation (C1, R2-2)`); return; }
    const norm = x => String(x).replace(/United States/g, 'U.S.').trim();
    from.forEach(fn => {
      // round 3 (the research lead's request): a boundary file may be a source too, named with its .geojson extension
      const src = load_dataset(String(fn).replace(/\.(csv|json|geojson)$/, ''), opts.data_dir);
      if (src.fault) { f.push(`dataset ${ds.file}: derived_from names ${fn}, which is not in the data folder`); return; }
      if (['public', 'secondary'].indexOf(src.meta.kind) < 0 || !spec.source_line) return;
      const line = norm(spec.source_line);
      // each "; " part of the publisher, whole, or its first comma part with or without a parenthesis, or its last
      const ok = String(src.meta.publisher || '').split(';').map(norm).every(p => {
        const first = p.split(',')[0].trim();
        return [p, first, first.replace(/\s*\([^)]*\)\s*/g, ' ').trim(), p.split(',').slice(-1)[0].trim()].some(x => x && line.indexOf(x) >= 0);
      });
      if (!ok) f.push(`source: the source line does not name ${src.meta.publisher}, whose ${fn} the table ${ds.file} was derived from (R2-2)`);
    });
  });
  // R2-4 (contract R2-C1): a form that draws an estimate with its interval
  const idef = spec.form && K.forms[spec.form];
  if (idef && idef.interval && sel.length) {
    const enc = spec.encode || {}, tb = spec.table || {};
    // ED-E17 (round 2): a no-break space (or a narrow one) may hold the level's words together, "90 percent" at a line end
    const ml = String(spec.measure_line || '').replace(/[\u00a0\u202f]/g, ' ');
    if (!(/\b\d{2}(?:\.\d+)? percent\b/.test(ml) && /margin of error|confidence|interval|probability/i.test(ml))) f.push('interval: the measure line names the interval\'s level, such as "90 percent margin of error" (R2-4)');
    if (idef.interval === true) {
      const lh = enc.low !== undefined || enc.high !== undefined, mg = enc.margin !== undefined;
      if ((enc.low === undefined) !== (enc.high === undefined) || lh === mg) f.push('interval: encode gives "low" and "high" together, or "margin" alone (contract R2-C1)');
      else if (K.parts && K.parts.interval_of) {
        const iv = K.parts.interval_of({ encode: enc }), kf = enc.category || enc.x || enc.key;
        let bad = 0, first = null;
        sel.forEach(r => {
          const x = iv(r);
          if (!(isFinite(x.v) && isFinite(x.lo) && isFinite(x.hi) && x.lo <= x.v + 1e-9 && x.v <= x.hi + 1e-9)) { bad++; if (!first) first = `${kf ? r[kf] : '?'}: ${x.lo} to ${x.hi} around ${x.v}`; }
        });
        if (bad) f.push(`interval: ${bad} row(s) whose interval does not hold its estimate, or lacks an end (${first})`);
      }
      const tf = new Set((tb.columns || []).map(c => c.field).concat(tb.pivot ? [tb.pivot.value] : []));
      // AX S8: the message names the fields the spec gives; a missing one is named by the encode fault above
      if (mg || (enc.low !== undefined && enc.high !== undefined)) {
        if (!(mg ? tf.has(enc.margin) : (tf.has(enc.low) && tf.has(enc.high)))) f.push(`interval: the table equivalent prints the interval: ${mg ? `the margin column "${enc.margin}"` : `both "${enc.low}" and "${enc.high}"`} (contract R2-C1)`);
      }
      // AX S8 (D3-905): a margin is in its value's unit (percentage points for a percent), and the margin a sidecar names
      // for the value (margin_columns) is the one a chart prints
      const cols = (first && first.meta.columns) || {}, vf = enc.value !== undefined ? enc.value : enc.y;
      const unit = c => cols[c] && cols[c].unit ? String(cols[c].unit) : null;
      const same_unit = (v, m) => v === m || (/^percent$/i.test(v) && /^percentage points$/i.test(m));
      [['margin', enc.margin], ['low', enc.low], ['high', enc.high]].forEach(([k, c]) => {
        if (c === undefined || !unit(c) || !unit(vf)) return;
        const ok = k === 'margin' ? same_unit(unit(vf), unit(c)) : unit(vf) === unit(c);
        if (!ok) f.push(`interval: the ${k} "${c}" is in ${unit(c)} and the value "${vf}" in ${unit(vf)}; ${k === 'margin' ? 'a margin is in its value\'s unit (percentage points for a percent)' : 'an interval\'s ends are in its value\'s unit'}${first.meta.margin_columns && first.meta.margin_columns[vf] ? `: the sidecar's margin for "${vf}" is "${first.meta.margin_columns[vf]}"` : ''} (AX S8)`);
      });
      const mc = first && first.meta.margin_columns;
      if (mg && mc && mc[vf] && mc[vf] !== enc.margin) f.push(`interval: the margin "${enc.margin}" is not the one the sidecar names for "${vf}"; print "${mc[vf]}" (margin_columns, AX S8)`);
    }
  }
  // AX S8 (D3-905): a sidecar's check_only_columns print nowhere, and its source_line_columns name the columns each source
  // line covers, so a chart prints a line for the measure it draws
  if (first && first.meta) {
    const m = first.meta, enc = spec.encode || {}, tb = spec.table || {}, cols = m.columns || {};
    const printed = [];
    Object.keys(enc).forEach(k => { if (k !== 'of') [].concat(enc[k]).forEach(x => { if (typeof x === 'string') printed.push(x); }); });
    (tb.columns || []).forEach(c => printed.push(c.field));
    if (tb.pivot) printed.push(tb.pivot.value);
    const co = new Set(m.check_only_columns || []);
    [...new Set(printed)].filter(c => co.has(c)).forEach(c => {
      const alt = Object.keys(m.margin_columns || {}).find(v => printed.indexOf(v) >= 0);
      f.push(`data: "${c}" is in its sidecar's check_only_columns and prints nowhere${alt ? `; print "${m.margin_columns[alt]}", the margin the sidecar names for "${alt}"` : ''} (AX S8)`);
    });
    const slc = m.source_line_columns;
    if (slc && spec.source_line) {
      const key = spec.source_line === m.printed_source_line ? 'printed_source_line' : Object.keys(m.source_line_variants || {}).find(k => m.source_line_variants[k] === spec.source_line);
      const num = c => cols[c] && ['number', 'integer'].indexOf(cols[c].type) >= 0;
      const drawn = [...new Set(printed)].filter(num);
      if (key && slc[key]) {
        const out = drawn.filter(c => slc[key].indexOf(c) < 0);
        if (out.length) {
          const fit = Object.keys(slc).filter(k => drawn.every(c => slc[k].indexOf(c) >= 0)).map(k => k === 'printed_source_line' ? 'its printed_source_line' : `its source_line_variants "${k}"`);
          f.push(`source: the source line printed (${key === 'printed_source_line' ? 'the sidecar\'s printed_source_line' : `variant "${key}"`}) covers ${slc[key].join(', ')}, and the chart prints ${out.join(', ')}; print ${fit.length ? fit.join(' or ') : 'a line for the measure drawn (ask the research lead for a variant)'} (AX S8)`);
        }
      }
    }
  }
  // the table equivalent's rows against the data rows
  if (rows && spec.table) {
    const t = K.table_rows(spec, sel);
    const cells = t.pivot ? Object.keys(t.cell).length : t.rows.length;
    if (cells !== sel.length) f.push(`table: ${cells} table rows or cells for ${sel.length} data rows`);
  }
  // AX-M1 (round 3 fix pass): a printed column that is empty in every row fails, so a blank column (S73's "From" under
  // the old 'first') cannot pass again. AX-M2 (warning only, the data lead's ruling): a column with words that prints a
  // stored value its words do not map; words_pass: true on the column where printing the stored value is meant (S82's
  // district numbers)
  const warnings = [];
  if (rows && spec.table && sel.length && !spec.table.pivot) {
    const tb = spec.table;
    const unmapped = (col, vals) => {
      if (!col.words || col.words_pass) return;
      const out = [...new Set(vals.filter(v => v !== null && v !== undefined && v !== '' && col.words[String(v)] === undefined).map(String))];
      if (out.length) warnings.push(`table: the column "${col.label}" has words and prints ${out.length} stored value${out.length > 1 ? 's' : ''} they do not map (${out.slice(0, 6).map(v => `"${v}"`).join(', ')}${out.length > 6 ? ', ...' : ''}); give each its words, or set "words_pass": true on the column where the stored value is meant to print (AX-M2)`);
    };
    if (tb.group) {
      const groups = K.table_groups(spec, sel);
      (tb.group.columns || []).forEach(col => {
        const a = col.agg || 'key';
        if (groups.every(g => String(K.group_cell(col, g)).trim() === '')) f.push(`table: the column "${col.label}" prints nothing in any of its ${groups.length} rows (${a}${col.field ? ` of "${col.field}"` : ''}); a printed column names something in at least one row (AX-M1)`);
        if (a === 'first') unmapped(col, groups.map(g => g.rows[0][col.field]));
        else if (a === 'key' && !col.state_name) unmapped(col, groups.map(g => g.key));
      });
    } else {
      const t = K.table_rows(spec, sel);
      (tb.columns || []).forEach(col => {
        if (t.rows.every(r => String(K.cell_text(col, r, spec)).replace(/<[^>]*>/g, '').trim() === '')) f.push(`table: the column "${col.label}" prints nothing in any of its ${t.rows.length} rows; a printed column names something in at least one row (AX-M1)`);
        unmapped(col, t.rows.map(r => r[col.field]));
      });
    }
  }
  return { faults: f, warnings, rows: sel, datasets };
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
function luma(hex) {
  // Chromium's grayscale(1): Rec. 709 weights on the encoded values, as the board's grayscale proofs and most office printers
  const m = /^#?([0-9a-f]{6})$/i.exec(String(hex).trim());
  if (!m) return null;
  const n = parseInt(m[1], 16);
  return (0.2126 * (n >> 16 & 255) + 0.7152 * (n >> 8 & 255) + 0.0722 * (n & 255)) / 255;
}
function role_color(role, tok) {
  // the hex a color role resolves to on a ground, from tokens.css's surface block (the same map kit.css reads)
  const names = {
    subject: 'chart-color-subject', context: 'chart-color-context', secondary: 'chart-color-secondary', label: 'chart-color-label',
    surface: 'color-surface', baseline: 'chart-color-baseline', gridline: 'chart-color-gridline', point: 'chart-color-point', band: 'chart-color-band', track: 'chart-color-track',
    'light-fill': 'chart-color-light-fill', land: 'chart-color-land', party: 'chart-color-party-mark', leader: 'chart-color-leader',
    'cat-1': 'chart-color-categorical-fill-group1', 'cat-2': 'chart-color-categorical-fill-group2',
    'cat-3': 'chart-color-categorical-fill-group3', 'cat-4': 'chart-color-categorical-fill-group4', ghost: 'chart-color-ghost',
    'on-cat-1': 'chart-color-categorical-label-group1', 'on-cat-2': 'chart-color-categorical-label-group2',
    'on-cat-3': 'chart-color-categorical-label-group3', 'beside-cat-4': 'chart-color-categorical-label-beside-group4',
  };
  for (let i = 1; i <= 5; i++) { names['seq-' + i] = 'chart-color-sequential-fill-step' + i; names['div-' + i] = 'chart-color-diverging-fill-step' + i; }
  for (let i = 1; i <= 4; i++) names['mag-' + i] = 'chart-color-magnitude-fill-step' + i;
  // round 3: each step's label ink
  for (let i = 1; i <= 5; i++) { names['on-seq-' + i] = 'chart-color-sequential-label-step' + i; names['on-div-' + i] = 'chart-color-diverging-label-step' + i; }
  for (let i = 1; i <= 4; i++) names['on-mag-' + i] = 'chart-color-magnitude-label-step' + i;
  const n = names[role];
  if (!n) return null;
  for (const x of [].concat(n)) { const v = tok['--oa-' + x]; if (v && /^#[0-9a-f]{6}$/i.test(v.trim())) return v.trim().toUpperCase(); }
  return null;
}

// WCAG's contrast ratio between two hexes
function contrast(a, b) {
  const lum = hex => {
    const m = /^#?([0-9a-f]{6})$/i.exec(String(hex || '').trim());
    if (!m) return null;
    const n = parseInt(m[1], 16), lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * lin(n >> 16 & 255) + 0.7152 * lin(n >> 8 & 255) + 0.0722 * lin(n & 255);
  };
  const x = lum(a), y = lum(b);
  if (x === null || y === null) return null;
  return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
}
const median = xs => { const v = xs.filter(x => isFinite(x)).sort((a, b) => a - b); return v.length ? (v.length % 2 ? v[(v.length - 1) / 2] : (v[v.length / 2 - 1] + v[v.length / 2]) / 2) : null; };
// D3-903 (AX M1, CD B-M1, BC S6): a band drawn through K.parts.band carries the form's meaning (an interval, a fan's
// step), so its fill, or its edge, meets 3 to 1 against what lies under it: the ground, or a wider band drawn before it
// that holds it (WCAG 1.4.11). A band under that with no edge fails; K.parts.band's edge: 'context' draws one.
function band_faults(d, tok, at) {
  const f = [], ground = tok['--oa-color-surface'] || tok['--oa-chart-color-surface'];
  (d.bands || []).forEach((b, i) => {
    if (!b.fill) return;   // a hatched band shows by its lines
    // RB3-G1 (round 3): a band lies under another only where the other holds it across as well as down (side by side links
    // and a Sankey's left and right bands lie on the ground)
    const across = o => o.left === undefined || b.left === undefined || (o.left <= b.left + 0.5 && o.right >= b.right - 0.5);
    const outer = (d.bands || []).slice(0, i).reverse().find(o => o.fill && o.top <= b.top + 0.5 && o.bottom >= b.bottom - 0.5 && across(o));
    const under = outer ? role_color(outer.fill, tok) : String(ground || '').trim().toUpperCase(), uname = outer ? `the ${outer.fill} band under it` : 'the ground';
    const fc = contrast(role_color(b.fill, tok), under), ec = b.edge ? contrast(role_color(b.edge, tok), under) : null;
    if (fc === null) { f.push(`band: its fill ${b.fill} has no resolved color${at}`); return; }
    if (fc >= 3 || (ec !== null && ec >= 3)) return;
    f.push(`band: a band in ${b.fill} measures ${fc.toFixed(2)} to 1 against ${uname}${b.edge ? `, and its ${b.edge} edge ${ec === null ? 'has no resolved color' : ec.toFixed(2) + ' to 1'}` : ' and has no edge'}, under 3 to 1; draw its edges in the context ink, K.parts.band(c, pts, {edge: 'context'}) (WCAG 1.4.11, D3-903)${at}`);
  });
  return f;
}
// D3-899 (call 9, V20 section 3; AX M1): an interval form's plot is wide enough for its marks. Each row's interval is read
// from what the drawing records, its low and high ends (K.parts.whisker and K.parts.band record them), and its estimate's
// mark (a dot's diameter; a line's width for a band, 2 px). The middle row's interval, in pixels, must run 5 px past a dot
// on each side (23 px for a 13 px dot) and 2 px past a line (6 px for a 2 px line); under that, most intervals hide behind
// their marks at this width (Rule 14.9's plate at 294 px with its rows side by side: 19.7 px against a 13 px dot), and the
// drawing fails.
function interval_faults(spec, d, def, at) {
  if (!def || !def.interval) return [];
  const enc = spec.encode || {}, vf = enc.value !== undefined ? enc.value : enc.y;
  const fl = enc.low, fh = enc.high;
  const by = new Map();
  for (const m of d.marks) {
    const k = m.data && m.data.key, fd = m.data && m.data.field;
    if (k === undefined || k === null) continue;
    const e = by.get(String(k)) || {};
    const cx = m.x + m.w / 2, cy = m.y + m.h / 2;
    if (fd === 'low' || (fl && fd === fl)) (e.lo = e.lo || []).push([cx, cy]);
    else if (fd === 'high' || (fh && fd === fh)) (e.hi = e.hi || []).push([cx, cy]);
    else if (fd === vf || fd === enc.y) e.est = Math.max(e.est || 0, m.kind === 'circle' ? 2 * (m.r || m.w / 2) : 0);
    by.set(String(k), e);
  }
  const line = Math.max(0, ...(d.bands || []).map(b => b.line || 0)) || 2;
  // RF-25, state 2: no interval lines, every row's margin printed beside its value and a note in the drawing
  if (d.margins_in_words) {
    const keys = [...new Set(d.marks.filter(m => m.data && m.data.key !== undefined && m.data.key !== null && (m.data.field === vf || m.data.field === enc.y)).map(m => String(m.data.key)))];
    const printed = new Set((d.texts || []).filter(t => t.margin_of !== undefined).map(t => t.margin_of));
    const missing = keys.filter(k => !printed.has(k)), note = (d.texts || []).some(t => t.margin_note);
    if (!keys.length || missing.length || !note) return [`interval: the margins print in words at this width, but ${!keys.length ? 'no estimate is recorded' : missing.length ? `${missing.length} row(s) print no margin (${missing.slice(0, 4).join(', ')})` : ''}${(!keys.length || missing.length) && !note ? ' and ' : ''}${!note ? 'the note saying so is not in the drawing' : ''} (RF-25)${at}`];
    return [];
  }
  const runs = [], needs = [];
  for (const e of by.values()) {
    if (!e.lo || !e.hi) continue;
    // a key that holds several bands (a fan's two steps) is read at its widest
    let len = 0;
    e.lo.forEach(a => e.hi.forEach(b => { len = Math.max(len, Math.hypot(b[0] - a[0], b[1] - a[1])); }));
    runs.push(len);
    // 5 px past a dot on each side, 2 px past a line (a dot hides the ends of a short line; a band shows past a thin one)
    needs.push(e.est ? e.est + 10 : line + 4);
  }
  // RF-25: an interval form with rows to draw that records no interval ends and does not print its margins in words
  // hides its intervals; a fan's later periods may carry no band, so only interval: true is held to it
  if (!runs.length) return def.interval === true && by.size ? [`interval: no row's interval is drawn at this width; draw the intervals, or print every margin in words with c.margins_in_words() (RF-25)${at}`] : [];
  const mr = median(runs), mn = median(needs);
  if (mr + 1e-6 < mn) return [`interval: at this width the middle row's interval spans ${mr.toFixed(1)} px, under the ${mn.toFixed(1)} px its estimate's mark needs (5 px past a dot, 2 px past a line, on each side), so the intervals cannot be seen; give the plot more width, stack the rows, draw 7 px dots, or print every margin in words (D3-899, RF-25)${at}`];
  return [];
}
// AX S2 and BC S1 (round 2 fix pass): no line, path or outline runs through a word. The kit gives a word on the ground the
// ground's halo where a quiet line drawn before it crosses it (a gridline, an axis, a total line: K.QUIET_STROKES); what
// is left fails here: a data line or outline drawn before a word with no halo, any stroke drawn after a word, and a dot
// or bar half under a word. A word is read by its box less 1.5 px a side, as the guard reads a leader through a label.
// Leaders are the guard's own; a stroke drawn through words on purpose (a step struck out) says strike: true; a filled
// shape drawn after a line that covers the word (a dot over its connector, a knockout) hides the line there.
const CROSS_SKIP = ['surface', 'none', 'leader'];
const FILL_SKIP = ['surface', 'none', 'band', 'track', 'land', 'mag-1', 'mag-2', 'light-fill', 'seq-1', 'div-3'];
function crossing_faults(d, at) {
  const K = globalThis.OAChart, f = [], seen = new Set();
  if (!K || !K.stroke_crosses) return f;
  const ink = d.ink || [];
  for (const t of d.texts || []) {
    if (t.w <= 3 || t.h <= 3) continue;
    const x0 = t.x + 1.5, x1 = t.x + t.w - 1.5, y0 = t.y + 1.5, y1 = t.y + t.h - 1.5;
    const cx = t.x + t.w / 2, cy = t.y + t.h / 2;
    // a stroke across the word: drawn after it (over its letters, halo or not), or before it on a word with no halo
    // R3-5: a link through a word is the layout guard's fault (K.guard), reported there once
    for (const b of K.crossed_by(ink, t, b => !b.link && CROSS_SKIP.indexOf(b.stroke) < 0 && (b.seq > t.seq || !t.halo))) {
      const k = 's|' + t.words + '|' + b.stroke + '|' + (b.seq > t.seq);
      if (seen.has(k)) continue;
      seen.add(k);
      f.push(`layout: a ${b.dash ? 'dashed ' : ''}${b.kind} in ${b.stroke} runs through "${String(t.words).slice(0, 30)}"${b.seq > t.seq ? ', drawn after the words' : ''}; draw the words after it with K.parts.clear_label, move them clear, or mark a stroke drawn through words on purpose strike: true (AX S2, BC S1)${at}`);
    }
    // a dot or bar half under the word: its fill reaches into the band its letters stand in (from the cap height to the
    // baseline, line by line as one band) but does not hold the word's middle
    const sz = t.size || 15, ly0 = t.y + 0.14 * sz, ly1 = t.y + t.h - 0.14 * sz;
    for (const b of ink) {
      if (!(b.fill && FILL_SKIP.indexOf(b.fill) < 0 && b.a > 0 && !b.plate && b.seq < t.seq)) continue;
      if (b.x > x1 || b.x + b.w < x0 || b.y > ly1 || b.y + b.h < ly0) continue;
      const inside = b.ring ? Math.hypot(cx - b.ring[0], cy - b.ring[1]) < b.ring[2] : b.poly ? null : (cx > b.x && cx < b.x + b.w && cy > b.y && cy < b.y + b.h);
      if (inside !== false) continue;
      let hit;
      if (b.ring) { const [rx, ry, r] = b.ring, nx = Math.max(x0, Math.min(rx, x1)), ny = Math.max(ly0, Math.min(ry, ly1)); hit = Math.hypot(nx - rx, ny - ry) < r - 0.5; }
      else hit = b.x < x1 - 0.5 && b.x + b.w > x0 + 0.5 && b.y < ly1 - 0.5 && b.y + b.h > ly0 + 0.5;
      // a shape drawn after it that covers the word (a knockout) hides it
      if (hit && ink.some(s => s.fill && s.fill !== 'none' && s.a > 0 && s.seq > b.seq && s.seq < t.seq && K.covers(s, t))) hit = false;
      if (!hit) continue;
      const k = 'f|' + t.words + '|' + b.fill;
      if (seen.has(k)) continue;
      seen.add(k);
      f.push(`layout: a ${b.kind} in ${b.fill} sits half under "${String(t.words).slice(0, 30)}"; set the words clear of the mark, wholly on it, or on a knockout (K.parts.clear_label) (AX S2)${at}`);
    }
  }
  return f;
}
// CD A-M2 (round 2 fix pass): Pillar Red's share of a view. Every shape's paint: its fill's area where the fill resolves to
// Pillar Red, and its stroke's length times its width where the stroke does. The view is the drawing, or, where the
// drawing is taller than a screen, the screen's height of it that holds the most red (900 px at a desk, 844 px on a phone).
const RED_SHARE = 0.05;
const VIEW_H = { desk: 900, phone: 844 };
function red_share(d, tok) {
  const items = [];
  for (const b of d.ink || []) {
    let a = 0;
    if (b.fill && role_color(b.fill, tok) === RED) a += b.a || 0;
    if (b.stroke && role_color(b.stroke, tok) === RED) a += (b.len || 0) * (b.sw || 1);
    if (a > 0) items.push({ a, y0: b.y, y1: b.y + b.h });
  }
  const W = d.width, H = d.height, view = d.phone ? VIEW_H.phone : VIEW_H.desk;
  const total = items.reduce((s, x) => s + x.a, 0);
  if (!(W > 0 && H > 0)) return { share: 0, area: 0 };
  if (H <= view) return { share: total / (W * H), area: total, window: false };
  // a screen's height of the drawing, set at each red shape's top (and the drawing's foot), the one holding the most red
  let best = 0;
  const tops = items.map(x => Math.min(Math.max(0, x.y0), H - view)).concat([H - view]);
  for (const t of tops) {
    let a = 0;
    for (const x of items) {
      const lo = Math.max(t, x.y0), hi = Math.min(t + view, x.y1), span = x.y1 - x.y0;
      a += span > 0 ? x.a * Math.max(0, hi - lo) / span : (x.y0 >= t && x.y0 <= t + view ? x.a : 0);
    }
    best = Math.max(best, a);
  }
  return { share: best / (W * view), area: best, window: true, view };
}

function check_drawing(spec, d, tok, where) {
  const f = [];
  const at = where ? ` (${where})` : '';
  d.guard.forEach(g => f.push('layout guard: ' + g + at));
  d.warnings.forEach(w => f.push('form: ' + w + at));
  const W = d.width, H = d.height;
  // K-S2 (round 1 fix pass): every shape the form draws, a mark a reader reads or not (a zero line, a gridline, a band),
  // sits inside the drawing's box; the drawing's own overflow would paint it over the figure's words (CD RM1)
  for (const b of d.ink || []) {
    if (b.x < -1 || b.y < -1 || b.x + b.w > W + 1 || b.y + b.h > H + 1) {
      f.push(`chart: a ${b.kind}${b.role ? ' (' + b.role + ')' : ''} drawn outside its drawing, at x ${Math.round(b.x)} to ${Math.round(b.x + b.w)}, y ${Math.round(b.y)} to ${Math.round(b.y + b.h)} in a ${W} by ${H} drawing${at}`);
      break;
    }
  }
  // access S2 (round 1 fix pass): two dots a form draws for one row (a dumbbell's two years) sit apart by more than a dot's
  // radius wherever the values differ by a tenth or more of the larger, or the drawing shows no change where the data holds
  // one; a small change drawn as touching dots is the honest drawing of a small change
  const by_row = {};
  for (const m of d.marks) if (m.row !== undefined && m.kind === 'circle') (by_row[m.row] = by_row[m.row] || []).push(m);
  const close = Object.keys(by_row).filter(k => {
    const ms = by_row[k];
    for (let i = 0; i < ms.length; i++) for (let j = i + 1; j < ms.length; j++) {
      const a = ms[i], b = ms[j];
      const dist = Math.hypot((a.x + a.w / 2) - (b.x + b.w / 2), (a.y + a.h / 2) - (b.y + b.h / 2));
      const va = Number((a.data || {}).value), vb = Number((b.data || {}).value);
      if (dist < Math.max(a.r || a.w / 2, b.r || b.w / 2) && Math.abs(va - vb) >= 0.1 * Math.max(Math.abs(va), Math.abs(vb))) return true;
    }
    return false;
  });
  if (close.length) f.push(`chart: ${close.length} row(s) draw their two dots closer than a dot's radius though their values differ by a tenth or more, so the drawing hides the change (${close.slice(0, 4).join(', ')}${close.length > 4 ? ', and more' : ''}); give each row its own scale, such as a percent change (Rule 14.26), or split the rows into panels by size${at}`);
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
  // forced colors (D3-94): no label in the ink of the mark under it, in the reader's system colors (kit.js, K.FC)
  if (d.fc) {
    const fills = d.marks.filter(m => m.fill && m.w > 0 && m.h > 0);
    // beside a red point the context marks take the ground with an outline (kit.css, access S10)
    const pointed = d.marks.some(m => m.fill === 'point' || m.stroke === 'point');
    // A-E1 (round 2): a filled path is read by its outline, not its box; a word on a filled path drawn as no mark (a band
    // under a stacked area's name) takes that path's fill when no mark lies under it
    const in_poly = (subs, px, py) => {
      let inside = false;
      for (const pts of subs || []) for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
        const a = pts[i], b = pts[j];
        if ((a[1] > py) !== (b[1] > py) && px < (b[0] - a[0]) * (py - a[1]) / (b[1] - a[1]) + a[0]) inside = !inside;
      }
      return inside;
    };
    const paths = (d.ink || []).filter(m => m.kind === 'path' && m.poly && m.fill && m.fill !== 'none');
    for (const t of d.texts || []) {
      const cx = t.x + t.w / 2, cy = t.y + t.h / 2;
      let ground = 'Canvas', hit = false;
      for (const m of fills) if (m.poly ? in_poly(m.poly, cx, cy) : (cx > m.x && cx < m.x + m.w && cy > m.y && cy < m.y + m.h)) { hit = true; ground = m.fc === 'total' || (pointed && m.fill === 'context') ? 'Canvas' : d.fc[m.fill] || 'CanvasText'; }
      if (!hit) for (const m of paths) if (in_poly(m.poly, cx, cy)) ground = pointed && m.fill === 'context' ? 'Canvas' : d.fc[m.fill] || 'CanvasText';
      // a word on a GrayText mark takes Canvas (second pass), except on context beside a red point (kit.css)
      const ink = (d.fc_on_dark || []).indexOf(t.fill) >= 0 || (t.on_gray && !(pointed && t.on_context)) ? 'Canvas' : 'CanvasText';
      if (ink === ground) f.push(`forced colors: "${String(t.words).slice(0, 30)}" prints in ${ink} on a mark in ${ground}${at}`);
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
  // ED-E15 (round 2): red marks of one job (a group the title names together, ruling (c); a red line with its vertex dots)
  // count as one working red; a red mark with no job is a job of its own
  const jobs = new Set(reds.map((m, i) => m.job !== undefined && m.job !== null ? 'job:' + m.job : 'mark:' + i));
  if (jobs.size > 1) f.push(`chart: ${jobs.size} working reds in one view (Rule 05.3)${at}`);
  // CD A-M2 (round 2 fix pass, D3-890): Rule 05.1 holds Pillar Red within 5 percent of every view. The kit measures the
  // red's painted area (fills, and strokes as length times width, from every shape drawn, marks or not) against the drawing,
  // and against a window of a screen's height (900 px at a desk, 844 on a phone) where the drawing is taller than one
  f.push(...crossing_faults(d, at));
  f.push(...band_faults(d, tok, at));
  f.push(...interval_faults(spec, d, { interval: d.interval }, at));
  const share = red_share(d, tok);
  if (share.share > RED_SHARE + 1e-9) f.push(`chart: Pillar Red covers ${(100 * share.share).toFixed(1)} percent of ${share.window ? `a ${share.view} px tall view of the drawing` : 'the drawing'}, over Rule 05.1's 5 percent; a named area past it takes the subject ink (D3-890)${at}`);
  for (const r of reds) {
    for (const m of d.marks) {
      if (m === r || color(m) !== PRUSSIAN) continue;
      if (r.x <= m.x + m.w + 1 && m.x <= r.x + r.w + 1 && r.y <= m.y + m.h + 1 && m.y <= r.y + r.h + 1) f.push(`chart: red touches Prussian${at}`);
    }
  }
  // keys told apart by lightness (access S5): the gap is the smaller of CIE L* and the grayscale proof's luma (x 100); a
  // direct label is an exemption only where every mark of that fill carries a text on or beside it; an ordered scale needs
  // its neighbors apart, at 8, and its lightest step apart from the ground unless its marks carry an outline
  const ground = tok['--oa-color-surface'] || tok['--oa-chart-color-surface'];
  const gap = (x, y) => {
    const la = hex_to_lab_l(x), lb = hex_to_lab_l(y), ya = luma(x), yb = luma(y);
    if (la === null || lb === null) return null;
    return Math.min(Math.abs(la - lb), ya === null || yb === null ? Infinity : Math.abs(ya - yb) * 100);
  };
  const earned = e => {
    if (!e.direct) return false;
    const ms = d.marks.filter(m => m.fill === e.fill && m.w > 0 && m.h > 0);
    return ms.every(m => (d.texts || []).some(t => t.x < m.x + m.w + 4 && m.x - 4 < t.x + t.w && t.y < m.y + m.h + 4 && m.y - 4 < t.y + t.h));
  };
  for (const key of d.keys || []) {
    const ordered = key.length && key.every(e => e.ordered);
    if (ordered) {
      for (let i = 0; i + 1 < key.length; i++) {
        if (key[i].pattern || key[i + 1].pattern || (earned(key[i]) && earned(key[i + 1]))) continue;
        const g = gap(role_color(key[i].fill, tok), role_color(key[i + 1].fill, tok));
        if (g === null) { f.push(`key: ${key[i].fill} or ${key[i + 1].fill} has no resolved color${at}`); continue; }
        if (g < KEY_ORDERED_MARGIN) f.push(`key: neighbors ${key[i].fill} and ${key[i + 1].fill} differ by ${g.toFixed(1)} in lightness, under ${KEY_ORDERED_MARGIN}${at}`);
      }
      const light = key[0];
      if (ground && !light.outline) {
        const g = gap(role_color(light.fill, tok), String(ground).trim());
        if (g !== null && g < KEY_ORDERED_MARGIN) f.push(`key: the lightest step ${light.fill} differs from the ground by ${g.toFixed(1)}, under ${KEY_ORDERED_MARGIN}, and its marks carry no outline${at}`);
      }
      continue;
    }
    const plain = key.filter(e => !e.pattern && !earned(e));
    for (let i = 0; i < plain.length; i++) for (let j = i + 1; j < plain.length; j++) {
      const g = gap(role_color(plain[i].fill, tok), role_color(plain[j].fill, tok));
      if (g === null) { f.push(`key: ${plain[i].fill} or ${plain[j].fill} has no resolved color${at}`); continue; }
      if (g < KEY_LIGHTNESS_MARGIN) f.push(`key: ${plain[i].fill} and ${plain[j].fill} differ by ${g.toFixed(1)} in lightness, under ${KEY_LIGHTNESS_MARGIN}, with no pattern or direct label${at}`);
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
  // R3-3: in a one-column file an empty cell is written "", so its line is not read as no row
  const one = columns.length === 1;
  const q = v => { if (v === null || v === undefined || v === '') return one ? '""' : ''; const s = String(v); return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  return [columns.join(',')].concat(rows.map(r => columns.map(c => q(r[c])).join(','))).join('\n') + '\n';
}

function id_types() {
  // the type word each chip carries (H11): Variable, Connection, Loop, Reform, Issue, and since round 3 Claim (C-3)
  const out = {};
  for (const [k, t] of v7().ids) if (['Variable', 'Connection', 'Loop', 'Reform', 'Issue', 'Claim'].indexOf(t) >= 0) out[k] = t;
  return out;
}

module.exports = { id_types, check_spec, check_drawing, check_csv, red_share, RED_SHARE, contrast, band_faults, interval_faults, crossing_faults, to_csv, load_dataset, rows_of, v7, role_color, hex_to_lab_l, strings, retrieved_dates,
  FAMILIES, TIERS, EVIDENCE, DISCLOSURE, KEY_LIGHTNESS_MARGIN, ROOT, DATA };
