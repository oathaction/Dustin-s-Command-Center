// Render one small HTML page to a PNG, at twice size by default: for a failure case that must show text under the
// 13 px floor as an image (D1-09), or at 1x to show how a small master falls on the pixel grid.
// Usage: node stage_a_identity_raster.js <page.html> <out.png> <width> <height> [scale]
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
(async () => {
  const [file, out, w, h, scale] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.max(+w, 64), height: Math.max(+h, 64) }, deviceScaleFactor: +(scale || 2) });
  await p.goto('file://' + path.resolve(file), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.locator('#c').screenshot({ path: out });
  await b.close();
})();
