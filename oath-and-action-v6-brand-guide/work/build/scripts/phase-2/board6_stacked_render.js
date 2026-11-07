// Board 6, section 3: renders lockups at true size in Chromium at device scale 1 (November 7, 2026).
// Usage: node board6_stacked_render.js <jobs.json> <out dir>
// Each job: { id, svg (inline markup with width and height set), w, h, bg }. Writes <out dir>/<id>.png.
// The board's minimum-size plates show these pixels enlarged four times, and the crisp share is measured from them.
const fs = require('fs');
const path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const out = process.argv[3];
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 400 }, deviceScaleFactor: 1 });
  for (const j of jobs) {
    await page.setContent(`<!doctype html><html><body style="margin:0;background:${j.bg}"><div id="c" style="width:${j.w}px;height:${j.h}px;line-height:0">${j.svg}</div></body></html>`);
    await page.locator('#c').screenshot({ path: path.join(out, j.id + '.png') });
  }
  await browser.close();
  console.log(`rendered ${jobs.length} cells`);
})();
