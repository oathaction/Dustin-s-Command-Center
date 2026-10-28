// Concept 3, Public sign: screenshot one HTML page to PNG with Chromium.
// Usage: node icons_r2_sign_shot.js <page.html> <out.png> [width=1440] [scale=2]
// Full-page capture. The page must load from an absolute file:// URL.
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [html, png, w, sc] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ deviceScaleFactor: +(sc || 2), viewport: { width: +(w || 1440), height: 900 } });
  await page.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: png, fullPage: true });
  await browser.close();
})();
