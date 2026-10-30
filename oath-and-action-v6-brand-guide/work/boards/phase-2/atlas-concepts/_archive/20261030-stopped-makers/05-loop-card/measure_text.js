// Measure word widths in the atlas faces, for wrapping SVG text in build_concept.py (concept 05, October 30, 2026).
// Usage: node measure_text.js <request.json> <answer.json>
// The request holds {"fonts": {"key": {"family", "weight", "size", "spacing"}}, "words": {"key": ["word", ...]}}.
// The answer holds {"key": {"word": width_px, " ": space_px}}. Fonts load from Google Fonts, as on the page.
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const [req, out] = process.argv.slice(2);
  const q = JSON.parse(fs.readFileSync(req, 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(`<!doctype html><html><head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400&display=swap">
    </head><body><div id="m"></div></body></html>`, { waitUntil: 'networkidle' });
  const res = await page.evaluate(async (q) => {
    const out = {};
    for (const [key, f] of Object.entries(q.fonts)) {
      await document.fonts.load(`${f.weight} ${f.size}px "${f.family}"`);
    }
    await document.fonts.ready;
    const box = document.getElementById('m');
    for (const [key, f] of Object.entries(q.fonts)) {
      const words = q.words[key] || [];
      const r = {};
      box.style.cssText = `position:absolute;white-space:pre;font-family:"${f.family}";font-weight:${f.weight};font-size:${f.size}px;letter-spacing:${f.spacing || 0}em;font-feature-settings:${f.tnum ? '"tnum" 1' : 'normal'}`;
      const span = document.createElement('span'); box.replaceChildren(span);
      for (const w of [...words, ' ', 'x x']) { span.textContent = w; r[w] = span.getBoundingClientRect().width; }
      r[' '] = r['x x'] - 2 * (() => { span.textContent = 'x'; return span.getBoundingClientRect().width; })();
      out[key] = r;
    }
    out._loaded = [...document.fonts].filter((x) => x.status === 'loaded').map((x) => x.family + ' ' + x.weight);
    return out;
  }, q);
  fs.writeFileSync(out, JSON.stringify(res));
  await browser.close();
})();
