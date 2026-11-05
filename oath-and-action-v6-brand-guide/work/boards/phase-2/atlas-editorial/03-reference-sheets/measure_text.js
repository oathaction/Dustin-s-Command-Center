// Measures text widths in Chromium with the page's own Google Fonts, for build_system.py.
// Usage: node measure_text.js <requests.json> <out.json>
// requests: [{"font": "600 15px Inter", "ls": 0.78, "text": "Safe seats"}, ...]  out: {"<font>|<ls>|<text>": width}
const fs = require('fs');
const { chromium } = require('playwright');
const FONTS = 'https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap';
(async () => {
  const reqs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(`<!doctype html><html><head><link rel="stylesheet" href="${FONTS}"></head><body><canvas id="c"></canvas></body></html>`, { waitUntil: 'networkidle' });
  const out = await page.evaluate(async (reqs) => {
    const fonts = [...new Set(reqs.map(r => r.font))];
    for (const f of fonts) { await document.fonts.load(f, 'AaBb0123'); }
    await document.fonts.ready;
    const ctx = document.getElementById('c').getContext('2d');
    const res = {};
    for (const r of reqs) {
      ctx.font = r.font; ctx.letterSpacing = (r.ls || 0) + 'px';
      res[`${r.font}|${r.ls || 0}|${r.text}`] = ctx.measureText(r.text).width;
    }
    res.__loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style);
    return res;
  }, reqs);
  fs.writeFileSync(process.argv[3], JSON.stringify(out));
  await browser.close();
})();
