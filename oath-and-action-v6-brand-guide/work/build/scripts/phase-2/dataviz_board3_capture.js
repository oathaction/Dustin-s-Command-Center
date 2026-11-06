// Captures for Board 3 of the data visualization round (November 6, 2026).
// Usage: node work/build/scripts/phase-2/dataviz_board3_capture.js
// For each concept: the White view's first screen at 1440 by 900; three specimens on White (S01, S02, S08) and S02 on
// Newsprint as element shots at 1440; S06 on White (the diverging test); the first two phone screens at 390 by 844;
// the Charcoal view's first screen; and the social card. Writes JPEGs to work/boards/phase-2/data-viz/board-3/captures/.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const DV = path.join(ROOT, 'work/boards/phase-2/data-viz');
const OUT = path.join(DV, 'board-3/captures');
const CONCEPTS = { '01': ['01-explainer', 'Explainer'], '02': ['02-register', 'Register'], '03': ['03-instrument', 'Instrument'] };
fs.mkdirSync(OUT, { recursive: true });

async function open(page, file, view) {
  await page.goto('file://' + file + '#' + view, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
}

async function shotFigure(page, view, spec, out) {
  const el = page.locator(`[data-view-root="${view}"] figure[data-spec="${spec}"]`).first();
  if (!(await el.count())) { console.log('missing', view, spec, out); return false; }
  await el.scrollIntoViewIfNeeded();
  await page.waitForTimeout(200);
  await el.screenshot({ path: out, type: 'jpeg', quality: 86 });
  return true;
}

(async () => {
  const browser = await chromium.launch();
  const log = [];
  for (const [n, [dir, name]] of Object.entries(CONCEPTS)) {
    const file = path.join(DV, dir, `20261106_Data-Viz-${n}-${name}.html`);
    const base = path.join(OUT, `${n}-${name}`);
    // desktop
    let ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    let page = await ctx.newPage();
    await open(page, file, 'white');
    await page.screenshot({ path: `${base}-white-first-screen.jpg`, type: 'jpeg', quality: 84 });
    for (const s of ['S01', 'S02', 'S03', 'S06', 'S08', 'S10']) {
      if (await shotFigure(page, 'white', s, `${base}-white-${s}.jpg`)) log.push(`${n} white ${s}`);
    }
    await open(page, file, 'newsprint');
    for (const s of ['S02', 'S06']) {
      if (await shotFigure(page, 'newsprint', s, `${base}-newsprint-${s}.jpg`)) log.push(`${n} newsprint ${s}`);
    }
    await open(page, file, 'dark');
    await page.screenshot({ path: `${base}-dark-first-screen.jpg`, type: 'jpeg', quality: 84 });
    await open(page, file, 'social');
    const card = page.locator('[data-view-root="social"] figure[data-spec]').first();
    if (await card.count()) { await card.screenshot({ path: `${base}-social-card.jpg`, type: 'jpeg', quality: 86 }); log.push(`${n} social card`); }
    else { await page.screenshot({ path: `${base}-social-card.jpg`, type: 'jpeg', quality: 84, fullPage: true }); log.push(`${n} social page`); }
    await open(page, file, 'system');
    await page.screenshot({ path: `${base}-system-first-screen.jpg`, type: 'jpeg', quality: 84 });
    await ctx.close();
    // phone
    ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    page = await ctx.newPage();
    await open(page, file, 'white');
    await page.screenshot({ path: `${base}-white-390-screen-1.jpg`, type: 'jpeg', quality: 80 });
    await page.screenshot({ path: `${base}-white-390-screens-1-3.jpg`, type: 'jpeg', quality: 78, clip: { x: 0, y: 0, width: 390, height: 844 * 3 }, fullPage: true });
    if (await shotFigure(page, 'white', 'S02', `${base}-white-390-S02.jpg`)) log.push(`${n} phone S02`);
    await ctx.close();
  }
  await browser.close();
  console.log(`wrote ${fs.readdirSync(OUT).length} captures to ${path.relative(ROOT, OUT)}`);
})();
