// Captures for the Board 6 hub (November 7, 2026), run by board6_hub_build.py on every build.
// Usage: node work/build/scripts/phase-2/board6_hub_capture.js <job.json>
//
// For each section page the job names, the script opens the page as it is now in a 1440 by 900 window at device
// scale 2 and:
//   - finds the lead comparison: the content's selector, else the page's own [data-board-lead] element, else the
//     section's default selectors, in that order;
//   - captures that element at true size as PNG (JPEG at quality 90 when the PNG passes job.max_png_bytes), with the
//     clip on whole CSS pixels so the image is exactly twice its CSS size;
//   - reads the page's title, its h1 and every id outside drawings, with the words a link to it should carry.
// Fixed and sticky elements outside the lead are hidden for the capture, so nothing floats over it. The page is never
// edited on disk. Writes the images to job.out and the facts to job.facts. Exit code 1 when a capture fails; the
// facts file still lists what was found.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const W = job.width || 1440;
const H = job.height || 900;
const SCALE = job.scale || 2;
const MAX_PNG = job.max_png_bytes || 4e6;
fs.mkdirSync(job.out, { recursive: true });
const facts = { captured: new Date().toISOString(), width: W, scale: SCALE, sections: {}, errors: [] };

(async () => {
  const browser = await chromium.launch();
  let ok = true;
  for (const s of job.sections) {
    const f = { key: s.key, page: s.page, page_mtime: fs.statSync(s.page).mtime.toISOString(), title: '', h1: '', ids: {}, lead: null, errors: [] };
    facts.sections[s.key] = f;
    const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => f.errors.push('page error: ' + String(e.message || e).slice(0, 160)));
    try {
      await page.goto('file://' + s.page, { waitUntil: 'networkidle', timeout: 120000 });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(600);
      Object.assign(f, await page.evaluate(() => {
        // the words of an element without its chips and hidden helpers, so "Option B ... Recommended" reads "Option B ..."
        const STRIP = '.chip, .tag, .badge, [class*="chip"], [class*="badge"], .vh, .sr-only, .visually-hidden, [aria-hidden="true"], svg';
        const txt = (el) => {
          if (!el) return '';
          const c = el.cloneNode(true);
          c.querySelectorAll(STRIP).forEach((x) => x.remove());
          return c.textContent.replace(/\s+/g, ' ').trim();
        };
        const ids = {};
        for (const el of document.querySelectorAll('body [id]')) {
          if (el.closest('svg, template, script, style')) continue;
          let label = '';
          if (/^H[1-6]$/.test(el.tagName)) label = txt(el);
          else {
            const h = el.querySelector('h1, h2, h3, h4, caption, legend');
            label = el.getAttribute('aria-label') || txt(h) || txt(el).slice(0, 60);
          }
          ids[el.id] = { tag: el.tagName.toLowerCase(), label: label.replace(/[.:]$/, '').slice(0, 120) };
        }
        return { title: document.title.trim(), h1: txt(document.querySelector('h1')), ids, lead_attr: !!document.querySelector('[data-board-lead]') };
      }));
      // the lead: the content's selector, the page's own mark, then the section's defaults
      const tries = [];
      if (s.selector) tries.push({ selector: s.selector, from: 'content' });
      else {
        tries.push({ selector: '[data-board-lead]', from: 'page' });
        for (const d of s.defaults || []) tries.push({ selector: d, from: 'default' });
      }
      let found = null;
      for (const t of tries) {
        const n = await page.evaluate((sel) => {
          try { const el = document.querySelector(sel); if (!el) return 0; const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 ? 1 : -1; } catch (e) { return -2; }
        }, t.selector);
        if (n === -2) { f.errors.push(`"${t.selector}" is not a valid CSS selector`); break; }
        if (n === -1) { f.errors.push(`"${t.selector}" matches an element with no size`); continue; }
        if (n === 1) { found = t; break; }
        if (t.from === 'content') f.errors.push(`"${t.selector}" matches nothing on the page`);
      }
      if (!found) {
        if (!s.selector) f.errors.push(`no lead found: the page has no [data-board-lead] element, and none of the defaults (${(s.defaults || []).join(', ') || 'none'}) match`);
        ok = false;
      } else {
        const box = await page.evaluate((sel) => {
          const el = document.querySelector(sel);
          el.scrollIntoView({ block: 'start' });
          // fixed and sticky elements outside the lead would float over it in a tall capture
          for (const e of document.querySelectorAll('body *')) {
            const p = getComputedStyle(e).position;
            if ((p === 'fixed' || p === 'sticky') && !e.contains(el) && !el.contains(e)) e.style.setProperty('visibility', 'hidden', 'important');
          }
          const r = el.getBoundingClientRect();
          const x = Math.floor(r.left + scrollX), y = Math.floor(r.top + scrollY);
          return { x, y, width: Math.ceil(r.right + scrollX) - x, height: Math.ceil(r.bottom + scrollY) - y, tag: el.tagName.toLowerCase(), id: el.id || null };
        }, found.selector);
        await page.evaluate(async (sel) => {
          const el = document.querySelector(sel);
          await Promise.all([...el.querySelectorAll('img')].map((i) => (i.decode ? i.decode().catch(() => {}) : null)));
        }, found.selector);
        await page.waitForTimeout(300);
        let file = `${s.stem}.png`;
        let buf = await page.screenshot({ fullPage: true, clip: { x: box.x, y: box.y, width: box.width, height: box.height }, type: 'png' });
        let format = 'png';
        if (buf.length > MAX_PNG) {
          file = `${s.stem}.jpg`; format = 'jpeg';
          buf = await page.screenshot({ fullPage: true, clip: { x: box.x, y: box.y, width: box.width, height: box.height }, type: 'jpeg', quality: 90 });
        }
        fs.writeFileSync(path.join(job.out, file), buf);
        f.lead = { selector: found.selector, from: found.from, file, format, bytes: buf.length, css_w: box.width, css_h: box.height,
          px_w: box.width * SCALE, px_h: box.height * SCALE, page_x: box.x, page_y: box.y, tag: box.tag, id: box.id };
      }
    } catch (e) {
      f.errors.push(String(e.message || e).slice(0, 200));
      ok = false;
    }
    if (f.errors.some((e) => e.startsWith('page error'))) ok = false;
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(job.facts, JSON.stringify(facts, null, 1));
  const n = Object.values(facts.sections).filter((x) => x.lead).length;
  console.log(`captured ${n} of ${job.sections.length} lead comparisons at ${W} px, device scale ${SCALE}`);
  for (const x of Object.values(facts.sections)) for (const e of x.errors) console.log(`  - ${x.key}: ${e}`);
  process.exit(ok ? 0 : 1);
})();
