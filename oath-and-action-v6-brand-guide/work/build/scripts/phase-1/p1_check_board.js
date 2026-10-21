// Check the Identity Refinement Board at 1440 and 390 px: horizontal overflow, broken images,
// fonts, heading order, and screenshots of key sections.
// Usage: node p1_check_board.js <board.html> <out_dir>
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [html, outDir] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const report = {};
  for (const width of [1440, 390]) {
    const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width, height: 1000 } });
    await page.goto('file://' + path.resolve(html), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    // force every lazy image to load, then wait for all
    await page.evaluate(async () => {
      const imgs = [...document.images];
      imgs.forEach(i => { i.loading = 'eager'; });
      await Promise.all(imgs.map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
    });
    const r = await page.evaluate(() => {
      const imgs = [...document.images];
      const broken = imgs.filter(i => !i.naturalWidth).map(i => i.getAttribute('src'));
      const de = document.documentElement;
      const wide = [...document.querySelectorAll('body *')].filter(e => {
        const b = e.getBoundingClientRect();
        return b.right > window.innerWidth + 1 && !e.closest('.scroll');
      }).slice(0, 10).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().right));
      const heads = [...document.querySelectorAll('h1,h2,h3')].map(h => h.tagName);
      let skips = 0;
      for (let i = 1; i < heads.length; i++) if (+heads[i][1] - +heads[i - 1][1] > 1) skips++;
      const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
      const small = [...document.querySelectorAll('p,li,td,th,figcaption,summary,span,a')].filter(e => {
        const fs = parseFloat(getComputedStyle(e).fontSize); return e.textContent.trim() && fs < 13;
      }).length;
      return { images: imgs.length, broken: broken.length, brokenSample: broken.slice(0, 5), scrollWidth: de.scrollWidth, innerWidth: window.innerWidth,
               overflowingOutsideScrollRegions: wide, height: de.scrollHeight, headingSkips: skips, fontsLoaded: [...new Set(fonts)], textUnder13px: small };
    });
    report[width] = r;
    for (const [i, sel] of ['header', '#item-3', '#item-4', '#item-5', '#item-6', '#item-7', '#item-10', '#decisions'].entries()) {
      await page.evaluate(s => document.querySelector(s).scrollIntoView(), sel);
      await page.screenshot({ path: path.join(outDir, `${width}-${String(i).padStart(2, '0')}-${sel.replace('#', '')}.png`) });
    }
    await page.close();
  }
  fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 1));
  console.log(JSON.stringify(report, null, 1));
  await browser.close();
})();
