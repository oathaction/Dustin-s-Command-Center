// Rendered checks for Direction A, Field Guide: the board and its five standalone pages.
// Usage: node work/build/scripts/phase-2/maps_r2_a_check.js
// 1. Captures what the pages and the board show as images: the reduced circuits for phones, each page at 390 px
//    (DSF 2, first 1600 px) and each page at 1440 px in grayscale, into work/boards/phase-2/maps-r2/a/.
// 2. Audits the board and every page at 1440 and 390 px: horizontal page scroll, text under 13 px (SVG text at its
//    drawing's rendered scale), text contrast from rendered colors, images, axe-core with WCAG 2.2 AA tags, and a
//    text check inside every drawing: each label inside its drawing, each box label inside its box, and no two
//    labels or a label and a sign disc overlapping.
// Writes work/boards/phase-2/maps-r2/a/20261028_A-Check-Results.json; screenshots for review go to
// work/boards/screens/phase-2-maps-r2-a/ (regenerable, not committed).
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const ROOT = path.resolve(__dirname, '../../../..');
const BOARD = path.join(ROOT, 'work/boards/20261028_Map-Direction-A-Field-Guide.html');
const ASSETS = path.join(ROOT, 'work/boards/phase-2/maps-r2/a');
const PAGES = ['Loop-Catalog', 'R8-Loop-Card', 'R10-Loop-Card', 'Circuit-Page', 'R-01-Reform-View'];
const NO_PHONE_CAPTURE = new Set(['Circuit-Page']);
const OUTJSON = path.join(ASSETS, '20261028_A-Check-Results.json');
const SHOTS = path.join(ROOT, 'work/boards/screens/phase-2-maps-r2-a');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');
fs.mkdirSync(SHOTS, { recursive: true });
const pageFile = (n) => path.join(ASSETS, `20261028_A-${n}.html`);

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
      // the filled shape directly under an SVG label: a box, tab, disc or card drawn before it
      if (!(el instanceof SVGTextElement)) return null;
      const bb = el.getBoundingClientRect();
      const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
      let node = el, found = null;
      while (node && !(node instanceof SVGSVGElement)) {
        let sib = node.previousElementSibling;
        while (sib) {
          const shapes = [sib, ...sib.querySelectorAll('circle,rect,polygon,path')].filter(s => ['circle', 'rect', 'polygon', 'path'].includes(s.tagName));
          for (const sh of shapes.reverse()) {
            if (sh.getAttribute('fill') === 'none' || !sh.getAttribute('fill')) continue;
            const f = parse(getComputedStyle(sh).fill);
            if (!f || f.a < 0.5) continue;
            const b = sh.getBoundingClientRect();
            if (b.width < 8 || b.height < 8) continue;
            if (cx >= b.x && cx <= b.x + b.width && cy >= b.y && cy <= b.y + b.height) { found = f; break; }
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
      if (!visible(el)) continue;
      // content inside a focusable scroll region may extend past the viewport by design
      const reg = el.closest('[role="region"][tabindex]');
      if (reg && reg !== el) continue;
      const r = el.getBoundingClientRect();
      if (r.right > vw + 0.5) out.overflowing.push({ tag: el.tagName, cls: (el.className && el.className.baseVal !== undefined) ? el.className.baseVal : el.className, right: Math.round(r.right) });
    }
    out.overflowing = out.overflowing.slice(0, 20);
    // text inside drawings: containment and collisions, from rendered boxes
    const tx = { drawings: 0, labels: 0, outside: [], outOfBox: [], overlaps: [], discOverlaps: [] };
    const inter = (a, b, pad) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > pad && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > pad;
    for (const svg of document.querySelectorAll('svg[data-view]')) {
      if (!visible(svg)) continue;
      tx.drawings++;
      const sr = svg.getBoundingClientRect();
      const name = (svg.getAttribute('data-view') || '') + ' ' + (svg.getAttribute('data-loop') || '') + (svg.getAttribute('data-reform') ? ' ' + svg.getAttribute('data-reform') : '');
      const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && visible(t));
      const rects = texts.map(t => t.getBoundingClientRect());
      tx.labels += texts.length;
      texts.forEach((t, i) => {
        const r = rects[i];
        if (r.left < sr.left - 0.5 || r.right > sr.right + 0.5 || r.top < sr.top - 0.5 || r.bottom > sr.bottom + 0.5) tx.outside.push({ svg: name, text: t.textContent.slice(0, 40) });
      });
      // box labels stay inside their box (the variable's first rect)
      for (const g of svg.querySelectorAll('g.var')) {
        const box = g.querySelector('rect');
        if (!box) continue;
        const br = box.getBoundingClientRect();
        if (br.width < 30) continue;
        for (const t of g.querySelectorAll('text')) {
          const r = t.getBoundingClientRect();
          if (r.top >= br.top - 1 && r.bottom <= br.bottom + 1 && (r.left < br.left - 0.5 || r.right > br.right + 0.5)) tx.outOfBox.push({ svg: name, node: g.getAttribute('data-node'), text: t.textContent.slice(0, 40) });
        }
      }
      // label against label: any overlap beyond 1.5 px in both directions
      for (let i = 0; i < texts.length; i++) {
        for (let j = i + 1; j < texts.length; j++) {
          if (inter(rects[i], rects[j], 1.5)) tx.overlaps.push({ svg: name, a: texts[i].textContent.slice(0, 30), b: texts[j].textContent.slice(0, 30) });
        }
      }
      // label against sign disc: a disc's own glyph excepted
      const discs = [...svg.querySelectorAll('g.pill')];
      for (const d of discs) {
        const dr = d.getBoundingClientRect();
        texts.forEach((t, i) => {
          if (d.contains(t)) return;
          if (inter(rects[i], dr, 1.5)) tx.discOverlaps.push({ svg: name, disc: d.getAttribute('data-for'), text: t.textContent.slice(0, 30) });
        });
      }
    }
    out.textCheck = tx;
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

async function open(browser, file, width, dsf = 1, height = 1000) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: dsf, ignoreHTTPSErrors: true });
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
  const results = { board: path.relative(ROOT, BOARD), run: new Date().toISOString(), widths: {}, pages: {}, captures: [] };

  // 1. captures. The reduced circuits come first, since the phone pages show them.
  for (const [pg, out] of [['Circuit-Page', '20261028_A-Circuit-Reduced.png'], ['R-01-Reform-View', '20261028_A-Reform-R-01-Circuit-Reduced.png']]) {
    const { ctx, page } = await open(browser, pageFile(pg), 1440, 1);
    const el = await page.$('.dsk svg[data-view="circuit-map"]');
    await el.screenshot({ path: path.join(ASSETS, out) });
    results.captures.push(out);
    await ctx.close();
  }
  for (const pg of PAGES) {
    if (!NO_PHONE_CAPTURE.has(pg)) {
      const { ctx, page } = await open(browser, pageFile(pg), 390, 2);
      const out = `20261028_A-${pg}-390.png`;
      await page.screenshot({ path: path.join(ASSETS, out), fullPage: true, clip: { x: 0, y: 0, width: 390, height: 1600 } });
      results.captures.push(out);
      await ctx.close();
    }
    const g = await open(browser, pageFile(pg), 1440, 1, 900);
    await g.page.addStyleTag({ content: 'html{filter:grayscale(1)}' });
    await g.page.waitForTimeout(200);
    const out = `20261028_A-${pg}-Grayscale.png`;
    await g.page.screenshot({ path: path.join(ASSETS, out) });
    results.captures.push(out);
    await g.ctx.close();
  }

  // 2. audits: every standalone page and the board, at both widths
  for (const pg of PAGES) {
    results.pages[pg] = {};
    for (const width of [1440, 390]) {
      const { ctx, page } = await open(browser, pageFile(pg), width, 1);
      const a = await audit(page);
      a.axe = await runAxe(page);
      a.screens = await shots(page, width, pg);
      results.pages[pg][width] = a;
      await ctx.close();
    }
  }
  for (const width of [1440, 390]) {
    const { ctx, page } = await open(browser, BOARD, width, 1);
    const a = await audit(page);
    a.axe = await runAxe(page);
    a.screens = await shots(page, width, 'board');
    results.widths[width] = a;
    await ctx.close();
  }
  // 3. self-test: plant one fault of each kind in a copy of the R8 card in memory and confirm the audit sees it
  {
    const { ctx, page } = await open(browser, pageFile('R8-Loop-Card'), 1440, 1);
    await page.evaluate(() => {
      const svg = document.querySelector('.dsk svg[data-view="fg-card"]');
      const ns = 'http://www.w3.org/2000/svg';
      const lab = svg.querySelector('g.steplabel text');
      const dup = lab.cloneNode(true); dup.setAttribute('y', +lab.getAttribute('y') + 3); lab.parentNode.appendChild(dup);
      const box = svg.querySelector('g.var text');
      const wide = box.cloneNode(true); wide.textContent = 'A label far too long to sit inside its box at this size'; box.parentNode.appendChild(wide);
      const tiny = document.createElementNS(ns, 'text'); tiny.setAttribute('x', 20); tiny.setAttribute('y', 20); tiny.setAttribute('font-size', '11'); tiny.textContent = 'tiny'; svg.appendChild(tiny);
      const disc = svg.querySelector('g.pill'); const r = disc.querySelector('rect,circle');
      const onDisc = document.createElementNS(ns, 'text'); onDisc.setAttribute('x', r.getAttribute('x') || r.getAttribute('cx')); onDisc.setAttribute('y', +(r.getAttribute('y') || r.getAttribute('cy')) + 8); onDisc.setAttribute('font-size', '14'); onDisc.textContent = 'on the disc'; svg.appendChild(onDisc);
      const out = document.createElementNS(ns, 'text'); out.setAttribute('x', svg.viewBox.baseVal.width - 10); out.setAttribute('y', 40); out.setAttribute('font-size', '14'); out.textContent = 'past the edge'; svg.appendChild(out);
    });
    const a = await audit(page);
    results.selfTest = {
      overlap: a.textCheck.overlaps.length > 0, outOfBox: a.textCheck.outOfBox.length > 0, under13: a.under13.length > 0,
      discOverlap: a.textCheck.discOverlaps.length > 0, outside: a.textCheck.outside.length > 0,
    };
    await ctx.close();
  }
  await browser.close();

  const axeN = (w) => (w.axe ? w.axe.violations.reduce((n, v) => n + v.nodes, 0) : 'not run');
  const txN = (w) => w.textCheck.outside.length + w.textCheck.outOfBox.length + w.textCheck.overlaps.length + w.textCheck.discOverlaps.length;
  const runs = [['board', '1440', results.widths[1440]], ['board', '390', results.widths[390]]];
  for (const pg of PAGES) for (const w of ['1440', '390']) runs.push([pg, w, results.pages[pg][w]]);
  const w14 = results.widths[1440], w39 = results.widths[390];
  const sum = (f) => runs.reduce((n, [, , a]) => n + f(a), 0);
  const maxScroll = runs.filter(([, w, a]) => a.scrollWidth > a.clientWidth);
  const imgs = runs.reduce((acc, [, , a]) => acc.concat(a.images), []);
  results.summary = [
    `Rendered in Chromium (Playwright) at 1440 and 390 px on ${results.run.slice(0, 10)}: the board and its five pages, ${runs.length} renders in all, with ${w14.fonts.length} Google Fonts faces loaded; ${w14.svgs} drawings inline on the board.`,
    `Horizontal page scroll: ${maxScroll.length ? maxScroll.map(([n, w, a]) => `${n} at ${w} (${a.scrollWidth})`).join(', ') : 'none in any render'}; the board at 390 measures ${w39.scrollWidth} of ${w39.clientWidth}.`,
    `Smallest rendered text, counting SVG text at its drawing's rendered scale: ${Math.min(...runs.map(([, w, a]) => w === '1440' ? a.minSize : 99))} px at 1440 and ${Math.min(...runs.map(([, w, a]) => w === '390' ? a.minSize : 99))} px at 390; text elements under 13 px across all renders: ${sum(a => a.under13.length)}.`,
    `Text below WCAG AA contrast, from rendered colors: ${sum(a => a.lowContrast.length)} across all renders.`,
    `Images loaded: ${imgs.filter(i => i.ok).length} of ${imgs.length} across all renders.`,
    `axe-core 4.10 with WCAG 2.2 AA tags: ${sum(a => (a.axe ? a.axe.violations.reduce((n, v) => n + v.nodes, 0) : 0))} violating nodes across all renders (board ${axeN(w14)} at 1440, ${axeN(w39)} at 390).`,
    `Text inside drawings: ${sum(a => a.textCheck.labels)} rendered labels in ${sum(a => a.textCheck.drawings)} drawings checked; ${sum(a => a.textCheck.outside.length)} outside their drawing, ${sum(a => a.textCheck.outOfBox.length)} outside their box, ${sum(a => a.textCheck.overlaps.length)} overlapping another label, ${sum(a => a.textCheck.discOverlaps.length)} overlapping a sign disc.`,
    `Captured ${results.captures.length} images for the board and the phone pages: ${results.captures.length - 2 - PAGES.length} pages at 390 px, ${PAGES.length} grayscale proofs and 2 reduced circuits.`,
    `Self-test of the text check on a planted copy of the R8 card: ${Object.values(results.selfTest).filter(Boolean).length} of ${Object.keys(results.selfTest).length} planted faults caught (overlapping label, label outside its box, label outside the drawing, label on a sign disc, 11 px text).`,
  ];
  results.not_checked = [
    'Screen readers, keyboard order, Firefox and Safari, print, forced colors and 200 percent zoom.',
    'Pixel contrast of strokes and marks. Mark colors are the locked palette values, measured by formula (Pillar Red 4.17:1 on White, Charcoal 18.1:1 on White).',
    'Labels crossing wires on the circuit. The three bus labels carry a background halo; the check above covers label against label and label against sign disc, not label against line.',
    'The live atlas renderer; these are specimens only (G1-08).',
  ];
  fs.writeFileSync(OUTJSON, JSON.stringify(results, null, 1));
  console.log(results.summary.join('\n'));
  for (const [n, w, a] of runs) {
    const k = `${n}@${w}`;
    if (a.under13.length) console.log(k, 'under13', JSON.stringify(a.under13.slice(0, 6)));
    if (a.lowContrast.length) console.log(k, 'lowContrast', JSON.stringify(a.lowContrast.slice(0, 6)));
    if (a.overflowing.length) console.log(k, 'overflowing', JSON.stringify(a.overflowing.slice(0, 6)));
    if (a.axe && a.axe.violations.length) console.log(k, 'axe', JSON.stringify(a.axe.violations));
    const bad = a.images.filter(i => !i.ok); if (bad.length) console.log(k, 'images', JSON.stringify(bad));
    if (txN(a)) console.log(k, 'text', JSON.stringify({ outside: a.textCheck.outside.slice(0, 6), outOfBox: a.textCheck.outOfBox.slice(0, 6), overlaps: a.textCheck.overlaps.slice(0, 8), disc: a.textCheck.discOverlaps.slice(0, 8) }));
  }
})();
