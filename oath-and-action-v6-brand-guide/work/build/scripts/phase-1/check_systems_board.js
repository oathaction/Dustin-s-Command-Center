// Rendered checks for the Systems Marks Board at 1440 and 390 px.
// Usage: node work/build/scripts/phase-1/check_systems_board.js
// Writes work/boards/phase-1/systems/20261021_Board-Check-Results.json and screenshots (regenerable, not committed)
// to work/boards/screens/phase-1-systems/.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const ROOT = path.resolve(__dirname, '../../../..');
const BOARD = path.join(ROOT, 'work/boards/20261021_Systems-Marks-Board.html');
const OUTJSON = path.join(ROOT, 'work/boards/phase-1/systems/20261021_Board-Check-Results.json');
const SHOTS = path.join(ROOT, 'work/boards/screens/phase-1-systems');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');
fs.mkdirSync(SHOTS, { recursive: true });

async function audit(page) {
  return page.evaluate(() => {
    function parse(c) {
      const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
      const p = m[1].split(',').map(s => parseFloat(s));
      return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
    }
    function lin(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    function L(c) { return 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b); }
    function gray(c) { const y = Math.round(0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b); return { r: y, g: y, b: y, a: c.a }; }
    function ratio(a, b) { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
    function bgOf(el) {
      let e = el;
      while (e && e.nodeType === 1) {
        if (!(e instanceof SVGElement)) {
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
      return true;
    }
    const out = { texts: 0, minSize: 99, under13: [], lowContrast: [], chips: {} };
    const all = document.querySelectorAll('body *');
    for (const el of all) {
      if (['SCRIPT', 'STYLE', 'TITLE'].includes(el.tagName)) continue;
      if (el.closest('title')) continue;
      const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
      if (!own) continue;
      if (!visible(el)) continue;
      const cs = getComputedStyle(el);
      let size = parseFloat(cs.fontSize);
      if (el instanceof SVGElement) {
        const root = el.closest('svg');
        const vb = root && root.viewBox && root.viewBox.baseVal;
        if (vb && vb.width) { const sc = root.getBoundingClientRect().width / vb.width; size = +(size * sc).toFixed(2); }
      }
      const weight = parseInt(cs.fontWeight, 10);
      const isSvg = el instanceof SVGElement;
      let fg = parse(isSvg ? cs.fill : cs.color);
      let bg = bgOf(el);
      if (!fg) continue;
      const inGray = !!el.closest('.gray');
      if (inGray) { fg = gray(fg); bg = gray(bg); }
      const op = parseFloat(cs.opacity);
      const cr = ratio(fg, bg);
      out.texts++;
      if (size < out.minSize) out.minSize = size;
      if (size < 13) out.under13.push({ text: own.slice(0, 40), size, tag: el.tagName });
      const large = size >= 24 || (size >= 18.66 && weight >= 700);
      const need = large ? 3 : 4.5;
      if (cr < need - 0.005 && op > 0.1) out.lowContrast.push({ text: own.slice(0, 50), size, ratio: +cr.toFixed(2), need, tag: el.tagName, gray: inGray });
      if (el.classList.contains('k') || el.classList.contains('c')) {
        if (el.parentElement && el.parentElement.classList.contains('chip')) {
          const s = el.closest('[class^="s-"],[class*=" s-"]');
          const key = (s ? [...s.classList].find(c => c.startsWith('s-')) : 'none') + (inGray ? '-gray' : '');
          const part = el.classList.contains('k') ? 'kind' : 'code';
          out.chips[key] = out.chips[key] || { kind: 99, code: 99, minSize: 99, count: 0 };
          out.chips[key][part] = Math.min(out.chips[key][part], +cr.toFixed(2));
          out.chips[key].minSize = Math.min(out.chips[key].minSize, size);
          out.chips[key].count++;
        }
      }
    }
    // overflow
    const vw = document.documentElement.clientWidth;
    out.scrollWidth = document.documentElement.scrollWidth;
    out.clientWidth = vw;
    out.overflowing = [];
    for (const el of all) {
      if (el.closest('.wrap')) continue;
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.right > vw + 0.5) out.overflowing.push({ tag: el.tagName, cls: el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className, right: Math.round(r.right) });
    }
    out.overflowing = out.overflowing.slice(0, 30);
    out.height = document.documentElement.scrollHeight;
    out.fontsLoaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style);
    out.images = [...document.images].map(i => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0 }));
    return out;
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

(async () => {
  const opts = { executablePath: '/opt/pw-browsers/chromium' };
  if (process.env.HTTPS_PROXY) opts.proxy = { server: process.env.HTTPS_PROXY };
  const browser = await chromium.launch(opts);
  const results = { board: path.relative(ROOT, BOARD), run: new Date().toISOString(), widths: {} };
  for (const width of [1440, 390]) {
    const ctx = await browser.newContext({ viewport: { width, height: 1000 }, deviceScaleFactor: 1, ignoreHTTPSErrors: true });
    const page = await ctx.newPage();
    await page.goto('file://' + BOARD, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(800);
    const a = await audit(page);
    let axe = null;
    if (fs.existsSync(AXE)) {
      await page.addScriptTag({ path: AXE });
      axe = await page.evaluate(async () => {
        const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
        return { violations: r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes.slice(0, 3).map(n => n.target.join(' ')) })), passes: r.passes.length };
      });
    }
    a.screens = await shots(page, width, 'board');
    if (width === 1440) {
      await page.addStyleTag({ content: 'html{filter:grayscale(1)}' });
      await page.waitForTimeout(200);
      a.grayScreens = await shots(page, width, 'board-grayscale');
    }
    a.axe = axe;
    results.widths[width] = a;
    await ctx.close();
  }
  await browser.close();
  const w14 = results.widths[1440], w39 = results.widths[390];
  const chipMin = (w) => Object.values(w.chips).reduce((m, c) => Math.min(m, c.kind, c.code), 99);
  const chipSize = (w) => Object.values(w.chips).reduce((m, c) => Math.min(m, c.minSize), 99);
  const axeCount = (w) => (w.axe ? w.axe.violations.reduce((n, v) => n + v.nodes, 0) : 'not run');
  results.summary = [
    `Rendered in Chromium (Playwright) at 1440 px and 390 px, ${results.run.slice(0, 10)}. Fonts loaded: ${[...new Set(w14.fontsLoaded)].length} faces from Google Fonts.`,
    `Horizontal page scroll: 1440 px scrollWidth ${w14.scrollWidth} of ${w14.clientWidth}; 390 px scrollWidth ${w39.scrollWidth} of ${w39.clientWidth}. Wide tables scroll inside their own frames.`,
    `Smallest rendered text, with SVG text scaled by its drawing's rendered size: ${w14.minSize} px at 1440, ${w39.minSize} px at 390; text elements under 13 px: ${w14.under13.length} and ${w39.under13.length}.`,
    `Text contrast below the WCAG AA threshold, computed from rendered colors (grayscale strips converted): ${w14.lowContrast.length} at 1440, ${w39.lowContrast.length} at 390.`,
    `Typed chips: ${Object.values(w14.chips).reduce((n, c) => n + c.count, 0)} chip cells measured at 1440; lowest rendered contrast ${chipMin(w14)}:1; smallest chip text ${chipSize(w14)} px.`,
    `axe-core 4.10 (WCAG 2.2 AA tags): ${axeCount(w14)} violating nodes at 1440, ${axeCount(w39)} at 390.`,
    `Images loaded: ${w14.images.filter(i => i.ok).length} of ${w14.images.length}.`,
    `Grayscale: the board carries a grayscale strip for every option, and a full-page grayscale capture at 1440 px was saved for review.`,
  ];
  results.not_checked = [
    'Screen readers, keyboard order through the board, Firefox and Safari, print, forced colors and 200 percent zoom.',
    'Pixel-level contrast of SVG strokes and marks (contrast was computed for text and from the locked hex values for marks).',
    'Whether readers decode the marks as intended; that needs testing with people.',
  ];
  fs.writeFileSync(OUTJSON, JSON.stringify(results, null, 1));
  console.log(results.summary.join('\n'));
  for (const w of [1440, 390]) {
    const r = results.widths[w];
    console.log(w, 'under13', JSON.stringify(r.under13.slice(0, 8)));
    console.log(w, 'lowContrast', JSON.stringify(r.lowContrast.slice(0, 12)));
    console.log(w, 'overflowing', JSON.stringify(r.overflowing.slice(0, 10)));
    console.log(w, 'chips', JSON.stringify(r.chips));
    if (r.axe) console.log(w, 'axe', JSON.stringify(r.axe.violations));
  }
})();
