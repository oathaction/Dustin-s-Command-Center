const path = require('path'); const { chromium } = require('playwright');
const [page, out, ...sids] = process.argv.slice(2);
(async () => { const b = await chromium.launch();
  for (const [w, sc] of [[1440, 1], [390, 1], [1440, 2], [390, 2]]) {
    const p = await b.newPage({ viewport: { width: w, height: 3000 }, deviceScaleFactor: sc });
    await p.goto('file://' + page, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    for (const sid of sids) {
      const fig = p.locator(`#fig-${sid}`);
      await fig.evaluate((e) => e.scrollIntoView({ block: 'start' })); await p.waitForTimeout(300);
      const r = await fig.evaluate((e) => { const q = e.getBoundingClientRect(); return { y: q.y, h: q.height, w: q.width }; });
      await p.screenshot({ path: path.join(out, `${sid}-${w}@${sc}x.png`), clip: { x: 0, y: Math.max(0, r.y - 4), width: w, height: Math.min(2990, r.h + 8) } });
      console.log(sid, w, sc, JSON.stringify(r));
    }
    await p.close(); }
  await b.close(); })();
