#!/usr/bin/env node
// Utility icon set, stage B round 1: PNG previews and review sheets (icon designer, utility hand, November 9, 2026).
//
// Usage:
//   node work/build/scripts/phase-2/utility_icons_render.js previews            # png/ beside the SVGs, 1x and 2x
//   node work/build/scripts/phase-2/utility_icons_render.js review <out.png>    # true-size sheet, 1x pixels
//   node work/build/scripts/phase-2/utility_icons_render.js plate [out.png]     # plate glyphs on whole pixels, capture
//
// Previews: each SVG drawn by Chromium at its own size, Charcoal ink (#121212) on a clear ground, at device scale 1
// and 2, as the Civic Line PNG previews are. The review sheet sets every option at 16 and 24 px on Newsprint and
// Charcoal at device scale 1, so the pixels are the ones a reader gets; scale it up with nearest-neighbour to look.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const DIR = path.join(ROOT, 'work', 'build', 'assets', 'utility-icons');
const MANIFEST = path.join(DIR, '20261109_Utility-Icons-Manifest.json');
const INK = '#121212';
const NEWSPRINT = '#DCD9D2';

function svgOf(rel) {
  return fs.readFileSync(path.join(DIR, rel), 'utf8').replace(/<!--[\s\S]*?-->/g, '');
}

async function previews(browser, manifest) {
  const outDir = path.join(DIR, 'png');
  fs.mkdirSync(outDir, { recursive: true });
  let n = 0;
  for (const scale of [1, 2]) {
    const ctx = await browser.newContext({ deviceScaleFactor: scale, viewport: { width: 200, height: 200 } });
    const page = await ctx.newPage();
    for (const a of manifest) {
      for (const o of a.options) {
        for (const size of ['24', '16']) {
          const rel = o.files[size];
          await page.setContent(`<!doctype html><html><head><style>html,body{margin:0;background:transparent}
            #b{position:absolute;left:0;top:0;width:${size}px;height:${size}px;color:${INK}}
            #b svg{display:block}</style></head><body><div id="b">${svgOf(rel)}</div></body></html>`);
          const base = path.basename(rel, '.svg');
          const file = path.join(outDir, base + (scale === 2 ? '-2x' : '') + '.png');
          await page.locator('#b').screenshot({ path: file, omitBackground: true });
          n++;
        }
      }
    }
    await ctx.close();
  }
  console.log(`wrote ${n} PNG previews to ${outDir}`);
}

async function review(browser, manifest, out) {
  const ctx = await browser.newContext({ deviceScaleFactor: 1, viewport: { width: 900, height: 400 } });
  const page = await ctx.newPage();
  const rows = manifest.map((a) => {
    const cells = a.options.map((o) => `
      <div class="opt"><div class="lab">${o.option}</div>
        <div class="sw np"><span class="i24">${svgOf(o.files['24'])}</span><span class="i16">${svgOf(o.files['16'])}</span></div>
        <div class="sw ch"><span class="i24">${svgOf(o.files['24'])}</span><span class="i16">${svgOf(o.files['16'])}</span></div>
      </div>`).join('');
    return `<div class="row"><div class="name">${a.word}</div>${cells}</div>`;
  }).join('');
  await page.setContent(`<!doctype html><html><head><style>
    body{margin:0;background:#fff;font:11px/1 Inter, sans-serif;color:#121212}
    .row{display:flex;align-items:center;height:34px;border-bottom:1px solid #eee}
    .name{width:110px;padding-left:6px}
    .opt{display:flex;align-items:center;margin-right:14px}
    .lab{width:12px}
    .sw{display:flex;align-items:center;gap:6px;padding:5px 6px;height:24px}
    .np{background:${NEWSPRINT};color:${INK}}
    .ch{background:${INK};color:${NEWSPRINT}}
    .i24,.i16{display:block;line-height:0}
    .i24 svg{width:24px;height:24px;display:block}.i16 svg{width:16px;height:16px;display:block}
  </style></head><body>${rows}</body></html>`);
  const h = await page.evaluate(() => document.body.scrollHeight);
  await page.setViewportSize({ width: 900, height: h });
  await page.screenshot({ path: out, fullPage: true });
  console.log('wrote', out);
}

// Plate check: every glyph on the plate page sits on whole CSS pixels at its drawn size, then a full-page capture.
async function plate(browser, out) {
  const file = path.join(ROOT, 'work', 'boards', 'phase-2', 'stage-b', 'drawings', 'utility', '20261109_Utility-Icons-Plates.html');
  const ctx = await browser.newContext({ deviceScaleFactor: 1, viewport: { width: 1176, height: 900 } });
  const page = await ctx.newPage();
  await page.goto('file://' + file);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => document.documentElement.dataset.snapped === '1');
  const res = await page.evaluate(() => {
    const off = [];
    let n = 0;
    for (const s of document.querySelectorAll('svg.g')) {
      const st = getComputedStyle(s).transform;
      const r = s.getBoundingClientRect();
      n++;
      const bad = [r.left + window.scrollX, r.top + window.scrollY, r.width, r.height].some((v) => Math.abs(v - Math.round(v)) > 0.01);
      if (bad) off.push({ use: s.querySelector('use').getAttribute('href'), x: r.left, y: r.top + window.scrollY, w: r.width, transform: st });
    }
    const wide = document.documentElement.scrollWidth;
    return { n, off, wide };
  });
  console.log(`plate: ${res.n} glyphs, ${res.off.length} off whole pixels, page ${res.wide} px wide`);
  for (const o of res.off.slice(0, 20)) console.log('  off:', JSON.stringify(o));
  if (out) { await page.screenshot({ path: out, fullPage: true }); console.log('wrote', out); }
  await ctx.close();
  if (res.off.length) process.exitCode = 1;
}

(async () => {
  const mode = process.argv[2];
  const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
  const browser = await chromium.launch();
  try {
    if (mode === 'previews') await previews(browser, manifest);
    else if (mode === 'review') await review(browser, manifest, process.argv[3]);
    else if (mode === 'plate') await plate(browser, process.argv[3]);
    else { console.error('usage: utility_icons_render.js previews | review out.png | plate [out.png]'); process.exitCode = 2; }
  } finally { await browser.close(); }
})();
