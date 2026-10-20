// Phase 0 UX audit: can a keyboard user pan a Full size report page at 390 px?
// Usage: node ux_reader_pan.js <project-root>
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = path.resolve(process.argv[2] || '.');
const V5 = 'file://' + path.join(ROOT, 'source', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 390, height: 844 } });
  await p.goto(V5); await p.waitForTimeout(1000);
  await p.click('#report-first'); await p.waitForTimeout(300);
  await p.selectOption('#report-zoom', 'full'); await p.waitForTimeout(300);
  await p.focus('#report-close');
  await p.keyboard.press('Tab'); // Chromium focuses the scroller
  const st = () => p.evaluate(() => ({ focus: document.activeElement.id, counter: document.getElementById('report-counter').textContent, scrollLeft: document.getElementById('report-body').scrollLeft, scrollTop: document.getElementById('report-body').scrollTop }));
  console.log('focused body', JSON.stringify(await st()));
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(200);
  console.log('after ArrowRight', JSON.stringify(await st()));
  await p.keyboard.press('ArrowDown'); await p.keyboard.press('ArrowDown'); await p.waitForTimeout(200);
  console.log('after ArrowDown x2', JSON.stringify(await st()));
  await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(200);
  console.log('after ArrowLeft', JSON.stringify(await st()));
  // Visible controls at 390 inside the dialog: sizes
  const sizes = await p.evaluate(() => [...document.querySelectorAll('#report-dialog button, #report-dialog select')].map((e) => { const r = e.getBoundingClientRect(); return e.id + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' font ' + getComputedStyle(e).fontSize; }));
  console.log(sizes.join('\n'));
  await b.close();
})();
