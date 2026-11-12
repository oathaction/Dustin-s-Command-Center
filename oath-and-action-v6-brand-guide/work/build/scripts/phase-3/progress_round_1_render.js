#!/usr/bin/env node
// Round 1 progress page renders (November 12, 2026, the page builder working as the design director; Phase 3, round 1).
// Called by progress_round_1_build.py; not run by hand. Adapted from board_1_render.js.
//
// Usage: node work/build/scripts/phase-3/progress_round_1_render.js <jobs.json>
//
// jobs.json is a list of pages to open, each {file, width, height, static_sticky, draw_all, items: [{selector, out}]}.
// Each item photographs the first match of its selector at device scale 1, as the page draws it at that window width.
// static_sticky turns every sticky or fixed bar into an ordinary block first, so no bar scrolls over a picture.
// draw_all calls OAChart.draw_all() and waits until every kit figure reports drawn (or an error), then waits for the
// page's height to hold still, so a chart drawn above an element cannot shift it after its picture is taken (D3-200).
// Each element is photographed only once its position holds still. One page and one window at a time, to keep memory low.
// Prints one line per item and exits 1 if any item failed.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const jobsPath = process.argv[2];
if (!jobsPath || !fs.existsSync(jobsPath)) { console.error('usage: node progress_round_1_render.js <jobs.json>'); process.exit(2); }
const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));

async function holdStill(pg, read, tries = 20, wait = 250) {
  let last = null;
  for (let k = 0; k < tries; k++) {
    const now = await read();
    if (now === last) return true;
    last = now;
    await pg.waitForTimeout(wait);
  }
  return false;
}

(async () => {
  const browser = await chromium.launch();
  let failed = 0;
  for (const j of jobs) {
    let ctx;
    try {
      ctx = await browser.newContext({ viewport: { width: j.width, height: j.height }, deviceScaleFactor: 1 });
      const pg = await ctx.newPage();
      const errors = [];
      pg.on('pageerror', (e) => errors.push(String(e)));
      await pg.goto('file://' + j.file, { waitUntil: 'load', timeout: 180000 });
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(300);
      if (j.static_sticky) {
        await pg.evaluate(() => {
          for (const e of document.querySelectorAll('body *')) {
            const p = getComputedStyle(e).position;
            if (p === 'sticky' || p === 'fixed') e.style.setProperty('position', 'static', 'important');
          }
        });
      }
      if (j.draw_all) {
        const had = await pg.evaluate(() => !!(window.OAChart && OAChart.draw_all));
        if (had) {
          await pg.evaluate(() => OAChart.draw_all());
          await pg.waitForFunction(() => Array.from(document.querySelectorAll('figure.oac-fig')).every((f) => f.getAttribute('data-oa-drawn') || f.getAttribute('data-oa-error')), null, { timeout: 120000 })
            .catch(() => console.log('note: not every chart reported drawn at ' + j.width));
        } else {
          console.log('note: the page has no OAChart.draw_all at ' + j.width);
        }
        await holdStill(pg, () => pg.evaluate(() => String(document.documentElement.scrollHeight)), 20, 300);
      }
      for (const it of j.items) {
        try {
          fs.mkdirSync(path.dirname(it.out), { recursive: true });
          const el = await pg.$(it.selector);
          if (!el) throw new Error('no match for ' + it.selector);
          await el.scrollIntoViewIfNeeded();
          await pg.waitForTimeout(200);
          await holdStill(pg, () => el.evaluate((n) => { const r = n.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)].join(','); }), 12, 200);
          await el.scrollIntoViewIfNeeded();
          await pg.waitForTimeout(120);
          await el.screenshot({ path: it.out });
          console.log('ok', path.basename(it.out));
        } catch (e) {
          failed++;
          console.log('failed', path.basename(it.out), String(e.message || e).slice(0, 200));
        }
      }
      errors.slice(0, 5).forEach((e) => console.log('page error at ' + j.width + ': ' + e.slice(0, 200)));
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
