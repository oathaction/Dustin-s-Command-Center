#!/usr/bin/env node
// Rendered check: Chromium loads tokens.css and resolves every token itself.
//
//   node work/build/tests/tokens/test_token_render.mjs [--json PATH] [--css PATH]
//
// Uses the preinstalled Playwright and its Chromium. Exit 1 on any failure, 2 when Playwright is missing.
//   1. Every color, dimension, duration, easing, weight, family and z-index token, applied to a real CSS
//      property, computes to the value tokens.json resolves to.
//   2. The browser's own color-mix(in oklab, ...) gives each derived color and tint the hex the token holds.
//   3. Inside each surface class, every short name computes to that surface's token, or to the fallback
//      where the surface has none, even when the surface sits inside another surface (no leaks).
//   4. Each type style, set with font: var(--oa-type-...), computes to its minimum size at 390 px wide and its
//      maximum at 1440 px, with its weight, line height and tracking.
//   5. Under prefers-reduced-motion every duration computes to 0 s.

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..', '..', '..');
const args = process.argv.slice(2);
const opt = (f, d) => (args.includes(f) ? args[args.indexOf(f) + 1] : d);
const JSON_PATH = path.resolve(opt('--json', path.join(ROOT, 'work/build/tokens/tokens.json')));
const CSS_PATH = path.resolve(opt('--css', path.join(ROOT, 'work/build/tokens/tokens.css')));

const require = createRequire(import.meta.url);
let chromium;
for (const where of [path.join(ROOT, 'work/build/node_modules/playwright'), (() => { try { return path.join(execSync('npm root -g', { encoding: 'utf8' }).trim(), 'playwright'); } catch { return null; } })()]) {
  try { if (where) { ({ chromium } = require(where)); break; } } catch { /* try the next */ }
}
if (!chromium) { console.log('render: Playwright is not installed; skipped.'); process.exit(2); }

// --- tokens.json, read and resolved here
const tree = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
const toks = new Map();
(function walk(n, p, inherited) {
  const typ = n.$type || inherited;
  for (const [k, v] of Object.entries(n)) {
    if (k.startsWith('$') || !v || typeof v !== 'object') continue;
    const cp = p ? `${p}.${k}` : k;
    if ('$value' in v) toks.set(cp, { ...v, $type: v.$type || typ }); else walk(v, cp, typ);
  }
})(tree, '', null);
const aliasOf = (v) => (typeof v === 'string' && /^\{[^{}]+\}$/.test(v) ? v.slice(1, -1) : null);
const resolve = (p, seen = []) => { const t = toks.get(p); const a = aliasOf(t.$value); return a && !seen.includes(a) ? resolve(a, [...seen, p]) : t.$value; };
const typeOf = (p) => { const t = toks.get(p); return t.$type || (aliasOf(t.$value) ? typeOf(aliasOf(t.$value)) : null); };
const ext = (p) => (toks.get(p).$extensions || {})['org.oathandaction'] || {};
const cssName = (p) => '--' + p.split('.').map((s) => s.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()).join('-');
const rgbOf = (h) => `rgb(${[1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16)).join(', ')})`;
const SURF = { onNewsprint: 'newsprint', onWhite: 'white', onCharcoal: 'charcoal', onPrussian: 'prussian' };

const probes = [];   // [path, cssProperty, expected computed value]
for (const p of toks.keys()) {
  const typ = typeOf(p);
  const v = resolve(p);
  const n = cssName(p);
  if (typ === 'color') probes.push([p, 'color', `var(${n})`, rgbOf(v.hex)]);
  else if (typ === 'dimension') probes.push([p, 'width', `var(${n})`, `${v.unit === 'rem' ? v.value * 16 : v.value}px`]);
  else if (typ === 'duration') probes.push([p, 'transition-duration', `var(${n})`, `${v.value / 1000}s`]);
  else if (typ === 'cubicBezier') probes.push([p, 'transition-timing-function', `var(${n})`, `cubic-bezier(${v.join(', ')})`]);
  else if (typ === 'fontWeight') probes.push([p, 'font-weight', `var(${n})`, String(v)]);
  else if (typ === 'fontFamily') probes.push([p, 'font-family', `var(${n})`, (Array.isArray(v) ? v : [v]).map((f) => (/\s/.test(f) ? `"${f}"` : f)).join(', ')]);
  else if (typ === 'number' && p.startsWith('oa.zIndex.')) probes.push([p, 'z-index', `var(${n})`, String(v)]);
  else if (typ === 'number' && ext(p).css) probes.push([p, 'border-top-left-radius', `var(${n})`, ext(p).css]);
}
const mixes = [...toks.keys()].filter((p) => ext(p).derivation).map((p) => [p, ext(p).derivation.css, resolve(p).hex]);
// surface short names
const bases = [];
for (const p of toks.keys()) { const s = p.split('.'); const last = s.pop(); if (last in SURF && typeOf(p) === 'color' && !bases.includes(s.join('.'))) bases.push(s.join('.')); }
const surfaceProbes = [];
for (const [key, s] of Object.entries(SURF)) {
  const outer = s === 'prussian' ? 'newsprint' : 'prussian';   // nest every surface inside another
  for (const b of bases) {
    const p = `${b}.${key}`;
    surfaceProbes.push([s, outer, b, cssName(b), toks.has(p) ? rgbOf(resolve(p).hex) : 'rgb(1, 2, 3)']);
  }
}
const typeStyles = [...toks.keys()].filter((p) => p.startsWith('oa.type.')).map((p) => {
  const v = toks.get(p).$value; const e = ext(p);
  return [p, cssName(p), e.minFontSize.value * 16, v.fontSize.value * 16, v.lineHeight, e.trackingEm, resolve(aliasOf(v.fontWeight))];
});

const css = fs.readFileSync(CSS_PATH, 'utf8');
const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body style="margin:0"><div id="host"></div></body></html>`;
const browser = await chromium.launch();
const fails = [];
let mixDiff = 0;
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.setContent(html);
  const got = await page.evaluate(({ probes, mixes, surfaceProbes }) => {
    const host = document.getElementById('host');
    const out = { probes: [], mixes: [], surfaces: [] };
    for (const [p, prop, value] of probes) {
      const el = document.createElement('div');
      el.style.setProperty(prop, value);
      if (prop === 'z-index') el.style.position = 'relative';
      host.appendChild(el);
      out.probes.push(getComputedStyle(el).getPropertyValue(prop));
      el.remove();
    }
    const cv = document.createElement('canvas'); cv.width = cv.height = 1;
    const cx = cv.getContext('2d', { willReadFrequently: true });
    for (const [, expr] of mixes) {
      cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000000'; cx.fillStyle = expr; cx.fillRect(0, 0, 1, 1);
      out.mixes.push([...cx.getImageData(0, 0, 1, 1).data.slice(0, 3)]);
    }
    for (const [s, outer, , short] of surfaceProbes) {
      const a = document.createElement('div'); a.className = `oa-surface-${outer}`;
      const b = document.createElement('div'); b.className = `oa-surface-${s}`;
      const el = document.createElement('div'); el.style.color = `var(${short}, rgb(1, 2, 3))`;
      b.appendChild(el); a.appendChild(b); host.appendChild(a);
      out.surfaces.push([getComputedStyle(el).color, getComputedStyle(b).backgroundColor]);
      a.remove();
    }
    return out;
  }, { probes: probes.map(([p, prop, v]) => [p, prop, v]), mixes, surfaceProbes });

  probes.forEach(([p, prop, , want], i) => {
    const have = got.probes[i].trim();
    // layout widths land on Chromium's 1/64 px grid, so a width may differ from its token by under 1/64 px
    const same = prop === 'font-family' ? have.replace(/"/g, '') === want.replace(/"/g, '')
      : prop === 'width' ? Math.abs(parseFloat(have) - parseFloat(want)) <= 1 / 64 + 1e-9 && have.endsWith('px')
        : have === want;
    if (!same) fails.push(`${p}: ${prop} computes to ${have}; tokens.json gives ${want}`);
  });
  mixes.forEach(([p, expr, hex], i) => {
    const want = [1, 3, 5].map((k) => parseInt(hex.slice(k, k + 2), 16));
    const d = Math.max(...want.map((w, k) => Math.abs(w - got.mixes[i][k])));
    mixDiff = Math.max(mixDiff, d);
    if (d > 1) fails.push(`${p}: the browser's ${expr} paints rgb(${got.mixes[i].join(', ')}); the token holds ${hex}`);
  });
  const surfaceHex = Object.fromEntries(Object.values(SURF).map((s) => [s, rgbOf(resolve(`oa.color.surface.${s}`).hex)]));
  surfaceProbes.forEach(([s, outer, b, , want], i) => {
    const [have, bg] = got.surfaces[i];
    if (have !== want) fails.push(`.oa-surface-${s} inside .oa-surface-${outer}: ${b} computes to ${have}; want ${want}`);
    if (bg !== surfaceHex[s]) fails.push(`.oa-surface-${s}: background computes to ${bg}; want ${surfaceHex[s]}`);
  });

  // type at both ends of the fluid range
  for (const width of [390, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    const sizes = await page.evaluate((styles) => styles.map(([, n]) => {
      const el = document.createElement('p');
      el.style.font = `var(${n})`; el.style.letterSpacing = `var(${n}-letter-spacing)`; el.textContent = 'Hamburgefonstiv 0123';
      document.body.appendChild(el);
      const cs = getComputedStyle(el);
      const r = [parseFloat(cs.fontSize), cs.fontWeight, parseFloat(cs.lineHeight), parseFloat(cs.letterSpacing) || 0, cs.fontFamily];
      el.remove();
      return r;
    }), typeStyles);
    typeStyles.forEach(([p, , minPx, maxPx, lh, em, wt], i) => {
      const [fs_, fw, lhPx, ls] = sizes[i];
      const want = width === 390 ? minPx : maxPx;
      if (Math.abs(fs_ - want) > 0.05) fails.push(`${p}: font-size at ${width} px wide computes to ${fs_} px; want ${want}`);
      if (Number(fw) !== Number(wt)) fails.push(`${p}: font-weight computes to ${fw}; want ${wt}`);
      if (Math.abs(lhPx - fs_ * lh) > 0.06) fails.push(`${p}: line-height computes to ${lhPx} px; want ${(fs_ * lh).toFixed(2)}`);
      if (Math.abs(ls - fs_ * em) > 0.06) fails.push(`${p}: letter-spacing computes to ${ls} px; want ${(fs_ * em).toFixed(2)}`);
    });
  }
  // reduced motion
  await page.emulateMedia({ reducedMotion: 'reduce' });
  const reduced = await page.evaluate((names) => names.map((n) => {
    const el = document.createElement('div'); el.style.transitionDuration = `var(${n})`; document.body.appendChild(el);
    const v = getComputedStyle(el).transitionDuration; el.remove(); return v;
  }), [...toks.keys()].filter((p) => typeOf(p) === 'duration').map(cssName));
  reduced.forEach((v, i) => { if (v !== '0s') fails.push(`reduced motion: duration ${i + 1} computes to ${v}; want 0s`); });

  console.log(`render: Chromium ${browser.version()} resolved ${probes.length} token values, ${mixes.length} color-mix() derivations `
    + `(largest channel difference ${mixDiff}), ${surfaceProbes.length} surface short names nested in another surface, `
    + `${typeStyles.length} type styles at 390 and 1440 px and ${reduced.length} durations under reduced motion; ${fails.length} failures`);
} finally {
  await browser.close();
}
for (const f of fails.slice(0, 40)) console.log('  FAIL', f);
process.exit(fails.length ? 1 : 0);
