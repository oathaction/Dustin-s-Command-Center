// Render and audit the supplied V5 Polished guide and its companion files.
// Usage: PWPATH=$(npm root -g)/playwright node render_v5.js <project-root>
// Reads source/ and work/extract/. Writes screenshots to work/boards/screens/ and data to work/handoffs/phase-0/.
const fs = require('fs');
const path = require('path');
const { chromium } = require(process.env.PWPATH);

const ROOT = path.resolve(process.argv[2]);
const SRC = path.join(ROOT, 'source');
const SHOTS = path.join(ROOT, 'work', 'boards', 'screens');
const DATA = path.join(ROOT, 'work', 'handoffs', 'phase-0');
const AXE = fs.readFileSync(path.join(ROOT, 'work', 'build', 'node_modules', 'axe-core', 'axe.min.js'), 'utf8');
const V5 = 'file://' + path.join(SRC, '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
const mk = (p) => { fs.mkdirSync(p, { recursive: true }); return p; };
const jpg = { type: 'jpeg', quality: 72 };

async function sections(browser, url, width, outDir) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  await page.goto(url);
  await page.waitForTimeout(1200);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  const ids = await page.evaluate(() => Array.from(document.querySelectorAll('section[id]')).map((s) => s.id));
  const out = [];
  for (let i = 0; i < ids.length; i++) {
    const el = await page.$(`section[id="${ids[i]}"]`);
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(250);
    const file = path.join(mk(outDir), `${String(i).padStart(2, '0')}-${ids[i]}.jpg`);
    await el.screenshot({ path: file, ...jpg });
    const box = await el.boundingBox();
    out.push({ id: ids[i], file: path.relative(ROOT, file), height: Math.round(box.height) });
  }
  await page.close();
  return out;
}

async function reportPages(browser, width) {
  const page = await browser.newPage({ viewport: { width, height: width > 800 ? 1000 : 844 } });
  await page.goto(V5);
  await page.waitForTimeout(1000);
  const n = await page.$$eval('.report-button', (b) => b.length);
  const outDir = mk(path.join(SHOTS, 'v5-polished', `reports-${width}`));
  const res = [];
  for (let i = 0; i < n; i++) {
    await page.evaluate((k) => document.querySelectorAll('.report-button')[k].click(), i);
    await page.waitForTimeout(500);
    const file = path.join(outDir, `${String(i + 1).padStart(2, '0')}.jpg`);
    await page.screenshot({ path: file, ...jpg });
    const label = await page.evaluate(() => {
      const d = document.getElementById('report-dialog');
      return { open: d.open, focus: document.activeElement && (document.activeElement.getAttribute('aria-label') || document.activeElement.textContent.trim().slice(0, 40)) };
    });
    res.push({ page: i + 1, file: path.relative(ROOT, file), ...label });
    await page.keyboard.press('Escape');
    await page.waitForTimeout(200);
  }
  await page.close();
  return res;
}

async function census(browser) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(V5);
  await page.waitForTimeout(1200);
  const result = await page.evaluate(() => {
    const lum = (c) => {
      const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
      const [r, g, b, a = 1] = m[1].split(',').map(Number);
      const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      return { L: 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b), a, rgb: [r, g, b] };
    };
    const bgOf = (el) => {
      for (let e = el; e; e = e.parentElement) {
        const c = getComputedStyle(e).backgroundColor;
        const l = lum(c);
        if (l && l.a > 0.5) return { c, l };
      }
      return { c: 'rgb(255,255,255)', l: lum('rgb(255,255,255)') };
    };
    const rows = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    while (walker.nextNode()) {
      const t = walker.currentNode; const el = t.parentElement;
      if (!el || seen.has(el) || !t.textContent.trim()) continue;
      if (el.closest('svg, script, style, dialog:not([open])')) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || el.getClientRects().length === 0) continue;
      seen.add(el);
      const fg = lum(cs.color); const bg = bgOf(el);
      const op = parseFloat(cs.opacity);
      const ratio = fg && bg.l ? (Math.max(fg.L, bg.l.L) + 0.05) / (Math.min(fg.L, bg.l.L) + 0.05) : null;
      const sec = el.closest('section[id]');
      rows.push({ section: sec ? sec.id : 'shell', tag: el.tagName.toLowerCase(), cls: el.className && String(el.className).slice(0, 40),
        size: parseFloat(cs.fontSize), weight: cs.fontWeight, tracking: cs.letterSpacing, transform: cs.textTransform,
        family: cs.fontFamily.split(',')[0].replace(/['"]/g, ''), color: cs.color, bg: bg.c, ratio: ratio && +ratio.toFixed(2),
        opacity: op, text: t.textContent.trim().slice(0, 50) });
    }
    return rows;
  });
  await page.close();
  return result;
}

async function tabOrder(browser) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(V5);
  await page.waitForTimeout(800);
  const stops = [];
  for (let i = 0; i < 90; i++) {
    await page.keyboard.press('Tab');
    const s = await page.evaluate(() => {
      const e = document.activeElement; if (!e || e === document.body) return null;
      const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
      const sec = e.closest('section[id]');
      return { tag: e.tagName.toLowerCase(), label: (e.getAttribute('aria-label') || e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 50),
        section: sec ? sec.id : 'shell', outline: `${cs.outlineStyle} ${cs.outlineWidth} ${cs.outlineColor}`, boxShadow: cs.boxShadow !== 'none',
        w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top) };
    });
    if (!s) break;
    stops.push(s);
  }
  await page.close();
  return stops;
}

async function axe(browser, url, width) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  await page.goto(url);
  await page.waitForTimeout(1000);
  await page.addScriptTag({ content: AXE });
  const r = await page.evaluate(async () => {
    const res = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
    return res.violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, count: v.nodes.length,
      examples: v.nodes.slice(0, 4).map((n) => ({ target: n.target.join(' '), summary: (n.failureSummary || '').slice(0, 220) })) }));
  });
  await page.close();
  return r;
}

async function fullPageTiles(browser, file, slug, width, maxTiles) {
  const page = await browser.newPage({ viewport: { width, height: 1000 } });
  await page.goto('file://' + path.join(SRC, file));
  await page.waitForTimeout(2500);
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  const outDir = mk(path.join(SHOTS, slug));
  const tile = 1800; const files = [];
  for (let y = 0, k = 0; y < h && k < maxTiles; y += tile, k++) {
    const f = path.join(outDir, `${String(k).padStart(2, '0')}.jpg`);
    await page.screenshot({ path: f, clip: { x: 0, y, width, height: Math.min(tile, h - y) }, fullPage: true, ...jpg });
    files.push(path.relative(ROOT, f));
  }
  await page.close();
  return { height: h, tiles: files };
}

async function spriteSheet(browser) {
  const dir = path.join(ROOT, 'work', 'extract', 'v5-polished', 'sprite');
  const ids = fs.readdirSync(dir).filter((f) => f.endsWith('.svg')).map((f) => f.replace('.svg', ''));
  const sprite = fs.readFileSync(path.join(SRC, '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html'), 'utf8')
    .match(/<svg[^>]*id="sprite"[\s\S]*?<\/svg>\s*(?=<)/);
  const symbols = sprite ? sprite[0] : '';
  const vb = {};
  for (const id of ids) { const m = fs.readFileSync(path.join(dir, id + '.svg'), 'utf8').match(/viewBox="([^"]+)"/); vb[id] = m ? m[1].split(/\s+/).map(Number) : [0, 0, 24, 24]; }
  const cell = (id, scale, bg, fg) => { const [, , w, h] = vb[id]; return `<svg width="${w * scale}" height="${h * scale}" style="color:${fg};background:${bg}"><use href="#${id}"/></svg>`; };
  const icons = ids.filter((i) => /^ic-.*-(48|24|16)$/.test(i));
  const names = [...new Set(icons.map((i) => i.replace(/-(48|24|16)$/, '')))];
  const other = ids.filter((i) => !icons.includes(i));
  const html = `<!doctype html><meta charset="utf-8"><style>body{margin:24px;font:13px/1.4 system-ui;background:#DCD9D2;color:#121212}
  .g{display:flex;flex-wrap:wrap;gap:16px}.c{border:1px solid #bbb;padding:8px;background:#DCD9D2}.c p{margin:4px 0 0;font-size:11px}
  .row{display:flex;gap:12px;align-items:end}.dark{background:#121212;color:#DCD9D2}</style>${symbols}
  <h2>Icons at 1x (16, 24, 48) and 4x of the 16 and 24 masters, Charcoal on Newsprint and Newsprint on Charcoal</h2><div class="g">${names.map((n) => `<div class="c"><div class="row">${cell(n + '-16', 1, '#DCD9D2', '#121212')}${cell(n + '-24', 1, '#DCD9D2', '#121212')}${cell(n + '-48', 1, '#DCD9D2', '#121212')}${cell(n + '-16', 4, '#DCD9D2', '#121212')}${cell(n + '-24', 4, '#DCD9D2', '#121212')}</div><div class="row dark" style="margin-top:6px">${cell(n + '-16', 1, '#121212', '#DCD9D2')}${cell(n + '-24', 1, '#121212', '#DCD9D2')}${cell(n + '-48', 1, '#121212', '#DCD9D2')}</div><p>${n}</p></div>`).join('')}</div>
  <h2>Other symbols at natural viewBox size (capped at 360 px wide)</h2><div class="g">${other.map((n) => { const [, , w] = vb[n]; const s = Math.min(1, 360 / w); return `<div class="c">${cell(n, s, '#DCD9D2', '#121212')}<p>${n} (${vb[n].slice(2).join(' x ')})</p></div>`; }).join('')}</div>`;
  const f = path.join(ROOT, 'work', 'boards', 'sprite-sheet.html');
  fs.writeFileSync(f, html);
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  await page.goto('file://' + f);
  await page.waitForTimeout(500);
  const out = path.join(mk(path.join(SHOTS, 'v5-polished')), 'sprite-sheet.png');
  await page.screenshot({ path: out, fullPage: true });
  await page.close();
  return { symbols: ids.length, icon_names: names, other, sheet: path.relative(ROOT, out) };
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const report = {};
  report.sections1440 = await sections(browser, V5, 1440, path.join(SHOTS, 'v5-polished', '1440'));
  report.sections390 = await sections(browser, V5, 390, path.join(SHOTS, 'v5-polished', '390'));
  report.reports1440 = await reportPages(browser, 1440);
  report.reports390 = await reportPages(browser, 390);
  report.sprite = await spriteSheet(browser);
  report.tabOrder = await tabOrder(browser);
  report.axe1440 = await axe(browser, V5, 1440);
  report.axe390 = await axe(browser, V5, 390);
  const rows = await census(browser);
  fs.writeFileSync(path.join(DATA, 'text-census.json'), JSON.stringify(rows));
  report.companions = {
    'atlas-visual-system': await fullPageTiles(browser, '20261018_Oath-And-Action-Atlas-Visual-System.html', 'atlas-visual-system', 1440, 40),
    'concepts-v2': await fullPageTiles(browser, '20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html', 'concepts-v2', 1440, 60),
    'v4-2': await fullPageTiles(browser, '20261018_Oath-And-Action-Brand-Guide_V4.2.html', 'v4-2', 1440, 60),
    'atlas-v7': await fullPageTiles(browser, '20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html', 'atlas-v7', 1440, 8),
  };
  fs.writeFileSync(path.join(DATA, 'render-report.json'), JSON.stringify(report, null, 1));
  await browser.close();
  console.log(JSON.stringify({ s1440: report.sections1440.length, s390: report.sections390.length, r1440: report.reports1440.length,
    r390: report.reports390.length, symbols: report.sprite.symbols, tabStops: report.tabOrder.length,
    axe1440: report.axe1440.map((v) => `${v.id}:${v.count}`), axe390: report.axe390.map((v) => `${v.id}:${v.count}`),
    census: rows.length, companions: Object.fromEntries(Object.entries(report.companions).map(([k, v]) => [k, `${v.height}px/${v.tiles.length} tiles`])) }, null, 1));
})();
