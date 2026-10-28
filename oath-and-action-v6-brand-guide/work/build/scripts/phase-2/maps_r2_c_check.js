// Direction C, Loop Lines: rendered checks, captures, grayscale proofs and the 24 by 36 inch poster PDF.
// Usage: node work/build/scripts/phase-2/maps_r2_c_check.js
// Reuses round one's audit and axe functions from check_maps_board.js, read from its source unchanged (that file
// runs its own board when required, so its functions are lifted as text): horizontal scroll, text under 13 px
// (SVG text at its rendered scale), text contrast from rendered colors against the drawn ground, images, axe-core
// 4.10.2 with WCAG 2.2 AA tags.
// 1. Each page at its own width: audit, axe, a capture and a grayscale proof into work/boards/phase-2/maps-r2/c/.
// 2. The poster print page to PDF at 36 by 24 inches.
// 3. The board at 1440 and 390 px: audit, axe, screenshots (work/boards/screens/phase-2-maps-r2-c/, regenerable).
// 4. 2x crops of the poster and the cards for the maker's review (scratchpad folder given in CROPS, if set).
// Writes work/boards/phase-2/maps-r2/c/20261028_Loop-Lines-Check-Results.json
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const ROOT = path.resolve(__dirname, '../../../..');
const ASSETS = path.join(ROOT, 'work/boards/phase-2/maps-r2/c');
const BOARD = path.join(ROOT, 'work/boards/20261028_Map-Direction-C-Loop-Lines.html');
const SHOTS = path.join(ROOT, 'work/boards/screens/phase-2-maps-r2-c');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');
const OUTJSON = path.join(ASSETS, '20261028_Loop-Lines-Check-Results.json');
const CROPS = process.env.CROPS || '';
fs.mkdirSync(SHOTS, { recursive: true });

// lift audit() and runAxe() from round one's checker, unchanged
const src = fs.readFileSync(path.join(__dirname, 'check_maps_board.js'), 'utf8');
const lifted = src.slice(src.indexOf('async function audit(page)'), src.indexOf('async function shots('));
const { audit, runAxe } = new Function('fs', 'path', 'AXE', lifted + '\nreturn { audit, runAxe };')(fs, path, AXE);

const PAGES = [
  ['Poster', 1440, 960], ['Working-Map', 1440, 960], ['Reform-View-R-01', 1440, 960],
  ['Catalog', 1440, 0], ['Catalog-Phone', 390, 0],
  ['Card-R8', 1440, 0], ['Card-R8-Phone', 390, 0], ['Card-R10', 1440, 0], ['Card-R10-Phone', 390, 0],
];

async function open(browser, file, width, dsf = 1, height = 1000) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: dsf, ignoreHTTPSErrors: true });
  const page = await ctx.newPage();
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  return { ctx, page };
}

async function shots(page, width, tag) {
  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  const slice = 3000; const parts = [];
  for (let y = 0, i = 0; y < total; y += slice, i++) {
    const h = Math.min(slice, total - y);
    const p = path.join(SHOTS, `${tag}-${width}-${String(i).padStart(2, '0')}.png`);
    await page.screenshot({ path: p, fullPage: true, clip: { x: 0, y, width, height: h } });
    parts.push(path.relative(ROOT, p));
  }
  return parts;
}

(async () => {
  const opts = { executablePath: '/opt/pw-browsers/chromium' };
  if (process.env.HTTPS_PROXY) opts.proxy = { server: process.env.HTTPS_PROXY };
  const browser = await chromium.launch(opts);
  const results = { run: new Date().toISOString(), pages: {}, board: {}, pdf: null };
  // 1. pages
  for (const [name, width, height] of PAGES) {
    const file = path.join(ASSETS, `20261028_Loop-Lines-${name}.html`);
    const { ctx, page } = await open(browser, file, width, 1, height || 1000);
    const a = await audit(page);
    a.axe = await runAxe(page);
    const cap = path.join(ASSETS, `20261028_Loop-Lines-${name}-Capture.png`);
    const full = !height;
    await page.screenshot({ path: cap, fullPage: full, clip: full ? undefined : { x: 0, y: 0, width, height } });
    await page.addStyleTag({ content: 'html{filter:grayscale(1)}' });
    await page.waitForTimeout(150);
    const gray = path.join(ASSETS, `20261028_Loop-Lines-${name}-Grayscale.png`);
    await page.screenshot({ path: gray, fullPage: full, clip: full ? undefined : { x: 0, y: 0, width, height } });
    a.capture = path.relative(ROOT, cap);
    a.grayscale = path.relative(ROOT, gray);
    results.pages[name] = a;
    await ctx.close();
  }
  // 2. poster PDF at 36 by 24 inches
  {
    const ctx = await browser.newContext();
    const page = await ctx.newPage();
    await page.goto('file://' + path.join(ASSETS, '20261028_Loop-Lines-Poster-Print.html'), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    const pdf = path.join(ASSETS, '20261028_Loop-Lines-Poster-24x36.pdf');
    await page.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
    results.pdf = { file: path.relative(ROOT, pdf), bytes: fs.statSync(pdf).size };
    await ctx.close();
  }
  // 3. board
  if (fs.existsSync(BOARD)) {
    for (const width of [1440, 390]) {
      const { ctx, page } = await open(browser, BOARD, width, 1);
      const a = await audit(page);
      a.axe = await runAxe(page);
      a.screens = await shots(page, width, 'board');
      if (width === 1440) {
        await page.addStyleTag({ content: 'html{filter:grayscale(1)}' });
        await page.waitForTimeout(200);
        a.grayScreens = await shots(page, width, 'board-grayscale');
      }
      results.board[width] = a;
      await ctx.close();
    }
  }
  // 4. 2x crops for review
  if (CROPS) {
    fs.mkdirSync(CROPS, { recursive: true });
    const { ctx, page } = await open(browser, path.join(ASSETS, '20261028_Loop-Lines-Poster.html'), 1440, 2, 960);
    const tiles = [[0, 0], [480, 0], [960, 0], [0, 320], [480, 320], [960, 320], [0, 640], [480, 640], [960, 640]];
    for (const [x, y] of tiles) await page.screenshot({ path: path.join(CROPS, `poster2x-${x}-${y}.png`), clip: { x, y, width: 480, height: 320 } });
    await ctx.close();
    for (const name of ['Catalog', 'Card-R8', 'Card-R10']) {
      const o = await open(browser, path.join(ASSETS, `20261028_Loop-Lines-${name}.html`), 1440, 2);
      await o.page.screenshot({ path: path.join(CROPS, `${name}-2x.png`), fullPage: true });
      await o.ctx.close();
    }
  }
  await browser.close();
  const axeN = (w) => (w && w.axe ? w.axe.violations.reduce((n, v) => n + v.nodes, 0) : 'not run');
  const lines = [];
  for (const [name, a] of Object.entries(results.pages)) {
    lines.push(`${name} at ${PAGES.find(p => p[0] === name)[1]} px: scrollWidth ${a.scrollWidth} of ${a.clientWidth}, smallest text ${a.minSize} px (${a.under13.length} under 13), ${a.lowContrast.length} low-contrast texts, images ${a.images.filter(i => i.ok).length}/${a.images.length}, axe ${axeN(a)} violating nodes.`);
  }
  for (const [w, a] of Object.entries(results.board)) {
    lines.push(`Board at ${w} px: scrollWidth ${a.scrollWidth} of ${a.clientWidth}, smallest text ${a.minSize} px (${a.under13.length} under 13), ${a.lowContrast.length} low-contrast texts, images ${a.images.filter(i => i.ok).length}/${a.images.length}, axe ${axeN(a)} violating nodes, fonts ${a.fonts.length}.`);
  }
  lines.push(`Poster PDF: ${results.pdf.file}, ${(results.pdf.bytes / 1024).toFixed(0)} KB, page size 36 by 24 inches.`);
  results.summary = lines;
  results.not_checked = [
    'Screen readers, keyboard order, Firefox and Safari, forced colors and 200 percent zoom.',
    'Pixel contrast of strokes and marks. Mark colors are locked palette values, measured by formula.',
    'A printed proof of the PDF; the PDF was checked for page size and rendering in Chromium only.',
  ];
  fs.writeFileSync(OUTJSON, JSON.stringify(results, null, 1));
  console.log(lines.join('\n'));
  for (const [k, a] of [...Object.entries(results.pages), ...Object.entries(results.board)]) {
    if (a.under13.length) console.log(k, 'under13', JSON.stringify(a.under13.slice(0, 6)));
    if (a.lowContrast.length) console.log(k, 'lowContrast', JSON.stringify(a.lowContrast.slice(0, 6)));
    if (a.overflowing.length) console.log(k, 'overflowing', JSON.stringify(a.overflowing.slice(0, 6)));
    if (a.axe && a.axe.violations.length) console.log(k, 'axe', JSON.stringify(a.axe.violations));
    const bad = a.images.filter(i => !i.ok); if (bad.length) console.log(k, 'images', JSON.stringify(bad));
  }
})();
