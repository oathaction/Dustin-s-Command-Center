#!/usr/bin/env node
// Gate 2 board renders (November 11, 2026, board builder, D2-1699). Called by gate_2_board_build.py; not run by hand.
//
// Usage: node work/build/scripts/phase-2/gate_2_board_render.js <jobs.json>
//
// jobs.json is a list of {out, markup, w, h, dsf, bg, ink, style}. Each job draws its markup (an <svg> with its width
// and height set) in a box w by h CSS px at the top left of an empty page, on the ground bg with color ink, at device
// scale dsf (1 or 2), and saves the box as a PNG at out. The box starts at 0,0, so a drawing whose own size is whole
// pixels lands on whole device pixels. Prints one line per job and exits 1 if any job failed.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const jobsPath = process.argv[2];
if (!jobsPath || !fs.existsSync(jobsPath)) { console.error('usage: node gate_2_board_render.js <jobs.json>'); process.exit(2); }
const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));

(async () => {
  const browser = await chromium.launch();
  const ctx = {};
  let failed = 0;
  for (const dsf of [...new Set(jobs.map(j => j.dsf || 1))]) {
    ctx[dsf] = await browser.newContext({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: dsf });
  }
  const pages = {};
  for (const [dsf, c] of Object.entries(ctx)) pages[dsf] = await c.newPage();
  for (const j of jobs) {
    const page = pages[j.dsf || 1];
    const w = j.w, h = j.h;
    if (j.shots) {
      // reader landings: open the page once at this width, then follow each anchor as a contents link does and
      // photograph the window once the scroll has settled and the pictures in view have loaded
      try {
        const ctx2 = await browser.newContext({ viewport: { width: j.width, height: j.height }, deviceScaleFactor: 1 });
        const pg = await ctx2.newPage();
        await pg.goto('file://' + j.file, { waitUntil: 'load', timeout: 180000 });
        await pg.waitForLoadState('networkidle', { timeout: 60000 }).catch(() => {});
        await pg.evaluate(() => document.fonts.ready);
        for (const s of j.shots) {
          await pg.evaluate((a) => { location.hash = a; }, s.anchor);
          await pg.waitForTimeout(500);
          await pg.evaluate(async () => {
            const vis = [...document.images].filter((im) => { const r = im.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; });
            vis.forEach((im) => { im.loading = 'eager'; });
            await Promise.all(vis.map((im) => im.complete ? 0 : new Promise((r) => { im.onload = im.onerror = r; setTimeout(r, 4000); })));
          });
          await pg.waitForTimeout(300);
          fs.mkdirSync(path.dirname(s.out), { recursive: true });
          await pg.screenshot({ path: s.out });
          console.log('ok', path.basename(s.out));
        }
        await ctx2.close();
      } catch (e) {
        failed++;
        console.log('failed', 'shots ' + j.width, String(e.message || e).slice(0, 160));
      }
      continue;
    }
    if (j.file) {
      // a part of a page: open the file, wait for its fonts, photograph the index-th match of the selector
      try {
        await page.setViewportSize({ width: j.viewport || 1200, height: 900 });
        await page.goto('file://' + j.file, { waitUntil: 'networkidle' });
        await page.evaluate(() => document.fonts.ready);
        const el = (await page.$$(j.selector))[j.index || 0];
        if (!el) throw new Error(`no match ${j.index || 0} for ${j.selector}`);
        fs.mkdirSync(path.dirname(j.out), { recursive: true });
        await el.screenshot({ path: j.out });
        console.log('ok', path.basename(j.out));
      } catch (e) {
        failed++;
        console.log('failed', path.basename(j.out), String(e.message || e).slice(0, 160));
      }
      continue;
    }
    try {
      await page.setViewportSize({ width: Math.max(320, Math.ceil(w) + 8), height: Math.max(200, Math.ceil(h) + 8) });
      await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>
        html,body{margin:0;padding:0;background:${j.bg}}
        #t{position:absolute;left:0;top:0;width:${w}px;height:${h}px;background:${j.bg};color:${j.ink};line-height:0;overflow:hidden;${j.style || ''}}
        #t svg{display:block;position:absolute;left:${j.x || 0}px;top:${j.y || 0}px}
      </style></head><body><div id="t">${j.markup}</div></body></html>`, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      fs.mkdirSync(path.dirname(j.out), { recursive: true });
      await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: w, height: h }, omitBackground: false });
      console.log('ok', path.basename(j.out));
    } catch (e) {
      failed++;
      console.log('failed', path.basename(j.out), String(e.message || e).slice(0, 160));
    }
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
