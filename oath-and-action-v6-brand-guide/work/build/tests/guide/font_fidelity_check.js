// Font fidelity (Gate 2, November 11, 2026, guide engineer): the embedded fonts draw exactly what Google's did.
// Usage, from work/build: node tests/guide/font_fidelity_check.js [V7_PAGE] [PREVIEW] [--json OUT]
// It opens version 7's page, whose fonts load from Google Fonts (asked for with the Chrome 153 user agent that
// fonts_fetch.py used, so Google serves the same files), and the preview, whose fonts sit inside the page, at 1440 px
// and device scale 1, hides the sticky masthead, and screenshots the same elements in each: chapter heads, rule
// titles, rule text, the cover's tagline and pillars, a part opener, and the first ten pieces of text the page sets in
// Lora. Every pair must match pixel for pixel. Exit 1 on any difference. The chapters are the same bytes in both pages
// (the preview changes no chapter), so any difference comes from the fonts.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '../../../..');
const args = process.argv.slice(2).filter((x, i, a) => !x.startsWith('--') && a[i - 1] !== '--json');
const v7 = path.resolve(args[0] || path.join(ROOT, 'work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html'));
const pv = path.resolve(args[1] || path.join(ROOT, 'work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html'));
const ji = process.argv.indexOf('--json');
const outJson = ji > 0 ? path.resolve(process.argv[ji + 1]) : path.join(ROOT, 'work/boards/phase-2/gate-2/evidence/20261111_Font-Fidelity-Results.json');
const UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36';
const SELS = ['#purpose .ch-head', '#rule-06-2 .rule-h', '#rule-05-3 .rule-text', '#voice .ch-head', '#rule-17-8 .rule-h', '#tokens .ch-head', '.cover .tagline', '.cover .pillars', '#part-foundations .part-inner'];
(async () => {
  const b = await chromium.launch();
  const shots = {};
  const lora = {};
  const requests = {};
  for (const [k, f] of [['v7', v7], ['pv', pv]]) {
    const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, userAgent: UA });
    const p = await ctx.newPage();
    const reqs = [];
    p.on('request', (r) => { if (/gstatic|googleapis/.test(r.url())) reqs.push(r.url()); });
    await p.goto('file://' + f, { waitUntil: 'load' });
    await p.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
    await p.evaluate(() => document.fonts.ready);
    await p.addStyleTag({ content: '.masthead { visibility: hidden !important } *, *::before, *::after { transition: none !important; animation: none !important }' });
    await p.waitForTimeout(300);
    shots[k] = {};
    for (const s of SELS) { const loc = p.locator(s).first(); if (await loc.count()) shots[k][s] = await loc.screenshot(); }
    // the first ten pieces of text the page sets in Lora, outside specimens and inside them
    const n = await p.evaluate(() => { let i = 0; for (const el of document.querySelectorAll('main *')) { if (i >= 10) break; const cs = getComputedStyle(el); if (/^"?Lora/.test(cs.fontFamily) && [...el.childNodes].some((x) => x.nodeType === 3 && x.textContent.trim()) && el.getBoundingClientRect().width > 0) { el.setAttribute('data-fid', String(i++)); } } return i; });
    lora[k] = [];
    for (let i = 0; i < n; i++) lora[k].push(await p.locator(`[data-fid="${i}"]`).screenshot().catch(() => null));
    requests[k] = reqs.length;
    await ctx.close();
  }
  const page = await (await b.newContext()).newPage();
  const cmp = async (a, c) => page.evaluate(async ([x64, y64]) => {
    const load = (s) => new Promise((res) => { const i = new Image(); i.onload = () => res(i); i.src = 'data:image/png;base64,' + s; });
    const [x, y] = await Promise.all([load(x64), load(y64)]);
    if (x.width !== y.width || x.height !== y.height) return { size: `${x.width}x${x.height} vs ${y.width}x${y.height}` };
    const cv = document.createElement('canvas'); cv.width = x.width; cv.height = x.height; const g = cv.getContext('2d');
    g.drawImage(x, 0, 0); const a = g.getImageData(0, 0, x.width, x.height).data; g.clearRect(0, 0, x.width, x.height); g.drawImage(y, 0, 0); const d = g.getImageData(0, 0, x.width, x.height).data;
    let n = 0, max = 0; for (let i = 0; i < a.length; i += 4) { const m = Math.max(Math.abs(a[i] - d[i]), Math.abs(a[i + 1] - d[i + 1]), Math.abs(a[i + 2] - d[i + 2])); if (m) { n++; if (m > max) max = m; } }
    return { w: x.width, h: x.height, differ: n, max };
  }, [a.toString('base64'), c.toString('base64')]);
  const res = [];
  for (const s of SELS) if (shots.v7[s] && shots.pv[s]) res.push({ el: s, ...(await cmp(shots.v7[s], shots.pv[s])) });
  for (let i = 0; i < Math.min(lora.v7.length, lora.pv.length); i++) if (lora.v7[i] && lora.pv[i]) res.push({ el: `Lora text ${i + 1}`, ...(await cmp(lora.v7[i], lora.pv[i])) });
  await b.close();
  const pass = res.length > 0 && res.every((r) => !r.size && r.differ === 0) && requests.pv === 0 && requests.v7 > 0;
  const report = { checked: new Date().toISOString(), version7: path.relative(ROOT, v7), preview: path.relative(ROOT, pv), userAgent: UA,
    fontRequests: { version7: requests.v7, preview: requests.pv }, pairs: res, pass };
  fs.mkdirSync(path.dirname(outJson), { recursive: true });
  fs.writeFileSync(outJson, JSON.stringify(report, null, 1));
  console.log(`${pass ? 'PASS' : 'FAIL'} font fidelity: ${res.filter((r) => !r.size && r.differ === 0).length} of ${res.length} elements match pixel for pixel; `
    + `font requests: version 7 ${requests.v7}, preview ${requests.pv}`);
  for (const r of res) if (r.size || r.differ) console.log(`  - ${r.el}: ${r.size || r.differ + ' pixels differ, by up to ' + r.max}`);
  console.log('  results: ' + path.relative(ROOT, outJson));
  process.exit(pass ? 0 : 1);
})();
