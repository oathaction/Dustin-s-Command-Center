// Concept 3, Public sign: check the concept board in Chromium at 1440 and 390 px.
// Usage: node icons_r2_sign_board_check.js <board.html> <results.json> <screens_dir>
// Checks at each width: no sideways scroll, no text under 13 px, every image loaded, the Material
// Symbols font loaded. Saves one screenshot per section at each width.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [board, out, shots] = process.argv.slice(2);
  fs.mkdirSync(shots, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const results = {};
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width, height: 900 } });
    await page.goto('file://' + path.resolve(board), { waitUntil: 'networkidle' });
    // Walk the page so lazy images load, then wait for them and for fonts.
    const h = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < h; y += 700) {
      await page.evaluate((yy) => window.scrollTo(0, yy), y);
      await page.waitForTimeout(40);
    }
    await page.evaluate(async () => {
      await Promise.all([...document.images].map((im) => im.complete ? null : new Promise((r) => { im.onload = im.onerror = r; })));
      await document.fonts.ready;
    });
    await page.evaluate(() => window.scrollTo(0, 0));
    const r = await page.evaluate(() => {
      const de = document.documentElement;
      const small = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walker.nextNode())) {
        if (!n.textContent.trim()) continue;
        const el = n.parentElement;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        const fs = parseFloat(cs.fontSize);
        if (fs < 13) small.push({ tag: el.tagName, cls: el.className, size: fs, text: n.textContent.trim().slice(0, 40) });
      }
      const imgs = [...document.images];
      const broken = imgs.filter((im) => !(im.complete && im.naturalWidth > 0)).map((im) => im.getAttribute('src'));
      const wide = [...document.querySelectorAll('main *')].filter((el) => {
        const b = el.getBoundingClientRect();
        if (b.width === 0) return false;
        let p = el.parentElement, inScroller = false;
        while (p) { const ov = getComputedStyle(p).overflowX; if (ov === 'auto' || ov === 'scroll') { inScroller = true; break; } p = p.parentElement; }
        return !inScroller && b.right > window.innerWidth + 0.5;
      }).slice(0, 10).map((el) => el.tagName + '.' + el.className);
      return {
        scrollWidth: de.scrollWidth, innerWidth: window.innerWidth, sideways: de.scrollWidth > window.innerWidth,
        textUnder13: small.length, textUnder13Samples: small.slice(0, 10),
        images: imgs.length, broken: broken.length, brokenSamples: broken.slice(0, 10),
        materialFont: document.fonts.check('24px "Material Symbols Outlined"'),
        overflowing: wide, height: de.scrollHeight,
      };
    });
    results[width] = r;
    const ids = await page.evaluate(() => [...document.querySelectorAll('main > section, main')].map((s) => s.id || ''));
    const sections = await page.$$('main > section');
    // first screen
    await page.screenshot({ path: path.join(shots, `w${width}-00-first-screen.png`) });
    for (let i = 0; i < sections.length; i++) {
      const id = await sections[i].getAttribute('id');
      await sections[i].screenshot({ path: path.join(shots, `w${width}-${String(i + 1).padStart(2, '0')}-${id}.png`) });
    }
    await page.close();
  }
  await browser.close();
  fs.writeFileSync(out, JSON.stringify(results, null, 2));
  for (const [w, r] of Object.entries(results)) {
    console.log(w, 'sideways', r.sideways, 'text<13', r.textUnder13, 'images', r.images, 'broken', r.broken, 'material', r.materialFont, 'overflowing', r.overflowing.length, 'height', r.height);
  }
})();
