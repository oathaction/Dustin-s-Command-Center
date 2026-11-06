// Captures for Board 4 of the data visualization round (November 6, 2026): the six stretch charts.
// Usage: node work/build/scripts/phase-2/dataviz_board4_capture.js
// From work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html it writes, to board-4/captures/:
//   newsprint-first-screen.jpg   the Newsprint view's first screen at 1440 by 900
//   newsprint-S11.jpg ...        each figure on the Newsprint view at 1440, at twice size so the board stays sharp
//   phone-S11.jpg ...            each figure at 390 px, at twice size
//   dark-first-screen.jpg and dark-S1N.jpg for the two Charcoal figures
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const DV = path.join(ROOT, 'work/boards/phase-2/data-viz');
const PAGE = path.join(DV, 'stretch/20261106_Data-Viz-Stretch.html');
const OUT = path.join(DV, 'board-4/captures');
const SPECS = ['S11', 'S12', 'S13', 'S14', 'S15', 'S16'];
fs.mkdirSync(OUT, { recursive: true });

async function open(page, view) {
  await page.goto('file://' + PAGE + '#' + view, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
}

async function shot(page, view, spec, out) {
  const el = page.locator(`[data-view-root="${view}"] figure[data-spec="${spec}"]`).first();
  if (!(await el.count())) return false;
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(150);
  await el.screenshot({ path: out, type: 'jpeg', quality: 84 });
  return true;
}

(async () => {
  const browser = await chromium.launch();
  const log = [];
  let ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  let page = await ctx.newPage();
  await open(page, 'newsprint');
  await page.screenshot({ path: path.join(OUT, 'newsprint-first-screen.jpg'), type: 'jpeg', quality: 84 });
  await open(page, 'dark');
  await page.screenshot({ path: path.join(OUT, 'dark-first-screen.jpg'), type: 'jpeg', quality: 84 });
  await ctx.close();

  ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  page = await ctx.newPage();
  await open(page, 'newsprint');
  for (const s of SPECS) if (await shot(page, 'newsprint', s, path.join(OUT, `newsprint-${s}.jpg`))) log.push(`newsprint ${s}`);
  await open(page, 'dark');
  for (const s of SPECS) if (await shot(page, 'dark', s, path.join(OUT, `dark-${s}.jpg`))) log.push(`dark ${s}`);
  await ctx.close();

  ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  page = await ctx.newPage();
  await open(page, 'newsprint');
  for (const s of SPECS) if (await shot(page, 'newsprint', s, path.join(OUT, `phone-${s}.jpg`))) log.push(`phone ${s}`);
  await ctx.close();
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'captures.json'), JSON.stringify(log, null, 1));
  console.log(`wrote ${log.length} figure captures and 2 screens to ${path.relative(ROOT, OUT)}`);
})();
