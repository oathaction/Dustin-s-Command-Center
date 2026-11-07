// Board 6, section 4 (November 7, 2026): captures of every color sheet, and a check of the colors the browser paints.
// Usage: node work/build/scripts/phase-2/board6_color_sheets_render.js
//
// For each full-size sheet (not the small copies in the strip) at 1440 and 390 px it saves a JPEG of the sheet alone,
// and at 1440 px it saves the strip of seven, in color and in grayscale. Then it reads every element the build tagged
// with data-chk="property|ground hex|minimum ratio|expected hex" (and data-chk2 for a focus ring), takes the color the
// browser computed for that property, and records the ratio against the ground. A pair fails when it falls under its
// minimum; a mismatch is a painted color that differs from the one the build measured.
// Writes .../color-sheets/20261107_Board-6-Color-Sheets-Render-Results.json and captures to .../color-sheets/captures/.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const DIR = path.join(ROOT, 'work/boards/phase-2/board-6/color-sheets');
const FILE = path.join(DIR, '20261107_Board-6-Color-Sheets.html');
const CAP = path.join(DIR, 'captures');
fs.mkdirSync(CAP, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const out = { file: path.relative(ROOT, FILE), checked: 0, failures: 0, mismatch: 0, bad: [], sheets: {}, captures: [] };
  for (const width of [1440, 390]) {
    const ctx = await browser.newContext({ viewport: { width, height: width === 1440 ? 900 : 844 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    await page.goto('file://' + FILE, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    const keys = await page.$$eval('section.sheet-sec > .cs', (els) => els.map((e) => e.getAttribute('data-sheet')));
    for (const k of keys) {
      const el = await page.$(`section.sheet-sec > .cs[data-sheet="${k}"]`);
      const box = await el.boundingBox();
      out.sheets[`${k}@${width}`] = { width: Math.round(box.width), height: Math.round(box.height) };
      const f = path.join(CAP, `20261107_Board-6-Color-Sheet-${k}-${width}.jpg`);
      await el.screenshot({ path: f, type: 'jpeg', quality: 82 });
      out.captures.push(path.relative(ROOT, f));
    }
    if (width === 1440) {
      const strip = await page.$('.thumbs-w');
      const f = path.join(CAP, '20261107_Board-6-Color-Sheets-Strip-1440.jpg');
      await strip.screenshot({ path: f, type: 'jpeg', quality: 85 });
      out.captures.push(path.relative(ROOT, f));
      await page.addStyleTag({ content: 'html{filter:grayscale(1)!important}' });
      const g = path.join(CAP, '20261107_Board-6-Color-Sheets-Strip-1440-Grayscale.jpg');
      await strip.screenshot({ path: g, type: 'jpeg', quality: 85 });
      out.captures.push(path.relative(ROOT, g));
      await page.reload({ waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      // painted colors, full-size sheets only
      const res = await page.evaluate(() => {
        const parse = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return p.slice(0, 3); };
        const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
        const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
        const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
        const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
        const rows = [];
        document.querySelectorAll('section.sheet-sec > .cs').forEach((sheet) => {
          const key = sheet.getAttribute('data-sheet');
          sheet.querySelectorAll('[data-chk],[data-chk2]').forEach((el) => {
            for (const attr of ['data-chk', 'data-chk2']) {
              const v = el.getAttribute(attr); if (!v) continue;
              const [prop, bg, min, want] = v.split('|');
              let t = el;
              if (el.tagName.toLowerCase() === 'g' || el.tagName.toLowerCase() === 'span' && prop !== 'color' && prop !== 'background-color' && prop !== 'outline-color') {
                t = el.querySelector('path,line,circle,rect,polyline,polygon') || el;
              }
              const got = parse(getComputedStyle(t).getPropertyValue(prop));
              if (!got) { rows.push({ key, prop, bg, ok: false, note: 'no paint read' }); continue; }
              const r = ratio(got, hex(bg)); const w = hex(want);
              const same = Math.max(...got.map((x, i) => Math.abs(x - w[i]))) <= 1;
              rows.push({ key, prop, bg, want, got: '#' + got.map((x) => Math.round(x).toString(16).padStart(2, '0')).join('').toUpperCase(), ratio: +r.toFixed(2), min: +min, ok: r + 0.005 >= +min, same });
            }
          });
        });
        return rows;
      });
      // row heights: each row's natural height, the tallest across the seven sheets (the build sets these as grid rows)
      out.rowsInUse = await page.evaluate(() => getComputedStyle(document.querySelector('section.sheet-sec .cs-g')).gridTemplateRows);
      out.overrun = await page.evaluate(() => {
        const bad = [];
        document.querySelectorAll('section.sheet-sec .cs-g').forEach((g) => {
          const tracks = getComputedStyle(g).gridTemplateRows.split(' ').map(parseFloat);
          const areas = { 'm-head': 0, 'm-hero': 0, 'm-pal': 1, 'm-side': 1, 'm-card': 2, 'm-icons': 2, 'm-dark': 2, 'm-btn': 3, 'm-chart': 3, 'm-jobs': 3, 'm-party': 4, 'm-sys': 4 };
          for (const [c, r] of Object.entries(areas)) {
            const el = g.querySelector(':scope > .' + c); if (!el) continue;
            let h = 0; for (const k of el.children) { const b = k.getBoundingClientRect(); h = Math.max(h, b.bottom - el.getBoundingClientRect().top); }
            if (h > tracks[r] + 1) bad.push({ sheet: g.closest('.cs').dataset.sheet, module: c, content: Math.round(h), track: tracks[r] });
          }
        });
        return bad;
      });
      await page.addStyleTag({ content: '.cs-g{grid-template-rows:none!important}.cs-g>*{align-self:start!important}' });
      await page.waitForTimeout(200);
      out.rows = await page.evaluate(() => {
        const groups = [['m-head', 'm-hero'], ['m-pal', 'm-side'], ['m-card', 'm-icons', 'm-dark'], ['m-btn', 'm-chart', 'm-jobs'], ['m-party', 'm-sys']];
        const max = groups.map(() => 0); const per = {};
        document.querySelectorAll('section.sheet-sec .cs-g').forEach((g) => {
          const key = g.closest('.cs').dataset.sheet; per[key] = [];
          groups.forEach((cls, i) => {
            const h = Math.max(...cls.map((c) => { const el = g.querySelector(':scope > .' + c); return el ? el.getBoundingClientRect().height : 0; }));
            per[key].push(Math.ceil(h)); max[i] = Math.max(max[i], Math.ceil(h));
          });
        });
        return { max, per };
      });
      out.rowsPerSheet = out.rows.per; out.rows = out.rows.max;
      out.checked = res.length;
      out.failures = res.filter((r) => !r.ok).length;
      out.mismatch = res.filter((r) => r.same === false).length;
      out.bad = res.filter((r) => !r.ok || r.same === false).slice(0, 40);
      out.byProp = res.reduce((a, r) => { a[r.prop] = (a[r.prop] || 0) + 1; return a; }, {});
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(DIR, '20261107_Board-6-Color-Sheets-Render-Results.json'), JSON.stringify(out, null, 1));
  console.log(`checked ${out.checked} painted pairs: ${out.failures} under their minimum, ${out.mismatch} painted off their measured hex`);
  console.log(JSON.stringify(out.sheets));
  console.log('rows in use', out.rowsInUse, '| natural max', JSON.stringify(out.rows), '| overruns', JSON.stringify(out.overrun));
  for (const b of out.bad) console.log('  -', JSON.stringify(b));
})();
