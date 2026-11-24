// Video frame renderer (chat 12b, CD-S7; contracts W-C1 to W-C4 in work/handoffs/phase-4/20261124_Chat-12b-Engineer-W-Notes.md,
// rulings DD12b-R1 in 20261124_Chat-12b-Design-Director-Notes.md): stills of the video on chart S04 that chapter 16's
// storyboard and vertical frame show (Rules 16.10 and 16.11), each exported at the true size of its row in the platform
// specifications table (video.vertical, 1080 by 1920; video.landscape, 1920 by 1080).
//
// A frame is laid out as a page at its pixels divided by its device scale (DD12b-R1: scale 2, a 540 by 960 page for the
// vertical frame, 960 by 540 for the storyboard's) and shown at that scale, so every part keeps the type tokens' proportions
// to the others: the export is that page captured at the device scale, and the guide's frame is that page, which the plate
// scales to its wrapper. Top to bottom, as the ruling orders them:
//   L8, the monogram, top right, 24 px in from the frame's top and right edges (Rule 12.3), the one mark outside the safe area;
//   the chart, drawn by the chart kit's own code (K.draw on work/build/chart-kit/specs/<id>.json and its rows) at the
//     view's width on the layout page: the drawing K.draw returns, nothing redrawn, no title, measure line or notes;
//   the chart's source line, the kit's own element (K.figure's p.oac-source) in the kit's source-line type, under the chart;
//   the caption band, Charcoal, Inter 600 in Newsprint, two lines at most (Rule 16.11), its foot on the caption-safe foot;
//   no name plate unless a view asks for one;
//   the safe areas as an overlay a reader switches on (lib.mjs overlay), and drawn on in an export of their own.
// Every place and size in the content file is in the exported frame's pixels, as the ruling gives them; the renderer
// divides by the view's scale. The checks (oa-app.mjs, video_checks) run on the export page.
//
// Content keys: id, type "video-frame", guide, export_date, chart (a chart kit spec id, "s04"), charts ({id: [px]}, the
// plate's chart inputs), words_generator (default chapter 16's), views [{key, platform, scale, moment, export_name,
// safe (insets with exclude, for a row that has none), safe_basis ("platform" or "studio"), basis_key (the safe_labels key
// naming the basis), chart {px (on the layout page), x, y}, source {gap, x, w}, band {x, w | center, max_w; bottom, size,
// lh, pad_y, pad_x}, sign {w, edge}, name_plate (bool), floor_px}], plate_head, plate_line.
// Words (W-C2): `phase4_ch16_build.py --page-words all`, entry "A21": frames.<key>.caption, frames.<key>.alt,
// frames.<key>.time, source, name_plate, signature, safe_labels {vertical, landscape, buttons, controls}, switch. Until the
// generator prints them, the file OA_PAGE_WORDS_A21 names (a stand-in), and the plate records provisional_words.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { spawnSync } from 'child_process';
import { ROOT, esc, mark, platform, safe_boxes, symbolize } from '../lib.mjs';

export const type = 'video-frame';
const require = createRequire(import.meta.url);
const GEN16 = 'work/build/scripts/phase-4/phase4_ch16_build.py';
const CK = path.join(ROOT, 'work/build/chart-kit');
const L8 = 'work/build/assets/identity/lockups/20261028_L8-Monogram-Master.svg';
const L8_RATIO = 108 / 299.67;   // the master's viewBox, height to width

// ------------------------------------------------------------------------------------------------------------- words
let WORDS = null;
export function video_words(id, generator = GEN16) {
  if (WORDS && WORDS.__id === id) return WORDS;
  let got = null, from = null;
  if (fs.existsSync(path.join(ROOT, generator))) {
    const r = spawnSync('python3', ['-I', path.join(ROOT, generator), '--page-words', 'all'], { encoding: 'utf8', cwd: ROOT, maxBuffer: 16 * 1024 * 1024 });
    if (r.status === 0 && r.stdout.trim()) {
      const all = JSON.parse(r.stdout);
      if (all[id]) { got = all[id]; from = generator; }
    }
  }
  if (!got && process.env.OA_PAGE_WORDS_A21) {
    const all = JSON.parse(fs.readFileSync(process.env.OA_PAGE_WORDS_A21, 'utf8'));
    got = all[id] || null;
    from = process.env.OA_PAGE_WORDS_A21;
  }
  if (!got) throw new Error(`no words for ${id}: ${generator} prints none (--page-words all), and OA_PAGE_WORDS_A21 names no stand-in`);
  WORDS = { ...got, __id: id, __from: from };
  return WORDS;
}

// ------------------------------------------------------------------------------------------------------------- chart
let KITMOD = null;
const RUNS = {};
async function kit() {
  if (!KITMOD) {
    const m = await import(path.join(CK, 'oa-chart.mjs'));
    KITMOD = { m, K: m.load_kit(), C: require(path.join(CK, 'checks.js')) };
  }
  return KITMOD;
}
// the chart kit's run of a spec (its rows and faults), once a build
async function run_of(id) {
  if (!RUNS[id]) {
    const { m } = await kit();
    const sp = path.join(CK, 'specs', `${id}.json`);
    const spec = JSON.parse(fs.readFileSync(sp, 'utf8'));
    RUNS[id] = { spec, res: m.run_spec(spec, { grounds: ['newsprint'], widths: [1440, 390], spec_path: sp, sweep: false, no_narrow: true }) };
  }
  return RUNS[id];
}
// the kit's drawing at px wide with its faults by the kit's own checks, and the kit's own source-line element
export async function chart_parts(id, px) {
  const { m, K, C } = await kit();
  const { spec, res } = await run_of(id);
  const d = K.draw(spec, res.rows, { width: px, ground: 'newsprint', tokens: m.TOK.newsprint, extra: m.extra_rows({ datasets: res.datasets }) });
  const faults = [...res.faults, ...C.check_drawing(spec, d, m.TOK.newsprint, `${px} px for the video frame`)];
  const vb = d.svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  // K.figure writes the source line as the guide prints it; the drawing goes in after, as web-page.mjs does
  const fig = K.figure(spec, res.rows, { id: 'vf21', svg: '<!--vf21-->', guide: true });
  const src = (fig.match(/<p class="oac-source"[^>]*>[\s\S]*?<\/p>/) || [null])[0];
  if (!src) faults.push('the chart kit wrote no source line (p.oac-source)');
  return { spec, svg: d.svg, w: vb ? +vb[1] : px, h: vb ? +vb[2] : d.height, faults, src, css: m.kit_parts().css };
}

// ------------------------------------------------------------------------------------------------------------- render
const r2 = (x) => +x.toFixed(3);

export async function render(spec) {
  const W = video_words(spec.id, spec.words_generator || GEN16);
  const views = [];
  let kit_css = '';
  const chart_faults = [], symbols = {};
  const css = `
.vf21{position:relative;box-sizing:border-box;overflow:hidden;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);font-kerning:normal;font-variant-ligatures:common-ligatures}
.vf21 p{margin:0}
.vf21-stack{position:absolute}
.vf21-stack .oac-svg{display:block;max-width:none}
.vf21 .oac-source{max-width:none}
.vf21-band{position:absolute;box-sizing:border-box;background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);text-align:center}
.vf21-band.c{left:0;right:0;margin:0 auto;width:fit-content}
.vf21-cap{font-family:var(--oa-type-body-font-family);font-weight:600;color:var(--oa-color-text-primary-on-charcoal)}
.vf21-cap .ln{display:block;white-space:nowrap}
.vf21-np{position:absolute;box-sizing:border-box;background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);font-family:var(--oa-type-body-font-family);font-weight:600}
.vf21-sign{position:absolute;display:block;color:var(--oa-color-text-primary-on-newsprint);--amp:var(--oa-color-identity-signature-on-newsprint)}
`;
  for (const v of spec.views) {
    const fw = W.frames && W.frames[v.key];
    if (!fw) throw new Error(`${spec.id}: the words print no frame ${v.key} (frames.${v.key})`);
    const row = platform(v.platform);
    const PW = row.width, PH = row.height;                 // the exported frame, px
    const k = v.scale || 2;                                // its device scale
    const w = r2(PW / k), h = r2(PH / k);                  // the layout page, CSS px
    const q = (x) => r2(x / k);                            // a ruling's px on the layout page
    // the safe area: the row's own, or the content file's for a row that has none (video.landscape), in exported px
    const srow = v.safe ? { safe_area: v.safe } : row;
    const safe = safe_boxes(srow, PW, PH).safe || [0, 0, PW, PH];
    const excl = ((srow.safe_area && srow.safe_area.exclude) || []).map((e) => [e.x, e.y, e.width, e.height]);
    const c = v.chart || {};
    const dr = await chart_parts(spec.chart, c.px || 420);
    chart_faults.push(...dr.faults.map((f) => `${v.key}: ${f}`));
    kit_css = dr.css;
    const s = v.source || {};
    const parts = [];
    // the chart and its source line in one column, so the line sits its gap under the drawing whatever the kit's height
    parts.push(`<div class="vf21-stack" data-vf21-part="stack" style="left:${q(c.x ?? safe[0])}px;top:${q(c.y ?? safe[1])}px;width:${q(s.w ?? safe[2])}px">`
      + `<div data-vf21-part="chart" style="width:${dr.w}px;height:${dr.h}px">${dr.svg}</div>`
      + `<div data-vf21-part="source" style="margin-top:${q(s.gap ?? 24)}px;width:${q(s.w ?? safe[2])}px">${dr.src || ''}</div></div>`);
    const b = v.band || {};
    const cap = fw.caption || [];
    if (cap.length > 2) throw new Error(`${spec.id} ${v.key}: ${cap.length} caption lines; Rule 16.11 allows two`);
    if (cap.length) {
      const place = b.center ? `bottom:${q(PH - b.bottom)}px;max-width:${q(b.max_w)}px` : `left:${q(b.x)}px;width:${q(b.w)}px;bottom:${q(PH - b.bottom)}px`;
      parts.push(`<div class="vf21-band oa-surface-charcoal${b.center ? ' c' : ''}" data-vf21-part="band" style="${place};padding:${q(b.pad_y ?? 16)}px ${q(b.pad_x ?? 24)}px">`
        + `<p class="vf21-cap" style="font-size:${q(b.size || 32)}px;line-height:${q(b.lh || 44)}px">${cap.map((l) => `<span class="ln">${esc(l)}</span>`).join('')}</p></div>`);
    }
    if (v.name_plate && W.name_plate) {
      const np = v.name_plate === true ? {} : v.name_plate;
      parts.push(`<p class="vf21-np" data-vf21-part="name-plate" style="left:${q(np.x ?? safe[0])}px;bottom:${q(PH - (np.bottom ?? safe[1] + safe[3]))}px;font-size:${q(np.size || 32)}px;line-height:${q(np.lh || 44)}px;padding:${q(16)}px ${q(24)}px">${esc(W.name_plate)}</p>`);
    }
    let sign = null;
    const sg = v.sign === false ? null : (v.sign || {});
    if (sg) {
      const sw = sg.w || 96, edge = sg.edge ?? 24, sh = r2(sw * L8_RATIO);
      parts.push(mark(L8, { cls: 'vf21-sign', width: q(sw), height: q(sh), label: W.signature || 'Oath & Action', red: 'signature',
        attrs: `data-vf21-part="sign" style="right:${q(edge)}px;top:${q(edge)}px"` }));
      sign = [PW - edge - sw, edge, sw, sh];
    }
    const raw = `<div class="vf21 oa-surface-newsprint" data-oa-theme="light" data-oa-application="${esc(spec.id)}" data-oa-view="${esc(v.key)}" style="width:${w}px;height:${h}px">`
      + parts.join('') + `</div>`;
    const sym = symbolize(raw);
    Object.assign(symbols, sym.symbols);
    // the overlay, on the layout page: the safe area's outline (2 px dashed at the exported size), each excluded box
    // hatched, each inset's figure in exported px, and the basis the page words name
    const L = W.safe_labels || {};
    // the chips' words at overlay_label exported px (DD12b-Q3: a plate that opens with its overlay shown keeps them at 13 px
    // or more at its scale, so 16.11's frame, placed at half its layout page, sets them at 52 exported px, 26 on the page)
    const ls = q(v.overlay_label || 28);
    const chip_w = (t) => Math.round(t.length * ls * 0.68 + ls * 0.8);
    const chip_h = r2(ls * 1.6);
    const [sx, sy, sw_, sh_] = safe.map(q);
    const basis = L[v.basis_key || (v.platform === 'video.vertical' ? 'vertical' : 'landscape')] || (v.safe_basis !== 'studio' ? L.safe : null) || null;
    const ins = srow.safe_area || {};
    const fig = (n) => `${n} px`;
    // the figures' row in the top inset: the sides' figure at the left, the top's centered
    const row1 = r2(Math.max(q(2), sy / 2 - chip_h / 2));
    const layers = [{ x: sx, y: sy, w: sw_, h: sh_, kind: 'edge', sw: q(2), ls }];
    if (ins.left) layers.push({ x: 0, y: 0, w: 0, h: 0, kind: 'label', ls, label: fig(ins.left), lx: q(8), ly: row1 });
    if (ins.right && ins.right !== ins.left) layers.push({ x: 0, y: 0, w: 0, h: 0, kind: 'label', ls, label: fig(ins.right), lx: r2(w - q(8) - chip_w(fig(ins.right))), ly: row1 });
    if (ins.top) layers.push({ x: 0, y: 0, w: 0, h: 0, kind: 'label', ls, label: fig(ins.top), lx: r2(w / 2 - chip_w(fig(ins.top)) / 2), ly: row1 });
    if (ins.bottom) layers.push({ x: 0, y: 0, w: 0, h: 0, kind: 'label', ls, label: fig(ins.bottom), lx: r2(w / 2 - chip_w(fig(ins.bottom)) / 2), ly: r2(h - q(8) - chip_h) });
    // the basis: in the bottom inset, a chip a line, under any excluded box's name, where the inset has room; else on the
    // figures' row after the sides' figure
    if (basis) {
      const per = Math.max(8, Math.floor((w - 2 * q(16)) / (ls * 0.68)) - 2);
      const lines = [];
      for (const word of basis.split(' ')) { const last = lines[lines.length - 1]; if (last && (last + ' ' + word).length <= per) lines[lines.length - 1] = last + ' ' + word; else lines.push(word); }
      const below = Math.max(sy + sh_, ...excl.map((e) => q(e[1] + e[3]) + q(8) + chip_h)) + q(16);
      if (h - below - q(16) - chip_h >= lines.length * (chip_h + q(8))) {
        lines.forEach((t, i) => layers.push({ x: 0, y: 0, w: 0, h: 0, kind: 'label', ls, label: t, lx: q(8), ly: r2(below + i * (chip_h + q(8))) }));
      } else {
        layers.push({ x: 0, y: 0, w: 0, h: 0, kind: 'label', ls, label: basis, lx: r2(q(8) + (ins.left ? chip_w(fig(ins.left)) + q(16) : 0)), ly: row1 });
      }
    }
    for (const e of excl) {
      const [ex, ey, ew, eh] = e.map(q);
      const what = ew >= w * 0.9 ? (L.controls || null) : (L.buttons || null);
      layers.push({ x: ex, y: ey, w: ew, h: eh, kind: 'hatch-in', sw: q(2), ls, label: what,
        lx: what ? r2(Math.max(q(8), Math.min(w - chip_w(what) - q(8), ex + ew - chip_w(what)))) : null, ly: what ? r2(ey + (ew >= w * 0.9 ? q(8) : eh + q(8))) : null });
    }
    views.push({ key: v.key, w, h, px: [PW, PH], scale: k, theme: 'light', platform: row.id, moment: fw.time || v.moment || null,
      html: sym.html, raw, alt: fw.alt, layers, live: safe, exclude: excl, sign, floor_px: v.floor_px || null, chart_px: dr.w, chart_h: dr.h,
      export_name: v.export_name, overlay_name: v.overlay_name || null, caption: cap, safe_basis: v.safe_basis || 'platform',
      source_gap: q(s.gap ?? 24), min_gap_band: v.min_gap_band ?? 16 });
  }
  const gen = spec.words_generator || GEN16;
  const from_gen = WORDS.__from === gen;
  const { spec: cs } = await run_of(spec.chart);
  return {
    id: spec.id, type, css, kit_css, views, symbols, chart_faults, source: W.source, chart_source: cs.source_line,
    switch_words: W.switch || 'Show the safe areas', words_from: WORDS.__from,
    ...(from_gen ? { words_records: [{ generator: gen, id: spec.id }] } : {}),
    plate: { head: spec.plate_head, line: spec.plate_line },
  };
}

// ------------------------------------------------------------------------------------------------------------- build
// Called by oa-app.mjs (R.build) for each content file of this type: per view, the export page, its facts and checks, the
// PNG at the row's pixels and the PNG with the safe areas drawn on, and the guide's frame; then the kit's plate.
// What a frame tells the checks, in the page: every word with its whole text, boxes, size and inks, and each part's box
function frame_facts() {
  const out = { words: [], parts: {} };
  const bg = (el) => { for (let e = el; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor; if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') return c; } return 'rgb(255, 255, 255)'; };
  const root = document.querySelector('.vf21');
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const t = n.textContent.replace(/\s+/g, ' ').trim();
    if (!t) continue;
    const el = n.parentElement;
    if (el.closest('title, desc, defs, style, script')) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const rects = [...r.getClientRects()].filter((x) => x.width > 0.5 && x.height > 0.5).map((x) => [x.left, x.top, x.width, x.height]);
    if (!rects.length) continue;
    const svg = el.closest('svg');
    let size = parseFloat(cs.fontSize);
    if (svg && svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width) size *= svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
    const part = el.closest('[data-vf21-part]');
    out.words.push({ text: t, size: +size.toFixed(2), color: svg ? cs.fill : cs.color, bg: bg(el), svg: !!svg, tick: !!el.closest('.oac-t-tick') || /\boac-t-tick\b/.test(el.getAttribute('class') || ''),
      part: part ? part.getAttribute('data-vf21-part') : null, rects });
  }
  root.querySelectorAll('[data-vf21-part]').forEach((e) => {
    const b = e.getBoundingClientRect();
    out.parts[e.getAttribute('data-vf21-part')] = [b.left, b.top, b.width, b.height];
  });
  // the chart's ink: the drawing's own box of marks and words, inside its svg
  const svg = root.querySelector('[data-vf21-part="chart"] svg');
  if (svg) { const sb = svg.getBoundingClientRect(); let y1 = -1; svg.querySelectorAll('text, circle, rect, line, path, polyline').forEach((x) => { const b = x.getBoundingClientRect(); if (b.height || b.width) y1 = Math.max(y1, b.bottom); }); out.chart_ink_bottom = y1; out.chart_box = [sb.left, sb.top, sb.width, sb.height]; }
  return out;
}

const norm = (s) => String(s || '').normalize('NFKC').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/−/g, '-')
  .replace(/[  ]/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase();
const lum = (c) => { const m = String(c).match(/[\d.]+/g); if (!m) return null; return m.slice(0, 3).map((x) => +x / 255).map((x) => (x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4)).reduce((a, x, i) => a + x * [0.2126, 0.7152, 0.0722][i], 0); };
const ratio = (a, b) => { const x = lum(a), y = lum(b); if (x == null || y == null) return null; return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
const inside = (r, b, tol = 0.75) => r[0] >= b[0] - tol && r[1] >= b[1] - tol && r[0] + r[2] <= b[0] + b[2] + tol && r[1] + r[3] <= b[1] + b[3] + tol;
const hits = (a, b, tol = 0.5) => a[0] < b[0] + b[2] - tol && b[0] < a[0] + a[2] - tol && a[1] < b[1] + b[3] - tol && b[1] < a[1] + a[3] - tol;

// every word the frame shows must be in its alt (D4-211, D4-299); axis numbers between the first and last tick count as
// carried when the alt gives both ends of the scale
const pct = (s) => s.replace(/(\d)\s*%/g, '$1 percent');
// a word is carried when the alt holds it whole: "50" is not carried by "2050", nor "4.7" by "47.7"
const carried = (A, t) => { const x = pct(norm(t)); const e = x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(^|[^\\w.])${e}(?![\\w]|\\.\\d)`).test(A) || (/^\W|\W$/.test(x) && A.includes(x)); };
export function alt_misses(words, alt) {
  const A = pct(norm(alt));
  const ticks = words.filter((x) => x.tick).map((x) => x.text);
  const ends = ticks.length >= 2 && carried(A, ticks[0]) && carried(A, ticks[ticks.length - 1]);
  const miss = [];
  for (const x of words) {
    if (x.tick && ends) continue;
    if (!carried(A, x.text)) miss.push(x.text);
  }
  return [...new Set(miss)];
}

export async function build({ r, spec, o, browser, dir, facts, manifest, stem, fonts, tokens }) {
  const L = await import('../lib.mjs');
  const faults = [...r.chart_faults];
  if (norm(r.source) !== norm(r.chart_source)) faults.push(`the words' source line is not ${spec.chart}.json's source_line (Rule 16.10: the source line as the chart's spec carries it)`);
  const sprite = L.identity_sprite(r.symbols);
  const views = [], frames = [];
  facts.views = facts.views || [];
  for (const v of r.views) {
    const vf = [];
    const W = Math.round(v.w), H = Math.round(v.h);
    if (Math.abs(W - v.w) > 1e-6 || Math.abs(H - v.h) > 1e-6) vf.push(`the layout page ${v.w} by ${v.h} px is not whole pixels at scale ${v.scale}`);
    const head = (extra = '') => `<!doctype html>
<html lang="en" data-oa-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(`${spec.id} ${v.key}`)}</title>
<style>${fonts}</style>
<style>${tokens}</style>
<style>${r.kit_css}</style>
<style>html,body{margin:0;padding:0}body{background:var(--oa-color-surface-newsprint)}.oa-app-art{position:relative;overflow:hidden;width:${W}px;height:${H}px}
${r.css}${extra}</style>
</head>
`;
    const pf = path.join(dir, `export-${v.key}.html`);
    fs.writeFileSync(pf, head() + `<body>${sprite}<div class="oa-app-art">${v.html}</div></body>\n</html>\n`);
    const p = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: v.scale });
    await p.goto('file://' + pf, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    let f = await p.evaluate(frame_facts);
    // DD12b-R1: the source line sits its gap under the chart's last ink, not under the drawing's box, which the kit pads;
    // the margin is set from the ink measured here, the page written again and measured again
    if (f.chart_ink_bottom > 0 && f.parts.source) {
      const want = +(f.chart_ink_bottom + v.source_gap).toFixed(3), now = f.parts.source[1];
      if (Math.abs(want - now) > 0.01) {
        const re = /(data-vf21-part="source" style="margin-top:)(-?[\d.]+)(px)/;
        const m0 = +v.html.match(re)[2];
        const fix = (h) => h.replace(re, `$1${+(m0 + want - now).toFixed(3)}$3`);
        v.html = fix(v.html); v.raw = fix(v.raw);
        fs.writeFileSync(pf, head() + `<body>${sprite}<div class="oa-app-art">${v.html}</div></body>\n</html>\n`);
        await p.goto('file://' + pf, { waitUntil: 'load' });
        await p.evaluate(() => document.fonts.ready);
        f = await p.evaluate(frame_facts);
      }
    }
    const X = (b) => b.map((x) => +(x * v.scale).toFixed(2));          // layout px to the exported frame's px
    const live = v.live;
    const words = f.words.map((x) => ({ ...x, rects: x.rects.map(X) }));
    const parts = Object.fromEntries(Object.entries(f.parts).map(([k, b]) => [k, X(b)]));
    // the checks: every word inside the live box and clear of every excluded box (L8 is Rule 12.3's, outside it); the parts
    // clear of each other; each HTML word 4.5 to 1 or more on its ground; the floor, where the view names one; the alt
    for (const x of words) {
      if (x.part === 'sign') continue;
      for (const rr of x.rects) {
        if (!inside(rr, live)) { vf.push(`"${x.text.slice(0, 40)}" leaves the safe area at [${rr.map(Math.round)}]`); break; }
        if (v.exclude.some((e) => hits(rr, e))) { vf.push(`"${x.text.slice(0, 40)}" sits in an excluded box at [${rr.map(Math.round)}]`); break; }
      }
      if (v.floor_px && x.size * v.scale < v.floor_px - 0.01) vf.push(`"${x.text.slice(0, 40)}" at ${x.size * v.scale} px, under the ${v.floor_px} px floor`);
      if (!x.svg) { const cr = ratio(x.color, x.bg); if (cr !== null && cr < 4.5) vf.push(`"${x.text.slice(0, 40)}" at ${cr.toFixed(2)} to 1`); }
    }
    const pnames = ['chart', 'source', 'band', 'name-plate'].filter((k) => parts[k]);
    for (let i = 0; i < pnames.length; i++) for (let j = i + 1; j < pnames.length; j++) {
      if (hits(parts[pnames[i]], parts[pnames[j]])) vf.push(`the ${pnames[i]} and the ${pnames[j]} overlap`);
    }
    for (const k of pnames) {
      if (k !== 'chart' && !inside(parts[k], live)) vf.push(`the ${k} leaves the safe area`);
      if (v.exclude.some((e) => hits(parts[k], e))) vf.push(`the ${k} meets an excluded box`);
    }
    const am = alt_misses(words, v.alt);
    if (am.length) vf.push(`the alt lacks ${am.length} of the frame's words: ${am.slice(0, 8).map((x) => `"${x.slice(0, 50)}"`).join(', ')}`);
    if (!v.alt || norm(v.alt).length < 15) vf.push('no alt of 15 characters or more');
    const src_words = words.filter((x) => x.part === 'source');
    const src_end = src_words.length ? Math.max(...src_words.flatMap((x) => x.rects.map((rr) => rr[1] + rr[3]))) : null;
    if (parts.band && src_end != null && parts.band[1] - src_end < v.min_gap_band - 0.01) vf.push(`the source line ends ${(parts.band[1] - src_end).toFixed(1)} px above the caption band, under ${v.min_gap_band}`);
    const rec = { key: v.key, platform: v.platform, layout: [W, H], scale: v.scale, px: v.px, live, exclude: v.exclude, parts,
      chart_ink_bottom: f.chart_ink_bottom != null ? +(f.chart_ink_bottom * v.scale).toFixed(2) : null, source_end: src_end,
      source_lines: src_words.length ? new Set(src_words.flatMap((x) => x.rects.map((rr) => Math.round(rr[1])))).size : 0,
      gap_source_band: parts.band && src_end != null ? +(parts.band[1] - src_end).toFixed(2) : null,
      sizes: [...new Set(words.map((x) => +(x.size * v.scale).toFixed(2)))].sort((a, b) => a - b), words: words.length, faults: vf };
    // the exports: the frame at the row's pixels, and the same with the safe areas drawn on
    if (o.export && v.export_name) {
      const file = stem(v.export_name) + '.png';
      await p.screenshot({ path: path.join(o.exports, file), clip: { x: 0, y: 0, width: W, height: H } });
      manifest.files.push({ file, spec: spec.id, platform: v.platform, format: 'png', theme: 'light', size: `${v.px[0].toLocaleString('en-US')} by ${v.px[1].toLocaleString('en-US')} px`,
        view: v.key, device_scale: v.scale, ...(v.safe_basis === 'studio' ? { safe_basis: 'studio' } : {}) });
      rec.png = file;
      if (v.overlay_name) {
        await p.addStyleTag({ content: L.PLATE_CSS + '.oa-app-safe{display:inline}' });
        await p.evaluate(({ svg }) => { document.querySelector('.oa-app-art').insertAdjacentHTML('beforeend', svg); }, { svg: `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" style="position:absolute;left:0;top:0" aria-hidden="true">${L.overlay(W, H, v.layers)}</svg>` });
        const of = stem(v.overlay_name) + '.png';
        await p.screenshot({ path: path.join(o.exports, of), clip: { x: 0, y: 0, width: W, height: H } });
        manifest.files.push({ file: of, spec: spec.id, platform: v.platform, format: 'png', theme: 'light', size: `${v.px[0].toLocaleString('en-US')} by ${v.px[1].toLocaleString('en-US')} px`,
          view: v.key, device_scale: v.scale, overlay: 'safe areas', ...(v.safe_basis === 'studio' ? { safe_basis: 'studio' } : {}) });
        rec.overlay_png = of;
      }
    }
    await p.close();
    facts.views.push(rec);
    faults.push(...vf.map((x) => `${v.key}: ${x}`));
    // the guide build gives every id in a specimen its specimen's prefix and rewrites url(#...) in the fragment, but not the
    // plate style's .hatch rule in the head, so a hatched box names its pattern inline (an inline style beats that rule)
    const fr = L.frame({ w: W, h: H, html: v.html, alt: v.alt, layers: v.layers, page: { id: spec.id, key: v.key, type: spec.type } })
      .replace(/<rect class="hatch" /g, '<rect class="hatch" style="fill:url(#oa-app-hatch)" ');
    frames.push(fr);
    views.push({ key: v.key, w: W, h: H, theme: 'light', alt: v.alt, html: fr });
    console.log(`  ${spec.id} ${v.key}: ${W} by ${H} px at ${v.scale} (${v.px.join(' by ')}), source line ends ${src_end} px over ${rec.source_lines} lines, band at ${parts.band ? Math.round(parts.band[1]) : '-'}; ${vf.length} fault(s)`);
  }
  facts.faults = faults;
  return {
    faults, kit_css: r.kit_css, sprite,
    plates: [{ id: spec.id, html: L.plate({ id: spec.id.toLowerCase(), head: r.plate.head || spec.id, line: r.plate.line, css: r.css, frames, switch_words: r.switch_words }) }],
    guide: { type: spec.type, css: r.css, views, words_from: r.words_from, symbols: r.symbols, switch_words: r.switch_words,
      ...(r.words_records ? { words_records: r.words_records } : {}) },
  };
}
