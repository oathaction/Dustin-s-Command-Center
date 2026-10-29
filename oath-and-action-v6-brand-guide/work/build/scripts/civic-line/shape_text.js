// Shape lines of text in Chromium and return each character's pen position.
// Usage: node shape_text.js <in.json> <out.json>
// in.json: { "fonts": { "<family>": "/abs/path.ttf", ... },
//            "lines": [ { "id": "...", "size": 100, "runs": [ { "family": "...", "text": "..." } ] } ] }
// out.json: { "<id>": { "chars": [ { "ch": "R", "family": "...", "x": 0.0 } ], "advance": 123.4 } }
// Kerning is on and contextual alternates and ligatures are off, so each
// character maps to its cmap glyph and the Python side can draw it with fontTools.
const fs = require('fs');
const path = require('path');
const os = require('os');

function loadPlaywright() {
  try { return require('playwright'); } catch (e) { /* fall through */ }
  const { execSync } = require('child_process');
  return require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
}

(async () => {
  const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const { chromium } = loadPlaywright();
  let browser;
  try { browser = await chromium.launch(); } catch (e) { browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); }
  const page = await browser.newPage();
  const faces = Object.entries(input.fonts).map(([fam, p]) =>
    `@font-face{font-family:"${fam}";src:url("file://${p}") format("truetype");font-display:block}`).join('\n');
  const esc = (t) => t.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const body = input.lines.map((l, i) => `<div class="l" id="l${i}" style="font-size:${l.size}px">` +
    l.runs.map((r) => `<span style="font-family:'${r.family}'">${esc(r.text)}</span>`).join('') + '</div>').join('\n');
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>${faces}
    body{margin:0} .l{white-space:pre;position:absolute;left:0;top:0;line-height:1;font-kerning:normal;
    font-feature-settings:"calt" 0,"liga" 0,"kern" 1;font-variant-ligatures:none;text-rendering:geometricPrecision}</style>
    </head><body>${body}</body></html>`;
  const tmp = path.join(os.tmpdir(), `civic-line-shape-${process.pid}.html`);
  fs.writeFileSync(tmp, html);
  await page.goto('file://' + tmp);
  await page.evaluate(async (fams) => {
    for (const f of fams) await document.fonts.load(`100px "${f}"`);
    await document.fonts.ready;
  }, Object.keys(input.fonts));
  const out = await page.evaluate((lines) => {
    const res = {};
    lines.forEach((l, i) => {
      const div = document.getElementById('l' + i);
      const x0 = div.getBoundingClientRect().left;
      const chars = [];
      div.querySelectorAll('span').forEach((span, k) => {
        const node = span.firstChild;
        const fam = l.runs[k].family;
        for (let j = 0; j < node.length; j++) {
          const r = document.createRange();
          r.setStart(node, j); r.setEnd(node, j + 1);
          chars.push({ ch: node.data[j], family: fam, x: r.getBoundingClientRect().left - x0 });
        }
      });
      res[l.id] = { chars, advance: div.getBoundingClientRect().width };
    });
    return res;
  }, input.lines);
  const loaded = await page.evaluate(() => [...document.fonts].map((f) => `${f.family}:${f.status}`));
  fs.writeFileSync(process.argv[3], JSON.stringify({ lines: out, fonts: loaded }));
  fs.unlinkSync(tmp);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
