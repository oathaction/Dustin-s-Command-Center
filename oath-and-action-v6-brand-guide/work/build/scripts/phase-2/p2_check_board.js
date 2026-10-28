// Check the Identity Masters Board at 1440 and 390 px, with its panels closed and open.
// Usage: node p2_check_board.js <absolute board path> <absolute out dir>
// Writes check.json and viewport-sized screenshots (segments) for review and the red audit.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [board, outDir] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const results = {};
  const states = process.env.HIDE_SPECIMENS ? ['open'] : ['closed', 'open'];
  for (const width of [1440, 390]) {
    for (const state of states) {
      const page = await browser.newPage({ viewport: { width, height: 1000 }, deviceScaleFactor: 1 });
      await page.goto('file://' + board, { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      if (state === 'open') await page.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
      if (process.env.HIDE_SPECIMENS) await page.evaluate(() => document.querySelectorAll('[data-redspecimen]').forEach(e => e.style.display = 'none'));
      await page.evaluate(() => document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; }));
      // scroll through so every image is requested, then wait for them
      const h0 = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < h0; y += 900) { await page.evaluate(v => window.scrollTo(0, v), y); }
      await page.evaluate(async () => {
        const imgs = [...document.images];
        await Promise.all(imgs.map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
      });
      const r = await page.evaluate(() => {
        const doc = document.documentElement;
        const imgs = [...document.images];
        const broken = imgs.filter(i => !i.naturalWidth).map(i => i.getAttribute('src'));
        const small = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = walker.nextNode())) {
          if (!n.textContent.trim()) continue;
          const el = n.parentElement;
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          const rect = el.getBoundingClientRect();
          if (!rect.width && !rect.height) continue;
          const fs = parseFloat(cs.fontSize);
          if (fs < 13) small.push({ text: n.textContent.trim().slice(0, 40), size: fs, tag: el.tagName });
        }
        const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
        let skips = 0;
        for (let i = 1; i < heads.length; i++) if (heads[i] > heads[i - 1] + 1) skips++;
        const wide = [...document.querySelectorAll('body *')].filter(e => {
          const b = e.getBoundingClientRect();
          if (!b.width) return false;
          // elements inside a horizontal scroller are allowed to overflow it
          let p = e.parentElement; while (p) { if (p.classList && p.classList.contains('scroll')) return false; p = p.parentElement; }
          return b.right > window.innerWidth + 0.5;
        }).slice(0, 10).map(e => e.tagName + '.' + e.className);
        return { scrollWidth: doc.scrollWidth, innerWidth: window.innerWidth, horizontalScroll: doc.scrollWidth > window.innerWidth,
                 height: doc.scrollHeight, images: imgs.length, broken: broken.length, brokenList: broken.slice(0, 10),
                 textUnder13: small.length, smallSamples: small.slice(0, 10), headingSkips: skips, overflowingElements: wide };
      });
      results[`${width}_${state}`] = r;
      // segment screenshots
      const segDir = path.join(outDir, `${width}_${state}`);
      fs.mkdirSync(segDir, { recursive: true });
      const H = r.height;
      let k = 0;
      for (let y = 0; y < H; y += 1000) {
        await page.evaluate(v => window.scrollTo(0, v), y);
        await page.waitForTimeout(30);
        await page.screenshot({ path: path.join(segDir, `seg-${String(k).padStart(3, '0')}.png`) });
        k++;
      }
      results[`${width}_${state}`].segments = k;
      await page.close();
    }
  }
  fs.writeFileSync(path.join(outDir, 'check.json'), JSON.stringify(results, null, 1));
  await browser.close();
})();
