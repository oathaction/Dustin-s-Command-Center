// Measure Board 6, section 1 (November 7, 2026) on the rendered page, and capture it for review.
// Usage: node work/build/scripts/phase-2/board6_tracker_measure.js
//
// Reads  work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker.html
// Writes work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker-Measurements.json, which the build prints on the board
//        work/boards/phase-2/board-6/tracker/captures/  (each option's state key and 360 px lists at twice size, the
//        comparison at 1440 px in color and in grayscale, and the page at 390 px)
// At 1440 and 390 px it measures: every take-part link and ask button (target size, WCAG 2.2 2.5.8), the table of
// contents links, the smallest drawn mark that carries a state, the smallest text, the rendered contrast of each mark and
// text role against its panel, the height of Option D's list for one bill at 360 px, and every Tab stop's focus ring.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const DIR = path.join(ROOT, 'work/boards/phase-2/board-6/tracker');
const FILE = path.join(DIR, '20261107_Board-6-Tracker.html');
const OUT = path.join(DIR, '20261107_Board-6-Tracker-Measurements.json');
const CAP = path.join(DIR, 'captures');
fs.mkdirSync(CAP, { recursive: true });

function measure() {
  const parse = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return +((Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05)).toFixed(2); };
  const box = (sel) => {
    const els = [...document.querySelectorAll(sel)].filter(e => e.getClientRects().length);
    const rs = els.map(e => e.getBoundingClientRect());
    return { count: els.length, minW: Math.min(...rs.map(r => r.width)), minH: Math.min(...rs.map(r => r.height)) };
  };
  const out = { targets: { cta: box('.tkp .cta'), ask: box('.ask'), toc: box('.toc a') } };
  // smallest drawn mark that carries a state: circles and squares in tracker marks, outside the retiring grids
  let minMark = 99, minRed = 99;
  document.querySelectorAll('.tkp svg.mk circle, .tkp svg.mk rect[width="11"]').forEach((el) => {
    if (el.closest('.ba-mark')) return;
    if (el.closest('[data-red]')) { const r = el.getBoundingClientRect(); if (r.width) minRed = Math.min(minRed, r.width + (parseFloat(getComputedStyle(el).strokeWidth) || 0)); return; }
    const r = el.getBoundingClientRect(); if (!r.width) return;
    const sw = parseFloat(getComputedStyle(el).strokeWidth) || 0;
    const stroked = getComputedStyle(el).stroke !== 'none';
    minMark = Math.min(minMark, Math.max(r.width, r.height) + (stroked ? sw : 0));
  });
  // smallest visible text
  let minText = 99;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode; if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (!el || el.closest('style,script,.sr')) continue;
    if (!el.getClientRects().length) continue;
    let size = parseFloat(getComputedStyle(el).fontSize);
    if (el instanceof SVGElement) { const s = el.closest('svg'); const vb = s.viewBox.baseVal; if (vb && vb.width) size *= s.getBoundingClientRect().width / vb.width; }
    minText = Math.min(minText, size);
  }
  out.marks = { minMark: +minMark.toFixed(2), minRed: +minRed.toFixed(2), minText: +minText.toFixed(2) };
  // rendered contrast of each role against its panel
  out.contrast = [];
  for (const [surf, sel] of [['Newsprint', '.tkp.oa-surface-newsprint'], ['Charcoal', '.tkp.oa-surface-charcoal']]) {
    const panel = document.querySelector('#option-b ' + sel); const bg = parse(getComputedStyle(panel).backgroundColor);
    const pick = (s, prop) => { const el = panel.querySelector(s); return el ? parse(getComputedStyle(el)[prop]) : null; };
    const roles = [
      ['Done mark', pick('svg.mk circle.fi', 'fill')],
      ['Not yet ring', pick('svg.mk circle.ss', 'stroke')],
      ['Red badge', pick('svg.mk circle.fr', 'fill')],
      ['Red badge keyline', pick('svg.mk circle.fr', 'stroke')],
      ['Not yet number', pick('svg.mk text.tl', 'fill')],
      ['Status text', pick('.st', 'color')],
      ['Key text', pick('.key-steps li', 'color')],
    ];
    for (const [name, c] of roles) if (c) out.contrast.push({ surface: surf, role: name, ratio: ratio(c, bg) });
    const done = panel.querySelector('svg.mk circle.fi'), num = done && done.parentElement.querySelector('text');
    if (num) out.contrast.push({ surface: surf, role: 'Number on a done step', ratio: ratio(parse(getComputedStyle(num).fill), parse(getComputedStyle(done).fill)) });
  }
  const ask = document.querySelector('.ask');
  if (ask) { const cs = getComputedStyle(ask); out.contrast.push({ surface: 'Newsprint', role: 'Ask button label, 19 px bold', ratio: ratio(parse(cs.color), parse(cs.backgroundColor)) }); }
  // Option D: height of one bill's list at 360 px
  const dl = [...document.querySelectorAll('#option-d .tkp--s .row')].map(r => Math.round(r.getBoundingClientRect().height));
  out.optionD360RowHeights = dl;
  out.pageHeight = document.documentElement.scrollHeight;
  out.sidewaysScroll = document.documentElement.scrollWidth > document.documentElement.clientWidth + 1;
  return out;
}

(async () => {
  const browser = await chromium.launch();
  const result = { file: path.relative(ROOT, FILE), measured: '', widths: {} };
  for (const width of [1440, 390]) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    await page.goto('file://' + FILE, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    const m = await page.evaluate(measure);
    // every Tab stop shows a ring
    const stops = [];
    await page.evaluate(() => window.scrollTo(0, 0));
    for (let i = 0; i < 400; i++) {
      await page.keyboard.press('Tab');
      const r = await page.evaluate(() => {
        const el = document.activeElement; if (!el || el === document.body) return null;
        const cs = getComputedStyle(el);
        return { tag: el.tagName, label: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 40), ring: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2 };
      });
      if (!r) break;
      if (stops.length && stops[0].label === r.label && stops[0].tag === r.tag && i > 2) break;
      stops.push(r);
    }
    m.focus = { stops: stops.length, withoutRing: stops.filter(s => !s.ring) };
    result.widths[width] = m;
    if (width === 1440) {
      const shots = [['#compare .mxw', 'Compare-1440'], ['#grid .ba', 'Grid-Before-After-1440']];
      for (const k of ['a', 'b', 'c', 'd']) shots.push([`#option-${k} .skey`, `Option-${k.toUpperCase()}-States`]);
      for (const [sel, name] of shots) {
        const el = await page.$(sel); if (el) await el.screenshot({ path: path.join(CAP, `20261107_Board-6-Tracker-${name}.png`) });
      }
      const gray = await page.addStyleTag({ content: 'html{filter:grayscale(1)!important}' });
      const el = await page.$('#compare .mxw'); if (el) await el.screenshot({ path: path.join(CAP, '20261107_Board-6-Tracker-Compare-1440-Grayscale.png') });
      await gray.evaluate((e) => e.remove());
    }
    await ctx.close();
  }
  // twice size: each option's 360 px list on Newsprint, and the state keys
  const ctx2 = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  const p2 = await ctx2.newPage();
  await p2.goto('file://' + FILE, { waitUntil: 'networkidle' });
  await p2.evaluate(() => document.fonts.ready);
  await p2.waitForTimeout(400);
  for (const k of ['a', 'b', 'c', 'd']) {
    const el = await p2.$(`#option-${k} .tkp--s.oa-surface-newsprint`);
    if (el) await el.screenshot({ path: path.join(CAP, `20261107_Board-6-Tracker-Option-${k.toUpperCase()}-360-Newsprint-2x.png`) });
  }
  const bp = await p2.$('#option-d .bp.tkp--s.oa-surface-newsprint');
  if (bp) await bp.screenshot({ path: path.join(CAP, '20261107_Board-6-Tracker-Option-D-Bill-Page-360-2x.png') });
  await ctx2.close();
  await browser.close();
  const d = new Date();
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  result.measured = `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  const w = result.widths[1440];
  result.targets = w.targets; result.marks = w.marks;
  fs.writeFileSync(OUT, JSON.stringify(result, null, 1));
  console.log(JSON.stringify({ targets1440: w.targets, targets390: result.widths[390].targets, marks: w.marks, contrast: w.contrast, d360: w.optionD360RowHeights,
    focus1440: { stops: w.focus.stops, without: w.focus.withoutRing.length }, focus390: { stops: result.widths[390].focus.stops, without: result.widths[390].focus.withoutRing.length },
    sideways390: result.widths[390].sidewaysScroll }, null, 1));
})();
