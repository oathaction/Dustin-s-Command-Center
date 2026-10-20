// Phase 0 UX audit: extra measurements (chart label size, icon size selector, status text, hinge and lever under reduced motion).
// Usage: node ux_extras.js <project-root>
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = path.resolve(process.argv[2] || '.');
const V5 = 'file://' + path.join(ROOT, 'source', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
const SHOTS = path.join(ROOT, 'work', 'boards', 'screens', 'phase-0-ux');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(V5); await p.waitForTimeout(1000);
    const r = await p.evaluate(() => {
      const charts = [...document.querySelectorAll('#data .chart svg[role="img"]')].map((s) => { const t = s.querySelector('text.lab'); const sc = s.getBoundingClientRect().width / s.viewBox.baseVal.width; return Math.round(parseFloat(getComputedStyle(t).fontSize) * sc * 10) / 10; });
      const st = [...document.querySelectorAll('#data .trow .st')].map((e) => getComputedStyle(e).fontSize + ' ' + getComputedStyle(e).color + ' ' + getComputedStyle(e).textTransform);
      const tiles = [...document.querySelectorAll('#in-use .app')].slice(0, 3).map((a) => { const t = [...a.querySelectorAll('*')].filter((e) => [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())); const sizes = t.map((e) => parseFloat(getComputedStyle(e).fontSize)); return { cls: a.className, min: Math.min(...sizes), w: Math.round(a.getBoundingClientRect().width) }; });
      return { charts, st, tiles, modalTop: getComputedStyle(document.querySelector('.modal-top')).fontSize };
    });
    console.log(w, JSON.stringify(r));
    if (w === 1440) {
      await p.selectOption('#icon-size', '16'); await p.waitForTimeout(150);
      const t = p.locator('.icon-tile').first();
      await t.scrollIntoViewIfNeeded();
      console.log('icon at 16 option', JSON.stringify(await p.evaluate(() => { const s = document.querySelector('.icon-tile svg'); const r = s.getBoundingClientRect(); return { w: r.width, inline: s.getAttribute('style'), varSize: getComputedStyle(document.getElementById('icon-browser')).getPropertyValue('--icon-size') }; })));
      await p.locator('#icon-grid').screenshot({ path: path.join(SHOTS, 'icons-size-16-option.png') });
    }
    await p.close();
  }
  await b.close();
})();
