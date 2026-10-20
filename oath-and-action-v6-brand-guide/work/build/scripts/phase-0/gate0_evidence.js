// Capture clean evidence crops from V5 Polished for the Gate 0 board.
// Usage: PWPATH=$(npm root -g)/playwright node gate0_evidence.js <project-root>
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PWPATH);
const ROOT = path.resolve(process.argv[2]);
const OUT = path.join(ROOT, 'work', 'boards', 'gate-0-images');
const V5 = 'file://' + path.join(ROOT, 'source', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
const SPRITE = path.join(ROOT, 'work', 'extract', 'v5-polished', 'sprite');

// Each target: text to find, how many ancestor levels to climb to reach a useful block, output name.
const targets = [
  { text: 'Closed primaries are the largest group.', up: 'figure,.chart,.spec,.card,div', minH: 250, out: 'ev-chart-title' },
  { text: 'The hearing', up: 'div', minH: 300, out: 'ev-voice-hinge' },
  { text: 'L5 · Horizontal with tagline', up: 'figure,div', minH: 120, out: 'ev-l5-lockup', pad: 0 },
  { text: 'L6 · Editorial signature', up: 'figure,div', minH: 120, out: 'ev-l6-lockup', pad: 0 },
  { text: 'Explain tile', up: 'div', minH: 300, out: 'ev-social-tiles' },
  { text: 'L8 · Monogram', up: 'div', minH: 150, out: 'ev-avatars' },
  { text: 'Where each election bill sits this week.', up: 'div', minH: 200, out: 'ev-tracker' },
];

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(V5);
  await page.waitForTimeout(1200);
  await page.addStyleTag({ content: 'nav{position:static!important}.skip{display:none!important}' });
  const report = [];
  for (const t of targets) {
    const box = await page.evaluate(({ text, up, minH }) => {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) {
        const n = walker.currentNode;
        if (!n.textContent.replace(/\s+/g, ' ').includes(text)) continue;
        let el = n.parentElement;
        while (el && el !== document.body) {
          const r = el.getBoundingClientRect();
          if (el.matches(up) && r.height >= minH && r.width >= 300) {
            el.scrollIntoView({ block: 'start' });
            const q = el.getBoundingClientRect();
            return { x: q.left + scrollX, y: q.top + scrollY, w: q.width, h: q.height };
          }
          el = el.parentElement;
        }
      }
      return null;
    }, t);
    if (!box) { report.push({ out: t.out, found: false }); continue; }
    const file = path.join(OUT, t.out + '.png');
    await page.screenshot({ path: file, fullPage: true, clip: { x: Math.max(0, box.x - 8), y: Math.max(0, box.y - 8), width: Math.min(1440, box.w + 16), height: Math.min(1400, box.h + 16) } });
    report.push({ out: t.out, found: true, w: Math.round(box.w), h: Math.round(box.h) });
  }

  // Magnified renders of small-size defects, drawn from the real sprite masters at 1x and enlarged without smoothing.
  const sym = (id) => fs.readFileSync(path.join(SPRITE, id + '.svg'), 'utf8');
  const cells = [
    { id: 'amp', h: 16, bg: '#DCD9D2', fg: '#E63946', out: 'mag-amp-16-newsprint' },
    { id: 'amp-16', h: 16, bg: '#DCD9D2', fg: '#E63946', out: 'mag-amp16-16-newsprint' },
    { id: 'wordmark', h: 16, bg: '#DCD9D2', fg: '#121212', out: 'mag-wordmark-16' },
    { id: 'lockmark', h: 16, bg: '#DCD9D2', fg: '#121212', out: 'mag-lockmark-16' },
    { id: 'ic-campaign-money-16', h: 16, bg: '#DCD9D2', fg: '#121212', out: 'mag-campaign-money-16' },
    { id: 'ic-contact-an-official-16', h: 16, bg: '#DCD9D2', fg: '#121212', out: 'mag-contact-official-16' },
    { id: 'tl-1', h: 40, bg: '#DCD9D2', fg: '#121212', out: 'mag-tagline-40' },
  ];
  const p2 = await browser.newPage({ viewport: { width: 1200, height: 400 }, deviceScaleFactor: 1 });
  for (const c of cells) {
    const svg = sym(c.id).replace('<svg ', `<svg height="${c.h}" `).replace(/style="color:[^"]*"/, `style="color:${c.fg};display:block"`);
    await p2.setContent(`<html><body style="margin:0;background:${c.bg}"><div id="c" style="display:inline-block;padding:4px;background:${c.bg}">${svg}</div></body></html>`);
    const el = await p2.$('#c');
    await el.screenshot({ path: path.join(OUT, c.out + '-1x.png') });
    report.push({ out: c.out, magnified: true });
  }
  await browser.close();
  console.log(JSON.stringify(report));
}
main();
