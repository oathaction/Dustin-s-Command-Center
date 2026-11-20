#!/usr/bin/env node
// Gate 3 board renders (November 20, 2026, the board builder working as the design director; Phase 3, Gate 3).
// Called by gate_3_board_build.py; not run by hand. Copied from board_3_render.js, which stays as it is. This copy adds:
// in the clip recipe, `first` (keep the first N matches of the words or patterns) and `subs` read as every match, the
// first one drawn on screen kept (a figure can hold a hidden desk drawing and a shown phone drawing); and the recipe
// "export" (the chart kit's own standalone SVG, set on the kit's own page as the kit sets it to draw its PNG, photographed
// at device scale 1 and clipped from `context` px above its footer to its foot, so the footer shows at true size).
//
// Board 3's notes, kept: text_scale (2 sets the root's text to 200 percent before anything is read); per item actions
// (clicks or checks run in order before the picture); recipe "rail-focus" (the masthead's focus picture); recipe "clip"
// (a crop to the change: the union of the blocks that hold given words or patterns, or of given parts, inside an element).
//
// Usage: node work/build/scripts/phase-3/gate_3_board_render.js <jobs.json>
//
// jobs.json is a list of pages to open, each {file, width, height, static_sticky, draw_all, text_scale,
// items: [{selector, out, measure, actions, recipe, clip, svg, context}]}.
// Each item photographs the first match of its selector at device scale 1, as the page draws it at that window width.
// static_sticky turns every sticky or fixed bar into an ordinary block first, so no bar scrolls over a picture.
// draw_all calls OAChart.draw_all() and waits until every kit figure reports drawn (or an error), then waits for the
// page's height to hold still (D3-200). An element taller than the window is photographed by making the window taller.
// CSS animations and transitions are turned off first. Prints one line per item and exits 1 if any item failed.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const jobsPath = process.argv[2];
if (!jobsPath || !fs.existsSync(jobsPath)) { console.error('usage: node gate_3_board_render.js <jobs.json>'); process.exit(2); }
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
      if (j.text_scale && j.text_scale !== 1) {
        await pg.addStyleTag({ content: 'html{font-size:' + (100 * j.text_scale) + '%!important}' });
      }
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
          for (const a of it.actions || []) {
            const n = a.times || 1;
            for (let k = 0; k < n; k++) {
              const target = await pg.$(a.click || a.check);
              if (!target) throw new Error('no match for the action ' + (a.click || a.check));
              await target.evaluate((x) => x.scrollIntoView({ block: 'center' }));
              if (a.check) await target.check({ force: true }); else await target.click();
              await pg.waitForTimeout(a.wait || 350);
            }
          }
          if (it.recipe === 'rail-focus') {
            // a keyboard reader in the chapter rail: from the last link up, as Shift+Tab moves
            await pg.evaluate(() => window.scrollTo(0, Math.min(900, document.documentElement.scrollHeight)));
            await pg.waitForTimeout(300);
            const links = await pg.$$(it.links || 'nav.rail a');
            if (!links.length) throw new Error('no rail links');
            await links[links.length - 1].focus();
            await pg.waitForTimeout(150);
            // the first link, going up, whose focus makes the rail scroll: the rail brings it to its own top edge, where
            // AX-M1 found the masthead covering it; the picture is taken while that link holds focus
            const read = () => pg.evaluate((sel) => {
              const a = document.activeElement, r = a.getBoundingClientRect(), rail = a.closest(sel);
              const rr = rail ? rail.getBoundingClientRect() : { top: 0 };
              return { top: r.top, bottom: r.bottom, railTop: rr.top, scroll: rail ? rail.scrollTop : null, text: (a.textContent || '').trim().slice(0, 60) };
            }, it.rail || 'nav.rail');
            let got = null;
            let prev = await read();
            for (let k = 0; k < Math.min(links.length + 2, 60); k++) {
              await pg.keyboard.press('Shift+Tab');
              await pg.waitForTimeout(150);
              const st = await read();
              if (st.scroll === null) break;
              // with until_text, the same link on every page: the one whose words hold it
              if (it.until_text) { if (st.text.includes(it.until_text)) { got = st; break; } prev = st; continue; }
              if (prev.scroll !== null && st.scroll < prev.scroll) { got = st; break; }
              prev = st;
            }
            if (!got) throw new Error('the rail never scrolled a focused link to its top edge');
            const h = await pg.evaluate((sel) => Math.ceil(document.querySelector(sel).getBoundingClientRect().bottom), it.head || 'header.masthead');
            const clipH = Math.min(winH, Math.max(h, Math.ceil(got.bottom)) + (it.below || 160));
            await pg.screenshot({ path: it.out, clip: { x: 0, y: 0, width: j.width, height: clipH }, animations: 'disabled' });
            console.log('ok', path.basename(it.out), JSON.stringify(got));
            continue;
          }
          if (it.recipe === 'export') {
            // the kit's standalone SVG, set on the kit's own page as the kit sets it for its PNG (oa-chart.mjs, captures()),
            // photographed at device scale 1 from `context` px above its footer to its foot
            const svg = fs.readFileSync(it.svg, 'utf8');
            const got = await pg.evaluate((x) => {
              const d = document.createElement('div'); d.id = 'oac-export-shot';
              d.style.cssText = 'position:absolute;left:0;top:0;line-height:0;z-index:9';
              d.innerHTML = x.replace(/^<\?xml[^>]*>\s*/, ''); document.body.append(d);
              const s = d.querySelector('svg'), r = s.getBoundingClientRect(), f = s.querySelector('[data-oa-export-foot]');
              const fr = f ? f.getBoundingClientRect() : null;
              return { w: r.width, h: r.height, x: r.left + scrollX, y: r.top + scrollY, foot: fr ? fr.top + scrollY : null };
            }, svg);
            if (got.foot === null) throw new Error('the export holds no footer');
            if (got.h + 4 > winH) { winH = Math.ceil(got.h) + 4; await pg.setViewportSize({ width: j.width, height: winH }); await pg.waitForTimeout(250); }
            await pg.evaluate(() => window.scrollTo(0, 0));
            await pg.waitForTimeout(250);
            const y0 = Math.max(Math.floor(got.y), Math.floor(got.foot - (it.context || 40)));
            await pg.screenshot({ path: it.out, clip: { x: Math.floor(got.x), y: y0, width: Math.round(got.w), height: Math.ceil(got.y + got.h) - y0 }, animations: 'disabled' });
            await pg.evaluate(() => document.getElementById('oac-export-shot').remove());
            console.log('ok', path.basename(it.out), JSON.stringify({ w: got.w, h: got.h, foot: got.foot - got.y }));
            continue;
          }
          if (it.recipe === 'clip') {
            // a crop to the change (the creative director's B3-M4 and B3-S1): the union of the blocks that hold the given
            // words or patterns, or of the given parts, inside the element; the element's folds opened first where asked;
            // `context` px above and below; the element's own width, or the page's whole scroll width where it overflows
            const o = it.clip || {};
            const got = await pg.evaluate((o) => {
              const root = document.querySelector(o.within);
              if (!root) return { err: 'no match for ' + o.within };
              if (o.open) root.querySelectorAll('details').forEach((d) => { d.open = true; });
              const out = [];
              const blk = (n) => { const e = n.nodeType === 3 ? n.parentElement : n; return e.closest(o.block || 'p,li,dd,td,th,tr,figcaption,h3,h4') || e; };
              for (const s of o.subs || []) { const e = Array.from(root.querySelectorAll(s)).find((x) => { const r = x.getBoundingClientRect(); return r.width > 2 && r.height > 2; }); if (e) out.push(e); }
              const pats = (o.texts || []).map((t) => ({ t })).concat((o.patterns || []).map((p) => ({ re: new RegExp(p) })));
              if (pats.length) {
                const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
                let n, found = 0;
                while ((n = w.nextNode())) {
                  const s = n.textContent;
                  if (o.first && found >= o.first) break;
                  if (pats.some((p) => (p.t ? s.includes(p.t) : p.re.test(s)))) { const b = blk(n); const r = b.getBoundingClientRect(); if (r.width > 2 && r.height > 2) { out.push(b); found++; } }
                }
              }
              const rs = out.map((e) => e.getBoundingClientRect()).filter((r) => r.width && r.height);
              if (!rs.length) return { err: 'nothing matched in ' + o.within };
              const rr = root.getBoundingClientRect();
              return { top: Math.min(...rs.map((r) => r.top)) + scrollY, bottom: Math.max(...rs.map((r) => r.bottom)) + scrollY,
                       left: rr.left, right: rr.right, maxRight: Math.max(...rs.map((r) => r.right)), n: rs.length,
                       scrollW: document.documentElement.scrollWidth };
            }, o);
            if (got.err) throw new Error(got.err);
            await pg.waitForTimeout(250);
            const ctxPx = o.context || 24;
            const y0 = Math.max(0, Math.floor(got.top - ctxPx)), h = Math.ceil(got.bottom + ctxPx) - y0;
            if (h + 4 > winH) { winH = h + 4; await pg.setViewportSize({ width: j.width, height: winH }); await pg.waitForTimeout(250); }
            await pg.evaluate((y) => window.scrollTo(0, y), y0);
            await pg.waitForTimeout(250);
            const sy = await pg.evaluate(() => scrollY);
            const x0 = o.overflow ? 0 : Math.max(0, Math.floor(got.left));
            const x1 = o.overflow ? Math.max(j.width, got.scrollW, Math.ceil(got.maxRight) + 4) : Math.ceil(got.right);
            await pg.screenshot({ path: it.out, clip: { x: x0, y: y0 - sy, width: x1 - x0, height: h }, animations: 'disabled' });
            console.log('ok', path.basename(it.out), JSON.stringify({ n: got.n, width: x1 - x0, height: h, scrollW: got.scrollW }));
            continue;
          }
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
