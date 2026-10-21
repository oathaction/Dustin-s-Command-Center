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
  // Start clean, so a version the boards dropped never lingers in the review board.
  for (const f of fs.readdirSync(OUT)) if (/\.(png|jpg|json)$/.test(f)) fs.unlinkSync(path.join(OUT, f));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

  // Symbol board: the composite posts (section 11) and the 48 and 96 px cells of both directions.
  let page = await open(browser, SYMBOL, 1440);
  // Every version of the composite post, however many the board holds, with its label and headline.
  const nPosts = await page.locator('#composite .post').count();
  if (nPosts < 1) throw new Error('no composite posts on the symbol board');
  for (let i = 0; i < nPosts; i++) {
    const name = `post-${i + 1}.jpg`;
    await shot(page, '#composite .post', name, { nth: i, source: SYMBOL + '#h-co' });
    manifest[name].info = await page.locator('#composite .post').nth(i).evaluate((el) => {
      // Text with each inline SVG read as its accessible name, so a drawn ampersand reads as "and".
      const read = (node) => {
        if (!node) return '';
        const c = node.cloneNode(true);
        c.querySelectorAll('svg').forEach((s) => s.replaceWith(' ' + (s.getAttribute('aria-label') || '') + ' '));
        c.querySelectorAll('.tag, .illus').forEach((s) => s.remove());
        return c.textContent.replace(/\s+/g, ' ').trim();
      };
      const named = [...el.querySelectorAll('[role="img"], [role="separator"]')]
        .filter((n) => !n.parentElement.closest('[role="img"], [role="separator"]') && !n.closest('.po-head'))
        .map((n) => n.getAttribute('aria-label')).filter(Boolean);
      return {
        label: el.getAttribute('aria-label') || '',
        kicker: read(el.querySelector('.po-k')),
        head: read(el.querySelector('.po-head')),
        covered: !!el.querySelector('.po-cover'),
        steps: el.querySelectorAll('ol li').length,
        named: [...new Set(named)],
        caption: (el.closest('figure') && el.closest('figure').querySelector('figcaption') || { textContent: '' }).textContent.replace(/\s+/g, ' ').trim(),
      };
    });
  }
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
  const nMocks = await page.locator('#act article.mock').count();
  if (nMocks < 1) throw new Error('no Act mocks on the strategy board');
  for (let i = 0; i < nMocks; i++) {
    const name = `act-mock-${i + 1}.jpg`;
    await shot(page, '#act article.mock', name, { nth: i, source: STRATEGY + '#h-act' });
    manifest[name].info = await page.locator('#act article.mock').nth(i).evaluate((el) => {
      const clean = (n) => (n ? n.textContent.replace(/Illustrative/g, '').replace(/\s+/g, ' ').trim() : '');
      return {
        label: el.getAttribute('aria-label') || '',
        kicker: clean(el.querySelector('.kicker')).replace(/^\d+\s*/, ''),
        head: clean(el.querySelector('.mh, h3')),
        sections: [...el.querySelectorAll('h4')].map(clean).map((s) => s.replace(/^\d+\s*/, '')),
        ask: clean(el.querySelector('.ask')),
        illustrative: el.querySelectorAll('.illus').length,
      };
    });
  }
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
