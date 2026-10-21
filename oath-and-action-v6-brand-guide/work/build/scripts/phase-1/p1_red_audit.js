// Screenshot the board in slices at a width, panels closed or open, for the red-on-Prussian audit.
// Usage: node p1_red_audit.js <board.html> <out_dir> <width> <open|closed>
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
(async () => {
  const [html, outDir, w, state, hide] = process.argv.slice(2);
  const width = parseInt(w, 10);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width, height: 2000 } });
  await page.goto('file://' + path.resolve(html), { waitUntil: 'load' });
  await page.evaluate(async (st) => {
    if (st === 'open') document.querySelectorAll('details').forEach(d => d.open = true);
    const imgs = [...document.images];
    imgs.forEach(i => { i.loading = 'eager'; });
    await Promise.all(imgs.map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
    document.querySelectorAll('.scroll').forEach(e => { e.style.overflow = 'visible'; });
  }, state);
  if (hide) await page.evaluate(sel => document.querySelectorAll(sel).forEach(e => { e.style.visibility = 'hidden'; }), hide);
  await page.evaluate(() => document.fonts.ready);
  const total = await page.evaluate(() => Math.max(document.documentElement.scrollHeight, document.body.scrollHeight));
  const vw = await page.evaluate(() => document.documentElement.scrollWidth);
  let i = 0;
  for (let y = 0; y < total; y += 2000, i++) {
    const h = Math.min(2000, total - y);
    await page.screenshot({ path: path.join(outDir, `s${String(i).padStart(4, '0')}.png`), clip: { x: 0, y, width: Math.max(width, vw), height: h }, fullPage: true });
  }
  console.log(JSON.stringify({ width, state, total, slices: i }));
  await browser.close();
})();
