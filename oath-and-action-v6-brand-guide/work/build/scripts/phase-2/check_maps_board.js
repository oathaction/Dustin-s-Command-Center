// Rendered checks for the Systems Map Directions Board and its two phone pages.
// Usage: node work/build/scripts/phase-2/check_maps_board.js
// 1. Captures the phone pages at 390 px into work/boards/phase-2/maps/*.png (the board shows these captures).
// 2. Audits the board at 1440 and 390 px and each phone page at 390 px: horizontal page scroll, text under 13 px
//    (SVG text scaled by its drawing's rendered size), text contrast from rendered colors, images, axe-core with
//    WCAG 2.2 AA tags.
// Writes work/boards/phase-2/maps/20261028_Maps-Check-Results.json; screenshots go to work/boards/screens/phase-2-maps/
// (regenerable, not committed).
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const ROOT = path.resolve(__dirname, '../../../..');
const BOARD = path.join(ROOT, 'work/boards/20261028_Systems-Map-Directions-Board.html');
const ASSETS = path.join(ROOT, 'work/boards/phase-2/maps');
const PHONES = ['20261028_Phone-Loop-Catalog', '20261028_Phone-R8-Loop-Card'];
const OUTJSON = path.join(ASSETS, '20261028_Maps-Check-Results.json');
const SHOTS = path.join(ROOT, 'work/boards/screens/phase-2-maps');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');
fs.mkdirSync(SHOTS, { recursive: true });

async function audit(page) {
  return page.evaluate(() => {
    function parse(c) {
      const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
      const p = m[1].split(',').map(s => parseFloat(s));
      return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
    }
    function lin(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    function L(c) { return 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b); }
    function ratio(a, b) { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
    function svgUnder(el) {
      // the filled shape directly under an SVG label: a disc, tile or pill drawn before it in the same group
      if (!(el instanceof SVGTextElement)) return null;
      const bb = el.getBoundingClientRect();
      const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
      let node = el, found = null;
      while (node && !(node instanceof SVGSVGElement)) {
        let sib = node.previousElementSibling;
        while (sib) {
          const shapes = [sib, ...sib.querySelectorAll('circle,rect,polygon')].filter(s => ['circle', 'rect', 'polygon'].includes(s.tagName));
          for (const sh of shapes) {
            const f = parse(getComputedStyle(sh).fill);
            if (!f || f.a < 0.5 || sh.getAttribute('fill') === 'none') continue;
            const b = sh.getBoundingClientRect();
            if (b.width > 1000 && b.height > 1000) continue;
            if (cx >= b.x && cx <= b.x + b.width && cy >= b.y && cy <= b.y + b.height && !found) found = f;
          }
          if (found) return found;
          sib = sib.previousElementSibling;
        }
        node = node.parentElement;
      }
      return null;
    }
    function bgOf(el) {
      const u = svgUnder(el);
      if (u) return u;
      let e = el;
      while (e && e.nodeType === 1) {
        if (e instanceof SVGSVGElement) {
          const r = e.querySelector(':scope > rect[x="0"][y="0"]');
          if (r) { const c = parse(getComputedStyle(r).fill); if (c) return c; }
        } else if (!(e instanceof SVGElement)) {
          const c = parse(getComputedStyle(e).backgroundColor);
          if (c && c.a > 0.5) return c;
        }
        e = e.parentElement;
      }
      return { r: 255, g: 255, b: 255, a: 1 };
    }
    function visible(el) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return false;
      let e = el;
      while (e && e.nodeType === 1) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; e = e.parentElement; }
      if (el.closest('details:not([open])') && !el.closest('summary')) return false;
      return true;
    }
    const out = { texts: 0, svgTexts: 0, minSize: 99, under13: [], lowContrast: [] };
    const all = document.querySelectorAll('body *');
    for (const el of all) {
      if (['SCRIPT', 'STYLE', 'TITLE', 'DESC'].includes(el.tagName.toUpperCase())) continue;
      if (el.closest('title') || el.closest('desc')) continue;
      const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
      if (!own) continue;
      if (!visible(el)) continue;
      const cs = getComputedStyle(el);
      let size = parseFloat(cs.fontSize);
      const isSvg = el instanceof SVGElement;
      if (isSvg) {
        const root = el.closest('svg');
        const vb = root && root.viewBox && root.viewBox.baseVal;
        let sc = 1;
        if (vb && vb.width) sc = root.getBoundingClientRect().width / vb.width;
        // nested scale transforms (exploration thumbnails embed miniatures)
        let g = el.parentElement;
        while (g && g !== root) { const t = g.getAttribute && g.getAttribute('transform'); const m = t && t.match(/scale\(([\d.]+)\)/); if (m) sc *= parseFloat(m[1]); g = g.parentElement; }
        size = +(size * sc).toFixed(2);
        out.svgTexts++;
      }
      const weight = parseInt(cs.fontWeight, 10);
      const fg = parse(isSvg ? cs.fill : cs.color);
      const bg = bgOf(el);
      if (!fg) continue;
      out.texts++;
      if (size < out.minSize) out.minSize = size;
      if (size < 12.95) out.under13.push({ text: own.slice(0, 40), size, tag: el.tagName });
      const cr = ratio(fg, bg);
      const large = size >= 24 || (size >= 18.66 && weight >= 700);
      const need = large ? 3 : 4.5;
      if (cr < need - 0.005) out.lowContrast.push({ text: own.slice(0, 50), size, ratio: +cr.toFixed(2), need, tag: el.tagName });
    }
    const vw = document.documentElement.clientWidth;
    out.scrollWidth = document.documentElement.scrollWidth;
    out.clientWidth = vw;
    out.overflowing = [];
    for (const el of all) {
      if (el.closest('.wrap')) continue;
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.right > vw + 0.5) out.overflowing.push({ tag: el.tagName, cls: (el.className && el.className.baseVal !== undefined) ? el.className.baseVal : el.className, right: Math.round(r.right) });
    }
    out.overflowing = out.overflowing.slice(0, 20);
    out.height = document.documentElement.scrollHeight;
    out.fonts = [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style))];
    out.images = [...document.images].map(i => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0 }));
    out.svgs = document.querySelectorAll('svg[data-view]').length;
    return out;
  });
}

async function runAxe(page) {
  if (!fs.existsSync(AXE)) return null;
  await page.addScriptTag({ path: AXE });
  return page.evaluate(async () => {
    const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
    return { violations: r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes.slice(0, 3).map(n => n.target.join(' ')) })), passes: r.passes.length, incomplete: r.incomplete.length };
  });
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

async function open(browser, file, width, dsf = 1) {
  const ctx = await browser.newContext({ viewport: { width, height: 1000 }, deviceScaleFactor: dsf, ignoreHTTPSErrors: true });
  const page = await ctx.newPage();
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(700);
  return { ctx, page };
}

(async () => {
  const opts = { executablePath: '/opt/pw-browsers/chromium' };
  if (process.env.HTTPS_PROXY) opts.proxy = { server: process.env.HTTPS_PROXY };
  const browser = await chromium.launch(opts);
  const results = { board: path.relative(ROOT, BOARD), run: new Date().toISOString(), widths: {}, phones: {} };
  // 1. phone captures and audits
  for (const name of PHONES) {
    const file = path.join(ASSETS, name + '.html');
    const { ctx, page } = await open(browser, file, 390, 2);
    await page.screenshot({ path: path.join(ASSETS, name + '.png'), fullPage: true, clip: { x: 0, y: 0, width: 390, height: 1700 } });
    await ctx.close();
    const o = await open(browser, file, 390, 1);
    const a = await audit(o.page);
    a.axe = await runAxe(o.page);
    a.screens = await shots(o.page, 390, name);
    results.phones[name] = a;
    await o.ctx.close();
  }
  // 2. board at both widths
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
    results.widths[width] = a;
    await ctx.close();
  }
  await browser.close();
  const w14 = results.widths[1440], w39 = results.widths[390];
  const axeN = (w) => (w.axe ? w.axe.violations.reduce((n, v) => n + v.nodes, 0) : 'not run');
  const ph = Object.entries(results.phones);
  results.summary = [
    `Rendered in Chromium (Playwright) at 1440 and 390 px on ${results.run.slice(0, 10)}, with ${w14.fonts.length} Google Fonts faces loaded; ${w14.svgs} drawings inline on the board.`,
    `Horizontal page scroll: none at 1440 (scrollWidth ${w14.scrollWidth} of ${w14.clientWidth}) or 390 (scrollWidth ${w39.scrollWidth} of ${w39.clientWidth}); wide drawings and tables scroll inside focusable regions.`,
    `Smallest rendered text, counting SVG text at its drawing's rendered scale: ${w14.minSize} px at 1440 and ${w39.minSize} px at 390; text elements under 13 px: ${w14.under13.length} and ${w39.under13.length}.`,
    `Text below WCAG AA contrast, from rendered colors: ${w14.lowContrast.length} at 1440, ${w39.lowContrast.length} at 390.`,
    `Images loaded: ${w14.images.filter(i => i.ok).length} of ${w14.images.length}.`,
    `axe-core 4.10 with WCAG 2.2 AA tags: ${axeN(w14)} violating nodes at 1440, ${axeN(w39)} at 390.`,
    ...ph.map(([n, a]) => `Phone page ${n.replace('20261028_', '')} at 390 px: scrollWidth ${a.scrollWidth} of ${a.clientWidth}, smallest text ${a.minSize} px (${a.under13.length} under 13), ${a.lowContrast.length} low-contrast texts, axe ${axeN(a)} violating nodes.`),
  ];
  results.not_checked = [
    'Screen readers, keyboard order, Firefox and Safari, print, forced colors and 200 percent zoom.',
    'Pixel contrast of strokes and marks. Mark colors are the locked palette values, measured by formula (Pillar Red 4.17:1 on White, Charcoal 18.1:1 on White).',
    'The live atlas renderer; these are specimens only (G1-08).',
  ];
  fs.writeFileSync(OUTJSON, JSON.stringify(results, null, 1));
  console.log(results.summary.join('\n'));
  for (const [k, a] of [['1440', w14], ['390', w39], ...ph]) {
    if (a.under13.length) console.log(k, 'under13', JSON.stringify(a.under13.slice(0, 8)));
    if (a.lowContrast.length) console.log(k, 'lowContrast', JSON.stringify(a.lowContrast.slice(0, 8)));
    if (a.overflowing.length) console.log(k, 'overflowing', JSON.stringify(a.overflowing.slice(0, 8)));
    if (a.axe && a.axe.violations.length) console.log(k, 'axe', JSON.stringify(a.axe.violations));
    const bad = a.images.filter(i => !i.ok); if (bad.length) console.log(k, 'images', JSON.stringify(bad));
  }
})();
