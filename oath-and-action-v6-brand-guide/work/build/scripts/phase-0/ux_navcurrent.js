// Phase 0 UX audit: which top-navigation link carries aria-current as each chapter fills the reading band.
// Usage: node ux_navcurrent.js <project-root>
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = path.resolve(process.argv[2] || '.');
const V5 = 'file://' + path.join(ROOT, 'source', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(V5); await p.waitForTimeout(1000);
  const ids = await p.evaluate(() => [...document.querySelectorAll('section[id]')].map((s) => [s.id, s.dataset.part || null]));
  for (const [id, part] of ids) {
    await p.evaluate((i) => { const el = document.getElementById(i); window.scrollTo({ top: el.offsetTop + 200, behavior: 'instant' }); }, id);
    await p.waitForTimeout(500);
    const cur = await p.evaluate(() => [...document.querySelectorAll('.nav-links a[aria-current]')].map((a) => a.textContent + '=' + a.getAttribute('aria-current')));
    console.log(JSON.stringify({ id, part, current: cur }));
  }
  await b.close();
})();
