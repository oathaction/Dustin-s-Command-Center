// C1's pixel proof (DR-331): every plate C1's 3a or 3c touches, captured in two pages built from one tree (C1 off and on), at each
// width, in tiles of the viewport, one browser and one tab at a time (chat 12b's M10: a plate taller than the viewport, captured
// whole, made Chromium render beyond it and ran 25 to 35 s; a tile runs under a second).
//
//   node proof.cjs OFF.html ON.html IDS.json OUTDIR [--widths 1440,390] [--shares 4]
//
// Writes OUTDIR/<width>/<off|on>/<specimen>--<tile>.png and OUTDIR/captures.json (each plate's box and tiles, any plate not
// found). Newsprint, reduced motion, device scale 1, the masthead and rail hidden; each share of the plates in a fresh tab.
// Run it from work/build so Playwright resolves. compare.py reads the folder.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const [off, on, idsFile, outDir] = args;
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const widths = opt('--widths', '1440,390').split(',').map(Number);
const shares = Number(opt('--shares', '4'));
const VH = 900;
const ids = JSON.parse(fs.readFileSync(idsFile, 'utf8'));
const stamp = () => new Date().toISOString().slice(11, 19) + ' UTC';

(async () => {
  const log = { started: stamp(), widths, plates: ids.length, pages: { off, on }, runs: [] };
  const browser = await chromium.launch();
  try {
    for (const w of widths) {
      for (const [label, file] of [['off', off], ['on', on]]) {
        const dir = path.join(outDir, String(w), label);
        fs.mkdirSync(dir, { recursive: true });
        const run = { width: w, page: label, started: stamp(), tiles: 0, missing: [], boxes: {} };
        for (let s = 0; s < shares; s++) {
          const share = ids.filter((_, i) => i % shares === s);
          const ctx = await browser.newContext({ viewport: { width: w, height: VH }, deviceScaleFactor: 1, reducedMotion: 'reduce', colorScheme: 'light' });
          const page = await ctx.newPage();
          await page.goto('file://' + path.resolve(file), { waitUntil: 'load', timeout: 300000 });
          await page.evaluate(() => document.fonts.ready);
          await page.addStyleTag({ content: '.masthead, .rail, .rail-more { visibility: hidden !important } html { scroll-behavior: auto !important }' });
          await page.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => null))));
          await page.waitForTimeout(1500);
          for (const sid of share) {
            const box = await page.evaluate((sid) => {
              const st = document.querySelector(`[data-specimen="${CSS.escape(sid)}"]`);
              if (!st) return null;
              const f = st.closest('figure.plate') || st;
              const r = f.getBoundingClientRect();
              return { top: r.top + window.scrollY, left: r.left + window.scrollX, w: r.width, h: r.height, fig: f.id || '' };
            }, sid);
            if (!box || box.h < 1 || box.w < 1) { run.missing.push(sid); continue; }
            run.boxes[sid] = box;
            const x0 = Math.max(0, box.left), x1 = Math.min(w, box.left + box.w);
            const n = Math.ceil(box.h / VH);
            for (let k = 0; k < n; k++) {
              const want = Math.floor(box.top) + k * VH;
              await page.evaluate((y) => window.scrollTo(0, y), want);
              await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
              const sy = await page.evaluate(() => window.scrollY);
              const top = box.top + k * VH - sy;
              const h = Math.min(VH, box.h - k * VH, VH - top);
              if (h < 1 || x1 - x0 < 1) continue;
              const buf = await page.screenshot({ clip: { x: x0, y: top, width: x1 - x0, height: h } });
              fs.writeFileSync(path.join(dir, `${sid}--${k}.png`), buf);
              run.tiles++;
            }
          }
          await ctx.close();
        }
        run.ended = stamp();
        log.runs.push(run);
        console.log(`${w} ${label}: ${run.tiles} tiles, ${Object.keys(run.boxes).length} plates, ${run.missing.length} not found, ${run.started} to ${run.ended}`);
      }
    }
  } finally {
    await browser.close();
  }
  log.ended = stamp();
  fs.writeFileSync(path.join(outDir, 'captures.json'), JSON.stringify(log, null, 1));
})().catch((e) => { console.error(e); process.exit(1); });
