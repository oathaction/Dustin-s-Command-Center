// Render checks for the combined Gate 1 review board.
//
// Usage: node check_gate1_board.js <project-root>
// Renders work/boards/20261021_Gate-1-Review-Board.html in Chromium at 1440 and 390 px, light and dark,
// inside a standard skeleton (doctype, charset, viewport, lang="en"), the way the publishing host serves
// the file. Records horizontal scroll, image loading, text under 13 px, heading levels, axe-core 4.10.2
// (wcag2a, wcag2aa, wcag21aa, wcag22aa), red outside specimens, alt text, tabular figures, keyboard focus,
// reduced motion, the copy control and the token ratios. Writes full-page screenshots to
// work/boards/screens/gate-1/ and the results to work/boards/phase-1/gate-1/20261021_Gate-1-Board-Check.json.
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(process.argv[2] || '.');
const BOARD = path.join(ROOT, 'work', 'boards', '20261021_Gate-1-Review-Board.html');
const SCREENS = path.join(ROOT, 'work', 'boards', 'screens', 'gate-1');
const RESULT = path.join(ROOT, 'work', 'boards', 'phase-1', 'gate-1', '20261021_Gate-1-Board-Check.json');
const AXE = path.join(ROOT, 'work', 'build', 'node_modules', 'axe-core', 'axe.min.js');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

function wcag(hex1, hex2) {
  const lum = (h) => {
    const c = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255).map((x) => (x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4));
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  };
  const [a, b] = [lum(hex1), lum(hex2)].sort((x, y) => y - x);
  return (a + 0.05) / (b + 0.05);
}

(async () => {
  fs.mkdirSync(SCREENS, { recursive: true });
  for (const f of fs.readdirSync(SCREENS)) if (/^gate1-.*\.png$/.test(f)) fs.unlinkSync(path.join(SCREENS, f));
  const raw = fs.readFileSync(BOARD, 'utf8');
  const wrappedPath = path.join(os.tmpdir(), 'gate1-board-wrapped.html');
  fs.writeFileSync(wrappedPath, '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' + raw + '</html>');
  const axeSource = fs.readFileSync(AXE, 'utf8');
  const axeVersion = (axeSource.match(/axe v([0-9.]+)/) || [])[1] || 'unknown';

  const results = {
    board: path.relative(ROOT, BOARD),
    checked: new Date().toISOString(),
    bytes: fs.statSync(BOARD).size,
    megabytes: +(fs.statSync(BOARD).size / 1048576).toFixed(2),
    underTenMegabytes: fs.statSync(BOARD).size < 10 * 1048576,
    startsWithTitle: raw.startsWith('<title>'),
    hasSkeletonTags: /<!doctype|<html|<head|<body/i.test(raw),
    externalScripts: (raw.match(/<script[^>]+src=/gi) || []).length,
    stylesheetLinks: (raw.match(/<link[^>]+rel="stylesheet"[^>]*>/gi) || []).map((l) => (l.match(/href="([^"]+)"/) || [])[1]),
    nonDataImageSources: (raw.match(/<img[^>]+src="(?!data:)[^"]*"/gi) || []).length,
    axeVersion,
    renderedIn: 'Chromium ' + chromium.name() + ', wrapped in a standard skeleton with lang="en"',
    views: [],
  };

  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  results.chromium = browser.version();
  for (const width of [1440, 390]) {
    for (const scheme of ['light', 'dark']) {
      const context = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme, deviceScaleFactor: 1 });
      await context.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'null' }).catch(() => {});
      const page = await context.newPage();
      const consoleErrors = [];
      page.on('pageerror', (e) => consoleErrors.push(String(e)));
      await page.goto('file://' + wrappedPath, { waitUntil: 'networkidle' });
      await page.evaluate(async () => { await document.fonts.ready; });
      const view = { width, scheme };

      Object.assign(view, await page.evaluate(() => {
        const out = {};
        const de = document.documentElement;
        out.scrollWidth = Math.max(de.scrollWidth, document.body.scrollWidth);
        out.clientWidth = de.clientWidth;
        out.horizontalScroll = out.scrollWidth > out.clientWidth;
        const imgs = [...document.images];
        out.images = imgs.length;
        out.imagesBroken = imgs.filter((i) => !(i.complete && i.naturalWidth > 0)).map((i) => i.alt.slice(0, 60));
        out.imagesWithoutAlt = imgs.filter((i) => !i.getAttribute('alt') || !i.getAttribute('alt').trim()).length;
        const svgs = [...document.querySelectorAll('svg')];
        out.inlineSvgs = svgs.length;
        out.svgsWithoutName = svgs.filter((s) => s.getAttribute('role') === 'img' && !s.getAttribute('aria-label')).length;
        out.svgsUnlabeledVisible = svgs.filter((s) => s.getAttribute('role') !== 'img' && s.getAttribute('aria-hidden') !== 'true' && !s.closest('[aria-hidden="true"]')).length;
        // Text under 13 px: every element that directly holds visible text.
        const small = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let n;
        const seen = new Set();
        while ((n = walker.nextNode())) {
          if (!n.textContent.trim()) continue;
          const el = n.parentElement;
          if (!el || seen.has(el) || el.closest('svg, script, style')) continue;
          seen.add(el);
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          const r = el.getBoundingClientRect();
          if (r.width === 0 && r.height === 0) continue;
          const fs = parseFloat(cs.fontSize);
          if (fs < 13) small.push({ size: fs, text: n.textContent.trim().slice(0, 50), tag: el.tagName });
        }
        out.textUnder13px = small;
        let minSize = Infinity;
        seen.forEach((el) => { minSize = Math.min(minSize, parseFloat(getComputedStyle(el).fontSize)); });
        out.smallestTextPx = minSize;
        // Headings
        const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((h) => +h.tagName[1]);
        out.headingCounts = hs.reduce((a, l) => ((a['h' + l] = (a['h' + l] || 0) + 1), a), {});
        out.h1Count = hs.filter((l) => l === 1).length;
        const skips = [];
        hs.forEach((l, i) => { if (i > 0 && l > hs[i - 1] + 1) skips.push(`h${hs[i - 1]} to h${l} at heading ${i + 1}`); });
        if (hs[0] !== 1) skips.push('first heading is not h1');
        out.headingSkips = skips;
        // Red outside specimens: the board's own interface must not use Pillar Red.
        const isRed = (c) => /rgba?\(\s*230,\s*57,\s*70/.test(c) || /rgba?\(\s*240,\s*98,\s*108/.test(c);
        const spec = '.spec, .tsurf, svg, img, .tokens';
        const reds = [];
        document.querySelectorAll('body *').forEach((el) => {
          if (el.closest(spec)) return;
          const cs = getComputedStyle(el);
          for (const p of ['color', 'backgroundColor', 'borderTopColor', 'borderLeftColor', 'outlineColor']) {
            if (isRed(cs[p]) && !(p.startsWith('border') && cs[p.replace('Color', 'Width')] === '0px') && !(p === 'outlineColor' && cs.outlineStyle === 'none')) reds.push(el.tagName + '.' + el.className + ' ' + p);
          }
        });
        out.redOutsideSpecimens = reds;
        // Tabular figures in table cells
        const cells = [...document.querySelectorAll('td, th')];
        out.tableCells = cells.length;
        out.cellsWithoutTabularFigures = cells.filter((c) => !getComputedStyle(c).fontVariantNumeric.includes('tabular-nums')).length;
        // Scroll regions are focusable and labeled
        const regions = [...document.querySelectorAll('.scroll, .table, .tall')];
        out.scrollRegions = regions.length;
        out.scrollRegionsNotFocusable = regions.filter((r) => r.tabIndex < 0 || !r.getAttribute('aria-label')).length;
        out.scrollBehavior = getComputedStyle(document.documentElement).scrollBehavior;
        // Token ratios against the WCAG formula
        out.tokenRows = [...document.querySelectorAll('.trow')].map((r) => ({ fg: r.dataset.fg, bg: r.dataset.bg, shown: +r.dataset.ratio, min: +r.dataset.min }));
        out.pageHeight = document.documentElement.scrollHeight;
        return out;
      }));
      view.tokenMismatches = view.tokenRows.filter((r) => Math.abs(+wcag(r.fg, r.bg).toFixed(2) - r.shown) > 0.005).length;
      view.tokenBelowMinimum = view.tokenRows.filter((r) => r.shown < r.min).length;
      view.tokenRows = view.tokenRows.length;

      // Keyboard: Tab to the first focusable elements and read the focus outline.
      const focus = [];
      for (let i = 0; i < 4; i++) {
        await page.keyboard.press('Tab');
        focus.push(await page.evaluate(() => {
          const el = document.activeElement;
          const cs = getComputedStyle(el);
          return { tag: el.tagName, text: (el.textContent || '').trim().slice(0, 30), outline: cs.outlineStyle + ' ' + cs.outlineWidth };
        }));
      }
      view.focusSample = focus;
      view.focusVisible = focus.every((f) => f.outline.startsWith('solid') && parseFloat(f.outline.split(' ')[1]) >= 2);
      // The copy control: click and read the status line.
      await page.click('#copy-btn');
      await page.waitForTimeout(300);
      view.copyStatus = await page.textContent('#copy-status');
      view.copyWorked = /Copied|selected/.test(view.copyStatus || '');

      // axe-core
      await page.addScriptTag({ content: axeSource });
      const axe = await page.evaluate(async () => {
        const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'] } });
        return { violations: r.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes.slice(0, 3).map((n) => n.target.join(' ') + ' :: ' + (n.failureSummary || '').slice(0, 160)) })), passes: r.passes.length, incomplete: r.incomplete.map((v) => ({ id: v.id, nodes: v.nodes.length })) };
      });
      view.axeViolations = axe.violations;
      view.axeViolationCount = axe.violations.reduce((a, v) => a + v.nodes, 0);
      view.axePassedRules = axe.passes;
      view.axeIncomplete = axe.incomplete;
      view.pageErrors = consoleErrors;

      // Screenshots in 2000 px tall chunks: a single full-page capture of a page this tall drops images.
      await page.evaluate(async () => { await Promise.all([...document.images].map((i) => i.decode().catch(() => null))); });
      await page.setViewportSize({ width, height: 2000 });
      const total = await page.evaluate(() => document.documentElement.scrollHeight);
      view.screenshots = [];
      for (let y = 0, k = 1; y < total; y += 2000, k++) {
        await page.evaluate((yy) => window.scrollTo(0, yy), y);
        await page.waitForTimeout(150);
        const shot = path.join(SCREENS, `gate1-${width}-${scheme}-${String(k).padStart(2, '0')}.png`);
        await page.screenshot({ path: shot });
        view.screenshots.push(path.relative(ROOT, shot));
      }
      results.views.push(view);
      await context.close();
    }
  }

  // Reduced motion: smooth scrolling switches off.
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  const p = await ctx.newPage();
  await p.goto('file://' + wrappedPath, { waitUntil: 'networkidle' });
  results.reducedMotion = { scrollBehaviorWhenReduced: await p.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior), animations: await p.evaluate(() => document.getAnimations().length) };
  await ctx.close();
  await browser.close();
  fs.unlinkSync(wrappedPath);

  const v = results.views;
  results.summary = {
    noHorizontalScroll: v.every((x) => !x.horizontalScroll),
    allImagesLoad: v.every((x) => x.imagesBroken.length === 0),
    noTextUnder13px: v.every((x) => x.textUnder13px.length === 0),
    oneH1NoSkips: v.every((x) => x.h1Count === 1 && x.headingSkips.length === 0),
    axeZeroViolations: v.every((x) => x.axeViolationCount === 0),
    noRedOutsideSpecimens: v.every((x) => x.redOutsideSpecimens.length === 0),
    allImagesHaveAlt: v.every((x) => x.imagesWithoutAlt === 0),
    tabularFiguresInTables: v.every((x) => x.cellsWithoutTabularFigures === 0),
    scrollRegionsFocusable: v.every((x) => x.scrollRegionsNotFocusable === 0),
    focusVisible: v.every((x) => x.focusVisible),
    copyControlResponds: v.every((x) => x.copyWorked),
    tokenRatiosMatchWcag: v.every((x) => x.tokenMismatches === 0),
    reducedMotionRespected: results.reducedMotion.scrollBehaviorWhenReduced === 'auto',
    underTenMegabytes: results.underTenMegabytes,
  };
  fs.writeFileSync(RESULT, JSON.stringify(results, null, 1));
  console.log(JSON.stringify(results.summary, null, 1));
  for (const x of v) console.log(x.width, x.scheme, 'scroll', x.scrollWidth, '/', x.clientWidth, 'imgs', x.images, 'broken', x.imagesBroken.length, 'small', x.textUnder13px.length, 'min', x.smallestTextPx, 'axe', x.axeViolationCount, JSON.stringify(x.axeViolations.map((a) => a.id + ':' + a.nodes)), 'red', x.redOutsideSpecimens.length, 'h', JSON.stringify(x.headingCounts), x.headingSkips.join(';'), 'height', x.pageHeight);
})().catch((e) => { console.error(e); process.exit(1); });
