// Captures for Board 1 of the atlas concepts (October 30, 2026): element screenshots from the Stage 1 pages.
// Usage: node work/build/scripts/phase-2/atlas_board1_capture.js
// Writes JPEGs to work/boards/phase-2/atlas-concepts/board-1/img/.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const AC = path.join(ROOT, 'work/boards/phase-2/atlas-concepts');
const OUT = path.join(AC, 'board-1/img');
fs.mkdirSync(OUT, { recursive: true });
const IDEAS = ['great-circle', 'star-atlas', 'ledger-grid', 'honeycomb', 'kitchen-table', 'spine', 'flywheels', 'crossroads', 'open-atlas', 'tabletop'];

async function settle(page) { await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(600); }

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();

  await page.goto('file://' + path.join(AC, 'ideas/20261030_From-Scratch-Directions-Sketches.html'), { waitUntil: 'networkidle' });
  await settle(page);
  for (const id of IDEAS) {
    await page.locator(`#${id} .sk`).first().screenshot({ path: path.join(OUT, `sketch-${id}.jpg`), type: 'jpeg', quality: 84 });
    await page.locator(`#${id} .strip`).first().screenshot({ path: path.join(OUT, `strip-${id}.jpg`), type: 'jpeg', quality: 84 });
  }

  await page.goto('file://' + path.join(AC, 'shared/20261030_Loop-Route-Thumbnails-Study.html'), { waitUntil: 'networkidle' });
  await settle(page);
  for (const id of ['plan', 'newsprint', 'charcoal']) {
    const box = await page.locator('#' + id).boundingBox();
    await page.screenshot({ path: path.join(OUT, `routes-${id}.jpg`), type: 'jpeg', quality: 84, fullPage: true, clip: { x: box.x, y: box.y, width: box.width, height: Math.min(box.height, 1250) } });
  }

  await page.goto('file://' + path.join(AC, 'shared/20261030_Atlas-Type-And-Line-Specimen.html'), { waitUntil: 'networkidle' });
  await settle(page);
  for (const id of ['type', 'lines', 'grounds']) {
    const box = await page.locator('#' + id).boundingBox();
    await page.screenshot({ path: path.join(OUT, `specimen-${id}.jpg`), type: 'jpeg', quality: 84, fullPage: true, clip: { x: box.x, y: box.y, width: box.width, height: Math.min(box.height, 1100) } });
  }

  for (const view of ['overview', 'loop-r10']) {
    await page.goto('file://' + path.join(AC, 'shared/20261030_Atlas-Kit-Demo.html') + '#' + view, { waitUntil: 'networkidle' });
    await settle(page);
    await page.screenshot({ path: path.join(OUT, `kit-${view}.jpg`), type: 'jpeg', quality: 84 });
  }
  const phone = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const pp = await phone.newPage();
  await pp.goto('file://' + path.join(AC, 'shared/20261030_Atlas-Kit-Demo.html') + '#loop-r10', { waitUntil: 'networkidle' });
  await settle(pp);
  await pp.screenshot({ path: path.join(OUT, 'kit-loop-r10-phone.jpg'), type: 'jpeg', quality: 84 });
  await browser.close();
  console.log('captures in', path.relative(ROOT, OUT), fs.readdirSync(OUT).length);
})();
