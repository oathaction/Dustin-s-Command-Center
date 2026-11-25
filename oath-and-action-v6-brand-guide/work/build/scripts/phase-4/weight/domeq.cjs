// 3d's document identity (DR-331): two pages loaded in Chromium with scripts off, each document serialized; the same characters
// and one SHA-256 mean the parser read the same document from both.
//
//   node domeq.cjs A.html B.html [OUT.json]
const { chromium } = require('playwright');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

(async () => {
  const [a, b, out] = process.argv.slice(2);
  const stamp = () => new Date().toISOString().slice(11, 19) + ' UTC';
  const rec = { started: stamp(), pages: {} };
  const browser = await chromium.launch();
  try {
    for (const f of [a, b]) {
      const ctx = await browser.newContext({ javaScriptEnabled: false });
      const page = await ctx.newPage();
      await page.goto('file://' + path.resolve(f), { waitUntil: 'load', timeout: 300000 });
      const html = await page.content();
      rec.pages[f] = { characters: html.length, sha256: crypto.createHash('sha256').update(html).digest('hex') };
      await ctx.close();
    }
  } finally {
    await browser.close();
  }
  const [x, y] = Object.values(rec.pages);
  rec.same = x.sha256 === y.sha256 && x.characters === y.characters;
  rec.ended = stamp();
  console.log(JSON.stringify(rec, null, 1));
  if (out) fs.writeFileSync(out, JSON.stringify(rec, null, 1));
  process.exit(rec.same ? 0 : 1);
})().catch((e) => { console.error(e); process.exit(2); });
