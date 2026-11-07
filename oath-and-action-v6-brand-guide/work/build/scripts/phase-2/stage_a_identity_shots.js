// Screenshot elements of a standalone page at a device scale, one PNG per element id, for the identity designer's board
// plates and measurements (fix pass, November 7, 2026).
// Usage: node stage_a_identity_shots.js <page.html> <outdir> <scale> <id> [<id> ...]
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'))); }
(async () => {
  const [page, out, scale, ...ids] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2000, height: 1200 }, deviceScaleFactor: +scale });
  await p.goto('file://' + path.resolve(page), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const fonts = await p.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family + ' ' + f.weight));
  for (const id of ids) {
    await p.locator('#' + id).screenshot({ path: path.join(out, `${id}@${scale}x.png`) });
  }
  console.log(JSON.stringify({ fonts: [...new Set(fonts)] }));
  await b.close();
})();
