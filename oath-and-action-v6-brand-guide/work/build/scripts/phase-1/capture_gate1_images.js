// Capture the Gate 1 review board's specimen images from the five Phase 1 boards.
//
// Usage: node capture_gate1_images.js <project-root>
// Playwright is global: NODE_PATH is not needed, the script requires it from `npm root -g`.
//
// Every capture is an element screenshot at device scale 2, so the board shows it at half its
// pixel width, which is its true CSS size on the source board. Large layouts are JPEG at quality 85;
// marks are PNG. The 16 and 24 px cells are not captured here: the board embeds the boards' own
// 1x renders for those, because a 2x screenshot would show a smoother drawing than a 1x screen does.
// A manifest records each file's pixel size and display size for the builder.
'use strict';
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(process.argv[2] || '.');
const BOARDS = path.join(ROOT, 'work', 'boards');
const OUT = path.join(BOARDS, 'phase-1', 'gate-1', 'img');
const npmRoot = execSync('npm root -g').toString().trim();
const { chromium } = require(path.join(npmRoot, 'playwright'));

const url = (rel) => 'file://' + path.join(BOARDS, rel);
const SYMBOL = '20261021_Symbol-Family-Board.html';
const STRATEGY = '20261021_Strategy-And-Direction-Board.html';
const SYSTEMS = '20261021_Systems-Marks-Board.html';

const manifest = {};

async function open(browser, rel, width) {
  const page = await browser.newPage({ viewport: { width, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto(url(rel), { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    // Load lazy images before any screenshot.
    for (const img of document.querySelectorAll('img[loading="lazy"]')) img.loading = 'eager';
    await Promise.all([...document.images].map((i) => (i.complete ? null : new Promise((r) => { i.onload = i.onerror = r; }))));
  });
  return page;
}

async function shot(page, selector, name, opts = {}) {
  const el = typeof selector === 'string' ? page.locator(selector).nth(opts.nth || 0) : selector;
  await el.scrollIntoViewIfNeeded();
  const box = await el.boundingBox();
  if (!box) throw new Error(`no box for ${selector} (${name})`);
  const file = path.join(OUT, name);
  const jpeg = name.endsWith('.jpg');
  await el.screenshot({ path: file, type: jpeg ? 'jpeg' : 'png', quality: jpeg ? 85 : undefined, animations: 'disabled' });
  const w = Math.round(box.width), h = Math.round(box.height);
  manifest[name] = { source: opts.source, selector: typeof selector === 'string' ? selector : opts.label, scale: 2, cssWidth: w, cssHeight: h, bytes: fs.statSync(file).size };
  return file;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

  // Symbol board: the composite posts (section 11) and the 48 and 96 px cells of both directions.
  let page = await open(browser, SYMBOL, 1440);
  const posts = ['post-today-width.jpg', 'post-condensed-width.jpg', 'post-wordmark-covered.jpg'];
  for (let i = 0; i < posts.length; i++) await shot(page, '#composite .post', posts[i], { nth: i, source: SYMBOL + '#h-co' });
  for (const dir of ['A', 'B']) {
    for (const treat of ['filled', 'line', 'tile']) {
      for (const pillar of ['Explain', 'Track', 'Connect', 'Act']) {
        const group = `[role="group"][aria-label="${pillar}, ${treat}, Direction ${dir}, on Newsprint, at 16, 24, 48 and 96 px"]`;
        const cells = page.locator(`${group} .mc`);
        const n = await cells.count();
        if (n !== 4) throw new Error(`${group}: expected 4 cells, found ${n}`);
        const sid = dir === 'A' ? 'h-direction-a' : 'h-direction-b';
        await shot(page, cells.nth(2), `sym-${dir}-${treat}-${pillar.toLowerCase()}-48.png`, { source: SYMBOL + '#' + sid, label: group + ' .mc 48' });
        await shot(page, cells.nth(3), `sym-${dir}-${treat}-${pillar.toLowerCase()}-96.png`, { source: SYMBOL + '#' + sid, label: group + ' .mc 96' });
      }
    }
  }
  await page.close();

  // Strategy board: the two Act mocks (section 5). At a 1200 px viewport each mock is 574 px wide,
  // which fits the review board's two-up grid at true size.
  page = await open(browser, STRATEGY, 1200);
  await shot(page, '#act article.mock', 'act-mock-process.jpg', { nth: 0, source: STRATEGY + '#h-act' });
  await shot(page, '#act article.mock', 'act-mock-position.jpg', { nth: 1, source: STRATEGY + '#h-act' });
  await page.close();

  // Systems board: the recommended options of marks 1 and 3, on all four surfaces.
  page = await open(browser, SYSTEMS, 1200);
  await shot(page, '#m1 .opt.rec-opt .surfaces:not(.gray)', 'systems-evidence-lines.png', { source: SYSTEMS + '#m1' });
  await shot(page, '#m3 .opt.rec-opt .surfaces', 'systems-typed-chips.png', { nth: 0, source: SYSTEMS + '#m3' });
  await page.close();

  // Strategy board reference p07, cropped to its seals row for the S9 card. This one is cut from the
  // 880 px reference file at 1x, since the board itself shows the file smaller than that.
  page = await browser.newPage({ viewport: { width: 880, height: 495 }, deviceScaleFactor: 1 });
  await page.goto(url('phase-1/strategy/refs/20261021_Ref-Page-07.jpg'));
  await page.addStyleTag({ content: 'body{margin:0} img{display:block}' });
  const clip = { x: 118, y: 287, width: 318, height: 100 };
  await page.screenshot({ path: path.join(OUT, 'ref-p07-seals.jpg'), type: 'jpeg', quality: 90, clip });
  manifest['ref-p07-seals.jpg'] = { source: 'phase-1/strategy/refs/20261021_Ref-Page-07.jpg (strategy board #h-art)', selector: 'clip ' + JSON.stringify(clip), scale: 1, cssWidth: clip.width, cssHeight: clip.height, bytes: fs.statSync(path.join(OUT, 'ref-p07-seals.jpg')).size };
  await page.close();

  await browser.close();
  fs.writeFileSync(path.join(OUT, 'manifest.json'), JSON.stringify(manifest, null, 1));
  const total = Object.values(manifest).reduce((a, m) => a + m.bytes, 0);
  console.log(`${Object.keys(manifest).length} images, ${Math.round(total / 1024)} KB, in ${OUT}`);
})().catch((e) => { console.error(e); process.exit(1); });
