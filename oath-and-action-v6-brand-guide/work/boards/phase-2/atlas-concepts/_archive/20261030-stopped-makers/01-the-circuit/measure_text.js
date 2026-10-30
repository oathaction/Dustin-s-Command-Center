// Measure text widths with the real web fonts, for build_concept.py (Concept 01, The Circuit).
// Usage: node measure_text.js <in.json> <out.json>, where in.json is [[css font, text], ...].
// Writes the advance widths in CSS px, in the same order. Loads Inter, Inter Tight and Lora from Google Fonts.
const fs = require('fs');
const { chromium } = require('playwright');
(async () => {
  const items = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.setContent('<html><head><link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet"></head><body></body></html>', { waitUntil: 'networkidle' });
  const out = await p.evaluate(async (items) => {
    const fonts = [...new Set(items.map((x) => x[0]))];
    for (const f of fonts) await document.fonts.load(f, 'AaBb0123');
    await document.fonts.ready;
    const c = document.createElement('canvas').getContext('2d');
    return items.map(([f, t]) => { c.font = f; return Math.round(c.measureText(t).width * 100) / 100; });
  }, items);
  fs.writeFileSync(process.argv[3], JSON.stringify(out));
  await b.close();
})();
