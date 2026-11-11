// Captures of the palette proof sheet (Phase 3, round 0, November 11, 2026).
// Usage: node work/boards/phase-3/round-0/palettes/capture_palette_proofs.js [--preview]
// Reads 20261111_Palette-Proofs.html beside this script and writes, beside it, at true size (device scale 1):
//   20261111_Palette-Proofs-<Section>-1440.png, and the same with -Grayscale, -Protanopia, -Deuteranopia, -Tritanopia
//   20261111_Palette-Proofs-Line-Code-1440-2x.png, the line code section at device scale 2
//   20261111_Palette-Proofs-Opening-1440.png, the sheet's opening, and -Page-390.png, the whole sheet at phone width
//   20261111_Palette-Proofs-Capture-Log.json, every capture with the position and token color of each probed swatch,
//   which build_palette_proofs.py --verify samples.
// --preview writes only the full page at 1440 to the scratchpad, for a look while the sheet is drawn.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const HERE = __dirname;
const PAGE = path.join(HERE, '20261111_Palette-Proofs.html');
const PREFIX = '20261111_Palette-Proofs';
const SCRATCH = '/tmp/claude-0/-home-user-Dustin-s-Command-Center/31ab6fca-308a-5402-b22c-b6bfd31a97ee/scratchpad/phase-3/round-0/palettes';
const SECTIONS = [
  ['sequential', 'Sequential'], ['diverging', 'Diverging'], ['categorical', 'Categorical'], ['past-four', 'Past-Four-Groups'],
  ['magnitude', 'Magnitude'], ['line-code', 'Line-Code'], ['red', 'Red-On-Red'], ['prussian', 'Prussian'],
];
const MODES = [['normal', ''], ['grayscale', '-Grayscale'], ['protanopia', '-Protanopia'], ['deuteranopia', '-Deuteranopia'], ['tritanopia', '-Tritanopia']];

async function open(page) {
  await page.goto('file://' + PAGE, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const fonts = await page.evaluate(() => [document.fonts.check('15px Inter'), document.fonts.check('600 15px Inter'), document.fonts.check('800 40px "Inter Tight"')]);
  if (fonts.includes(false)) throw new Error('fonts did not load: ' + JSON.stringify(fonts));
  await page.waitForTimeout(300);
}

async function setMode(page, mode) {
  await page.evaluate((m) => {
    if (m === 'normal') document.documentElement.removeAttribute('data-sim');
    else document.documentElement.setAttribute('data-sim', m);
  }, mode);
  await page.waitForTimeout(120);
}

async function probes(page, sel) {
  return page.evaluate((s) => {
    const root = document.querySelector(s);
    const r0 = root.getBoundingClientRect();
    return [...root.querySelectorAll('[data-probe]')].map((el) => {
      const r = el.getBoundingClientRect();
      return { kind: el.dataset.probe, hex: el.dataset.hex, ground: el.dataset.ground || null,
        x: r.left - r0.left, y: r.top - r0.top, w: r.width, h: r.height };
    });
  }, sel);
}

(async () => {
  const preview = process.argv.includes('--preview');
  const browser = await chromium.launch();
  const log = { page: path.basename(PAGE), date: '2026-11-11', captures: [] };
  let ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  let page = await ctx.newPage();
  await open(page);
  if (preview) {
    await page.screenshot({ path: path.join(SCRATCH, 'preview-1440.png'), fullPage: true });
    await browser.close();
    console.log('preview written');
    return;
  }
  for (const [id, name] of SECTIONS) {
    const sel = `section#${id}`;
    const pr = await probes(page, sel);
    for (const [mode, suffix] of MODES) {
      await setMode(page, mode);
      const file = `${PREFIX}-${name}-1440${suffix}.png`;
      await page.locator(sel).screenshot({ path: path.join(HERE, file) });
      log.captures.push({ file, section: id, mode, width: 1440, deviceScaleFactor: 1, probes: pr });
    }
    await setMode(page, 'normal');
  }
  const headH = await page.evaluate(() => { window.scrollTo(0, 0); return Math.round(document.querySelector('main').getBoundingClientRect().top + window.scrollY); });
  await page.screenshot({ path: path.join(HERE, `${PREFIX}-Opening-1440.png`), fullPage: true, clip: { x: 0, y: 0, width: 1440, height: headH } });
  log.captures.push({ file: `${PREFIX}-Opening-1440.png`, section: 'opening', mode: 'normal', width: 1440, deviceScaleFactor: 1, probes: [] });
  await ctx.close();

  ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  page = await ctx.newPage();
  await open(page);
  await page.locator('section#line-code').screenshot({ path: path.join(HERE, `${PREFIX}-Line-Code-1440-2x.png`) });
  log.captures.push({ file: `${PREFIX}-Line-Code-1440-2x.png`, section: 'line-code', mode: 'normal', width: 1440, deviceScaleFactor: 2, probes: [] });
  await ctx.close();

  ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  page = await ctx.newPage();
  await open(page);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  await page.screenshot({ path: path.join(HERE, `${PREFIX}-Page-390.png`), fullPage: true });
  log.captures.push({ file: `${PREFIX}-Page-390.png`, section: 'page', mode: 'normal', width: 390, deviceScaleFactor: 1, probes: [], pageOverflowPx: overflow });
  await ctx.close();
  await browser.close();
  fs.writeFileSync(path.join(HERE, `${PREFIX}-Capture-Log.json`), JSON.stringify(log, null, 1) + '\n');
  console.log(`wrote ${log.captures.length} captures; page overflow at 390 px: ${overflow} px`);
})().catch((err) => { console.error(err); process.exit(1); });
