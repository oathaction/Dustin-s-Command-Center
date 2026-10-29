// Civic Line batch renderer: one Chromium launch renders every job in a list.
// Usage: node render_svgs.js <jobs.json>
// jobs.json: [{ "svg": "<svg ...>", "w": 128, "h": 128, "bg": "#DCD9D2" | null, "out": "/abs/path.png" }]
// bg null gives a transparent PNG. The SVG is placed at the page origin at
// device scale 1, so its width and height attributes set the pixel size.
const fs = require('fs');
const path = require('path');

function loadPlaywright() {
  try { return require('playwright'); } catch (e) { /* fall through */ }
  const { execSync } = require('child_process');
  const root = execSync('npm root -g').toString().trim();
  return require(path.join(root, 'playwright'));
}

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const { chromium } = loadPlaywright();
  let browser;
  try {
    browser = await chromium.launch();
  } catch (e) {
    browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  }
  const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: 64, height: 64 } });
  for (const j of jobs) {
    await page.setViewportSize({ width: Math.max(1, j.w), height: Math.max(1, j.h) });
    const bg = j.bg ? j.bg : 'transparent';
    await page.setContent(`<!doctype html><html><head><style>
      html,body{margin:0;padding:0;background:${bg};overflow:hidden}
      svg{display:block;position:absolute;left:0;top:0}
    </style></head><body>${j.svg}</body></html>`);
    fs.mkdirSync(path.dirname(j.out), { recursive: true });
    await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.w, height: j.h }, omitBackground: !j.bg });
  }
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
