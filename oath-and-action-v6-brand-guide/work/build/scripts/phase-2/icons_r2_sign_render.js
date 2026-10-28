// Concept 3, Public sign: render cells to PNG with Chromium at device scale 1, waiting for web
// fonts first (Material Symbols for the benchmark and look-alike checks).
// Usage: node icons_r2_sign_render.js <jobs.json> <out_dir> [head.html]
// jobs.json: [{ "id": "name", "w": 24, "h": 24, "bg": "#FFFFFF", "html": "<svg ...>" }]
// Each cell sits at whole-pixel page coordinates, so antialiasing matches a page at 1x.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [jobsPath, outDir, headPath] = process.argv.slice(2);
  const jobs = JSON.parse(fs.readFileSync(jobsPath, 'utf8'));
  const head = headPath ? fs.readFileSync(headPath, 'utf8') : '';
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: 2400, height: 1600 } });
  const batch = 80;
  for (let s = 0; s < jobs.length; s += batch) {
    const part = jobs.slice(s, s + batch);
    const cells = part.map((j, k) =>
      `<div class="cell" id="c${k}" style="width:${j.w}px;height:${j.h}px;background:${j.bg};">${j.html}</div>`
    ).join('');
    await page.setContent(`<!doctype html><html><head>${head}<style>
      html,body{margin:0;padding:0;background:#888}
      .cell{display:block;position:relative;margin:0 0 6px 0;overflow:hidden}
      .cell > svg, .cell > img{display:block;position:absolute;left:0;top:0}
      .ms{font-family:'Material Symbols Outlined';font-weight:400;font-style:normal;line-height:1;display:block;position:absolute;left:0;top:0;color:#000;
          font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24}
    </style></head><body>${cells}</body></html>`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    for (let k = 0; k < part.length; k++) {
      await page.locator(`#c${k}`).screenshot({ path: path.join(outDir, `${part[k].id}.png`) });
    }
  }
  await browser.close();
})();
