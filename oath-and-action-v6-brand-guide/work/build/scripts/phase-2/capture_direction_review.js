// Capture the direction review page's specimen images from the Phase 2 map and icon boards.
//
// Usage: node capture_direction_review.js <project-root>
// Run by build_direction_review.py on every build, so one rerun picks up any change to the boards.
//
// Each capture is an element screenshot at device scale 2, shown on the review page at half its pixel
// width, which is its true CSS size on the source board. The poster, the hub crop and the icons are not
// captured: the builder inlines their own SVG files, which stay sharp at any size.
'use strict';
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(process.argv[2] || '.');
const BOARDS = path.join(ROOT, 'work', 'boards');
const OUT = path.join(BOARDS, 'phase-2', 'direction-review', 'img');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const FIELD = '20261028_Map-Direction-A-Field-Guide.html';
const OVERPRINT = '20261028_Icon-Concept-1-Overprint.html';
const manifest = {};

async function open(browser, rel, width) {
  const page = await browser.newPage({ viewport: { width, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(BOARDS, rel), { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    for (const img of document.querySelectorAll('img[loading="lazy"]')) img.loading = 'eager';
    await Promise.all([...document.images].map((i) => (i.complete ? null : new Promise((r) => { i.onload = i.onerror = r; }))));
  });
  return page;
}

function record(name, source, label, box, info) {
  const file = path.join(OUT, name);
  manifest[name] = { source, selector: label, scale: 2, cssWidth: Math.round(box.width), cssHeight: Math.round(box.height), bytes: fs.statSync(file).size, info: info || {} };
}

async function shot(page, selector, name, source, nth = 0, info) {
  const el = page.locator(selector).nth(nth);
  if (!(await el.count())) throw new Error(`missing ${selector} on ${source}`);
  await el.scrollIntoViewIfNeeded();
  const box = await el.boundingBox();
  const jpeg = name.endsWith('.jpg');
  await el.screenshot({ path: path.join(OUT, name), type: jpeg ? 'jpeg' : 'png', quality: jpeg ? 85 : undefined, animations: 'disabled' });
  record(name, source, selector + (nth ? ` (${nth + 1})` : ''), box, info);
}

// A clip from the top of one element to the bottom of another, across the full page width.
async function span(page, topSel, bottomSel, name, source) {
  const top = await page.locator(topSel).first().evaluate((e) => { const r = e.getBoundingClientRect(); return { y: r.top + scrollY }; });
  const bottom = await page.locator(bottomSel).first().evaluate((e) => { const r = e.getBoundingClientRect(); return { y: r.bottom + scrollY }; });
  const width = await page.evaluate(() => document.documentElement.clientWidth);
  const clip = { x: 0, y: Math.floor(top.y), width, height: Math.ceil(bottom.y - top.y) };
  await page.screenshot({ path: path.join(OUT, name), type: 'jpeg', quality: 85, fullPage: true, clip, animations: 'disabled' });
  record(name, source, `${topSel} to ${bottomSel}`, clip);
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  for (const f of fs.readdirSync(OUT)) if (/\.(png|jpg|json)$/.test(f)) fs.unlinkSync(path.join(OUT, f));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

  // The Field Guide board renders each page inline, so its elements are the pages themselves.
  let page = await open(browser, FIELD, 1440);
  await shot(page, '#spec-r8 article.fga-card', 'r8-card.jpg', FIELD + '#spec-r8');
  await shot(page, '#spec-catalog article.fga-tile[data-loop="R8"]', 'r8-tile.jpg', FIELD + '#spec-catalog');
  await span(page, '#spec-catalog header.fga-head', '#spec-catalog section.fga-plate', 'catalog-1440.jpg', FIELD + '#spec-catalog');
  const signs = await page.locator('#sign article.fga-card').count();
  if (signs < 2) throw new Error('expected two R8 cards in the sign section');
  const signHeads = await page.locator('#sign h3').allTextContents();
  for (let i = 0; i < signs; i++) await shot(page, '#sign article.fga-card', `sign-${i + 1}.jpg`, FIELD + '#sign', i, { option: signHeads.filter((h) => /^Option/.test(h.trim()))[i] || '' });
  await page.close();

  page = await open(browser, FIELD, 390);
  await span(page, '#spec-catalog header.fga-head', '#spec-catalog section.fga-plate', 'catalog-390.jpg', FIELD + '#spec-catalog at 390 px');
  await page.close();

  // The Overprint menu rows, on Newsprint and on Charcoal, with Track current.
  page = await open(browser, OVERPRINT, 860);  // the rows stack into a column below 760 px
  const rows = await page.locator('#s-contexts .navrow').count();
  for (let i = 0; i < Math.min(rows, 2); i++) await shot(page, '#s-contexts .navrow', `menu-row-${i + 1}.png`, OVERPRINT + '#s-contexts', i, { dark: await page.locator('#s-contexts .navrow').nth(i).evaluate((e) => e.classList.contains('dark')) });
  const cap = await page.locator('#s-contexts .ctx > figure').first().locator('figcaption').textContent();
  manifest['menu-row-1.png'].info.caption = (cap || '').trim();
  await page.close();

  await browser.close();
  fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 1));
  const total = Object.values(manifest).reduce((a, m) => a + m.bytes, 0);
  console.log(`${Object.keys(manifest).length} images, ${Math.round(total / 1024)} KB, in ${OUT}`);
})().catch((e) => { console.error(e); process.exit(1); });
