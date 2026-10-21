// Creative director, Phase 1: render checks for the Strategy and Direction board.
// Usage: node work/build/scripts/phase-1/cd_check_board.js <project root>
// Renders the board in Chromium at 1440 and 390 px, then reports horizontal overflow,
// text under 13 px (HTML and SVG), images that failed to load, red that touches Prussian,
// web font status, visible word count, a keyboard pass and an axe-core scan.
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

const ROOT = path.resolve(process.argv[2] || '.');
const BOARD = path.join(ROOT, 'work/boards/20261021_Strategy-And-Direction-Board.html');
const OUTDIR = path.join(ROOT, 'work/boards/phase-1/strategy');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');

async function inspect(page, width) {
  return page.evaluate((width) => {
    const out = { width };
    const de = document.documentElement;
    out.scrollWidth = de.scrollWidth;
    out.clientWidth = de.clientWidth;
    out.pageOverflowPx = Math.max(0, de.scrollWidth - de.clientWidth);
    const inScroll = (el) => !!el.closest('.scroll');
    const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
    // elements sticking out past the viewport
    out.beyondViewport = [];
    for (const el of document.querySelectorAll('body *')) {
      if (!visible(el) || inScroll(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.right > de.clientWidth + 0.5 || r.left < -0.5) {
        out.beyondViewport.push({ tag: el.tagName.toLowerCase(), cls: el.className && el.className.baseVal === undefined ? el.className : '', text: (el.textContent || '').trim().slice(0, 60), left: Math.round(r.left), right: Math.round(r.right) });
      }
    }
    // boxes whose own content overflows them (clipping risk)
    out.innerOverflow = [];
    for (const el of document.querySelectorAll('p, li, td, th, h1, h2, h3, h4, dd, dt, figcaption, span, a, div')) {
      if (!visible(el) || inScroll(el) || el.classList.contains('scroll')) continue;
      if (el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflowX !== 'visible') {
        out.innerOverflow.push({ tag: el.tagName.toLowerCase(), text: (el.textContent || '').trim().slice(0, 60), sw: el.scrollWidth, cw: el.clientWidth });
      }
    }
    // smallest HTML text
    const small = [];
    let minHtml = 999;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const t = walker.currentNode; if (!t.textContent.trim()) continue;
      const el = t.parentElement; if (!el || el.closest('svg')) continue;
      if (!visible(el)) continue;
      const fs = parseFloat(getComputedStyle(el).fontSize);
      minHtml = Math.min(minHtml, fs);
      if (fs < 13) small.push({ text: t.textContent.trim().slice(0, 50), fs });
    }
    out.minHtmlFontPx = minHtml;
    out.htmlUnder13 = small;
    // rendered size of SVG text
    let minSvg = 999; const svgSmall = [];
    for (const tx of document.querySelectorAll('svg text')) {
      if (!visible(tx)) continue;
      const ctm = tx.getScreenCTM();
      const fs = parseFloat(getComputedStyle(tx).fontSize) * Math.hypot(ctm.a, ctm.b);
      minSvg = Math.min(minSvg, fs);
      if (fs < 13) svgSmall.push({ text: tx.textContent.trim(), px: Math.round(fs * 10) / 10 });
    }
    out.minSvgTextPx = minSvg === 999 ? null : Math.round(minSvg * 10) / 10;
    out.svgUnder13 = svgSmall;
    // images
    out.images = [...document.images].map((im) => ({ src: im.getAttribute('src'), ok: im.complete && im.naturalWidth > 0, alt: !!im.getAttribute('alt') }));
    out.brokenImages = out.images.filter((i) => !i.ok).map((i) => i.src);
    // red touching Prussian: any red text, fill or background whose nearest painted background is Prussian
    const RED = 'rgb(230, 57, 70)', PRU = 'rgb(31, 45, 90)';
    const bgOf = (el) => { for (let e = el; e; e = e.parentElement) { const b = getComputedStyle(e).backgroundColor; if (b && b !== 'rgba(0, 0, 0, 0)' && b !== 'transparent') return b; } return 'none'; };
    out.redOnPrussian = [];
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      const red = cs.color === RED && (el.childNodes.length && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()))
        || cs.backgroundColor === RED || (el instanceof SVGElement && (cs.fill === RED));
      if (!red) continue;
      const parentBg = bgOf(el.parentElement);
      if (parentBg === PRU) out.redOnPrussian.push({ tag: el.tagName.toLowerCase(), text: (el.textContent || '').trim().slice(0, 40) });
    }
    // fonts
    out.fonts = {
      interTight800: document.fonts.check('800 16px "Inter Tight"'),
      interTight600: document.fonts.check('600 16px "Inter Tight"'),
      inter400: document.fonts.check('400 16px "Inter"'),
      inter700: document.fonts.check('700 16px "Inter"'),
      loraItalic: document.fonts.check('italic 400 16px "Lora"'),
    };
    out.fontFacesLoaded = [...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family} ${f.weight} ${f.style}`);
    // word count of visible text in main
    out.words = (document.querySelector('main').innerText.match(/[A-Za-z0-9][A-Za-z0-9'’.,:;()\/-]*/g) || []).length;
    out.pageHeight = de.scrollHeight;
    return out;
  }, width);
}

async function keyboardPass(page) {
  const stops = [];
  await page.evaluate(() => window.scrollTo(0, 0));
  for (let i = 0; i < 40; i++) {
    await page.keyboard.press('Tab');
    const info = await page.evaluate(() => {
      const a = document.activeElement; if (!a || a === document.body) return null;
      const cs = getComputedStyle(a);
      return { tag: a.tagName.toLowerCase(), text: (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0, 40), outline: cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0 };
    });
    if (!info) break;
    stops.push(info);
  }
  return stops;
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const report = { board: path.relative(ROOT, BOARD), runs: [] };
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    await page.goto('file://' + BOARD, { waitUntil: 'networkidle' });
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((im) => im.decode().catch(() => null))); });
    const res = await inspect(page, w);
    res.keyboard = await keyboardPass(page);
    res.keyboardStops = res.keyboard.length;
    res.keyboardWithoutOutline = res.keyboard.filter((k) => !k.outline);
    delete res.keyboard;
    await page.addScriptTag({ path: AXE });
    res.axe = await page.evaluate(async () => {
      const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } });
      return { version: axe.version, violations: r.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes.slice(0, 3).map((n) => n.target.join(' ')) })), passes: r.passes.length, incomplete: r.incomplete.map((v) => ({ id: v.id, nodes: v.nodes.length })) };
    });
    await page.evaluate(() => window.scrollTo(0, 0));
    const shot = path.join(OUTDIR, `20261021_Strategy-Board-Render-${w}.jpg`);
    await page.screenshot({ path: shot, fullPage: true, type: 'jpeg', quality: 70 });
    res.screenshot = path.relative(ROOT, shot);
    report.runs.push(res);
    await ctx.close();
  }
  await browser.close();
  const outFile = path.join(OUTDIR, '20261021_Board-Render-Report.json');
  fs.writeFileSync(outFile, JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
})();
