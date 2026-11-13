// Board 2 only (fix round, B2-S2): sketch 14.124's plate at a 1440 px window in a strict build, photographed twice in the
// same plate, heading, bar and caption: as built (red and blue), and with the gray half the guide printed before DR-255 set
// in its place in the page's memory (the file is never written), its caption the one that build printed. Newsprint as
// built, then Charcoal by the stage's surface class. The cartographer, November 13, 2026.
//   node 20261113_S-14-124-Sketch-Plate-Photos.cjs STRICT_BUILD.html GRAY_FRAGMENT.html GRAY_PLATE_PAGE.html OUT_DIR
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path'), url = require('url');
(async () => {
  const [guide, frag, platePage, out] = process.argv.slice(2);
  const gray = fs.readFileSync(frag, 'utf8').match(/<svg\b[\s\S]*?<\/svg>/)[0];                  // the gray misleading half
  const pageHtml = fs.readFileSync(platePage, 'utf8');
  const cap = pageHtml.match(/<figcaption class="plate-cap">([\s\S]*?)<\/figcaption>/)[1];          // the caption as built in gray
  if (!/Drawn here in gray/.test(cap) || !/oac-f-mag-4/.test(gray)) throw new Error('not the gray before');
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  await p.goto(url.pathToFileURL(guide).href, { waitUntil: 'load', timeout: 180000 });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => document.getElementById('fig-s-14-124-sketch').scrollIntoView());
  const fig = p.locator('#fig-s-14-124-sketch');
  const ground = (g) => p.evaluate((g) => { const st = document.querySelector('#fig-s-14-124-sketch .plate-stage'); st.className = st.className.replace(/oa-surface-\w+/, 'oa-surface-' + g); st.setAttribute('data-surface', g); }, g);
  const out_files = [];
  const shot = async (name) => { await fig.screenshot({ path: path.join(out, name) }); const b = await fig.boundingBox(); out_files.push([name, +b.width.toFixed(2), +b.height.toFixed(2)]); };
  for (const g of ['newsprint', 'charcoal']) { await ground(g); await shot(`20261113_S-14-124-Sketch-After-Plate-1440-${g === 'newsprint' ? 'Newsprint' : 'Charcoal'}.png`); }
  // the gray half in place of the red and blue: the drawing's children and its first <desc>, and the caption as built in gray
  await p.evaluate(({ gray, cap }) => {
    const f = document.getElementById('fig-s-14-124-sketch'), svg = f.querySelector('.sk-avoid svg');
    const t = document.createElement('div'); t.innerHTML = gray; const g = t.firstElementChild;
    const desc = svg.querySelector('desc'), gdesc = g.querySelector('desc');
    Array.from(svg.childNodes).forEach((n) => { if (n.nodeName !== 'title' && n.nodeName !== 'desc') n.remove(); });
    Array.from(g.childNodes).forEach((n) => { if (n.nodeName !== 'title' && n.nodeName !== 'desc') svg.appendChild(n.cloneNode(true)); });
    if (desc && gdesc) desc.textContent = gdesc.textContent;
    f.querySelector('figcaption.plate-cap').innerHTML = cap;
  }, { gray, cap });
  for (const g of ['newsprint', 'charcoal']) { await ground(g); await shot(`20261113_S-14-124-Sketch-Gray-Before-Plate-1440-${g === 'newsprint' ? 'Newsprint' : 'Charcoal'}.png`); }
  const check = await p.evaluate(() => { const f = document.getElementById('fig-s-14-124-sketch'); return { fills: Array.from(f.querySelectorAll('.sk-avoid svg [fill]')).length, mag4: f.querySelectorAll('.sk-avoid svg .oac-f-mag-4').length, cap: f.querySelector('figcaption').textContent.slice(0, 40) }; });
  await browser.close();
  console.log(JSON.stringify({ out_files, gray_half_check: check }));
})();
