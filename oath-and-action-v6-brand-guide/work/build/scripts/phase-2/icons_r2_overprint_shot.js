// Concept 1, Overprint: capture an HTML page to PNG with Chromium (design director, round two).
// Usage: node icons_r2_overprint_shot.js <absolute html path> <png path> <width> [deviceScale]
// The page is captured full height at the given CSS width.
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [html, png, width, scale] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: +width || 1440, height: 800 }, deviceScaleFactor: +scale || 1 });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path: png, fullPage: true });
  await browser.close();
})();
