// Rendered checks for Direction B, Snowball and Thermostat: its five specimen pages and its board.
// Usage: node work/build/scripts/phase-2/maps_r2_b_check.js
// 1. Captures each specimen page at 1440 and 390 px, in color and in grayscale, into work/boards/phase-2/maps-r2/b/*.png
//    (the board shows these captures as the pages), and renders the 24 px kind marks at 16 and 24 px for measurement.
// 2. Audits each page at both widths and the board at both widths: horizontal page scroll, text under 13 px (SVG text
//    at its rendered scale), text contrast from rendered colors, images, axe-core 4.10.2 with WCAG 2.2 AA tags. The audit
//    function is round one's (check_maps_board.js), copied because that script runs on require, with two adaptations:
//    its scroll-region exclusion uses the class .wrap-scroll (these pages use .wrap as the page container), and an SVG's
//    ground is its first child rect wherever it sits (the card drawings are cropped, so the rect is not at 0,0).
// 3. Label test inside every drawing: each label's box against the drawn curve, the discs and the other labels.
// 4. 2x crops of the R8, R10 and B4 miniatures and card drawings into work/boards/screens/phase-2-maps-r2-b/ (not committed).
// Writes work/boards/phase-2/maps-r2/b/20261028_B-Check-Results.json.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const ROOT = path.resolve(__dirname, '../../../..');
const ASSETS = path.join(ROOT, 'work/boards/phase-2/maps-r2/b');
const BOARD = path.join(ROOT, 'work/boards/20261028_Map-Direction-B-Snowball-And-Thermostat.html');
const SHOTS = path.join(ROOT, 'work/boards/screens/phase-2-maps-r2-b');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');
const OUTJSON = path.join(ASSETS, '20261028_B-Check-Results.json');
const PAGES = [
  ['Loop-Catalog', '20261028_Direction-B-Loop-Catalog.html'],
  ['Loop-Card-R8', '20261028_Direction-B-Loop-Card-R8.html'],
  ['Loop-Card-R10', '20261028_Direction-B-Loop-Card-R10.html'],
  ['Loop-Card-B4', '20261028_Direction-B-Loop-Card-B4.html'],
  ['Reform-View-R-01', '20261028_Direction-B-Reform-View-R-01.html'],
];
fs.mkdirSync(SHOTS, { recursive: true });

// ---------------------------------------------------------------- round one's audit, two adaptations noted above
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
          const r = e.querySelector(':scope > rect');
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
      if (el.closest('.wrap-scroll')) continue;
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
    return { version: axe.version, violations: r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes.slice(0, 3).map(n => n.target.join(' ')) })), passes: r.passes.length, incomplete: r.incomplete.length };
  });
}

// ---------------------------------------------------------------- label test inside the drawings
async function labelTest(page) {
  return page.evaluate(() => {
    const res = { drawings: 0, labels: 0, curveClash: [], discClash: [], labelClash: [], idOverflow: [], minCurveGap: 99 };
    const visible = (el) => { const r = el.getBoundingClientRect(); if (!r.width) return false; let e = el; while (e && e.nodeType === 1) { const cs = getComputedStyle(e); if (cs.display === 'none') return false; e = e.parentElement; } return true; };
    for (const svg of document.querySelectorAll('svg[data-loop]')) {
      if (!visible(svg)) continue;
      res.drawings++;
      const loop = svg.getAttribute('data-loop'), view = svg.getAttribute('data-view');
      // curve samples, in the drawing's own units, from every step line and arrowhead
      const pts = [];
      for (const p of svg.querySelectorAll('g.step path[data-texture]')) {
        const len = p.getTotalLength();
        for (let s = 0; s <= len; s += 1.5) { const q = p.getPointAtLength(s); pts.push([q.x, q.y]); }
      }
      for (const pg of svg.querySelectorAll('g.step polygon')) {
        for (const q of pg.points) pts.push([q.x, q.y]);
      }
      const discs = [...svg.querySelectorAll('g.var circle, g.echo circle, g.sketch circle')].map(c => [+c.getAttribute('cx'), +c.getAttribute('cy'), +c.getAttribute('r')]);
      const boxes = [];
      for (const g of svg.querySelectorAll('g.lbl')) {
        const texts = [...g.querySelectorAll('text')];
        for (const t of texts) {
          if (t.closest('g.pill')) continue;
          const b = t.getBBox();
          boxes.push({ g, b, text: t.textContent });
        }
        const pill = g.querySelector('g.pill');
        if (pill) { const b = pill.getBBox(); boxes.push({ g, b, text: 'pill ' + (pill.getAttribute('data-for') || '') }); }
      }
      res.labels += boxes.length;
      for (const bx of boxes) {
        const { x, y, width, height } = bx.b;
        let dmin = 99;
        for (const [px, py] of pts) {
          const dx = Math.max(x - px, 0, px - (x + width)), dy = Math.max(y - py, 0, py - (y + height));
          dmin = Math.min(dmin, Math.hypot(dx, dy));
        }
        res.minCurveGap = Math.min(res.minCurveGap, +dmin.toFixed(2));
        if (dmin < 4) res.curveClash.push({ loop, view, text: bx.text.slice(0, 30), gap: +dmin.toFixed(2) });
        for (const [cx, cy, r] of discs) {
          const dx = Math.max(x - cx, 0, cx - (x + width)), dy = Math.max(y - cy, 0, cy - (y + height));
          if (Math.hypot(dx, dy) < r + 3) res.discClash.push({ loop, view, text: bx.text.slice(0, 30) });
        }
      }
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        if (boxes[i].g === boxes[j].g) continue;
        const a = boxes[i].b, b = boxes[j].b;
        if (!(a.x + a.width + 4 <= b.x || b.x + b.width + 4 <= a.x || a.y + a.height + 2 <= b.y || b.y + b.height + 2 <= a.y))
          res.labelClash.push({ loop, view, a: boxes[i].text.slice(0, 24), b: boxes[j].text.slice(0, 24) });
      }
      // every ID sits inside its own disc
      for (const g of svg.querySelectorAll('g.var, g.echo')) {
        const c = g.querySelector('circle'), t = g.querySelector('text');
        if (!c || !t) continue;
        const b = t.getBBox(), cx = +c.getAttribute('cx'), cy = +c.getAttribute('cy'), r = +c.getAttribute('r');
        const far = Math.max(Math.hypot(b.x - cx, b.y + b.height * 0.25 - cy), Math.hypot(b.x + b.width - cx, b.y + b.height * 0.25 - cy));
        if (b.width / 2 > r - 1.5) res.idOverflow.push({ loop, view, id: t.textContent, half: +(b.width / 2).toFixed(1), r });
      }
    }
    return res;
  });
}

async function open(browser, file, width, dsf = 1) {
  const ctx = await browser.newContext({ viewport: { width, height: 1000 }, deviceScaleFactor: dsf, ignoreHTTPSErrors: true });
  const page = await ctx.newPage();
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
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
  const results = { run: new Date().toISOString(), pages: {}, board: {}, captures: [], crops: [] };
  const boardOnly = process.argv.includes('--board-only');
  // 1. pages: captures for the board, grayscale proofs, audits, label tests
  if (!boardOnly) for (const [tag, file] of PAGES) {
    const f = path.join(ASSETS, file);
    results.pages[tag] = {};
    for (const width of [1440, 390]) {
      const { ctx, page } = await open(browser, f, width, 1);
      const cap = path.join(ASSETS, `20261028_B-Page-${tag}-${width}.png`);
      await page.screenshot({ path: cap, fullPage: true });
      const a = await audit(page);
      a.labels = await labelTest(page);
      a.axe = await runAxe(page);
      await page.addStyleTag({ content: 'html{filter:grayscale(1)}' });
      await page.waitForTimeout(150);
      const gcap = path.join(ASSETS, `20261028_B-Page-${tag}-${width}-Grayscale.png`);
      await page.screenshot({ path: gcap, fullPage: true });
      results.captures.push(path.relative(ROOT, cap), path.relative(ROOT, gcap));
      a.capture = path.relative(ROOT, cap);
      results.pages[tag][width] = a;
      await ctx.close();
    }
  }
  // 2. 2x crops for the 2x test
  if (!boardOnly) {
    const crops = [['Loop-Catalog', 1440, ['R8', 'R10', 'B4', 'R15', 'R9']], ['Loop-Catalog', 390, ['R8', 'R10', 'B4']]];
    for (const [tag, width, loops] of crops) {
      const { ctx, page } = await open(browser, path.join(ASSETS, PAGES.find(p => p[0] === tag)[1]), width, 2);
      for (const lid of loops) {
        const el = await page.$(`li.tile[data-loop="${lid}"]`);
        const p = path.join(SHOTS, `2x-${tag}-${width}-${lid}.png`);
        await el.screenshot({ path: p });
        results.crops.push(path.relative(ROOT, p));
      }
      await ctx.close();
    }
    for (const tag of ['Loop-Card-R8', 'Loop-Card-R10', 'Loop-Card-B4', 'Reform-View-R-01']) {
      for (const width of [1440, 390]) {
        const { ctx, page } = await open(browser, path.join(ASSETS, PAGES.find(p => p[0] === tag)[1]), width, 2);
        const el = await page.$(width === 1440 ? 'svg.desk' : 'svg.phone');
        const p = path.join(SHOTS, `2x-${tag}-${width}-figure.png`);
        await el.screenshot({ path: p });
        results.crops.push(path.relative(ROOT, p));
        await ctx.close();
      }
    }
    // 3. the kind marks as rasters at 1x, Charcoal on White, for the pixel-fit and similarity measures
    for (const kind of ['Snowball', 'Thermostat']) {
      const svg = fs.readFileSync(path.join(ASSETS, `20261028_B-Kind-Mark-${kind}-24.svg`), 'utf8').replace(/^<\?xml[^>]*>\s*/, '');
      for (const size of [16, 24]) {
        const ctx = await browser.newContext({ viewport: { width: size, height: size }, deviceScaleFactor: 1 });
        const page = await ctx.newPage();
        const s2 = svg.replace(/width="24" height="24"/, `width="${size}" height="${size}"`);
        await page.setContent(`<html><body style="margin:0;background:#FFFFFF">${s2}</body></html>`);
        const p = path.join(ASSETS, `20261028_B-Kind-Mark-${kind}-${size}px.png`);
        await page.screenshot({ path: p, clip: { x: 0, y: 0, width: size, height: size } });
        results.captures.push(path.relative(ROOT, p));
        await ctx.close();
      }
    }
  }
  // 4. the board at both widths
  if (fs.existsSync(BOARD)) {
    for (const width of [1440, 390]) {
      const { ctx, page } = await open(browser, BOARD, width, 1);
      const a = await audit(page);
      a.labels = await labelTest(page);
      a.axe = await runAxe(page);
      a.screens = await shots(page, width, 'board');
      results.board[width] = a;
      await ctx.close();
    }
  }
  await browser.close();
  if (boardOnly && fs.existsSync(OUTJSON)) {
    const prev = JSON.parse(fs.readFileSync(OUTJSON, 'utf8'));
    prev.board = results.board; prev.board_run = results.run;
    Object.assign(results, { pages: prev.pages, captures: prev.captures, crops: prev.crops });
  }
  const axeN = (w) => (w && w.axe ? w.axe.violations.reduce((n, v) => n + v.nodes, 0) : 'not run');
  const lines = [];
  for (const [tag, byW] of Object.entries(results.pages)) for (const [w, a] of Object.entries(byW)) {
    lines.push(`${tag} at ${w} px: scrollWidth ${a.scrollWidth} of ${a.clientWidth}; smallest text ${a.minSize} px (${a.under13.length} under 13); ${a.lowContrast.length} low-contrast texts; ${a.images.filter(i => !i.ok).length} broken images; axe ${axeN(a)} violating nodes; labels ${a.labels.labels} in ${a.labels.drawings} drawings, ${a.labels.curveClash.length + a.labels.discClash.length + a.labels.labelClash.length + a.labels.idOverflow.length} collisions, nearest label to a curve ${a.labels.minCurveGap} px.`);
  }
  for (const [w, a] of Object.entries(results.board)) {
    lines.push(`Board at ${w} px: scrollWidth ${a.scrollWidth} of ${a.clientWidth}; smallest text ${a.minSize} px (${a.under13.length} under 13); ${a.lowContrast.length} low-contrast texts; images ${a.images.filter(i => i.ok).length} of ${a.images.length} loaded; axe ${axeN(a)} violating nodes; ${a.fonts.length} font faces loaded.`);
  }
  results.summary = lines;
  results.not_checked = [
    'Screen readers, keyboard order, Firefox and Safari, print, forced colors and 200 percent zoom.',
    'Widths between 390 and 1440 px other than the two named; the card pages switch to the phone figure under 1000 px.',
    'Pixel contrast of strokes and marks; mark colors are locked palette values, measured by formula.',
  ];
  fs.writeFileSync(OUTJSON, JSON.stringify(results, null, 1));
  console.log(lines.join('\n'));
  const report = (k, a) => {
    if (a.under13.length) console.log(k, 'under13', JSON.stringify(a.under13.slice(0, 6)));
    if (a.lowContrast.length) console.log(k, 'lowContrast', JSON.stringify(a.lowContrast.slice(0, 6)));
    if (a.overflowing.length) console.log(k, 'overflowing', JSON.stringify(a.overflowing.slice(0, 6)));
    if (a.axe && a.axe.violations.length) console.log(k, 'axe', JSON.stringify(a.axe.violations));
    const L = a.labels; if (L) for (const key of ['curveClash', 'discClash', 'labelClash', 'idOverflow']) if (L[key].length) console.log(k, key, JSON.stringify(L[key].slice(0, 6)));
    const bad = a.images.filter(i => !i.ok); if (bad.length) console.log(k, 'images', JSON.stringify(bad.slice(0, 6)));
  };
  for (const [tag, byW] of Object.entries(results.pages)) for (const [w, a] of Object.entries(byW)) report(`${tag}@${w}`, a);
  for (const [w, a] of Object.entries(results.board)) report(`board@${w}`, a);
})();
