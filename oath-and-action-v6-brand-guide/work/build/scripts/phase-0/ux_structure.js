// Phase 0 UX audit, part 1: information architecture and structure of V5 Polished.
// Usage: node ux_structure.js <project-root>
// Reads source/ only through a browser. Writes JSON to work/handoffs/phase-0/ux-data/ and screenshots to work/boards/screens/phase-0-ux/.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const PW = path.join(execSync('npm root -g').toString().trim(), 'playwright');
const { chromium } = require(PW);

const ROOT = path.resolve(process.argv[2] || '.');
const V5 = 'file://' + path.join(ROOT, 'source', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
const OUT = path.join(ROOT, 'work', 'handoffs', 'phase-0', 'ux-data');
const SHOTS = path.join(ROOT, 'work', 'boards', 'screens', 'phase-0-ux');
fs.mkdirSync(OUT, { recursive: true });
fs.mkdirSync(SHOTS, { recursive: true });

async function open(browser, width, height = 900) {
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto(V5);
  await page.waitForTimeout(1200);
  return page;
}

// Characters per line for body paragraphs: column width divided by the paragraph's mean glyph advance.
const measureFn = () => {
  const skip = '.report-page,.report-thumb,.app,.poster,.slide,.slide16,.email,.tile,.card,.stage,.icon-tile,.quote-card,.sig,.navbar,.phone,.browser,.social,.carousel,.event-kit,.timeline,.chart,.src,.section-foot,svg,dialog,table,.voice-row blockquote';
  const cv = document.createElement('canvas').getContext('2d');
  const rows = [];
  for (const p of document.querySelectorAll('section.chapter p')) {
    if (p.closest(skip)) continue;
    const cs = getComputedStyle(p);
    const fs = parseFloat(cs.fontSize);
    const text = p.textContent.replace(/\s+/g, ' ').trim();
    if (text.length < 90 || fs < 14 || fs > 24) continue;
    const r = p.getBoundingClientRect();
    if (r.width === 0) continue;
    cv.font = `${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const adv = cv.measureText(text).width / text.length;
    const range = document.createRange();
    range.selectNodeContents(p);
    const tops = new Set([...range.getClientRects()].map((q) => Math.round(q.top)));
    const sec = p.closest('section.chapter');
    rows.push({ chapter: sec && sec.id, cls: p.className || p.parentElement.className.split(' ')[0] || 'p', fs, width: Math.round(r.width), cpl: Math.round(r.width / adv), lines: tops.size, sample: text.slice(0, 50) });
  }
  return rows;
};

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const data = {};
  const page = await open(browser, 1440);

  // Heading outline in DOM order, with visibility and whether a button swallows it.
  data.headings = await page.evaluate(() => {
    const out = [];
    let prev = 0;
    for (const h of document.querySelectorAll('h1,h2,h3,h4,h5,h6')) {
      const lvl = Number(h.tagName[1]);
      const sec = h.closest('section');
      const inButton = !!h.closest('button');
      const cs = getComputedStyle(h);
      const hidden = h.closest('[hidden]') || cs.display === 'none' || cs.visibility === 'hidden';
      const exposed = !inButton && !hidden;
      const ctx = h.closest('.report-page,.app,.poster,.slide,.slide16,.email,.icon-tile,.chart,.phone,.browser,.social,.card,.tile,.stage,.navbar,.event-kit');
      const rec = { lvl, text: h.textContent.replace(/\s+/g, ' ').trim().slice(0, 70), chapter: sec && sec.id, inButton, exposed, specimen: ctx ? ctx.className.split(' ')[0] : null };
      if (exposed) { rec.skip = prev && lvl > prev + 1 ? `h${prev} to h${lvl}` : null; prev = lvl; }
      out.push(rec);
    }
    return out;
  });

  // Landmarks and regions.
  data.landmarks = await page.evaluate(() => {
    const sel = 'header,nav,main,footer,aside,form,[role=banner],[role=navigation],[role=main],[role=contentinfo],[role=complementary],[role=region],section[aria-labelledby],section[aria-label],dialog';
    return [...document.querySelectorAll(sel)].map((e) => ({ tag: e.tagName.toLowerCase(), id: e.id || null, cls: e.className && String(e.className).split(' ')[0], label: e.getAttribute('aria-label') || (e.getAttribute('aria-labelledby') && document.getElementById(e.getAttribute('aria-labelledby'))?.textContent.trim().slice(0, 50)) || null, insideMain: !!e.closest('main'), insideSection: !!(e.parentElement && e.parentElement.closest('section')) }));
  });
  data.ariaSnapshotNav = await page.locator('nav.site-nav').ariaSnapshot();
  data.ariaSnapshotToc = await page.locator('nav.toc').ariaSnapshot();

  // Anchors: every link whose href starts with # outside SVG.
  data.anchors = await page.evaluate(() => {
    const out = [];
    for (const a of document.querySelectorAll('a[href^="#"]')) {
      if (a.closest('svg')) continue;
      const id = a.getAttribute('href').slice(1);
      const t = document.getElementById(id);
      out.push({ href: '#' + id, text: a.textContent.replace(/\s+/g, ' ').trim().slice(0, 40), where: a.closest('nav') ? a.closest('nav').getAttribute('aria-label') : (a.closest('section') || {}).id, targetExists: !!t, targetTag: t && t.tagName.toLowerCase(), targetFocusable: t ? t.tabIndex >= 0 : null });
    }
    return out;
  });
  data.sections = await page.evaluate(() => [...document.querySelectorAll('section[id]')].map((s) => ({ id: s.id, part: s.dataset.part || null, title: (s.querySelector('h1,h2') || {}).textContent })));
  data.duplicateIds = await page.evaluate(() => { const c = {}; document.querySelectorAll('[id]').forEach((e) => { c[e.id] = (c[e.id] || 0) + 1; }); return Object.entries(c).filter(([, n]) => n > 1); });
  data.textCrossRefs = await page.evaluate(() => {
    const out = [];
    const re = /chapter\s+\d{2}/gi;
    const walker = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
    let n;
    while ((n = walker.nextNode())) { const m = n.textContent.match(re); if (m) out.push({ chapter: n.parentElement.closest('section').id, refs: m, linked: !!n.parentElement.closest('a') }); }
    return out;
  });

  // aria-current of the top navigation as each chapter scrolls into view.
  data.navCurrent = [];
  for (const s of data.sections) {
    await page.evaluate((id) => { const el = document.getElementById(id); window.scrollTo(0, el.offsetTop + 40); }, s.id);
    await page.waitForTimeout(250);
    const cur = await page.evaluate(() => [...document.querySelectorAll('.nav-links a[aria-current]')].map((a) => a.textContent));
    data.navCurrent.push({ section: s.id, part: s.part, current: cur });
  }
  data.navHeight1440 = await page.evaluate(() => document.querySelector('.site-nav').getBoundingClientRect().height);
  data.measure1440 = await page.evaluate(measureFn);
  await page.close();

  // Phone navigation at 390 and 360.
  for (const w of [390, 360, 320]) {
    const p = await open(browser, w, 844);
    const nav = await p.evaluate(() => {
      const n = document.querySelector('.site-nav').getBoundingClientRect();
      const l = document.querySelector('.nav-links');
      const links = [...l.querySelectorAll('a')].map((a) => { const r = a.getBoundingClientRect(); return { text: a.textContent, left: Math.round(r.left), right: Math.round(r.right), w: Math.round(r.width), h: Math.round(r.height), visible: r.right <= innerWidth && r.left >= 0 }; });
      return { navHeight: Math.round(n.height), linksScrollWidth: l.scrollWidth, linksClientWidth: l.clientWidth, scrollbarHidden: getComputedStyle(l).scrollbarWidth, fontSize: getComputedStyle(l).fontSize, links, scrollPaddingTop: getComputedStyle(document.documentElement).scrollPaddingTop, navShareOfViewport: Math.round((n.height / innerHeight) * 100) };
    });
    data['nav' + w] = nav;
    await p.screenshot({ path: path.join(SHOTS, `nav-${w}.png`), clip: { x: 0, y: 0, width: w, height: 200 } });
    if (w === 390) {
      data.measure390 = await p.evaluate(measureFn);
      // Contents list at 390
      const toc = await p.evaluate(() => { const t = document.querySelector('nav.toc'); const r = t.getBoundingClientRect(); return { top: Math.round(r.top + scrollY), height: Math.round(r.height) }; });
      data.toc390 = toc;
    }
    await p.close();
  }

  fs.writeFileSync(path.join(OUT, '20261020_UX-Structure-Data.json'), JSON.stringify(data, null, 1));
  await browser.close();
  console.log('done');
})();
