// Check the Civic Line catalog page in Chromium.
// Usage: node check_catalog.js <catalog.html> <screens dir> <axe.min.js>
// Wraps the file in the publish skeleton (charset, viewport with viewport-fit=cover,
// the small reset), then at 1440 and 390 px in light and dark: runs axe-core,
// measures horizontal scroll, takes screenshots, and exercises search, the sheet
// filter, the edition and size controls, the detail view, keyboard focus,
// reduced motion, explicit data-theme overrides and blocked localStorage.
const fs = require('fs');
const path = require('path');
const os = require('os');

function loadPlaywright() {
  try { return require('playwright'); } catch (e) { /* fall through */ }
  const { execSync } = require('child_process');
  return require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
}

const SKELETON_HEAD = '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">' +
  '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}' +
  'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>';

(async () => {
  const [file, outDir, axePath] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const page0 = fs.readFileSync(file, 'utf8');
  const wrapped = path.join(os.tmpdir(), `civic-line-catalog-check-${process.pid}.html`);
  fs.writeFileSync(wrapped, SKELETON_HEAD + page0 + '</body></html>');
  const { chromium } = loadPlaywright();
  const proxy = process.env.HTTPS_PROXY || process.env.https_proxy;
  const launch = { args: [] };
  if (proxy) launch.proxy = { server: proxy };
  let browser;
  try { browser = await chromium.launch(launch); } catch (e) { browser = await chromium.launch({ ...launch, executablePath: '/opt/pw-browsers/chromium' }); }
  const results = { file: path.basename(file), bytes: fs.statSync(file).size, runs: [], functional: {} };
  const blocked = [];

  async function newPage(opts, init) {
    const ctx = await browser.newContext({ ignoreHTTPSErrors: true, deviceScaleFactor: 1, ...opts });
    if (init) await ctx.addInitScript(init);
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('requestfailed', (r) => blocked.push(r.url().slice(0, 100)));
    await page.goto('file://' + wrapped, { waitUntil: 'load', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    return { ctx, page, errors };
  }
  async function axe(page) {
    await page.addScriptTag({ path: axePath });
    return page.evaluate(async () => {
      const r = await window.axe.run(document, { resultTypes: ['violations'] });
      return { version: window.axe.version, violations: r.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length,
        help: v.help, sample: v.nodes.slice(0, 3).map((n) => n.target.join(' ')) })) };
    });
  }
  async function hscroll(page) {
    return page.evaluate(() => ({ docScroll: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      bodyScroll: document.body.scrollWidth - document.body.clientWidth }));
  }

  for (const [w, h] of [[1440, 900], [390, 844]]) {
    for (const scheme of ['light', 'dark']) {
      const { ctx, page, errors } = await newPage({ viewport: { width: w, height: h }, colorScheme: scheme });
      const tag = `${w}-${scheme}`;
      const info = await page.evaluate(() => ({
        cards: document.querySelectorAll('.cell:not([hidden])').length,
        bg: getComputedStyle(document.body).backgroundColor,
        fontsLoaded: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family} ${f.weight}`),
        interTight: document.fonts.check('700 30px "Inter Tight"'),
        tileBg: getComputedStyle(document.querySelector('.tile')).backgroundColor,
      }));
      const scroll = await hscroll(page);
      await page.screenshot({ path: path.join(outDir, `${tag}.png`) });
      await page.screenshot({ path: path.join(outDir, `${tag}-full.png`), fullPage: true });
      const a = await axe(page);
      // detail view
      await page.click('[data-open="R-35"]');
      await page.waitForSelector('dialog[open] .view img');
      await page.waitForFunction(() => { const i = document.querySelector('dialog[open] .view img'); return i && i.complete && i.naturalWidth > 0; });
      const det = await page.evaluate(() => {
        const d = document.querySelector('dialog[open]');
        const img = d.querySelector('.view img');
        const svg = d.querySelector('.view svg');
        const r1 = img.getBoundingClientRect(), r2 = svg.getBoundingClientRect();
        return { title: d.querySelector('h2').textContent, imgNatural: [img.naturalWidth, img.naturalHeight],
          imgShown: [Math.round(r1.width), Math.round(r1.height)], svgShown: [Math.round(r2.width), Math.round(r2.height)],
          dialogScroll: d.scrollWidth - d.clientWidth, raised: getComputedStyle(d).backgroundColor,
          corrections: d.querySelectorAll('ol.corr li').length };
      });
      const scrollDetail = await hscroll(page);
      await page.screenshot({ path: path.join(outDir, `${tag}-detail.png`) });
      const aDetail = await axe(page);
      await page.keyboard.press('Escape');
      const afterClose = await page.evaluate(() => ({ open: !!document.querySelector('dialog[open]'),
        focus: document.activeElement && document.activeElement.getAttribute('data-open') }));
      results.runs.push({ tag, info, scroll, axe: a, detail: det, scrollDetail, axeDetail: aDetail, afterClose, errors });
      await ctx.close();
    }
  }

  // functional checks at 1440 light
  {
    const { ctx, page, errors } = await newPage({ viewport: { width: 1440, height: 900 }, colorScheme: 'light' });
    const F = results.functional;
    F.initialVisible = await page.evaluate(() => document.querySelectorAll('.cell:not([hidden])').length);
    await page.fill('#q', 'term limits');
    F.searchTermLimits = await page.evaluate(() => [...document.querySelectorAll('.cell:not([hidden])')].map((c) => c.dataset.id));
    await page.fill('#q', 'r-35');
    F.searchR35 = await page.evaluate(() => [...document.querySelectorAll('.cell:not([hidden])')].map((c) => c.dataset.id));
    await page.fill('#q', 'cl-021');
    F.searchCL021 = await page.evaluate(() => [...document.querySelectorAll('.cell:not([hidden])')].map((c) => c.dataset.id));
    await page.fill('#q', 'zzzz');
    F.emptyState = await page.evaluate(() => ({ visible: document.querySelectorAll('.cell:not([hidden])').length,
      emptyShown: !document.getElementById('empty').hidden, text: document.getElementById('empty').textContent.trim() }));
    await page.click('#clear');
    await page.selectOption('#sheet', '04');
    F.sheet04 = await page.evaluate(() => ({ visible: document.querySelectorAll('.cell:not([hidden])').length,
      count: document.getElementById('count').textContent }));
    await page.selectOption('#sheet', '');
    const accentStroke = () => page.evaluate(() => {
      const el = document.querySelector('[data-id="CL-021"] svg [id$="accent"] path');
      return getComputedStyle(el).stroke;
    });
    F.accentRedBlack = await accentStroke();
    await page.click('label:has(#ed-bk)');
    F.accentBlack = await accentStroke();
    await page.click('label:has(#ed-rb)');
    await page.click('.seg label:has(input[value="128"])');
    F.size128 = await page.evaluate(() => document.querySelector('.ic').getBoundingClientRect().width);
    await page.click('.seg label:has(input[value="24"])');
    F.size24 = await page.evaluate(() => document.querySelector('.ic').getBoundingClientRect().width);
    F.scroll24 = await hscroll(page);
    // keyboard: on a fresh page the first Tab lands on the search field with a visible outline
    {
      const k = await newPage({ viewport: { width: 1440, height: 900 }, colorScheme: 'light' });
      await k.page.keyboard.press('Tab');
      F.firstTab = await k.page.evaluate(() => ({ id: document.activeElement.id, outline: getComputedStyle(document.activeElement).outlineStyle,
        width: getComputedStyle(document.activeElement).outlineWidth }));
      const stops = [];
      for (let i = 0; i < 4; i++) {
        await k.page.keyboard.press('Tab');
        stops.push(await k.page.evaluate(() => document.activeElement.id || document.activeElement.name || document.activeElement.getAttribute('data-open')));
      }
      F.tabOrder = stops;
      F.cardFocus = await k.page.evaluate(() => ({ card: document.activeElement.getAttribute('data-open'),
        outline: getComputedStyle(document.activeElement).outlineStyle, width: getComputedStyle(document.activeElement).outlineWidth }));
      await k.ctx.close();
    }
    // tab to a card, open with Enter, step with Next, close with Escape
    await page.focus('[data-open="CL-001"]');
    await page.keyboard.press('Enter');
    F.enterOpens = await page.evaluate(() => !!document.querySelector('dialog[open]') && document.querySelector('dialog h2').textContent);
    await page.click('dialog [data-step="1"]');
    F.nextGoesTo = await page.evaluate(() => document.querySelector('dialog h2').textContent);
    F.hash = await page.evaluate(() => location.hash);
    await page.keyboard.press('Escape');
    F.escapeCloses = await page.evaluate(() => !document.querySelector('dialog[open]'));
    F.errors = errors;
    await ctx.close();
  }
  // hash opens a detail view
  {
    const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: { width: 1024, height: 800 } });
    const page = await ctx.newPage();
    await page.goto('file://' + wrapped + '#r-35', { waitUntil: 'load' });
    results.functional.hashOpens = await page.evaluate(() => !!document.querySelector('dialog[open]') && document.querySelector('dialog h2').textContent);
    await ctx.close();
  }
  // explicit theme overrides
  for (const [scheme, theme] of [['light', 'dark'], ['dark', 'light']]) {
    const { ctx, page } = await newPage({ viewport: { width: 1024, height: 800 }, colorScheme: scheme });
    await page.evaluate((t) => document.documentElement.setAttribute('data-theme', t), theme);
    results.functional[`os-${scheme}-theme-${theme}`] = await page.evaluate(() => ({ bg: getComputedStyle(document.body).backgroundColor,
      text: getComputedStyle(document.body).color, tile: getComputedStyle(document.querySelector('.tile')).backgroundColor }));
    if (theme === 'dark') await page.screenshot({ path: path.join(outDir, `1024-data-theme-dark.png`) });
    await ctx.close();
  }
  // reduced motion
  {
    const { ctx, page } = await newPage({ viewport: { width: 1024, height: 800 }, reducedMotion: 'reduce' });
    results.functional.reducedMotionTransition = await page.evaluate(() => getComputedStyle(document.querySelector('.tile')).transitionDuration);
    await ctx.close();
    const n = await newPage({ viewport: { width: 1024, height: 800 }, reducedMotion: 'no-preference' });
    results.functional.normalMotionTransition = await n.page.evaluate(() => getComputedStyle(document.querySelector('.tile')).transitionDuration);
    await n.ctx.close();
  }
  // storage that throws
  {
    const init = () => { Object.defineProperty(window, 'localStorage', { get() { throw new Error('blocked'); } }); };
    const { ctx, page, errors } = await newPage({ viewport: { width: 1024, height: 800 } }, init);
    results.functional.storageBlocked = await page.evaluate(() => document.querySelectorAll('.cell:not([hidden])').length);
    await page.click('label:has(#ed-bk)');
    results.functional.storageBlockedEditionWorks = await page.evaluate(() => document.getElementById('catalog').dataset.edition);
    results.functional.storageBlockedErrors = errors;
    await ctx.close();
  }
  results.failedRequests = [...new Set(blocked)];
  fs.writeFileSync(path.join(outDir, 'check.json'), JSON.stringify(results, null, 2));
  fs.unlinkSync(wrapped);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
