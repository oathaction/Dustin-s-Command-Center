// Rendered checks for one atlas concept page (October 30, 2026; brief section 8, D2-49 to D2-51).
// Usage: node work/build/scripts/phase-2/atlas_concepts_check.js <concept.html> [--no-captures] [--board]
//
// The page lists its views in <meta name="atlas-views" content="overview area-c loop-r10">, and each view's root
// element carries data-view-root="<view>". For every view at 1440 and 390 px the script checks:
//   - the view root is visible after loading <file>#<view>;
//   - no sideways scroll (content inside a focusable role="region" may run wide by design);
//   - no text under 13 px (SVG text at its rendered scale) and text contrast from rendered colors;
//   - inside every <svg data-view>: labels inside the drawing and no two labels overlapping;
//   - Rule 05.3 as read in DR-18: every Pillar Red mark sits under data-red, at most one working-red job per view,
//     and no red over Prussian;
//   - axe-core 4.10.2 with WCAG 2.2 AA tags; outside requests other than Google Fonts; page errors;
//   - focus: every element reached in the first 40 Tab stops shows an outline or a box shadow.
// On the overview it also clicks the first link into a close-up and goes back.
// Writes <concept dir>/<page stem>-Check-Results.json and captures to <concept dir>/captures/.
// Exit code 1 when any check fails.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');
const RED = [230, 57, 70];
const PRUSSIAN = [31, 45, 90];
const ALLOWED_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com'];

const file = path.resolve(process.argv[2] || '');
const captures = !process.argv.includes('--no-captures');
const BOARD = process.argv.includes('--board');   // a review board: one view, no close-up navigation to test
if (!fs.existsSync(file)) { console.error('usage: node atlas_concepts_check.js <concept.html>'); process.exit(2); }
const dir = path.dirname(file);
const stem = path.basename(file, '.html');
const capDir = path.join(dir, 'captures');
if (captures) fs.mkdirSync(capDir, { recursive: true });

async function audit(page, view) {
  return page.evaluate(({ view, RED, PRUSSIAN }) => {
    const parse = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
    const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
    const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const near = (c, t, tol = 3) => c && c.a > 0.3 && Math.abs(c.r - t[0]) <= tol && Math.abs(c.g - t[1]) <= tol && Math.abs(c.b - t[2]) <= tol;
    const visible = (el) => {
      const r = el.getBoundingClientRect(); if (r.width === 0 && r.height === 0) return false;
      for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false; }
      return !(el.closest('details:not([open])') && !el.closest('summary'));
    };
    function svgUnder(el) {
      if (!(el instanceof SVGElement)) return null;
      const bb = el.getBoundingClientRect(); const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
      for (let node = el; node && !(node instanceof SVGSVGElement); node = node.parentElement) {
        for (let sib = node.previousElementSibling; sib; sib = sib.previousElementSibling) {
          const shapes = [sib, ...sib.querySelectorAll('circle,rect,polygon,path,ellipse')].filter(s => ['circle', 'rect', 'polygon', 'path', 'ellipse'].includes(s.tagName)).reverse();
          for (const sh of shapes) {
            const f = parse(getComputedStyle(sh).fill); if (!f || f.a < 0.5 || getComputedStyle(sh).fill === 'none') continue;
            const b = sh.getBoundingClientRect(); if (b.width < 8 || b.height < 8) continue;
            if (cx >= b.x && cx <= b.right && cy >= b.y && cy <= b.bottom) return f;
          }
        }
      }
      return null;
    }
    function bgOf(el) {
      const u = svgUnder(el); if (u) return u;
      for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
        if (!(e instanceof SVGElement)) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return c; }
      }
      return { r: 255, g: 255, b: 255, a: 1 };
    }
    const root = document.querySelector(`[data-view-root="${view}"]`);
    const out = { view, rootVisible: !!(root && visible(root)), texts: 0, minSize: 99, under13: [], lowContrast: [] };
    const all = [...document.querySelectorAll('body *')].filter(el => !['SCRIPT', 'STYLE', 'TITLE', 'DESC', 'DEFS'].includes(el.tagName.toUpperCase()) && !el.closest('title,desc,defs'));
    for (const el of all) {
      const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
      if (!own || !visible(el) || el.closest('[aria-hidden="true"]') && !(el instanceof SVGElement)) continue;
      const cs = getComputedStyle(el); let size = parseFloat(cs.fontSize);
      const isSvg = el instanceof SVGElement;
      if (isSvg) { const s = el.closest('svg'); const vb = s && s.viewBox && s.viewBox.baseVal; if (vb && vb.width) size = +(size * s.getBoundingClientRect().width / vb.width).toFixed(2); }
      const fg = parse(isSvg ? cs.fill : cs.color); if (!fg) continue;
      out.texts++; out.minSize = Math.min(out.minSize, size);
      if (size < 12.95) out.under13.push({ text: own.slice(0, 40), size });
      const cr = ratio(fg, bgOf(el)); const large = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight, 10) >= 700);
      if (cr < (large ? 3 : 4.5) - 0.005) out.lowContrast.push({ text: own.slice(0, 50), size, ratio: +cr.toFixed(2) });
    }
    const vw = document.documentElement.clientWidth;
    out.scrollWidth = document.documentElement.scrollWidth; out.clientWidth = vw; out.overflowing = [];
    for (const el of all) {
      if (!visible(el)) continue;
      const reg = el.closest('[role="region"][tabindex]'); if (reg && reg !== el) continue;
      const r = el.getBoundingClientRect(); if (r.right > vw + 0.5) out.overflowing.push({ tag: el.tagName, cls: String(el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className).slice(0, 40), right: Math.round(r.right) });
    }
    out.overflowing = out.overflowing.slice(0, 15);
    // labels inside drawings
    const inter = (a, b, pad) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > pad && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > pad;
    const tx = { drawings: 0, labels: 0, outside: [], overlaps: [] };
    for (const svg of document.querySelectorAll('svg[data-view]')) {
      if (!visible(svg)) continue; tx.drawings++;
      const sr = svg.getBoundingClientRect(); const name = svg.getAttribute('data-view');
      const ts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && visible(t)); const rs = ts.map(t => t.getBoundingClientRect());
      tx.labels += ts.length;
      ts.forEach((t, i) => { const r = rs[i]; if (r.left < sr.left - 0.5 || r.right > sr.right + 0.5 || r.top < sr.top - 0.5 || r.bottom > sr.bottom + 0.5) tx.outside.push({ svg: name, text: t.textContent.slice(0, 40) }); });
      for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) {
        if (ts[i].contains(ts[j]) || ts[j].contains(ts[i])) continue;
        if (inter(rs[i], rs[j], 1.5)) tx.overlaps.push({ svg: name, a: ts[i].textContent.slice(0, 30), b: ts[j].textContent.slice(0, 30) });
      }
    }
    tx.overlaps = tx.overlaps.slice(0, 30); out.textCheck = tx;
    // Rule 05.3 as read in DR-18
    const red = { marks: 0, unmarked: [], jobs: [], onPrussian: [] };
    const jobs = new Set();
    for (const el of all) {
      if (!visible(el)) continue;
      const cs = getComputedStyle(el); const isSvg = el instanceof SVGElement;
      const hasOwnText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      const cands = [];
      if (isSvg) { if (cs.fill !== 'none') cands.push(parse(cs.fill)); if (cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0) cands.push(parse(cs.stroke)); }
      else {
        if (hasOwnText) cands.push(parse(cs.color));
        cands.push(parse(cs.backgroundColor));
        if (parseFloat(cs.borderTopWidth) > 0) cands.push(parse(cs.borderTopColor));
        if (parseFloat(cs.borderLeftWidth) > 0) cands.push(parse(cs.borderLeftColor));
        if (parseFloat(cs.borderBottomWidth) > 0) cands.push(parse(cs.borderBottomColor));
      }
      if (!cands.some(c => near(c, RED))) continue;
      if (isSvg && ['svg', 'g'].includes(el.tagName)) continue;   // inherited paint on containers
      red.marks++;
      const tag = el.closest('[data-red]');
      if (!tag) { red.unmarked.push({ tag: el.tagName, id: el.id || null, cls: String(el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className).slice(0, 30), text: (el.textContent || '').trim().slice(0, 30) }); continue; }
      if (tag.getAttribute('data-red') === 'working') jobs.add(tag.getAttribute('data-red-job') || '(no job named)');
      if (near(bgOf(el), PRUSSIAN, 4)) red.onPrussian.push({ tag: el.tagName, text: (el.textContent || '').trim().slice(0, 30) });
    }
    red.unmarked = red.unmarked.slice(0, 20); red.jobs = [...jobs]; out.red = red;
    out.fonts = [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '')))];
    out.height = document.documentElement.scrollHeight;
    return out;
  }, { view, RED, PRUSSIAN });
}

async function focusAudit(page) {
  const results = [];
  await page.evaluate(() => { document.activeElement && document.activeElement.blur && document.activeElement.blur(); window.scrollTo(0, 0); });
  for (let i = 0; i < 40; i++) {
    await page.keyboard.press('Tab');
    const r = await page.evaluate(() => {
      const el = document.activeElement; if (!el || el === document.body) return null;
      const cs = getComputedStyle(el);
      const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow && cs.boxShadow !== 'none');
      const label = (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
      return { tag: el.tagName, label, ring };
    });
    if (!r) break;
    results.push(r);
  }
  return results;
}

(async () => {
  const browser = await chromium.launch();
  const html = fs.readFileSync(file, 'utf8');
  const meta = html.match(/<meta\s+name="atlas-views"\s+content="([^"]+)"/);
  const views = meta ? meta[1].trim().split(/\s+/) : ['overview'];
  const report = { file: path.relative(ROOT, file), checked: new Date().toISOString(), views, runs: [], navigation: null, failures: [] };
  const axeSrc = fs.existsSync(AXE) ? AXE : null;
  for (const width of [1440, 390]) {
    const ctx = await browser.newContext({ viewport: { width, height: width === 1440 ? 900 : 844 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const outside = new Set(); const errors = [];
    page.on('request', (req) => { const u = req.url(); if (u.startsWith('file:') || u.startsWith('data:') || u.startsWith('blob:') || u.startsWith('about:')) return; const h = new URL(u).hostname; if (!ALLOWED_HOSTS.includes(h)) outside.add(h); });
    page.on('pageerror', (e) => errors.push(String(e.message || e).slice(0, 200)));
    for (const view of views) {
      await page.goto('file://' + file + '#' + view, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(700);
      const a = await audit(page, view);
      let axe = null;
      if (axeSrc) {
        await page.addScriptTag({ path: axeSrc });
        axe = await page.evaluate(async () => { const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } }); return r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes[0] && v.nodes[0].target.join(' ') })); });
      }
      const focus = width === 1440 ? await focusAudit(page) : null;
      const run = { width, ...a, axe, focusStops: focus ? focus.length : null, focusWithoutRing: focus ? focus.filter(f => !f.ring).slice(0, 10) : null };
      report.runs.push(run);
      const tag = `${width} ${view}`;
      if (!a.rootVisible) report.failures.push(`${tag}: view root [data-view-root="${view}"] not visible`);
      if (a.scrollWidth > a.clientWidth + 1) report.failures.push(`${tag}: sideways scroll (${a.scrollWidth} > ${a.clientWidth})`);
      if (a.under13.length) report.failures.push(`${tag}: ${a.under13.length} text items under 13 px (min ${a.minSize})`);
      if (a.lowContrast.length) report.failures.push(`${tag}: ${a.lowContrast.length} text items under contrast`);
      if (a.textCheck.outside.length) report.failures.push(`${tag}: ${a.textCheck.outside.length} labels outside their drawing`);
      if (a.textCheck.overlaps.length) report.failures.push(`${tag}: ${a.textCheck.overlaps.length} overlapping labels`);
      if (a.red.unmarked.length) report.failures.push(`${tag}: ${a.red.unmarked.length} red marks without data-red`);
      if (a.red.jobs.length > 1) report.failures.push(`${tag}: ${a.red.jobs.length} working-red jobs (${a.red.jobs.join(', ')})`);
      if (a.red.onPrussian.length) report.failures.push(`${tag}: red over Prussian (${a.red.onPrussian.length})`);
      if (axe && axe.length) report.failures.push(`${tag}: axe ${axe.map(v => v.id + 'x' + v.nodes).join(', ')}`);
      if (!axe) report.failures.push(`${tag}: axe-core not found at ${path.relative(ROOT, AXE)}`);
      if (focus && focus.some(f => !f.ring)) report.failures.push(`${tag}: ${focus.filter(f => !f.ring).length} focus stops without a visible ring`);
      if (captures) {
        const base = path.join(capDir, `${stem}-${view}-${width}`);
        await page.evaluate(() => window.scrollTo(0, 0));
        if (width === 1440) {
          await page.screenshot({ path: base + '.jpg', fullPage: true, type: 'jpeg', quality: 84 });
          await page.addStyleTag({ content: 'html{filter:grayscale(1)!important}' });
          await page.screenshot({ path: base + '-grayscale.jpg', fullPage: true, type: 'jpeg', quality: 70 });
        } else {
          await page.screenshot({ path: base + '.jpg', fullPage: true, type: 'jpeg', quality: 80 });
        }
      }
    }
    if (width === 1440 && !BOARD) {
      // navigation: the first link into a close-up, then back
      await page.goto('file://' + file + '#overview', { waitUntil: 'networkidle' });
      await page.waitForTimeout(400);
      const target = await page.evaluate((views) => {
        const root = document.querySelector('[data-view-root="overview"]') || document;
        const close = views.filter(v => v !== 'overview');
        for (const v of close) { const el = root.querySelector(`a[href="#${v}"], [data-goto="${v}"]`); if (el) { el.setAttribute('data-check-click', '1'); return v; } }
        return null;
      }, views);
      const nav = { target, ok: false };
      if (target) {
        await page.click('[data-check-click="1"]');
        await page.waitForTimeout(700);
        nav.afterClick = await page.evaluate((v) => ({ hash: location.hash, visible: !!document.querySelector(`[data-view-root="${v}"]`) && getComputedStyle(document.querySelector(`[data-view-root="${v}"]`)).display !== 'none' }), target);
        await page.goBack(); await page.waitForTimeout(700);
        nav.afterBack = await page.evaluate(() => ({ hash: location.hash, visible: !!document.querySelector('[data-view-root="overview"]') && getComputedStyle(document.querySelector('[data-view-root="overview"]')).display !== 'none' }));
        nav.ok = nav.afterClick.hash === '#' + target && nav.afterClick.visible && nav.afterBack.visible;
      }
      report.navigation = nav;
      if (!nav.ok) report.failures.push(`navigation: overview to close-up and back failed (${JSON.stringify(nav)})`);
    }
    if (outside.size) report.failures.push(`${width}: outside requests to ${[...outside].join(', ')}`);
    if (errors.length) report.failures.push(`${width}: page errors: ${errors.slice(0, 3).join(' | ')}`);
    await ctx.close();
  }
  await browser.close();
  report.pass = report.failures.length === 0;
  const outPath = path.join(dir, `${stem}-Check-Results.json`);
  fs.writeFileSync(outPath, JSON.stringify(report, null, 1));
  console.log(`${report.pass ? 'PASS' : 'FAIL'} ${path.relative(ROOT, file)}: ${views.length} views x 2 widths, ${report.failures.length} failures`);
  for (const f of report.failures) console.log('  - ' + f);
  console.log('  results: ' + path.relative(ROOT, outPath));
  process.exit(report.pass ? 0 : 1);
})();
