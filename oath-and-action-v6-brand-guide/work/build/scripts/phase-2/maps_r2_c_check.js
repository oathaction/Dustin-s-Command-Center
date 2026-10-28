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

// [result name, page file, width, capture height (0 = full page)]. The three view pages are one responsive page
// each, rendered at 1440 (the drawing inline) and at 390 (the drawing fit to the screen, then the lines in words).
const PAGES = [
  ['Poster', 'Poster', 1440, 960], ['Working-Map', 'Working-Map', 1440, 960], ['Reform-View-R-01', 'Reform-View-R-01', 1440, 960],
  ['Poster-Phone', 'Poster', 390, 0], ['Working-Map-Phone', 'Working-Map', 390, 0], ['Reform-View-R-01-Phone', 'Reform-View-R-01', 390, 0],
  ['Catalog', 'Catalog', 1440, 0], ['Catalog-Phone', 'Catalog-Phone', 390, 0],
  ['Card-R8', 'Card-R8', 1440, 0], ['Card-R8-Phone', 'Card-R8-Phone', 390, 0], ['Card-R10', 'Card-R10', 1440, 0], ['Card-R10-Phone', 'Card-R10-Phone', 390, 0],
];

// Label audit, ported from Direction A's maps_r2_a_check.js (text check in its audit) and extended to C's marks.
// For every visible drawing: text outside the drawing; label against label (overlap beyond 1.5 px both ways);
// label against mark (sign tags, line bullets, station shapes; a mark's own text excepted); label against line
// (each step path, leader and ghost stub sampled every 2 px in screen space; texts that sit on lines by design,
// inside a sign tag, bullet or station, excepted).
async function labelAudit(page) {
  return page.evaluate(() => {
    // a drawing inside a display:none container (the 1440 frame on a phone) has no box and is skipped
    const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; };
    const inter = (a, b, pad) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > pad && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > pad;
    const tx = { drawings: 0, labels: 0, marks: 0, lineSamples: 0, outside: [], overlaps: [], markOverlaps: [], lineOverlaps: [] };
    for (const svg of document.querySelectorAll('svg[data-view]')) {
      if (!visible(svg)) continue;
      const sr = svg.getBoundingClientRect();
      if (sr.width < 2) continue;
      tx.drawings++;
      const name = (svg.getAttribute('data-view') || '') + (svg.getAttribute('data-loop') ? ' ' + svg.getAttribute('data-loop') : '') + (svg.getAttribute('data-reform') ? ' ' + svg.getAttribute('data-reform') : '');
      const texts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && t.getBoundingClientRect().width > 0);
      const rects = texts.map(t => t.getBoundingClientRect());
      tx.labels += texts.length;
      texts.forEach((t, i) => {
        const r = rects[i];
        if (r.left < sr.left - 0.5 || r.right > sr.right + 0.5 || r.top < sr.top - 0.5 || r.bottom > sr.bottom + 0.5) tx.outside.push({ svg: name, text: t.textContent.slice(0, 40) });
      });
      for (let i = 0; i < texts.length; i++) {
        for (let j = i + 1; j < texts.length; j++) {
          if (inter(rects[i], rects[j], 1.5)) tx.overlaps.push({ svg: name, a: texts[i].textContent.slice(0, 30), b: texts[j].textContent.slice(0, 30) });
        }
      }
      // marks: the shape of each sign tag, line bullet and station
      const marks = [];
      for (const g of svg.querySelectorAll('g.sign, g.bullet, g.var')) {
        const shapes = [...g.querySelectorAll(':scope > polygon, :scope > rect, :scope > circle')];
        for (const sh of shapes) marks.push({ g, r: sh.getBoundingClientRect(), what: (g.getAttribute('class') || '') + ' ' + (g.getAttribute('data-for') || g.getAttribute('data-bullet') || g.getAttribute('data-node') || '') });
      }
      tx.marks += marks.length;
      texts.forEach((t, i) => {
        for (const m of marks) {
          if (m.g.contains(t)) continue;
          if (inter(rects[i], m.r, 1.5)) tx.markOverlaps.push({ svg: name, mark: m.what.trim(), text: t.textContent.slice(0, 30) });
        }
      });
      // lines
      const free = texts.map((t, i) => ({ t, r: rects[i] })).filter(o => !o.t.closest('g.sign, g.bullet, g.var'));
      const paths = [...svg.querySelectorAll('g.step path[data-texture], path.leader, path[data-ghost]')];
      for (const p of paths) {
        const len = p.getTotalLength();
        const m = p.getScreenCTM();
        const sw = parseFloat(p.getAttribute('stroke-width') || '1') * (m ? Math.hypot(m.a, m.b) : 1);
        const step = p.closest('g.step');
        const hitList = new Set();
        for (let s = 0; s <= len; s += 2) {
          const pt = p.getPointAtLength(s);
          const x = m.a * pt.x + m.c * pt.y + m.e, y = m.b * pt.x + m.d * pt.y + m.f;
          tx.lineSamples++;
          const inf = sw / 2 - 1.5;
          for (const o of free) {
            if (step && step.contains(o.t)) continue;
            if (x > o.r.left - inf && x < o.r.right + inf && y > o.r.top - inf && y < o.r.bottom + inf) hitList.add(o);
          }
        }
        for (const o of hitList) tx.lineOverlaps.push({ svg: name, line: (step ? step.getAttribute('data-link') : (p.getAttribute('class') || 'ghost')), text: o.t.textContent.slice(0, 30) });
      }
    }
    tx.total = tx.outside.length + tx.overlaps.length + tx.markOverlaps.length + tx.lineOverlaps.length;
    return tx;
  });
}

// Content inside each White card (the loop card page, every catalog card) stays inside the card: an element whose
// box runs past the card's left or right edge counts, unless it sits inside a focusable scroll region.
async function cardProbe(page) {
  return page.evaluate(() => {
    const out = { cards: 0, past: [] };
    for (const card of document.querySelectorAll('article.cardpage, article.card')) {
      const cr = card.getBoundingClientRect();
      if (cr.width < 2) continue;
      out.cards++;
      for (const el of card.querySelectorAll('*')) {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        const reg = el.closest('[role="region"][tabindex]');
        if (reg && reg !== el && card.contains(reg)) continue;
        if (r.right > cr.right + 0.5 || r.left < cr.left - 0.5) out.past.push({ card: card.getAttribute('data-loop'), tag: el.tagName, right: Math.round(r.right), cardRight: Math.round(cr.right) });
      }
    }
    out.past = out.past.slice(0, 30);
    return out;
  });
}

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
  for (const [name, fname, width, height] of PAGES) {
    const file = path.join(ASSETS, `20261028_Loop-Lines-${fname}.html`);
    const { ctx, page } = await open(browser, file, width, 1, height || 1000);
    const a = await audit(page);
    a.labels = await labelAudit(page);
    a.cardFit = await cardProbe(page);
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
  // 2a. field tint proof: the poster with round two's tint (#2C3B64) and with the stronger step (#39476D), in grayscale
  // at 25 percent size, the size at which the review asked whether the five areas read
  {
    results.tintProof = [];
    for (const [tag, tint] of [['Current', '#2C3B64'], ['Stronger', '#39476D']]) {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 960 }, deviceScaleFactor: 0.25 });
      const page = await ctx.newPage();
      await page.goto('file://' + path.join(ASSETS, '20261028_Loop-Lines-Poster.html'), { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      await page.evaluate((t) => { for (const f of document.querySelectorAll('svg[data-view="c-poster"] path.field')) { f.setAttribute('fill', t); f.setAttribute('stroke', t); } }, tint);
      await page.addStyleTag({ content: 'html{filter:grayscale(1)}' });
      await page.waitForTimeout(300);
      const out = path.join(ASSETS, `20261028_Loop-Lines-Field-Tint-${tag}-Gray-25.png`);
      await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1440, height: 960 } });
      results.tintProof.push({ tint, file: path.relative(ROOT, out) });
      await ctx.close();
    }
  }
  // 2b. the label audit on the print drawing at its print scale, and the self-test of the audit
  {
    const { ctx, page } = await open(browser, path.join(ASSETS, '20261028_Loop-Lines-Poster-Print.html'), 1440, 1);
    results.printLabels = await labelAudit(page);
    await ctx.close();
  }
  {
    const { ctx, page } = await open(browser, path.join(ASSETS, '20261028_Loop-Lines-Poster.html'), 1440, 1, 960);
    await page.evaluate(() => {
      const svg = document.querySelector('svg[data-view="c-poster"]');
      const ns = 'http://www.w3.org/2000/svg';
      const add = (x, y, txt, size) => { const t = document.createElementNS(ns, 'text'); t.setAttribute('x', x); t.setAttribute('y', y); t.setAttribute('font-size', size || 15); t.setAttribute('class', 't s'); t.textContent = txt; svg.appendChild(t); return t; };
      const lab = svg.querySelector('g.label text');
      const dup = lab.cloneNode(true); dup.setAttribute('y', +lab.getAttribute('y') + 3); lab.parentNode.appendChild(dup);   // label on label
      const tag = svg.querySelector('g.sign polygon').getBBox(); add(tag.x, tag.y + tag.height / 2 + 4, 'on the tag');      // label on mark
      const st = svg.querySelector('g.step path').getPointAtLength(40); add(st.x - 20, st.y + 5, 'on the line');             // label on line
      add(svg.viewBox.baseVal.width - 10, 400, 'past the edge');                                                             // outside
      add(20, 400, 'tiny', 11);                                                                                                // under 13 px
    });
    const t = await labelAudit(page);
    const a = await audit(page);
    results.selfTest = { overlap: t.overlaps.length > 0, markOverlap: t.markOverlaps.length > 0, lineOverlap: t.lineOverlaps.length > 0,
                         outside: t.outside.length > 0, under13: a.under13.length > 0 };
    await ctx.close();
  }
  // 3. board
  if (fs.existsSync(BOARD)) {
    for (const width of [1440, 390]) {
      const { ctx, page } = await open(browser, BOARD, width, 1);
      const a = await audit(page);
      a.labels = await labelAudit(page);
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
    for (const name of ['Catalog', 'Card-R8', 'Card-R10', 'Working-Map', 'Reform-View-R-01']) {
      const o = await open(browser, path.join(ASSETS, `20261028_Loop-Lines-${name}.html`), 1440, 2);
      await o.page.screenshot({ path: path.join(CROPS, `${name}-2x.png`), fullPage: true });
      await o.ctx.close();
    }
  }
  await browser.close();
  if (results.printLabels.total) console.log('print labels', JSON.stringify([...results.printLabels.outside, ...results.printLabels.overlaps, ...results.printLabels.markOverlaps, ...results.printLabels.lineOverlaps].slice(0, 12)));
  const axeN = (w) => (w && w.axe ? w.axe.violations.reduce((n, v) => n + v.nodes, 0) : 'not run');
  const lines = [];
  const lab = (t) => `labels ${t.labels} in ${t.drawings} drawings: ${t.outside.length} outside, ${t.overlaps.length} on labels, ${t.markOverlaps.length} on marks, ${t.lineOverlaps.length} on lines`;
  for (const [name, a] of Object.entries(results.pages)) {
    lines.push(`${name} at ${PAGES.find(p => p[0] === name)[2]} px: scrollWidth ${a.scrollWidth} of ${a.clientWidth}, smallest text ${a.minSize} px (${a.under13.length} under 13), ${a.lowContrast.length} low-contrast texts, images ${a.images.filter(i => i.ok).length}/${a.images.length}, axe ${axeN(a)} violating nodes; ${lab(a.labels)}${a.cardFit.cards ? `; ${a.cardFit.past.length} elements past the edge of ${a.cardFit.cards} White cards` : ''}.`);
  }
  lines.push(`Poster print drawing: ${lab(results.printLabels)}.`);
  lines.push(`Label audit self-test on a planted copy of the poster: ${Object.values(results.selfTest).filter(Boolean).length} of ${Object.keys(results.selfTest).length} planted faults caught (label on label, label on a sign tag, label on a line, label past the edge, 11 px text).`);
  for (const [w, a] of Object.entries(results.board)) {
    lines.push(`Board at ${w} px: scrollWidth ${a.scrollWidth} of ${a.clientWidth}, smallest text ${a.minSize} px (${a.under13.length} under 13), ${a.lowContrast.length} low-contrast texts, images ${a.images.filter(i => i.ok).length}/${a.images.length}, axe ${axeN(a)} violating nodes, fonts ${a.fonts.length}; ${lab(a.labels)}.`);
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
    if (a.cardFit && a.cardFit.past.length) console.log(k, 'past card', JSON.stringify(a.cardFit.past.slice(0, 8)));
    if (a.labels && a.labels.total) console.log(k, 'labels', JSON.stringify([...a.labels.outside, ...a.labels.overlaps, ...a.labels.markOverlaps, ...a.labels.lineOverlaps].slice(0, 12)));
  }
})();
