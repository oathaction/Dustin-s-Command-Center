// Phase 0 UX audit: where each contents link lands relative to the sticky nav, and where Tab goes next.
// Usage: node ux_anchor_landing.js <project-root>
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = path.resolve(process.argv[2] || '.');
const V5 = 'file://' + path.join(ROOT, 'source', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const w of [1440, 390]) {
    const ctx = await b.newContext({ viewport: { width: w, height: 844 }, reducedMotion: 'reduce' });
    const p = await ctx.newPage();
    await p.goto(V5); await p.waitForTimeout(1000);
    const hrefs = await p.$$eval('nav.toc a', (as) => as.map((a) => a.getAttribute('href')));
    const rows = [];
    for (const h of hrefs) {
      await p.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
      await p.focus(`nav.toc a[href="${h}"]`);
      await p.keyboard.press('Enter');
      await p.waitForTimeout(250);
      const r = await p.evaluate((id) => { const s = document.querySelector(id); const e = s.querySelector('.eyebrow') || s; const n = document.querySelector('.site-nav').getBoundingClientRect(); return { eyebrowTop: Math.round(e.getBoundingClientRect().top), navBottom: Math.round(n.bottom) }; }, h);
      await p.keyboard.press('Tab');
      const next = await p.evaluate(() => { const a = document.activeElement; return (a.closest('section') || {}).id + ':' + (a.getAttribute('aria-label') || a.textContent).trim().slice(0, 24); });
      rows.push(`${h} eyebrowTop=${r.eyebrowTop} navBottom=${r.navBottom} nextTab=${next}`);
    }
    console.log(w + '\n' + rows.join('\n'));
    await ctx.close();
  }
  await b.close();
})();
