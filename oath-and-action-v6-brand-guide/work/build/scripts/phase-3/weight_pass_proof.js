// Proves two builds of the guide page draw the same pixels (weight pass, Phase 3 round 0, November 11, 2026).
// Opens both pages in Chromium side by side and compares screenshots of the whole page, one viewport at a time, at each
// width and theme asked for. Every image loads first (lazy images are scrolled into view), motion is reduced, and both pages
// stand at the same scroll position for each pair of screenshots. Exit 1 when any pair differs; the first differing pair
// is saved beside --out.
//
//   node work/build/scripts/phase-3/weight_pass_proof.js BEFORE.html AFTER.html [--widths 390,1280] [--themes light,dark]
//        [--out DIR] [--only SECTION_ID,...]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const [A, B] = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
const widths = opt('--widths', '390,1280').split(',').map(Number);
const themes = opt('--themes', 'light,dark').split(',');
const out = opt('--out', null);
const only = opt('--only', null);
const VH = 1200;

async function prepare(page, file, theme) {
  await page.goto('file://' + path.resolve(file), { waitUntil: 'load', timeout: 180000 });
  await page.evaluate((t) => { document.documentElement.setAttribute('data-oa-theme', t); }, theme);
  await page.evaluate(async () => {
    document.querySelectorAll('img[loading="lazy"]').forEach((i) => { i.loading = 'eager'; });
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => i.complete ? null : new Promise((r) => { i.onload = i.onerror = r; })));
  });
  await page.waitForTimeout(500);
  return page.evaluate(() => document.documentElement.scrollHeight);
}

async function spans(page) {
  // the page's top and bottom, or the named sections' spans
  if (!only) return [[0, await page.evaluate(() => document.documentElement.scrollHeight)]];
  return page.evaluate((ids) => ids.split(',').map((id) => {
    const el = document.getElementById(id);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return [Math.floor(r.top + scrollY), Math.ceil(r.bottom + scrollY)];
  }).filter(Boolean), only);
}

(async () => {
  const browser = await chromium.launch();
  let diff = 0, shots = 0;
  const log = [];
  for (const theme of themes) for (const w of widths) {
    const ctx = await browser.newContext({ viewport: { width: w, height: VH }, deviceScaleFactor: 1, reducedMotion: 'reduce', colorScheme: theme });
    const pa = await ctx.newPage(), pb = await ctx.newPage();
    const ha = await prepare(pa, A, theme), hb = await prepare(pb, B, theme);
    if (ha !== hb) { console.log(`DIFFERS ${theme} ${w}px: page heights ${ha} and ${hb}`); diff++; await ctx.close(); continue; }
    let d = 0, n = 0;
    for (const [top, bottom] of await spans(pa)) {
      for (let y = top; y < bottom; y += VH) {
        await pa.evaluate((y) => window.scrollTo(0, y), y); await pb.evaluate((y) => window.scrollTo(0, y), y);
        await pa.waitForTimeout(30);
        const [sa, sb] = [await pa.screenshot(), await pb.screenshot()];
        n++;
        if (!sa.equals(sb)) {
          d++;
          if (out && d === 1) { fs.mkdirSync(out, { recursive: true }); fs.writeFileSync(path.join(out, `a-${theme}-${w}-${y}.png`), sa); fs.writeFileSync(path.join(out, `b-${theme}-${w}-${y}.png`), sb); }
          if (d <= 5) console.log(`DIFFERS ${theme} ${w}px at y ${y}`);
        }
      }
    }
    shots += n; diff += d;
    log.push(`${theme} ${w}px: ${n} screenshots over ${ha} px, ${d} differ`);
    console.log(log[log.length - 1]);
    await ctx.close();
  }
  await browser.close();
  console.log(`${diff ? 'FAIL' : 'PASS'} ${shots} screenshot pairs compared, ${diff} differ`);
  process.exit(diff ? 1 : 0);
})();
