// Measures label widths in Chromium with the locked Google Fonts, for build_concept.py (concept 04, Civic Landscape).
// Usage: node measure_labels.js <requests.json> <out.json>
// Each request: {"k": key, "t": text, "f": CSS font shorthand, "ls": letter-spacing in em, "up": uppercase}
const fs = require('fs');
const { chromium } = require('playwright');
(async () => {
  const reqs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.setContent('<html><head><link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet"></head><body><svg id="s" width="2000" height="200"></svg></body></html>', { waitUntil: 'networkidle' });
  await p.evaluate(async () => {
    const fams = ['400 13px Inter', '500 13px Inter', '600 15px Inter', '700 14px Inter', '700 13px Inter', '400 15px Inter', '400 14px Inter',
      '700 20px "Inter Tight"', '800 22px "Inter Tight"', '800 40px "Inter Tight"', 'italic 400 19px Lora'];
    await Promise.all(fams.map((f) => document.fonts.load(f)));
    await document.fonts.ready;
  });
  const out = await p.evaluate((reqs) => {
    const s = document.getElementById('s'), res = {};
    const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    t.setAttribute('x', 10); t.setAttribute('y', 100); s.append(t);
    for (const r of reqs) {
      t.style.font = r.f; t.style.letterSpacing = (r.ls || 0) + 'em'; t.style.textTransform = r.up ? 'uppercase' : 'none';
      t.textContent = r.up ? r.t.toUpperCase() : r.t;
      res[r.k] = +t.getComputedTextLength().toFixed(2);
    }
    return res;
  }, reqs);
  const fonts = await p.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family + ' ' + f.weight + ' ' + f.style));
  fs.writeFileSync(process.argv[3], JSON.stringify({ fonts, widths: out }, null, 0));
  await b.close();
})();
