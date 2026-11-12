#!/usr/bin/env node
// Board 1 renders (November 12, 2026, board builder; Phase 3, round 0). Called by board_1_build.py; not run by hand.
//
// Usage: node work/build/scripts/phase-3/board_1_render.js <jobs.json>
//
// jobs.json is a list of pages to open, each {file, hash, width, height, static_sticky, items: [...]}:
//   an item {selector, out} photographs the first match of selector at device scale 1, as the page draws it at that
//   window width (a chart that draws as it nears the screen is scrolled to and given time to draw first);
//   an item {anchor, out} follows the anchor as a contents link does and photographs the window.
// static_sticky turns every sticky or fixed bar into an ordinary block first, so an element's picture never carries a
// bar that scrolled over it. Prints one line per item and exits 1 if any item failed.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const jobsPath = process.argv[2];
if (!jobsPath || !fs.existsSync(jobsPath)) { console.error('usage: node board_1_render.js <jobs.json>'); process.exit(2); }
const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));

async function settle(pg) {
  await pg.evaluate(async () => {
    const vis = [...document.images].filter((im) => { const r = im.getBoundingClientRect(); return r.bottom > -200 && r.top < innerHeight + 200; });
    vis.forEach((im) => { im.loading = 'eager'; });
    await Promise.all(vis.map((im) => im.complete ? 0 : new Promise((r) => { im.onload = im.onerror = r; setTimeout(r, 4000); })));
  });
}

(async () => {
  const browser = await chromium.launch();
  let failed = 0;
  for (const j of jobs) {
    let ctx;
    try {
      ctx = await browser.newContext({ viewport: { width: j.width, height: j.height }, deviceScaleFactor: 1 });
      const pg = await ctx.newPage();
      await pg.goto('file://' + j.file + (j.hash || ''), { waitUntil: 'load', timeout: 180000 });
      await pg.waitForLoadState('networkidle', { timeout: 60000 }).catch(() => {});
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(400);
      if (j.static_sticky) {
        await pg.evaluate(() => {
          for (const e of document.querySelectorAll('body *')) {
            const p = getComputedStyle(e).position;
            if (p === 'sticky' || p === 'fixed') e.style.setProperty('position', 'static', 'important');
          }
        });
      }
      if (j.prime) {
        // draw every chart that waits for the screen: walk through the region once, then let the layout settle
        await pg.evaluate(async (s) => {
          const e = document.querySelector(s); if (!e) return;
          const top = e.getBoundingClientRect().top + scrollY, h = e.getBoundingClientRect().height;
          for (let y = top - innerHeight; y < top + h + innerHeight; y += Math.round(innerHeight * 0.7)) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); }
        }, j.prime);
        await pg.waitForTimeout(1000);
      }
      for (const it of j.items) {
        try {
          fs.mkdirSync(path.dirname(it.out), { recursive: true });
          if (it.anchor) {
            await pg.evaluate((a) => { location.hash = a; }, it.anchor);
            await pg.waitForTimeout(600);
            await settle(pg);
            await pg.waitForTimeout(300);
            await pg.screenshot({ path: it.out });
          } else {
            const el = await pg.$(it.selector);
            if (!el) throw new Error('no match for ' + it.selector);
            await el.scrollIntoViewIfNeeded();
            await pg.waitForTimeout(400);
            await settle(pg);
            // wait until the element stops moving: a chart drawn above it can shift it after the scroll
            let last = null;
            for (let k = 0; k < 12; k++) {
              const b = await el.evaluate((n) => { const r = n.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.height)].join(','); });
              if (b === last) break;
              last = b;
              await pg.waitForTimeout(250);
            }
            await el.scrollIntoViewIfNeeded();
            await pg.waitForTimeout(150);
            await el.screenshot({ path: it.out });
          }
          console.log('ok', path.basename(it.out));
        } catch (e) {
          failed++;
          console.log('failed', path.basename(it.out), String(e.message || e).slice(0, 200));
        }
      }
    } catch (e) {
      failed++;
      console.log('failed', 'page ' + path.basename(j.file) + ' at ' + j.width, String(e.message || e).slice(0, 200));
    } finally {
      if (ctx) await ctx.close();
    }
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
