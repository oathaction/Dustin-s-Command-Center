// Concept 2, Moving part: capture an HTML page to PNG with Chromium (design director, Phase 2 round two).
// Usage: node icons_r2_moving_shot.js <page.html> <out.png> [viewport width] [device scale]
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
(async () => {
  const [inp, out, w, s] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ deviceScaleFactor: parseFloat(s || '1'), viewport: { width: parseInt(w || '1200', 10), height: 60 } });
  await page.goto('file://' + path.resolve(inp));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  await page.screenshot({ path: out, fullPage: true });
  await browser.close();
})();
