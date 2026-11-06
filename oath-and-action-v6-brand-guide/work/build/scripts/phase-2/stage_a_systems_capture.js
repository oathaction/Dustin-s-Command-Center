// Rendered measurements for chapters 05, 06 and 07 of stage board A (systems designer, November 6, 2026).
// Usage: node work/build/scripts/phase-2/stage_a_systems_capture.js <scratch dir written by the build's probe stage>
//
// Opens <scratch>/measure.html in Chromium at 1440 by 900, waits for the Google Fonts files, and measures:
//   cpl     characters on each full line of a paragraph (trailing spaces dropped, the last line left out),
//           found by reading each character's line box with a DOM Range
//   width   the rendered width of an element in CSS px
//   space   the width of "n n" less the width of "nn" in the same style: one word space as set
//   fonts   document.fonts.check() for each face and weight the guide loads
// then takes each screenshot probe (a phone page) at device scale 1. Writes <scratch>/results.json.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const dir = path.resolve(process.argv[2] || '');
const spec = JSON.parse(fs.readFileSync(path.join(dir, 'probes.json'), 'utf8'));

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto('file://' + path.join(dir, 'measure.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const results = await page.evaluate(() => {
    const out = {};
    for (const el of document.querySelectorAll('[data-probe]')) {
      const key = el.getAttribute('data-probe');
      const kind = el.getAttribute('data-kind');
      if (kind === 'cpl') {
        const tn = el.firstChild;
        const text = tn.textContent;
        const lines = [];
        let lastTop = null;
        for (let i = 0; i < text.length; i++) {
          const r = document.createRange();
          r.setStart(tn, i); r.setEnd(tn, i + 1);
          const rects = r.getClientRects();
          if (!rects.length) { if (lines.length) lines[lines.length - 1] += text[i]; continue; }
          const top = Math.round(rects[0].top);
          if (lastTop === null || Math.abs(top - lastTop) > 2) { lines.push(''); lastTop = top; }
          lines[lines.length - 1] += text[i];
        }
        const counts = lines.map((l) => l.replace(/\s+$/, '').replace(/^\s+/, '').length);
        const full = counts.slice(0, -1);
        const mean = full.reduce((a, b) => a + b, 0) / (full.length || 1);
        out[key] = { lines: counts.length, full_lines: full.length, counts: full, mean: +mean.toFixed(2),
          min: Math.min(...full), max: Math.max(...full), chars: text.length,
          width_px: +el.getBoundingClientRect().width.toFixed(2), font_size_px: parseFloat(getComputedStyle(el).fontSize) };
      } else if (kind === 'width') {
        out[key] = { width: +el.getBoundingClientRect().width.toFixed(2), font_size_px: parseFloat(getComputedStyle(el).fontSize),
          font_family: getComputedStyle(el).fontFamily };
      } else if (kind === 'space') {
        const a = el.querySelector('.a').getBoundingClientRect().width;
        const b = el.querySelector('.b').getBoundingClientRect().width;
        out[key] = { width: +(a - b).toFixed(3), font_size_px: parseFloat(getComputedStyle(el.querySelector('.a')).fontSize) };
      } else if (kind === 'fonts') {
        const faces = { 'Inter Tight 800': '800 24px "Inter Tight"', 'Inter 400': '400 17px "Inter"', 'Inter 600': '600 17px "Inter"',
          'Inter 700': '700 17px "Inter"', 'Lora Italic 400': 'italic 400 24px "Lora"' };
        const f = {};
        for (const [k, v] of Object.entries(faces)) f[k] = document.fonts.check(v);
        out[key] = f;
      }
    }
    return out;
  });
  for (const [key, p] of Object.entries(spec.probes)) {
    if (p.kind !== 'screenshot') continue;
    const pg = await ctx.newPage();
    await pg.goto('file://' + path.join(dir, p.page));
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(300);
    await pg.locator(p.selector).screenshot({ path: path.join(dir, p.file) });
    results[key] = { file: p.file };
    await pg.close();
  }
  results._env = { browser: 'chromium ' + browser.version(), viewport: '1440x900', deviceScaleFactor: 1,
    fonts: 'Google Fonts css2: Inter 400 500 600 700, Inter Tight 800, Lora italic 400 500', date: new Date().toISOString() };
  fs.writeFileSync(path.join(dir, 'results.json'), JSON.stringify(results, null, 1));
  console.log(`capture: ${Object.keys(results).length - 1} results in ${path.join(dir, 'results.json')}`);
  await browser.close();
})();
