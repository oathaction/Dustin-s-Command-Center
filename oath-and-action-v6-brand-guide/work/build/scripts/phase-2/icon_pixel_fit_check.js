#!/usr/bin/env node
// Pixel-fit check for icons drawn to sit on the pixel grid (stage B, November 9, 2026).
//
// Usage:
//   node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 24 a.svg [b.svg ...] [folder/]
//   node work/build/scripts/phase-2/icon_pixel_fit_check.js --size 16,24 --weight 1.5,2 --json out.json --png outdir/ a.svg
//   node work/build/scripts/phase-2/icon_pixel_fit_check.js --self-test
// A bare number also sets the size ("24 a.svg"). A folder stands for the .svg files directly inside it.
// `python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py ...` runs this same file with the same arguments.
//
// What it does. Chromium (Playwright) draws each SVG with its box set to the target size, at 1x (one device pixel per
// CSS pixel) and at 2x (two), on a clear canvas, so ink is the alpha channel and every colour counts the same. It also
// draws a supersampled copy (at least 640 px across) to measure the geometry. For each size and scale it reports:
//   1. Stroke widths in device px: the widths the SVG declares (stroke-width times the drawing's scale), and the widths
//      measured from the ink, which also covers outlined and filled drawings. "Thinnest" is the thinnest width that
//      covers at least a quarter of a device pixel of ink; "main" is the most common width.
//   2. Soft edges: the share of ink pixels (alpha 8 to 255) with partial coverage (alpha 8 to 246).
//   3. Straight strokes on whole pixels: every horizontal or vertical edge at least 1.5 px long, its position read to
//      a hundredth of a pixel from the supersampled coverage, and whether it lands within 0.1 px of a pixel edge.
//      Edges pair into strokes. A stroke of whole-pixel width must have both edges on pixel edges; a stroke of
//      fractional width (1.5 px at 16 px) must have one. An edge with no partner must sit on a pixel edge.
//   4. Gaps: the smallest gap between separate ink parts, and whether the enclosed spaces (counters) of half a pixel
//      or more stay as drawn at that scale: none fills in, and no narrow opening closes into a new one.
// Pass or fail, per scale (the thresholds are RULES below, and the notes explain them):
//   width    thinnest stroke at least 1.0 device px            soft     soft-edge share at most 95 percent
//   straight every straight stroke fit as in 3                 gap      smallest gap at least 1.0 device px
//   counters the same enclosed spaces as the drawing: none fills in, and no opening closes into a new one
//   weight   (only with --weight) the main width within 0.15 px of the grid's line
// A file passes at a size when it passes at 1x and at 2x. Exit 0 when every file passes, 1 when any fails, 2 on misuse.
// The check assumes the icon's box sits on whole CSS pixels in the page, as the guide places it.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const RULES = {
  minStroke: 1.0,        // device px: a line under one device pixel never reaches full ink
  minThinArea: 0.25,     // device px²: a width counts as the thinnest only if it covers this much ink
  maxSoftShare: 0.95,    // share of ink pixels with partial coverage: above it, under one ink pixel in 20 is full ink
  inkAlpha: 8,           // alpha at or above this is ink (about 3 percent)
  fullAlpha: 247,        // alpha at or above this is full ink (about 97 percent)
  edgeTolerance: 0.10,   // device px: an edge this close to a pixel edge leaves a fringe of 10 percent or less
  minStraight: 1.5,      // device px at 1x: shorter flat runs are not counted as straight edges
  straightness: 0.01,    // device px: an edge whose position wanders more than this is a curve
  minGap: 1.0,           // device px between separate ink parts
  minCounterArea: 0.5,   // device px²: smaller enclosed spaces are not counted as counters
  weightTolerance: 0.15, // device px, for --weight
};

// ---------- arguments ----------
function usage(msg) {
  if (msg) console.error('icon_pixel_fit_check: ' + msg);
  console.error('Usage: node icon_pixel_fit_check.js --size 24[,16] [--weight 2[,1.5]] [--json out.json] [--png dir] [--quiet] file.svg|folder ...\n       node icon_pixel_fit_check.js --self-test');
  process.exit(2);
}
function parseArgs(argv) {
  const o = { sizes: [], weights: [], files: [], json: null, png: null, quiet: false, selfTest: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const val = () => { if (i + 1 >= argv.length) usage(a + ' needs a value'); return argv[++i]; };
    if (a === '--size' || a === '-s') o.sizes.push(...val().split(',').map(Number));
    else if (a.startsWith('--size=')) o.sizes.push(...a.slice(7).split(',').map(Number));
    else if (a === '--weight') o.weights.push(...val().split(',').map(Number));
    else if (a === '--json') o.json = val();
    else if (a === '--png') o.png = val();
    else if (a === '--quiet' || a === '-q') o.quiet = true;
    else if (a === '--self-test') o.selfTest = true;
    else if (a === '--help' || a === '-h') usage();
    else if (/^\d+(\.\d+)?$/.test(a) && !fs.existsSync(a)) o.sizes.push(Number(a));
    else if (a.startsWith('-')) usage('unknown option ' + a);
    else o.files.push(a);
  }
  if (o.sizes.some((s) => !(s >= 4 && s <= 512))) usage('size must be a number of px from 4 to 512');
  if (o.weights.length && o.weights.length !== o.sizes.length) usage('give one --weight per --size, in the same order');
  return o;
}
function expandFiles(list) {
  const out = [];
  for (const f of list) {
    if (!fs.existsSync(f)) usage('no such file ' + f);
    if (fs.statSync(f).isDirectory()) {
      const inside = fs.readdirSync(f).filter((n) => n.toLowerCase().endsWith('.svg')).sort().map((n) => path.join(f, n));
      if (!inside.length) usage('no .svg files in ' + f);
      out.push(...inside);
    } else out.push(f);
  }
  return out;
}

// ---------- SVG sizing ----------
// Sets the root <svg> to D x D px, keeping its viewBox (adding one from width and height when it has none).
function sized(svgText, D) {
  const s = svgText.replace(/<\?xml[^>]*>\s*/, '').replace(/<!DOCTYPE[^>]*>\s*/i, '');
  const m = s.match(/<svg\b[^>]*>/);
  if (!m) throw new Error('no <svg> element');
  let tag = m[0];
  const num = (name) => { const r = tag.match(new RegExp('\\s' + name + '="\\s*([\\d.]+)(px)?\\s*"')); return r ? Number(r[1]) : null; };
  const vbm = tag.match(/\sviewBox="([^"]+)"/);
  let vb = vbm ? vbm[1].trim().split(/[\s,]+/).map(Number) : null;
  if (!vb) {
    const w = num('width'), h = num('height');
    if (!(w > 0 && h > 0)) throw new Error('the root <svg> has neither a viewBox nor a width and height');
    vb = [0, 0, w, h];
    tag = tag.replace(/<svg\b/, `<svg viewBox="0 0 ${w} ${h}"`);
  }
  tag = tag.replace(/\s(width|height)="[^"]*"/g, '').replace(/<svg\b/, `<svg width="${D}" height="${D}"`);
  return { text: s.replace(m[0], tag), viewBox: vb };
}

// ---------- image analysis (all in Node, on alpha arrays) ----------
// Squared Euclidean distance transform (Felzenszwalb and Huttenlocher). f: 0 at sources, Infinity elsewhere.
function edt2(f, W, H) {
  const n = Math.max(W, H);
  const d = new Float64Array(n), v = new Int32Array(n), z = new Float64Array(n + 1), g = new Float64Array(n);
  const pass = (get, set, len) => {
    for (let q = 0; q < len; q++) g[q] = get(q);
    let k = 0; v[0] = 0; z[0] = -Infinity; z[1] = Infinity;
    for (let q = 1; q < len; q++) {
      if (g[q] === Infinity) continue;
      if (g[v[k]] === Infinity) { v[k] = q; z[k] = -Infinity; z[k + 1] = Infinity; continue; }
      let s = ((g[q] + q * q) - (g[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
      while (s <= z[k]) { k--; if (k < 0) break; s = ((g[q] + q * q) - (g[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]); }
      k++; v[k] = q; z[k] = s; z[k + 1] = Infinity;
    }
    if (g[v[0]] === Infinity) { for (let q = 0; q < len; q++) set(q, Infinity); return; }
    k = 0;
    for (let q = 0; q < len; q++) { while (z[k + 1] < q) k++; set(q, (q - v[k]) * (q - v[k]) + g[v[k]]); }
  };
  const out = Float64Array.from(f);
  const put = (q, val) => { d[q] = val; };
  for (let x = 0; x < W; x++) { pass((q) => out[q * W + x], put, H); for (let q = 0; q < H; q++) out[q * W + x] = d[q]; }
  for (let y = 0; y < H; y++) { pass((q) => out[y * W + q], put, W); for (let q = 0; q < W; q++) out[y * W + q] = d[q]; }
  return out;
}

function labels(mask, W, H, want, conn8) {
  const lab = new Int32Array(W * H).fill(-1); const comps = []; const stack = new Int32Array(W * H);
  for (let i = 0; i < W * H; i++) {
    if (mask[i] !== want || lab[i] >= 0) continue;
    const id = comps.length; let sp = 0; stack[sp++] = i; lab[i] = id;
    let area = 0, border = false, x0 = W, y0 = H, x1 = -1, y1 = -1;
    while (sp) {
      const p = stack[--sp]; area++;
      const x = p % W, y = (p - x) / W;
      if (x === 0 || y === 0 || x === W - 1 || y === H - 1) border = true;
      if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue; if (!conn8 && dx && dy) continue;
        const xx = x + dx, yy = y + dy; if (xx < 0 || yy < 0 || xx >= W || yy >= H) continue;
        const q = yy * W + xx; if (mask[q] === want && lab[q] < 0) { lab[q] = id; stack[sp++] = q; }
      }
    }
    comps.push({ id, area, border, x0, y0, x1, y1 });
  }
  return { lab, comps };
}

// Width at every ink pixel of the supersampled mask, in supersampled px.
function thicknessMap(mask, W, H) {
  const N = W * H;
  const f = new Float64Array(N); for (let i = 0; i < N; i++) f[i] = mask[i] ? Infinity : 0;
  const dt2 = edt2(f, W, H);
  // Local thickness: each ridge pixel paints its inscribed ball with the ball's diameter.
  const lt = new Float32Array(N);
  const dt = new Float32Array(N); for (let i = 0; i < N; i++) dt[i] = mask[i] ? Math.sqrt(dt2[i]) : 0;
  const ridges = [];
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    const i = y * W + x; if (!mask[i]) continue; const v = dt[i]; let ok = true;
    for (let dy = -1; dy <= 1 && ok; dy++) for (let dx = -1; dx <= 1; dx++) if ((dx || dy) && dt[i + dy * W + dx] > v) { ok = false; break; }
    if (ok) ridges.push(i);
  }
  for (const i of ridges) {
    const r = dt[i], r2 = dt2[i], dia = 2 * r - 0.5, R = Math.floor(r);
    const cx = i % W, cy = (i - cx) / W;
    for (let dy = -R; dy <= R; dy++) {
      const yy = cy + dy; if (yy < 0 || yy >= H) continue;
      const span = Math.floor(Math.sqrt(Math.max(0, r2 - dy * dy - 1e-9)));
      for (let dx = -span; dx <= span; dx++) {
        const xx = cx + dx; if (xx < 0 || xx >= W) continue;
        const q = yy * W + xx; if (mask[q] && lt[q] < dia) lt[q] = dia;
      }
    }
  }
  // Pixels no ridge ball reaches (the tips of square corners, stair steps on a curve) take the width of the nearest
  // pixel that one does, so a square corner never reads as a thin stroke.
  const queue = new Int32Array(N); let qh = 0, qt = 0;
  for (let i = 0; i < N; i++) if (mask[i] && lt[i] > 0) queue[qt++] = i;
  while (qh < qt) {
    const p = queue[qh++]; const x = p % W, y = (p - x) / W;
    for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
      const xx = x + dx, yy = y + dy; if ((!dx && !dy) || xx < 0 || yy < 0 || xx >= W || yy >= H) continue;
      const q = yy * W + xx; if (mask[q] && lt[q] === 0) { lt[q] = lt[p]; queue[qt++] = q; }
    }
  }
  const th = lt;
  return th;
}

function strokeWidths(mask, W, H, k) {
  const th = thicknessMap(mask, W, H);
  const idx = []; for (let i = 0; i < W * H; i++) if (mask[i]) idx.push(i);
  if (!idx.length) return null;
  idx.sort((a, b) => th[a] - th[b]);
  const vals = idx.map((i) => th[i] / k);
  const need = Math.max(1, Math.round(RULES.minThinArea * k * k));
  const at = Math.min(vals.length - 1, need - 1);
  const thinnest = vals[at];
  let sx = 0, sy = 0; for (let j = 0; j <= at; j++) { sx += idx[j] % W; sy += Math.floor(idx[j] / W); }
  const thinAt = [(sx / (at + 1) + 0.5) / k, (sy / (at + 1) + 0.5) / k];
  const bins = new Map(); for (const v of vals) { const b = Math.round(v / 0.05); bins.set(b, (bins.get(b) || 0) + 1); }
  let mode = 0, best = -1; for (const [b, c] of bins) if (c > best) { best = c; mode = b * 0.05; }
  return { thinnest, thinAt, main: mode, median: vals[vals.length >> 1], widest: vals[vals.length - 1] };
}

// Horizontal and vertical straight edges, positions in device px at 1x.
function straightEdges(alpha, mask, W, H, k) {
  const a = (x, y) => alpha[y * W + x] / 255;
  const edges = [];
  const minLen = RULES.minStraight * k, tol = RULES.straightness * k;
  for (const orient of ['h', 'v']) {
    const along = orient === 'h' ? W : H, across = orient === 'h' ? H : W;
    const M = orient === 'h' ? (u, b) => mask[b * W + u] : (u, b) => mask[u * W + b];
    const A = orient === 'h' ? (u, b) => a(u, b) : (u, b) => a(b, u);
    for (let b = 1; b < across; b++) {
      let u = 0;
      while (u < along) {
        const t = M(u, b - 1) - M(u, b);
        if (!t) { u++; continue; }
        let u1 = u; while (u1 < along && M(u1, b - 1) - M(u1, b) === t) u1++;
        if (u1 - u >= minLen) {
          // ink before the boundary (t = 1): pos = (b-1) + a(b-1) + a(b); ink after (t = -1): pos = b + 1 - a(b-1) - a(b)
          const pos = []; for (let q = u; q < u1; q++) pos.push(t === 1 ? (b - 1) + A(q, b - 1) + A(q, b) : b + 1 - A(q, b - 1) - A(q, b));
          let s = 0;
          while (s < pos.length) {
            let e = s + 1, sum = pos[s];
            while (e < pos.length && Math.abs(pos[e] - sum / (e - s)) <= tol) { sum += pos[e]; e++; }
            if (e - s >= minLen) edges.push({ orient, inkBefore: t === 1, pos: sum / (e - s) / k, from: (u + s) / k, to: (u + e) / k, b, u0: u + s, u1: u + e });
            s = e;
          }
        }
        u = u1;
      }
    }
  }
  // Pair a leading edge with the nearest trailing edge across ink to make a stroke.
  for (const e of edges) e.partner = null;
  for (const lead of edges.filter((e) => !e.inkBefore)) {
    let best = null;
    for (const tr of edges) {
      if (tr.orient !== lead.orient || !tr.inkBefore || tr.pos <= lead.pos) continue;
      const lo = Math.max(lead.from, tr.from), hi = Math.min(lead.to, tr.to);
      if (hi - lo < 0.5 * Math.min(lead.to - lead.from, tr.to - tr.from)) continue;
      const mid = Math.round(((lo + hi) / 2) * k);
      let solid = true;
      for (let q = lead.b; q < tr.b && solid; q++) { const i = lead.orient === 'h' ? q * W + mid : mid * W + q; if (!mask[i]) solid = false; }
      if (solid && (!best || tr.pos < best.pos)) best = tr;
    }
    if (best && !best.partner) { lead.partner = best; best.partner = lead; }
  }
  return edges;
}

function judgeEdges(edges, scale) {
  const tol = RULES.edgeTolerance;
  const on = (p) => Math.abs(p * scale - Math.round(p * scale)) <= tol;
  const items = [];
  const done = new Set();
  for (const e of edges) {
    if (done.has(e)) continue;
    if (e.partner) {
      const lead = e.inkBefore ? e.partner : e, tr = e.inkBefore ? e : e.partner;
      done.add(lead); done.add(tr);
      const w = (tr.pos - lead.pos) * scale;
      const whole = Math.abs(w - Math.round(w)) <= tol;
      const n = (on(lead.pos) ? 1 : 0) + (on(tr.pos) ? 1 : 0);
      const ok = whole ? n === 2 : n >= 1;
      items.push({ kind: 'stroke', orient: e.orient, width: w, edges: [lead.pos * scale, tr.pos * scale], from: Math.max(lead.from, tr.from) * scale, to: Math.min(lead.to, tr.to) * scale, ok, need: whole ? 'both edges' : 'one edge' });
    } else {
      done.add(e);
      items.push({ kind: 'edge', orient: e.orient, edges: [e.pos * scale], from: e.from * scale, to: e.to * scale, ok: on(e.pos), need: 'on a pixel edge' });
    }
  }
  return items;
}

function gaps(mask, W, H, k) {
  const { lab, comps } = labels(mask, W, H, 1, true);
  const parts = comps.filter((c) => c.area >= Math.max(4, 0.02 * k * k));
  if (parts.length < 2) return { parts: parts.length, smallest: null };
  let best = null;
  const list = parts.slice(0, 80);
  for (let ai = 0; ai < list.length - 1; ai++) {
    const A = list[ai];
    const f = new Float64Array(W * H); for (let i = 0; i < W * H; i++) f[i] = lab[i] === A.id ? 0 : Infinity;
    const d2 = edt2(f, W, H);
    for (let bi = ai + 1; bi < list.length; bi++) {
      const B = list[bi];
      for (let y = B.y0; y <= B.y1; y++) for (let x = B.x0; x <= B.x1; x++) {
        const i = y * W + x; if (lab[i] !== B.id) continue;
        if (!best || d2[i] < best.d2) best = { d2: d2[i], at: [x, y], a: ai + 1, b: bi + 1 };
      }
    }
  }
  return { parts: parts.length, smallest: { gap: (Math.sqrt(best.d2) - 1) / k, near: [best.at[0] / k, best.at[1] / k], between: [best.a, best.b] } };
}

function counters(mask, W, H, minArea) {
  const { comps } = labels(mask, W, H, 0, false);
  return comps.filter((c) => !c.border && c.area >= minArea).length;
}

function soft(alpha) {
  let ink = 0, part = 0;
  for (const v of alpha) { if (v >= RULES.inkAlpha) { ink++; if (v < RULES.fullAlpha) part++; } }
  return { ink, partial: part, share: ink ? part / ink : 0 };
}

// ---------- rendering ----------
const PAGE_JS = `
window.b64 = (u8) => { let s = ''; for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000)); return btoa(s); };
window.decode = async (png) => {
  const img = new Image(); img.src = 'data:image/png;base64,' + png; await img.decode();
  const W = img.naturalWidth, H = img.naturalHeight;
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, W, H).data; const a = new Uint8Array(W * H);
  for (let i = 0; i < W * H; i++) a[i] = d[4 * i + 3];
  return [W, b64(a)];
};
window.place = (svg) => { document.getElementById('host').innerHTML = svg; };
window.nominal = (svg) => {
  const host = document.getElementById('host'); host.innerHTML = svg;
  const out = [];
  for (const el of host.querySelectorAll('path,line,polyline,polygon,rect,circle,ellipse')) {
    const cs = getComputedStyle(el);
    if (cs.stroke === 'none' || cs.display === 'none' || cs.visibility === 'hidden' || Number(cs.strokeOpacity) === 0) continue;
    const sw = parseFloat(cs.strokeWidth); if (!(sw > 0)) continue;
    const m = el.getScreenCTM(); const sc = cs.vectorEffect === 'non-scaling-stroke' ? 1 : Math.sqrt(Math.abs(m.a * m.d - m.b * m.c));
    out.push(Math.round(sw * sc * 1000) / 1000);
  }
  host.innerHTML = '';
  return out;
};
window.preview = (a1, a2, S, marks1, marks2) => {
  const Z1 = Math.max(8, Math.round(384 / S)), Z2 = Z1 / 2, gap = 24, W = S * Z1 * 2 + gap * 3, H = S * Z1 + gap * 2 + 18;
  const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
  g.fillStyle = '#fff'; g.fillRect(0, 0, W, H);
  const draw = (b, D, Z, ox, marks) => {
    const a = Uint8Array.from(atob(b), (ch) => ch.charCodeAt(0));
    for (let y = 0; y < D; y++) for (let x = 0; x < D; x++) { const v = 255 - a[y * D + x]; g.fillStyle = 'rgb(' + v + ',' + v + ',' + v + ')'; g.fillRect(ox + x * Z, gap + y * Z, Z, Z); }
    g.strokeStyle = 'rgba(0,120,255,0.25)'; g.lineWidth = 1;
    for (let i = 0; i <= D; i++) { g.beginPath(); g.moveTo(ox + i * Z + 0.5, gap); g.lineTo(ox + i * Z + 0.5, gap + D * Z); g.stroke(); g.beginPath(); g.moveTo(ox, gap + i * Z + 0.5); g.lineTo(ox + D * Z, gap + i * Z + 0.5); g.stroke(); }
    g.strokeStyle = '#E00'; g.lineWidth = 2;
    for (const m of marks) for (const p of m.edges) { g.beginPath(); if (m.orient === 'h') { g.moveTo(ox + m.from * Z, gap + p * Z); g.lineTo(ox + m.to * Z, gap + p * Z); } else { g.moveTo(ox + p * Z, gap + m.from * Z); g.lineTo(ox + p * Z, gap + m.to * Z); } g.stroke(); }
    g.fillStyle = '#000'; g.font = '13px sans-serif'; g.fillText((D === S ? '1x' : '2x') + ', ' + D + ' device px', ox, gap + D * Z + 16);
  };
  draw(a1, S, Z1, gap, marks1); draw(a2, 2 * S, Z2, gap * 2 + S * Z1, marks2);
  return c.toDataURL('image/png');
};`;

// Every raster is a screenshot of the SVG inline in a page, as the guide sets icons, at a device scale of 1, 2 or the
// supersample factor. A canvas would keep a non-scaling stroke at one canvas pixel at any zoom; a page scales it.
const HTML = '<!doctype html><html><body style="margin:0;background:transparent;color:#000"><div id="host" style="position:absolute;left:0;top:0;line-height:0"></div></body></html>';
async function openRenderer() {
  const browser = await chromium.launch();
  const pages = new Map();
  const at = async (dpr) => {
    if (!pages.has(dpr)) {
      const ctx = await browser.newContext({ deviceScaleFactor: dpr, viewport: { width: 64, height: 64 } });
      const pg = await ctx.newPage(); await pg.setContent(HTML); await pg.addScriptTag({ content: PAGE_JS });
      pages.set(dpr, pg);
    }
    return pages.get(dpr);
  };
  const page = await at(1);
  page.rasterAt = async (svg, S, dpr) => {
    const pg = await at(dpr);
    await pg.setViewportSize({ width: Math.max(S, 16), height: Math.max(S, 16) });
    await pg.evaluate((t) => window.place(t), svg);
    const png = await pg.screenshot({ clip: { x: 0, y: 0, width: S, height: S }, omitBackground: true, animations: 'disabled' });
    await pg.evaluate(() => window.place(''));
    const [W, b] = await page.evaluate((x) => window.decode(x), png.toString('base64'));
    if (W !== Math.round(S * dpr)) throw new Error(`screenshot is ${W} px, expected ${S * dpr}`);
    return b;
  };
  return { browser, page };
}
const fromB64 = (s) => new Uint8Array(Buffer.from(s, 'base64'));

// ---------- one file at one size ----------
async function checkOne(page, file, svgText, S, weight) {
  const k = Math.max(8, Math.ceil(640 / S));
  const one = sized(svgText, S);
  const unitsPerPx = one.viewBox[2] / S;
  const b1 = await page.rasterAt(one.text, S, 1);
  const b2 = await page.rasterAt(one.text, S, 2);
  const bs = await page.rasterAt(one.text, S, k);
  const nominal = await page.evaluate((t) => window.nominal(t), one.text);
  const a1 = fromB64(b1), a2 = fromB64(b2), as = fromB64(bs), N = S * k;
  const mask = new Uint8Array(N * N); for (let i = 0; i < N * N; i++) mask[i] = as[i] >= 128 ? 1 : 0;
  const widths = strokeWidths(mask, N, N, k);
  const edges = straightEdges(as, mask, N, N, k);
  const gp = gaps(mask, N, N, k);
  const ssCounters = counters(mask, N, N, RULES.minCounterArea * k * k);
  const nominalSet = [...new Set(nominal)].sort((x, y) => x - y);
  const scales = {};
  for (const [scale, a, D] of [[1, a1, S], [2, a2, 2 * S]]) {
    const m = new Uint8Array(D * D); for (let i = 0; i < D * D; i++) m[i] = a[i] >= 128 ? 1 : 0;
    const sf = soft(a);
    const res = scale / k; // measuring resolution at this scale: one supersampled pixel
    const items = judgeEdges(edges, scale);
    const kept = counters(m, D, D, 1);
    const w = widths ? { thinnest: widths.thinnest * scale, main: widths.main * scale, median: widths.median * scale, at: widths.thinAt.map((v) => +(v * scale).toFixed(1)) } : null;
    const gapPx = gp.smallest ? gp.smallest.gap * scale : null;
    const fails = [];
    if (!w) fails.push('no ink');
    if (w && w.thinnest < RULES.minStroke - res) fails.push('width');
    if (sf.share > RULES.maxSoftShare) fails.push('soft');
    if (items.some((it) => !it.ok)) fails.push('straight');
    if (gapPx !== null && gapPx < RULES.minGap - res) fails.push('gap');
    if (kept !== ssCounters) fails.push('counters');
    if (weight && w && Math.abs(w.main - weight * scale) > RULES.weightTolerance * scale) fails.push('weight');
    scales[scale + 'x'] = {
      device_px: D,
      stroke_px: { declared: nominalSet.map((v) => +(v * scale).toFixed(3)), thinnest: w && +w.thinnest.toFixed(2), thinnest_near_px: w && w.at, main: w && +w.main.toFixed(2), median: w && +w.median.toFixed(2) },
      soft_edges: { ink_px: sf.ink, partial_px: sf.partial, share: +sf.share.toFixed(3) },
      straight: {
        strokes: items.filter((i) => i.kind === 'stroke').length, lone_edges: items.filter((i) => i.kind === 'edge').length,
        fit: items.filter((i) => i.ok).length, total: items.length,
        off: items.filter((i) => !i.ok).map((i) => ({ kind: i.kind, orient: i.orient === 'h' ? 'horizontal' : 'vertical', at_px: i.edges.map((p) => +p.toFixed(2)), width_px: i.width !== undefined ? +i.width.toFixed(2) : undefined, span_px: [+i.from.toFixed(2), +i.to.toFixed(2)], needs: i.need })),
      },
      gap: { parts: gp.parts, smallest_px: gapPx === null ? null : +gapPx.toFixed(2), near_px: gp.smallest ? gp.smallest.near.map((v) => +(v * scale).toFixed(1)) : null },
      counters: { drawn: ssCounters, open: kept },
      fails, pass: fails.length === 0,
      _items: items,
    };
  }
  return { file, size: S, viewBox: one.viewBox, units_per_px: +unitsPerPx.toFixed(4), supersample: k, weight: weight || null, scales, pass: scales['1x'].pass && scales['2x'].pass, _a: [b1, b2] };
}

function report(r) {
  const L = [];
  const name = path.basename(r.file);
  L.push(`${r.pass ? 'PASS' : 'FAIL'}  ${name} at ${r.size} px (viewBox ${r.viewBox[2]} units, ${r.units_per_px} units per px)`);
  for (const sc of ['1x', '2x']) {
    const s = r.scales[sc];
    const sp = s.stroke_px;
    const why = s.pass ? 'pass' : 'fail: ' + s.fails.join(', ');
    L.push(`  ${sc} (${s.device_px} device px) ${why}`);
    L.push(`     stroke widths: thinnest ${sp.thinnest} px near (${sp.thinnest_near_px.join(', ')}), main ${sp.main} px${sp.declared.length ? `, declared ${sp.declared.join(', ')} px` : ', none declared (filled shapes)'}  [min ${RULES.minStroke}${r.weight ? `, weight ${r.weight * (sc === '2x' ? 2 : 1)} ± ${RULES.weightTolerance * (sc === '2x' ? 2 : 1)}` : ''}]`);
    L.push(`     soft edges: ${(s.soft_edges.share * 100).toFixed(0)}% of ${s.soft_edges.ink_px} ink px  [max ${RULES.maxSoftShare * 100}%]`);
    const st = s.straight;
    L.push(`     straight: ${st.fit} of ${st.total} fit (${st.strokes} strokes, ${st.lone_edges} lone edges)  [within ${RULES.edgeTolerance} px of a pixel edge]`);
    for (const o of st.off.slice(0, 6)) L.push(`       off: ${o.orient} ${o.kind}${o.width_px !== undefined ? ` ${o.width_px} px wide` : ''} at ${o.at_px.join(' and ')} px, from ${o.span_px[0]} to ${o.span_px[1]} px; needs ${o.needs}`);
    if (st.off.length > 6) L.push(`       and ${st.off.length - 6} more`);
    L.push(`     gap: ${s.gap.parts < 2 ? `one part, no gap` : `${s.gap.parts} parts, smallest gap ${s.gap.smallest_px} px near (${s.gap.near_px.join(', ')})`}; counters: ${s.counters.drawn} drawn, ${s.counters.open} at this scale  [gap min ${RULES.minGap} px]`);
  }
  return L.join('\n');
}

async function run(files, sizes, weights, opts) {
  const { browser, page } = await openRenderer();
  const results = [];
  try {
    for (const f of files) {
      const text = fs.readFileSync(f, 'utf8');
      for (let i = 0; i < sizes.length; i++) {
        let r;
        try { r = await checkOne(page, f, text, sizes[i], weights[i]); } catch (e) { r = { file: f, size: sizes[i], error: String(e.message || e), pass: false }; }
        results.push(r);
        if (!opts.quiet) console.log(r.error ? `FAIL  ${path.basename(f)} at ${sizes[i]} px: ${r.error}` : report(r));
        if (opts.png && !r.error) {
          fs.mkdirSync(opts.png, { recursive: true });
          const marks = (sc) => r.scales[sc]._items.filter((it) => !it.ok);
          const url = await page.evaluate(([a1, a2, S, m1, m2]) => window.preview(a1, a2, S, m1, m2), [r._a[0], r._a[1], r.size, marks('1x'), marks('2x')]);
          const out = path.join(opts.png, path.basename(f).replace(/\.svg$/i, '') + `_${r.size}px-pixel-fit.png`);
          fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64'));
        }
      }
    }
  } finally { await browser.close(); }
  for (const r of results) { delete r._a; if (r.scales) for (const s of Object.values(r.scales)) delete s._items; }
  return { results, ua: null };
}

// ---------- self-test: planted faults and one allowance ----------
const FIX = {
  crisp: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="5" y="5" width="14" height="14" fill="none" stroke="#000" stroke-width="2"/></svg>',
  halfPixel: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="5.5" y="5.5" width="14" height="14" fill="none" stroke="#000" stroke-width="2"/></svg>',
  hairline: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="5" y="5" width="14" height="14" fill="none" stroke="#000" stroke-width="2"/><line x1="8" y1="12.25" x2="16" y2="12.25" stroke="#000" stroke-width="0.5"/></svg>',
  nearParts: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="4" y="4" width="8" height="16"/><rect x="12.5" y="4" width="7.5" height="16"/></svg>',
  closingCounter: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill-rule="evenodd" d="M4 4h16v16H4z M11.7 11.3h0.6v1.4h-0.6z"/></svg>',
  soft: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="12.25" cy="12.25" r="7.25" fill="none" stroke="#000" stroke-width="1.05"/><path d="M5.25 18.75 L18.75 5.25" stroke="#000" stroke-width="1.05"/></svg>',
  weightOff: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect x="5" y="5" width="14" height="14" fill="none" stroke="#000" stroke-width="2"/></svg>',
  // Allowance: a 1.5 px line at 16 px with one edge on a pixel edge passes (whole pixels cannot hold both edges).
  oneAndAHalf: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M3 3.75H13M3.75 3V13M3 12.25H13M12.25 3V13M6 8.75H10" fill="none" stroke="#000" stroke-width="1.5"/></svg>',
  // Allowance: a round drawing fit to the grid (circle extremes on pixel edges, 2 px line) passes despite its curves.
  roundFit: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7" fill="none" stroke="#000" stroke-width="2"/><path d="M16 16L20 20" stroke="#000" stroke-width="2" stroke-linecap="round"/></svg>',
};
const PLANTS = [
  { fix: 'crisp', size: 24, expect: true, why: 'clean square, 2 px line on whole pixels' },
  { fix: 'halfPixel', size: 24, expect: 'straight', why: 'the same square half a pixel off' },
  { fix: 'hairline', size: 24, expect: 'width', why: 'a 0.5 px line inside the square' },
  { fix: 'nearParts', size: 24, expect: 'gap', why: 'two parts 0.5 px apart' },
  { fix: 'closingCounter', size: 24, expect: 'counters', why: 'a 0.6 px hole that fills in at 1x' },
  { fix: 'soft', size: 24, expect: 'soft', why: 'a 1.05 px ring and diagonal set between pixels' },
  { fix: 'weightOff', size: 24, weight: 1.5, expect: 'weight', why: 'a 2 px line where the grid asks for 1.5 px' },
  { fix: 'oneAndAHalf', size: 16, weight: 1.5, expect: true, why: 'allowance: 1.5 px strokes with one edge on a pixel edge' },
  { fix: 'roundFit', size: 24, weight: 2, expect: true, why: 'allowance: a round drawing fit to the grid' },
];
async function selfTest(opts) {
  let bad = 0;
  const { browser, page } = await openRenderer();
  try {
    for (const p of PLANTS) {
      const r = await checkOne(page, p.fix + '.svg', FIX[p.fix], p.size, p.weight);
      const fails = r.scales['1x'].fails;
      const ok = p.expect === true ? r.pass : fails.includes(p.expect);
      if (!ok) bad++;
      console.log(`${ok ? 'ok  ' : 'MISS'} ${p.fix} at ${p.size} px: ${p.why}; 1x fails [${fails.join(', ')}], 2x fails [${r.scales['2x'].fails.join(', ')}]`);
      if (!ok || opts.verbose) console.log(report(r));
    }
  } finally { await browser.close(); }
  console.log(bad ? `self-test: ${bad} of ${PLANTS.length} cases wrong` : `self-test: ${PLANTS.length} of ${PLANTS.length} cases right (7 planted faults caught, 2 allowances quiet)`);
  return bad ? 1 : 0;
}

(async () => {
  const o = parseArgs(process.argv.slice(2));
  if (o.selfTest) process.exit(await selfTest(o));
  if (!o.sizes.length) usage('give a target size, such as --size 24');
  if (!o.files.length) usage('give at least one SVG file or folder');
  const files = expandFiles(o.files);
  const { results } = await run(files, o.sizes, o.weights, o);
  const passed = results.filter((r) => r.pass).length;
  console.log(`\n${passed} of ${results.length} checks pass (${files.length} files at ${o.sizes.join(' and ')} px).`);
  if (o.json) {
    fs.mkdirSync(path.dirname(path.resolve(o.json)), { recursive: true });
    fs.writeFileSync(o.json, JSON.stringify({ tool: 'work/build/scripts/phase-2/icon_pixel_fit_check.js', run: new Date().toISOString(), rules: RULES, results }, null, 1));
  }
  process.exit(passed === results.length ? 0 : 1);
})().catch((e) => { console.error(e); process.exit(2); });
