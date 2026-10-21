// Layout and type check for the Symbol Family Board (Phase 1, design director).
// Usage: node symbols_board_check.js <board.html> <out.json> <screens_dir>
// Opens the board in Chromium at 1440 and 390 px, checks horizontal overflow, heading
// widows, tabular figures, ASCII minus signs in numeric cells and text under 13 px,
// and saves full-page captures.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [board, outJson, screens] = process.argv.slice(2);
  fs.mkdirSync(screens, { recursive: true });
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const result = { widths: {}, summary: [] };
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.resolve(board), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    const r = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const out = { scrollWidth: document.documentElement.scrollWidth, clientWidth: vw, overflow: [], widows: [], tabular: { cells: 0, ok: 0 }, asciiMinus: [], small: 0, smallSamples: [], fonts: [] };
      document.fonts.forEach(f => { if (f.status === 'loaded') out.fonts.push(f.family + ' ' + f.weight); });
      // elements that stick out of the viewport, outside the scroll regions that are meant to scroll
      for (const el of document.querySelectorAll('main *')) {
        if (el.closest('.scroll')) continue;
        const b = el.getBoundingClientRect();
        if (b.width && (b.right > vw + 0.5 || b.left < -0.5)) out.overflow.push(el.tagName.toLowerCase() + '.' + (el.className && el.className.baseVal === undefined ? el.className : '') + ' ' + Math.round(b.left) + '..' + Math.round(b.right));
      }
      // widows: last line of a heading holds one word
      const sel = 'h1,h2,h3,h4,.so-head,.ah,.kh,.lede';
      for (const el of document.querySelectorAll(sel)) {
        const text = el.textContent.trim();
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        const words = [];
        let n;
        while ((n = walker.nextNode())) {
          const re = /\S+/g; let m;
          while ((m = re.exec(n.nodeValue))) {
            const rg = document.createRange(); rg.setStart(n, m.index); rg.setEnd(n, m.index + m[0].length);
            const rects = rg.getClientRects();
            if (rects.length) words.push({ w: m[0], top: Math.round(rects[0].top) });
          }
        }
        if (words.length < 3) continue;
        const lines = [...new Set(words.map(x => x.top))].sort((a, b) => a - b);
        if (lines.length < 2) continue;
        const last = words.filter(x => x.top === lines[lines.length - 1]);
        if (last.length === 1) out.widows.push(el.tagName.toLowerCase() + ': "' + text.slice(0, 60) + '" ends with "' + last[0].w + '"');
      }
      for (const td of document.querySelectorAll('td.n')) {
        out.tabular.cells++;
        if (getComputedStyle(td).fontVariantNumeric.includes('tabular-nums')) out.tabular.ok++;
        if (/(^|\s)-\d/.test(td.textContent)) out.asciiMinus.push(td.textContent.trim());
      }
      for (const el of document.querySelectorAll('main *')) {
        if (!el.childNodes.length) continue;
        const own = [...el.childNodes].some(c => c.nodeType === 3 && c.nodeValue.trim());
        if (!own) continue;
        if (el.closest('svg')) continue;
        const fs = parseFloat(getComputedStyle(el).fontSize);
        if (fs < 12.95) { out.small++; if (out.smallSamples.length < 6) out.smallSamples.push(el.tagName.toLowerCase() + ' ' + fs.toFixed(1) + 'px "' + el.textContent.trim().slice(0, 30) + '"'); }
      }
      out.height = document.documentElement.scrollHeight;
      return out;
    });
    const shot = path.join(screens, `20261021_Symbol-Family-Board-${w}.png`);
    await page.screenshot({ path: shot, fullPage: true });
    r.capture = shot;
    result.widths[w] = r;
    await page.close();
  }
  await browser.close();
  for (const [w, r] of Object.entries(result.widths)) {
    result.summary.push(`${w} px: page ${r.scrollWidth} px wide in a ${r.clientWidth} px viewport; ${r.overflow.length} elements outside the viewport, not counting the tables that scroll on purpose.`);
    result.summary.push(`${w} px: ${r.widows.length} headings end on a single word${r.widows.length ? ' (' + r.widows.slice(0, 3).join('; ') + ')' : ''}.`);
    result.summary.push(`${w} px: ${r.tabular.ok} of ${r.tabular.cells} numeric cells use tabular figures; ${r.asciiMinus.length} numeric cells use a hyphen for minus.`);
    result.summary.push(`${w} px: ${r.small} text elements set under 13 px${r.small ? ' (' + r.smallSamples.join('; ') + ')' : ''}.`);
  }
  const f = result.widths['1440'].fonts;
  result.summary.push(f.length ? `Web fonts loaded in the check: ${[...new Set(f)].join(', ')}.` : 'Web fonts did not load in the check environment; the captures use fallback faces.');
  fs.writeFileSync(outJson, JSON.stringify(result, null, 1));
  console.log(JSON.stringify(result.summary, null, 1));
  for (const [w, r] of Object.entries(result.widths)) console.log(w, 'overflow sample', r.overflow.slice(0, 8));
})();
