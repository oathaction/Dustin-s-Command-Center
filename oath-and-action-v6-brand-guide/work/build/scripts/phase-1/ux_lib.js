// Shared helpers for the Phase 1 UX checks.
// Launches Chromium and answers Google Fonts requests with the Inter, Inter Tight and Lora files
// extracted from V5 Polished, so renders use the real faces without network access.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const FONT_DIR = (root) => path.join(root, 'work', 'extract', 'v5-polished', 'fonts');
const FACES = [
  ['Inter', 400, 'normal', 'Inter-400-normal.ttf'],
  ['Inter', 600, 'normal', 'Inter-600-normal.ttf'],
  ['Inter', 700, 'normal', 'Inter-700-normal.ttf'],
  ['Inter Tight', 600, 'normal', 'Inter-Tight-600-normal.ttf'],
  ['Inter Tight', 800, 'normal', 'Inter-Tight-800-normal.ttf'],
  ['Lora', 400, 'italic', 'Lora-Italic-400-normal.ttf'],
];

async function routeFonts(ctx, root) {
  const css = FACES.map(([fam, w, st, file]) =>
    `@font-face{font-family:'${fam}';font-style:${st};font-weight:${w};font-display:block;src:url(https://fonts.gstatic.com/oa-local/${file}) format('truetype')}`).join('\n');
  await ctx.route('https://fonts.googleapis.com/**', (r) => r.fulfill({ status: 200, contentType: 'text/css', headers: { 'Access-Control-Allow-Origin': '*' }, body: css }));
  await ctx.route('https://fonts.gstatic.com/oa-local/**', (r) => {
    const file = path.basename(new URL(r.request().url()).pathname);
    r.fulfill({ status: 200, contentType: 'font/ttf', headers: { 'Access-Control-Allow-Origin': '*' }, body: fs.readFileSync(path.join(FONT_DIR(root), file)) });
  });
}

async function launch() {
  return chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
}

// Persistent context with Chromium's default font size set, to emulate a reader's text-size setting.
async function launchWithFontSize(root, px, userDir) {
  fs.mkdirSync(path.join(userDir, 'Default'), { recursive: true });
  fs.writeFileSync(path.join(userDir, 'Default', 'Preferences'), JSON.stringify({ webkit: { webprefs: { default_font_size: px, default_fixed_font_size: Math.round(px * 0.8125) } } }));
  const ctx = await chromium.launchPersistentContext(userDir, { executablePath: '/opt/pw-browsers/chromium', viewport: { width: 1440, height: 900 } });
  await routeFonts(ctx, root);
  return ctx;
}

async function newPage(browser, root, opts = {}) {
  const ctx = await browser.newContext({
    viewport: { width: opts.width || 1440, height: opts.height || 900 },
    deviceScaleFactor: opts.dsf || 1,
    reducedMotion: opts.reduced ? 'reduce' : 'no-preference',
    forcedColors: opts.forced ? 'active' : 'none',
    acceptDownloads: true,
    permissions: opts.clipboard ? ['clipboard-read', 'clipboard-write'] : [],
  });
  await routeFonts(ctx, root);
  const page = await ctx.newPage();
  return { ctx, page };
}

async function settle(page) {
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.waitForTimeout(150);
}

module.exports = { launch, launchWithFontSize, newPage, routeFonts, settle };
