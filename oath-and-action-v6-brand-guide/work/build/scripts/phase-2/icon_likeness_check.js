#!/usr/bin/env node
// Look-alike check for new icons against the Civic Line (stage B, November 9, 2026).
//
// Usage:
//   node work/build/scripts/phase-2/icon_likeness_check.js work/build/assets/utility-icons/
//   node work/build/scripts/phase-2/icon_likeness_check.js folder/ [more folders or .svg files] [--recursive]
//        [--flag 99] [--watch 95] [--masters in-use|october] [--json out.json] [--quiet]
//   node work/build/scripts/phase-2/icon_likeness_check.js --self-test
//
// The method is Board 6's silhouette likeness, ported from board6_pillar_icons_build.js (November 7) without change:
// each drawing is drawn by Chromium in its own box at 24 px, its ink read against Newsprint (#DCD9D2) and Charcoal
// (18, 18, 18), blurred with a Gaussian of sigma 1.2 px, and two drawings are compared by Pearson correlation of their
// ink maps, best over shifts of up to 1 px either way. A 24-unit utility icon and a 128-unit Civic Line drawing are
// both drawn at 24 px, so they compare as they would sit side by side. Ink is the drawing's coverage in Charcoal, so a
// red part, a grey part or `currentColor` counts the same as black.
//
// It compares each new drawing against the Civic Line masters (black editions) and against each other, and ranks every
// likeness as a percentile of the pairs of the masters themselves. The masters are the set in use by default (D2-748,
// promotion, November 10, 2026): the drawings in civic-line-v6/, one per inventory row (125 since CL-075 Housing joined,
// DR-207, promotion C, November 11, 2026: 7,750 pairs). --masters october reads the 122
// October masters (7,381 pairs), which Board 6 measured; the self-test runs both, and proves the port on October's.
//   flag  (default the 99th percentile): as alike as the closest one pair in a hundred among the masters. These are
//         listed as look-alikes, and the check exits 1.
//   watch (default the 95th percentile): listed for a look, without failing.
// Pairs the check reports apart and never fails:
//   - a drawing and its own original, when the file name carries the master's ID (CL-025, R-13): a redraw should stay
//     close to the drawing it replaces;
//   - options of one subject: files whose names match once the option (Option-A, Opt-2, Fit-1), the size (16px) and
//     the edition (Red-Black, Black, Newsprint, Red-Newsprint, One-Color, Two-Color) are set aside.
// Editions of one drawing (the same name apart from the edition) are compared once, with the black edition preferred.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
// The master sets: the folder holding black/ and red-black/, and its inventory, whose icons name their files.
const SETS = {
  'in-use': { name: 'the set in use (civic-line-v6)', dir: 'work/build/assets/civic-line-v6', inv: '20261110_Civic-Line-V6-Inventory.json' },
  october: { name: 'the October set (civic-line)', dir: 'work/build/assets/civic-line', inv: '20261029_Civic-Line-Inventory.json' },
};
let SET, CL, INV, masterIds;
function useSet(key) {
  if (!SETS[key]) usage(`--masters is ${Object.keys(SETS).join(' or ')}`);
  SET = SETS[key]; CL = path.join(ROOT, SET.dir);
  INV = JSON.parse(fs.readFileSync(path.join(CL, SET.inv), 'utf8'));
  masterIds = new Set(INV.icons.map((i) => i.id));
}
const B6 = path.join(ROOT, 'work/boards/phase-2/board-6/pillar-icons/20261107_Board-6-Pillar-Icons-Measurements.json');
const PX = 24, SIGMA = 1.2, SHIFT = 1;

// ---------- arguments ----------
function usage(msg) {
  if (msg) console.error('icon_likeness_check: ' + msg);
  console.error('Usage: node icon_likeness_check.js folder/|file.svg ... [--recursive] [--flag 99] [--watch 95] [--json out.json] [--quiet]\n       node icon_likeness_check.js --self-test');
  process.exit(2);
}
function parseArgs(argv) {
  const o = { inputs: [], flag: 99, watch: 95, json: null, quiet: false, recursive: false, selfTest: false, masters: 'in-use' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => { if (i + 1 >= argv.length) usage(a + ' needs a value'); return argv[++i]; };
    if (a === '--flag') o.flag = Number(val());
    else if (a === '--watch') o.watch = Number(val());
    else if (a === '--json') o.json = val();
    else if (a === '--masters') o.masters = val();
    else if (a === '--quiet' || a === '-q') o.quiet = true;
    else if (a === '--recursive' || a === '-r') o.recursive = true;
    else if (a === '--self-test') o.selfTest = true;
    else if (a === '--help' || a === '-h') usage();
    else if (a.startsWith('-')) usage('unknown option ' + a);
    else o.inputs.push(a);
  }
  if (!(o.flag > 0 && o.flag < 100) || !(o.watch > 0 && o.watch <= o.flag)) usage('--flag and --watch are percentiles, with --watch at or under --flag');
  return o;
}
function collect(inputs, recursive) {
  const out = [];
  const walk = (dir) => {
    for (const n of fs.readdirSync(dir).sort()) {
      const p = path.join(dir, n);
      if (fs.statSync(p).isDirectory()) { if (recursive) walk(p); } else if (n.toLowerCase().endsWith('.svg')) out.push(p);
    }
  };
  for (const f of inputs) {
    if (!fs.existsSync(f)) usage('no such file or folder ' + f);
    if (fs.statSync(f).isDirectory()) walk(f); else out.push(f);
  }
  if (!out.length) usage('no .svg files found' + (recursive ? '' : ' (add --recursive to look in subfolders)'));
  return out.map((f) => ({ name: path.basename(f), file: f, text: fs.readFileSync(f, 'utf8') }));
}

// ---------- names ----------
const EDITION = /[-_ ](red[-_ ]black|red[-_ ]newsprint|black|newsprint|one[-_ ]colou?r|two[-_ ]colou?r|mono)$/i;
const OPTION = /[-_ ](option|opt|fit|variant)[-_ ]?[a-z0-9]+$/i;
const SIZE = /[-_ ]\d{1,3}[-_ ]?px(?=$|[-_ ])/ig;
function stems(name) {
  let s = name.replace(/\.svg$/i, '').replace(/^\d{8}_/, '');
  const strip = (re) => { let prev; do { prev = s; s = s.replace(re, ''); } while (s !== prev); };
  strip(EDITION); const drawing = s;            // the same drawing in another edition
  s = s.replace(SIZE, '');
  for (let n = 0; n < 3; n++) { strip(OPTION); strip(EDITION); }
  return { drawing: drawing.toLowerCase(), subject: s.toLowerCase() };
}
function ownIds(name) {
  const ids = new Set();
  for (const m of name.matchAll(/(?:^|[^A-Za-z0-9])((?:CL|R)-\d{1,3})(?=[^0-9]|$)/g)) {
    const id = m[1].replace(/^(CL)-(\d+)$/, (x, p, n) => `${p}-${n.padStart(3, '0')}`);
    if (masterIds.has(id)) ids.add(id);
  }
  return ids;
}
function dedupeEditions(items) {
  const groups = new Map();
  for (const it of items) { const k = stems(it.name).drawing; if (!groups.has(k)) groups.set(k, []); groups.get(k).push(it); }
  const kept = [], skipped = [];
  for (const g of groups.values()) {
    const pick = g.find((it) => /[-_ ]black\.svg$/i.test(it.name) && !/red[-_ ]black\.svg$/i.test(it.name)) || g[0];
    kept.push(pick); for (const it of g) if (it !== pick) skipped.push({ name: it.name, as: pick.name });
  }
  return { kept, skipped };
}

// ---------- sizing (as in the pixel-fit check) ----------
function sized(svgText, D) {
  const s = svgText.replace(/<\?xml[^>]*>\s*/, '').replace(/<!DOCTYPE[^>]*>\s*/i, '');
  const m = s.match(/<svg\b[^>]*>/);
  if (!m) throw new Error('no <svg> element');
  let tag = m[0];
  const num = (name) => { const r = tag.match(new RegExp('\\s' + name + '="\\s*([\\d.]+)(px)?\\s*"')); return r ? Number(r[1]) : null; };
  let vb = (tag.match(/\sviewBox="([^"]+)"/) || [])[1];
  if (!vb) {
    const w = num('width'), h = num('height');
    if (!(w > 0 && h > 0)) throw new Error('the root <svg> has neither a viewBox nor a width and height');
    vb = `0 0 ${w} ${h}`; tag = tag.replace(/<svg\b/, `<svg viewBox="${vb}"`);
  }
  tag = tag.replace(/\s(width|height)="[^"]*"/g, '').replace(/<svg\b/, `<svg width="${D}" height="${D}"`);
  return { text: s.replace(m[0], tag), units: Number(vb.trim().split(/[\s,]+/)[2]) };
}

// ---------- measuring, in the page (Board 6's functions, with ink from coverage) ----------
async function inkMaps(drawings) {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.setContent('<!doctype html><html><body></body></html>');
    return await page.evaluate(async ({ list, PX, SIGMA }) => {
      const NP = [220, 217, 210], CH = [18, 18, 18];  // Newsprint #DCD9D2 and Charcoal #121212
      const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      const lum = (r, g, b) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
      const Lbg = lum(...NP), Lch = lum(...CH);
      const blur = (m, px, s) => {
        const r = Math.ceil(3 * s), k = []; let t = 0; for (let i = -r; i <= r; i++) { const v = Math.exp(-i * i / (2 * s * s)); k.push(v); t += v; } for (let i = 0; i < k.length; i++) k[i] /= t;
        const a = new Float64Array(px * px), b = new Float64Array(px * px);
        for (let y = 0; y < px; y++) for (let x = 0; x < px; x++) { let v = 0; for (let i = -r; i <= r; i++) { const xx = x + i; if (xx >= 0 && xx < px) v += k[i + r] * m[y * px + xx]; } a[y * px + x] = v; }
        for (let y = 0; y < px; y++) for (let x = 0; x < px; x++) { let v = 0; for (let i = -r; i <= r; i++) { const yy = y + i; if (yy >= 0 && yy < px) v += k[i + r] * a[yy * px + x]; } b[y * px + x] = v; }
        return b;
      };
      const out = [];
      for (const it of list) {
        const img = new Image(); img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(it.text); await img.decode();
        const c = document.createElement('canvas'); c.width = c.height = PX; const g = c.getContext('2d');
        g.fillStyle = '#DCD9D2'; g.fillRect(0, 0, PX, PX);
        if (it.direct) g.drawImage(img, 0, 0, PX, PX);    // a black master, drawn exactly as Board 6 drew it
        else {                                              // any other drawing: its coverage, in Charcoal
          const t = document.createElement('canvas'); t.width = t.height = PX; const h = t.getContext('2d');
          h.drawImage(img, 0, 0, PX, PX); h.globalCompositeOperation = 'source-in'; h.fillStyle = '#121212'; h.fillRect(0, 0, PX, PX);
          g.drawImage(t, 0, 0);
        }
        const d = g.getImageData(0, 0, PX, PX).data;
        // Board 6's ink: (L_newsprint - L) / (L_newsprint - L_charcoal), clamped to 0 to 1.
        const m = new Float64Array(PX * PX); let x0 = PX, y0 = PX, x1 = -1, y1 = -1;
        for (let i = 0; i < PX * PX; i++) {
          const L = lum(d[4 * i], d[4 * i + 1], d[4 * i + 2]);
          m[i] = Math.max(0, Math.min(1, (Lbg - L) / (Lbg - Lch)));
          if (m[i] > 0.5) { const x = i % PX, y = (i - x) / PX; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
        }
        out.push({ map: Array.from(blur(m, PX, SIGMA)), extent: x1 < 0 ? 0 : Math.max(x1 - x0 + 1, y1 - y0 + 1) / PX });
      }
      return { maps: out, ua: navigator.userAgent };
    }, { list: drawings.map((d) => (d.direct ? { text: d.text, direct: true } : { text: sized(d.text, PX).text })), PX, SIGMA });
  } finally { await browser.close(); }
}
function corr(A, B, px, sh) {
  let best = -1;
  for (let dy = -sh; dy <= sh; dy++) for (let dx = -sh; dx <= sh; dx++) {
    let n = 0, sa = 0, sb = 0, saa = 0, sbb = 0, sab = 0;
    for (let y = Math.max(0, dy); y < px + Math.min(0, dy); y++) for (let x = Math.max(0, dx); x < px + Math.min(0, dx); x++) {
      const a = A[y * px + x], b = B[(y - dy) * px + (x - dx)]; n++; sa += a; sb += b; saa += a * a; sbb += b * b; sab += a * b;
    }
    const cov = sab - sa * sb / n, va = saa - sa * sa / n, vb = sbb - sb * sb / n;
    if (va > 0 && vb > 0) best = Math.max(best, cov / Math.sqrt(va * vb));
  }
  return best;
}
const r4 = (v) => Math.round(v * 1e4) / 1e4;
function pct(sorted, v) { let lo = 0, hi = sorted.length; while (lo < hi) { const m = (lo + hi) >> 1; if (sorted[m] < v) lo = m + 1; else hi = m; } return 100 * lo / sorted.length; }
const atPct = (sorted, p) => sorted[Math.min(sorted.length - 1, Math.floor(sorted.length * p / 100))];

function loadMasters() {
  return INV.icons.map((i) => ({ id: i.id, label: i.label, name: i.exports.svg_black, direct: true, text: fs.readFileSync(path.join(CL, 'black', i.exports.svg_black), 'utf8') }));
}

// ---------- the check ----------
async function check(items, opts) {
  const masters = loadMasters();
  const { kept, skipped } = dedupeEditions(items);
  const res = await inkMaps([...masters, ...kept]);
  const M = res.maps.slice(0, masters.length), N = res.maps.slice(masters.length);
  const all = [];
  const masterPair = {};
  for (let i = 0; i < M.length; i++) for (let j = i + 1; j < M.length; j++) {
    const v = r4(corr(M[i].map, M[j].map, PX, SHIFT)); all.push(v); masterPair[masters[i].id + '|' + masters[j].id] = v;
  }
  const sorted = all.slice().sort((a, b) => a - b);
  const flagAt = atPct(sorted, opts.flag), watchAt = atPct(sorted, opts.watch);
  const rows = { flagged: [], watch: [], own: [], options: [], closest: [] };
  kept.forEach((it, a) => {
    const own = ownIds(it.name);
    let best = null;
    masters.forEach((m, b) => {
      const v = r4(corr(N[a].map, M[b].map, PX, SHIFT));
      const row = { a: it.name, b: `${m.id} ${m.label}`, likeness: v, percentile: +pct(sorted, v).toFixed(1) };
      if (own.has(m.id)) { rows.own.push(row); return; }
      if (!best || v > best.likeness) best = row;
      if (v >= flagAt) rows.flagged.push({ ...row, against: 'master' });
      else if (v >= watchAt) rows.watch.push({ ...row, against: 'master' });
    });
    rows.closest.push({ ...best, extent: +N[a].extent.toFixed(2) });
  });
  for (let a = 0; a < kept.length; a++) for (let b = a + 1; b < kept.length; b++) {
    const v = r4(corr(N[a].map, N[b].map, PX, SHIFT));
    const row = { a: kept[a].name, b: kept[b].name, likeness: v, percentile: +pct(sorted, v).toFixed(1), against: 'new' };
    if (stems(kept[a].name).subject === stems(kept[b].name).subject) rows.options.push(row);
    else if (v >= flagAt) rows.flagged.push(row);
    else if (v >= watchAt) rows.watch.push(row);
  }
  for (const k of ['flagged', 'watch', 'own', 'options']) rows[k].sort((x, y) => y.likeness - x.likeness);
  const masterTop = Object.entries(masterPair).sort((x, y) => y[1] - x[1]).slice(0, 12).map(([k, v]) => ({ pair: k.replace('|', ' and '), likeness: v }));
  return {
    renderer: res.ua, files: items.length, compared: kept.length, editions_skipped: skipped,
    distribution: { pairs: sorted.length, p50: atPct(sorted, 50), p90: atPct(sorted, 90), p95: atPct(sorted, 95), p99: atPct(sorted, 99), p999: atPct(sorted, 99.9), max: sorted[sorted.length - 1] },
    thresholds: { flag: { percentile: opts.flag, likeness: flagAt }, watch: { percentile: opts.watch, likeness: watchAt } },
    masters_closest_pairs: masterTop, masterPair, ...rows,
  };
}

function print(r) {
  const L = [];

  L.push(`Look-alike check at ${PX} px: ${r.compared} new drawings${r.editions_skipped.length ? ` (${r.editions_skipped.length} more files are other editions of these)` : ''} against the ${INV.icons.length} Civic Line masters of ${SET.name} and each other.`);
  L.push(`Masters: ${r.distribution.pairs} pairs; median likeness ${r.distribution.p50}, 95th percentile ${r.distribution.p95}, 99th ${r.distribution.p99}.`);
  L.push(`Flag at ${r.thresholds.flag.likeness} (${r.thresholds.flag.percentile}th percentile); watch from ${r.thresholds.watch.likeness} (${r.thresholds.watch.percentile}th).`);
  L.push('Columns: likeness, then its percentile among the master pairs.');
  const block = (title, list, fmt) => { L.push(`\n${title}: ${list.length ? '' : 'none'}`); for (const x of list) L.push('  ' + fmt(x)); };
  const pair = (x) => `${x.likeness.toFixed(3)}  ${x.percentile.toFixed(1).padStart(5)}  ${x.a}  ~  ${x.b}`;
  block('Look-alikes (flagged)', r.flagged, pair);
  block('Worth a look (watch)', r.watch, pair);
  block('Own originals, reported apart', r.own, pair);
  block('Options of one subject, reported apart', r.options, pair);
  block('Closest master for each new drawing', r.closest, (x) => `${x.likeness.toFixed(3)}  ${x.percentile.toFixed(1).padStart(5)}  ${x.a}  ~  ${x.b}   (ink spans ${Math.round(x.extent * 100)}% of the box)`);
  return L.join('\n');
}

// ---------- self-test ----------
function selfFixtures() {
  const by = Object.fromEntries(loadMasters().map((m) => [m.id, m]));
  const inner = (t) => t.replace(/^[\s\S]*?<svg\b[^>]*>/, '').replace(/<\/svg>\s*$/, '').replace(/\sid="[^"]*"/g, '');
  const at24 = (id) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g transform="scale(${24 / 128})">${inner(by[id].text)}</g></svg>`;
  const red = fs.readFileSync(path.join(CL, 'red-black', INV.icons.find((i) => i.id === 'CL-019').exports.svg_red_black), 'utf8');
  return [
    { name: 'Utility-Refresh-Option-A.svg', text: by['CL-024'].text, expect: { flagged: 'CL-024' }, why: 'CL-024 Feedback Loop under a utility name' },
    { name: 'Utility-Reload-Option-B.svg', text: at24('CL-024'), expect: { flagged: 'CL-024' }, why: 'the same drawing on a 24-unit grid' },
    { name: 'Utility-Plus-Option-A.svg', text: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>', expect: { quiet: true }, why: 'a plus sign, not like any master' },
    { name: 'CL-025-Congress-Redraw-Option-A-Black.svg', text: by['CL-025'].text, expect: { own: 'CL-025' }, why: 'a redraw named for its original' },
    { name: 'CL-019-Explain-24px-Fit-1-Red-Black.svg', text: red, expect: { edition: true }, why: 'a red-black edition beside its black edition' },
    { name: 'CL-019-Explain-24px-Fit-1-Black.svg', text: by['CL-019'].text, expect: { own: 'CL-019' }, why: 'a pixel fit named for its master' },
    { name: 'CL-019-Explain-16px-Fit-2-Black.svg', text: at24('CL-019'), expect: { option: true }, why: 'another size and fit of one subject' },
  ];
}
async function selfTest() {
  let bad = 0;
  const say = (ok, msg) => { if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'MISS'} ${msg}`); };
  for (const key of ['october', 'in-use']) {
    useSet(key);
    console.log(`Masters: ${SET.name}, ${INV.icons.length} drawings`);
    await selfTestSet(key, say);
  }
  console.log(bad ? `self-test: ${bad} wrong` : 'self-test: all right');
  return bad ? 1 : 0;
}
async function selfTestSet(key, say) {
  const fx = selfFixtures();
  if (key === 'in-use') fx.push({ name: 'CL-073-Testify-Option-A-Black.svg', text: Object.fromEntries(loadMasters().map((m) => [m.id, m]))['CL-073'].text, expect: { own: 'CL-073' }, why: 'a new topic drawing named for its own ID, a master in the set in use' });
  const r = await check(fx, { flag: 99, watch: 95 });
  const d = r.distribution;
  if (key === 'october') {
    // 1. The port reproduces Board 6, which measured the October masters.
    const b6 = JSON.parse(fs.readFileSync(B6, 'utf8'));
    const dd = ['p50', 'p90', 'p95'].map((k) => Math.abs(d[k] - b6.pair_distribution[k]));
    say(d.pairs === 7381 && Math.max(...dd) <= 0.002, `masters: ${d.pairs} pairs; p50 ${d.p50}, p90 ${d.p90}, p95 ${d.p95} against Board 6's ${b6.pair_distribution.p50}, ${b6.pair_distribution.p90}, ${b6.pair_distribution.p95} (largest difference ${Math.max(...dd).toFixed(4)})`);
    let worst = 0, n = 0;
    for (const s of b6.sets) for (const p of s.pairs) { const v = r.masterPair[`${p.a}|${p.b}`] ?? r.masterPair[`${p.b}|${p.a}`]; worst = Math.max(worst, Math.abs(v - p.likeness)); n++; }
    say(worst <= 0.002, `Board 6's ${n} set pairs reproduced within ${worst.toFixed(4)} (allowed 0.002)`);
  } else {
    // 1. The set in use: every drawing read, each pair once. The count follows the set in use (promotion C): one inventory
    // row per drawing, one black file per row, and nothing in black/ the inventory leaves out.
    const k = INV.icons.length;
    const files = fs.readdirSync(path.join(CL, 'black')).filter((f) => /-Black\.svg$/.test(f)).length;
    say(k === files && new Set(INV.icons.map((i) => i.id)).size === k && d.pairs === k * (k - 1) / 2,
      `masters: ${k} drawings in the inventory, ${files} black files, ${d.pairs} pairs; p50 ${d.p50}, p95 ${d.p95}, p99 ${d.p99}, closest ${d.max}`);
  }
  // 2. Plants.
  const flaggedWith = (name, id) => r.flagged.some((x) => x.a === name && x.b.startsWith(id + ' '));
  for (const f of fx) {
    const e = f.expect;
    if (e.flagged) say(flaggedWith(f.name, e.flagged), `${f.name}: ${f.why}, flagged against ${e.flagged}`);
    if (e.quiet) say(!r.flagged.some((x) => x.a === f.name || x.b === f.name), `${f.name}: ${f.why}, not flagged (closest ${r.closest.find((x) => x.a === f.name).b}, ${r.closest.find((x) => x.a === f.name).percentile}th)`);
    if (e.own) say(r.own.some((x) => x.a === f.name && x.b.startsWith(e.own + ' ')) && !flaggedWith(f.name, e.own), `${f.name}: ${f.why}, its pair with ${e.own} reported apart and not flagged`);
    if (e.edition) say(r.editions_skipped.some((x) => x.name === f.name), `${f.name}: ${f.why}, compared once`);
    if (e.option) say(r.options.some((x) => x.a === f.name || x.b === f.name) && !r.flagged.some((x) => x.against === 'new' && (x.a === f.name || x.b === f.name)), `${f.name}: ${f.why}, reported apart`);
  }
}

(async () => {
  const o = parseArgs(process.argv.slice(2));
  if (o.selfTest) process.exit(await selfTest());
  useSet(o.masters);
  if (!o.inputs.length) usage('give a folder of new SVGs');
  const items = collect(o.inputs, o.recursive);
  const r = await check(items, o);
  if (!o.quiet) console.log(print(r));
  console.log(`\n${r.flagged.length ? `${r.flagged.length} look-alike pair${r.flagged.length > 1 ? 's' : ''} at or above the ${o.flag}th percentile.` : `No look-alike pair at or above the ${o.flag}th percentile.`}`);
  if (o.json) {
    const { masterPair, ...keep } = r;
    fs.mkdirSync(path.dirname(path.resolve(o.json)), { recursive: true });
    fs.writeFileSync(o.json, JSON.stringify({ tool: 'work/build/scripts/phase-2/icon_likeness_check.js', run: new Date().toISOString(), method: `Ink maps at ${PX} px from coverage in Charcoal over Newsprint, Gaussian blur sigma ${SIGMA} px, Pearson correlation best over shifts up to ${SHIFT} px, percentile among the ${r.distribution.pairs} pairs of the ${INV.icons.length} Civic Line masters of ${SET.name} (Board 6's method).`, masters: SET.dir, ...keep }, null, 1));
  }
  process.exit(r.flagged.length ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
