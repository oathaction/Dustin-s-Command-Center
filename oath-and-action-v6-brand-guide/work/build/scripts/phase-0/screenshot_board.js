// Full-page PNG of a board, at device scale 1, stitched from viewport slices so very tall pages stay intact.
// Usage: node screenshot_board.js <board.html> <out.png> [width]
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [html, out, widthArg] = process.argv.slice(2);
  const width = parseInt(widthArg || '1944', 10);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width, height: 2000 } });
  await page.goto('file://' + path.resolve(html), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  const slice = 4000;
  const dir = out + '.parts';
  fs.mkdirSync(dir, { recursive: true });
  const parts = [];
  for (let y = 0, i = 0; y < total; y += slice, i++) {
    const h = Math.min(slice, total - y);
    const p = path.join(dir, `part-${String(i).padStart(3, '0')}.png`);
    await page.screenshot({ path: p, fullPage: true, clip: { x: 0, y, width, height: h } });
    parts.push(p);
  }
  fs.writeFileSync(out + '.parts.json', JSON.stringify({ width, total, parts }));
  await browser.close();
  console.log(JSON.stringify({ width, total, parts: parts.length }));
})();
