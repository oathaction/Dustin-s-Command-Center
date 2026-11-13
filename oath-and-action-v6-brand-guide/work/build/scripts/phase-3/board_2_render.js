#!/usr/bin/env node
// Board 2 renders (November 13, 2026, the board builder working as the design director; Phase 3, board 2).
// Called by board_2_build.py; not run by hand. Copied from progress_round_2_render.js, which stays as it is; the one
// change is that a measure item also reads the width of the chart drawing (svg.oac-svg) and of the figure.
//
// Usage: node work/build/scripts/phase-3/board_2_render.js <jobs.json>
//
// jobs.json is a list of pages to open, each {file, width, height, static_sticky, draw_all, items: [{selector, out, measure}]}.
// Each item photographs the first match of its selector at device scale 1, as the page draws it at that window width.
// An item with measure: true takes no picture: it writes to its out file, as JSON, the width the element's chart drawing
// (svg.oac-svg) and the element itself draw at, and the plate stage's and frame's widths where the element has them, so
// the build can ask the kit for drawings at the widths the guide gives them.
// static_sticky turns every sticky or fixed bar into an ordinary block first, so no bar scrolls over a picture.
// draw_all calls OAChart.draw_all() and waits until every kit figure reports drawn (or an error), then waits for the
// page's height to hold still, so a chart drawn above an element cannot shift it after its picture is taken (D3-200).
// Each element is photographed only once its position holds still. One page and one window at a time, to keep memory low.
// An element taller than the window is photographed by making the window taller (its width, and so every layout width,
// stays the same) and clipping the picture from the window: Playwright's capture beyond the window takes tens of seconds
// on the 10 MB guide. CSS animations and transitions are turned off first.
// Prints one line per item and exits 1 if any item failed.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const jobsPath = process.argv[2];
if (!jobsPath || !fs.existsSync(jobsPath)) { console.error('usage: node board_2_render.js <jobs.json>'); process.exit(2); }
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
      await pg.addStyleTag({ content: '*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}' });
      await pg.waitForTimeout(300);
      let winH = j.height;
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
          if (it.measure) {
            const m = await el.evaluate((n) => {
              const st = n.querySelector('.plate-stage');
              const sc = n.querySelector('.plate-scroll');
              const w = (e) => (e ? Math.round(e.getBoundingClientRect().width * 100) / 100 : null);
              const sv = n.querySelector('svg.oac-svg');
              return { window: window.innerWidth, el_w: w(n), svg_w: sv ? Number(sv.getAttribute('width')) || w(sv) : null,
                       stage_w: w(st), frame_w: w(sc), wide: sc ? Number(sc.getAttribute('data-wide')) || null : null,
                       narrow: sc ? Number(sc.getAttribute('data-width')) || null : null };
            });
            fs.writeFileSync(it.out, JSON.stringify(m));
            console.log('ok', path.basename(it.out), JSON.stringify(m));
            continue;
          }
          await el.evaluate((n) => n.scrollIntoView({ block: 'start' }));
          await pg.waitForTimeout(150);
          await holdStill(pg, () => el.evaluate((n) => { const r = n.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)].join(','); }), 12, 200);
          let box = null;
          for (let k = 0; k < 4; k++) {
            await el.evaluate((n) => n.scrollIntoView({ block: 'start' }));
            await pg.waitForTimeout(100);
            box = await el.evaluate((n) => { const r = n.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
            const need = Math.ceil(Math.max(0, box.y) + box.h) + 2;
            if (box.y >= 0 && need <= winH) break;
            winH = Math.max(winH, need);
            await pg.setViewportSize({ width: j.width, height: winH });
            await pg.waitForTimeout(250);
          }
          // whole pixels, rounded outward as an element picture is, so no edge of the element is cut
          const x0 = Math.floor(box.x), y0 = Math.floor(box.y);
          const clip = { x: x0, y: y0, width: Math.ceil(box.x + box.w) - x0, height: Math.ceil(box.y + box.h) - y0 };
          if (clip.y < 0 || clip.y + clip.height > winH) throw new Error('the element does not fit the window: ' + JSON.stringify(clip) + ' in ' + winH);
          await pg.screenshot({ path: it.out, clip, animations: 'disabled' });
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
