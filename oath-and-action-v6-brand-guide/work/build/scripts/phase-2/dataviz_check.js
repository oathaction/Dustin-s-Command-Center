// Rendered checks for one data visualization concept page (November 6, 2026), adapted from atlas_concepts_check.js.
// Usage: node work/build/scripts/phase-2/dataviz_check.js <concept.html> [--no-captures] [--board] [--mid]
//
// The page lists its views in <meta name="chart-views" content="white newsprint dark social system">, and each view's
// root element carries data-view-root="<view>". The first view links to the others. For every view at 1440, 390 and
// 360 px the script checks:
//   - the view root is visible after loading <file>#<view>;
//   - no sideways scroll (content inside a focusable role="region" may run wide by design);
//   - no text under 13 px (SVG text at its rendered scale) and text contrast from rendered colors;
//   - inside every <svg data-view>: labels and marks (circles and data-mark shapes) inside the drawing, no two labels overlapping;
//   - Rule 05.3 as read in DR-18: every Pillar Red mark sits under data-red, at most one working-red job per view,
//     and no red over Prussian;
//   - axe-core 4.10.2 with WCAG 2.2 AA tags; outside requests other than Google Fonts; page errors;
//   - focus: every element reached in the first 40 Tab stops shows an outline or a box shadow.
//   - scale: inside each chart drawing and in HTML tables, bars (data-mark="bar") have lengths proportional to data-value from a zero
//     baseline (or, in a 100 percent stacked bar, as its share of the row), and points (data-mark="point") sit on one straight scale, per figure, drawing and data-scale group,
//     along data-axis ("x" or "y"); deviations over 1 px (and 1.5 percent for bars) fail;
//   - party: no mark under [data-party] is painted Pillar Red or Prussian (DR-48).
// On the first view it also clicks the first link into another view and goes back.
// Writes <concept dir>/<page stem>-Check-Results.json and captures to <concept dir>/captures/.
// Exit code 1 when any check fails.
//
// Phase 3 (round 0): --kit checks every chart kit figure (figure.oac-fig) on any page, such as a guide build or a kit page,
// as the browser draws it, so the kit's own layout guard, which measures text with its metrics table, is proven against
// real rendering: at 1440 and 390 px, every SVG text at 13 px or more at its rendered scale, inside its drawing and clear of
// every other text; no mark cut by the drawing's edge; no party mark ([data-party]) painted Pillar Red or Prussian; one
// working red per drawing; no em dash and no copy of the retired disclosure in the figure (DR-100). --kit-self-test plants
// each fault in a small page and must catch every one.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const AXE = path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js');
const RED = [230, 57, 70];
const PRUSSIAN = [31, 45, 90];
const ALLOWED_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com'];

const file = path.resolve(process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : '');
const captures = !process.argv.includes('--no-captures');
const BOARD = process.argv.includes('--board');   // a review board: one view, no close-up navigation to test
const MID = process.argv.includes('--mid');       // also check 1024 and 768 px (D2-126)
if (!process.argv.includes('--kit-self-test') && !fs.existsSync(file)) { console.error('usage: node dataviz_check.js <concept.html> [--kit] | --kit-self-test'); process.exit(2); }
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
    const tx = { drawings: 0, labels: 0, outside: [], overlaps: [], marksOutside: [] };
    for (const svg of document.querySelectorAll('svg[data-view]')) {
      if (!visible(svg)) continue; tx.drawings++;
      const sr = svg.getBoundingClientRect(); const name = svg.getAttribute('data-view');
      const ts = [...svg.querySelectorAll('text')].filter(t => t.textContent.trim() && visible(t)); const rs = ts.map(t => t.getBoundingClientRect());
      tx.labels += ts.length;
      ts.forEach((t, i) => { const r = rs[i]; if (r.left < sr.left - 0.5 || r.right > sr.right + 0.5 || r.top < sr.top - 0.5 || r.bottom > sr.bottom + 0.5) tx.outside.push({ svg: name, text: t.textContent.slice(0, 40) }); });
      // marks inside the drawing too (D2-126): a dot or circle cut by the drawing's edge fails
      for (const m of svg.querySelectorAll('circle, [data-mark]:not([data-mark="label"])')) {
        if (m.tagName.toLowerCase() === 'text' || !visible(m)) continue;
        const r = m.getBoundingClientRect(); if (r.width === 0 && r.height === 0) continue;
        if (r.left < sr.left - 0.5 || r.right > sr.right + 0.5 || r.top < sr.top - 0.5 || r.bottom > sr.bottom + 0.5) tx.marksOutside.push({ svg: name, mark: (m.getAttribute('data-key') || m.tagName).slice(0, 40) });
      }
      for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) {
        if (ts[i].contains(ts[j]) || ts[j].contains(ts[i])) continue;
        if (inter(rs[i], rs[j], 1.5)) tx.overlaps.push({ svg: name, a: ts[i].textContent.slice(0, 30), b: ts[j].textContent.slice(0, 30) });
      }
    }
    tx.overlaps = tx.overlaps.slice(0, 30); tx.marksOutside = tx.marksOutside.slice(0, 30); out.textCheck = tx;
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

    // scale: bars from zero, points on one straight scale (data viz brief, section 6)
    const scale = { groups: 0, marks: 0, bad: [] };
    const groups = new Map();
    document.querySelectorAll('figure[data-spec]').forEach((fig, fi) => {
      fig.querySelectorAll('svg').forEach((svg, si) => {
        if (!visible(svg)) return;
        svg.querySelectorAll('[data-mark="bar"][data-value],[data-mark="point"][data-value]').forEach((el) => {
          if (!visible(el)) return;
          const kind = el.getAttribute('data-mark'); const axis = el.getAttribute('data-axis') || (kind === 'bar' ? 'x' : 'y');
          const id = `${fig.getAttribute('data-spec')}#${fi}/svg${si}/${el.getAttribute('data-scale') || 'default'}/${kind}/${axis}`;
          const v = parseFloat(el.getAttribute('data-value')); const r = el.getBoundingClientRect();
          const len = axis === 'x' ? r.width : r.height; const pos = axis === 'x' ? r.left + r.width / 2 : r.top + r.height / 2;
          if (!groups.has(id)) groups.set(id, []);
          groups.get(id).push({ v, len, pos, key: el.getAttribute('data-key') });
        });
      });
    });
    // bars drawn in HTML (in-row bars in tables): grouped by data-scale, else by their table, else the figure
    document.querySelectorAll('figure[data-spec]').forEach((fig, fi) => {
      const tables = [...fig.querySelectorAll('table')];
      fig.querySelectorAll('[data-mark="bar"][data-value]').forEach((el) => {
        if (el instanceof SVGElement || el.closest('svg') || !visible(el)) return;
        const axis = el.getAttribute('data-axis') || 'x';
        const t = el.closest('table'); const where = el.getAttribute('data-scale') || (t ? 'table' + tables.indexOf(t) : 'html');
        const id = `${fig.getAttribute('data-spec')}#${fi}/html/${where}/bar/${axis}`;
        const r = el.getBoundingClientRect(); const v = parseFloat(el.getAttribute('data-value'));
        if (!groups.has(id)) groups.set(id, []);
        groups.get(id).push({ v, len: axis === 'x' ? r.width : r.height, pos: 0, key: el.getAttribute('data-key') });
      });
    });
    for (const [id, ms] of groups) {
      const kind = id.split('/')[3];
      const distinct = new Set(ms.map(m => m.v)).size;
      // a 100 percent stacked bar: several segments per key whose lengths add to the same total in every row.
      // Then each segment must be its value's share of the row (within 1 px), and the shared scale test does not apply.
      const byKey = new Map(); for (const m of ms) { if (!byKey.has(m.key)) byKey.set(m.key, []); byKey.get(m.key).push(m); }
      const rowsLen = [...byKey.values()].map(g => g.reduce((a, m) => a + m.len, 0));
      const medLen = [...rowsLen].sort((a, b) => a - b)[rowsLen.length >> 1];
      const tol = Math.max(1.5, 0.015 * medLen);
      const full = rowsLen.filter(l => Math.abs(l - medLen) <= tol).length;
      const multi = [...byKey.values()].filter(g => g.length >= 2).length;
      // most rows hold several segments that fill one common length: read the group as 100 percent bars
      const stacked = kind === 'bar' && byKey.size >= 3 && multi >= 0.75 * byKey.size && full >= 0.75 * byKey.size;
      if (stacked) {
        scale.groups++; scale.marks += ms.length;
        for (const [k, g] of byKey) {
          const tl0 = g.reduce((a, m) => a + m.len, 0);
          if (Math.abs(tl0 - medLen) > tol) { scale.bad.push({ group: id + ' (share)', key: k, value: null, px: +tl0.toFixed(1), off: +(tl0 - medLen).toFixed(1), note: 'row does not fill the 100 percent bar' }); continue; }
        }
        for (const g of byKey.values()) {
          const tv = g.reduce((a, m) => a + Math.abs(m.v), 0), tl = g.reduce((a, m) => a + m.len, 0);
          for (const m of g) { const d = Math.abs(m.len - tl * Math.abs(m.v) / tv); if (d > 1.0) scale.bad.push({ group: id + ' (share)', key: m.key, value: m.v, px: +m.len.toFixed(1), off: +d.toFixed(1) }); }
        }
        continue;
      }
      if (kind === 'bar' && distinct >= 2) {
        scale.groups++; scale.marks += ms.length;
        const med = (xs) => { const t = [...xs].sort((a, b) => a - b); const h = t.length >> 1; return t.length % 2 ? t[h] : (t[h - 1] + t[h]) / 2; };
        const k = med(ms.filter(m => m.v !== 0).map(m => m.len / Math.abs(m.v)));   // median ratio, so one bad bar cannot move the scale
        for (const m of ms) { const d = Math.abs(m.len - k * Math.abs(m.v)); if (d > Math.max(1.0, 0.015 * m.len)) scale.bad.push({ group: id, key: m.key, value: m.v, px: +m.len.toFixed(1), off: +d.toFixed(1) }); }
      }
      if (kind === 'point' && distinct >= 3) {
        scale.groups++; scale.marks += ms.length;
        // Theil-Sen fit (median of pairwise slopes), so one misplaced point is named and cannot move the scale
        const med = (xs) => { const t = [...xs].sort((a, b) => a - b); const h = t.length >> 1; return t.length % 2 ? t[h] : (t[h - 1] + t[h]) / 2; };
        const slopes = []; for (let i = 0; i < ms.length; i++) for (let j = i + 1; j < ms.length; j++) if (ms[i].v !== ms[j].v) slopes.push((ms[j].pos - ms[i].pos) / (ms[j].v - ms[i].v));
        const b = med(slopes), a0 = med(ms.map(m => m.pos - b * m.v));
        for (const m of ms) { const d = Math.abs(m.pos - (a0 + b * m.v)); if (d > 1.0) scale.bad.push({ group: id, key: m.key, value: m.v, px: +m.pos.toFixed(1), off: +d.toFixed(1) }); }
      }
    }
    scale.bad = scale.bad.slice(0, 20); out.scale = scale;
    // party marks never in Pillar Red or Prussian (DR-48)
    const party = { marks: 0, bad: [] };
    document.querySelectorAll('[data-party]').forEach((root) => {
      [root, ...root.querySelectorAll('*')].forEach((el) => {
        if (!visible(el)) return; const cs = getComputedStyle(el); party.marks++;
        const cands = el instanceof SVGElement ? [cs.fill !== 'none' ? parse(cs.fill) : null, cs.stroke !== 'none' ? parse(cs.stroke) : null] : [parse(cs.backgroundColor), parse(cs.color), parse(cs.borderLeftColor)];
        if (cands.some(c => near(c, RED) || near(c, PRUSSIAN, 4))) party.bad.push({ party: root.getAttribute('data-party'), tag: el.tagName });
      });
    });
    party.bad = party.bad.slice(0, 10); out.party = party;
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

// ---------------------------------------------------------------------------------------------------------------- Phase 3
const KIT_MODE = process.argv.includes('--kit') || process.argv.includes('--kit-self-test');
async function kitAudit(page) {
  return page.evaluate(({ RED, PRUSSIAN }) => {
    const rgb = (s) => { const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(s || ''); return m ? [+m[1], +m[2], +m[3]] : null; };
    const same = (a, b) => a && b && Math.abs(a[0] - b[0]) < 3 && Math.abs(a[1] - b[1]) < 3 && Math.abs(a[2] - b[2]) < 3;
    const out = [];
    document.querySelectorAll('figure.oac-fig').forEach((fig) => {
      const id = fig.id || fig.getAttribute('data-oa-chart-id');
      const f = [];
      const svg = fig.querySelector('svg.oac-svg');
      const txt = fig.textContent;
      if (/\u2014/.test(txt)) f.push('an em dash in the figure');
      if (/Yes on 3|Veterans for All Voters|Ranked Choice Melrose/.test(txt)) f.push('the retired disclosure in the figure (DR-100)');
      if (!svg) { out.push({ id, f: f.concat(fig.getAttribute('data-oa-error') ? ['drawing error: ' + fig.getAttribute('data-oa-error')] : ['no drawing']) }); return; }
      // the drawing's name and description name elements that are on the page (D3-101, access M3)
      ['aria-labelledby', 'aria-describedby'].forEach((a) => {
        (svg.getAttribute(a) || '').split(/\s+/).filter(Boolean).forEach((ref) => { if (!document.getElementById(ref)) f.push(`the drawing's ${a} names ${ref}, which is not on the page`); });
      });
      const named = (svg.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean).map((r) => (document.getElementById(r) || {}).textContent || '').join(' ').trim() || svg.getAttribute('aria-label') || (svg.querySelector('title') || {}).textContent;
      if (!named) f.push('the drawing has no accessible name');
      const sb = svg.getBoundingClientRect(), scale = sb.width / (+svg.getAttribute('width') || sb.width);
      const boxes = [];
      svg.querySelectorAll('text').forEach((t) => {
        const r = t.getBoundingClientRect();
        if (!r.width) return;
        const size = parseFloat(getComputedStyle(t).fontSize) * scale;
        if (size < 12.99) f.push(`text "${t.textContent.slice(0, 30)}" at ${size.toFixed(1)} px`);
        if (r.left < sb.left - 1 || r.right > sb.right + 1 || r.top < sb.top - 1 || r.bottom > sb.bottom + 1) f.push(`text "${t.textContent.slice(0, 30)}" outside its drawing`);
        // the glyphs' own box: the line box less the leading, so two lines set tight do not count as touching
        const lines = Math.max(1, t.querySelectorAll('tspan').length);
        const pad = (r.height / lines - size) / 2;
        boxes.push({ s: t.textContent.slice(0, 30), l: r.left, r: r.right, t: r.top + Math.max(0, pad), b: r.bottom - Math.max(0, pad) });
      });
      for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i], b = boxes[j];
        if (a.l + 1 < b.r && b.l + 1 < a.r && a.t + 1 < b.b && b.t + 1 < a.b) f.push(`texts overlap: "${a.s}" and "${b.s}"`);
      }
      let reds = 0;
      svg.querySelectorAll('rect, circle, path, polygon, line').forEach((m) => {
        const cs = getComputedStyle(m), fill = rgb(cs.fill), stroke = rgb(cs.stroke);
        const r = m.getBoundingClientRect();
        if (r.width && (r.left < sb.left - 1.5 || r.right > sb.right + 1.5 || r.top < sb.top - 1.5 || r.bottom > sb.bottom + 1.5)) f.push(`a ${m.tagName} cut by the drawing's edge`);
        if (same(fill, RED) || same(stroke, RED)) reds++;
        if (m.closest('[data-party]') || m.hasAttribute('data-party')) {
          if (same(fill, RED) || same(fill, PRUSSIAN) || same(stroke, RED) || same(stroke, PRUSSIAN)) f.push('a party mark in Pillar Red or Prussian (DR-48)');
        }
      });
      if (reds > 1) f.push(`${reds} working-red marks in one drawing (Rule 05.3)`);
      out.push({ id, f, texts: boxes.length });
    });
    return out;
  }, { RED, PRUSSIAN });
}
// Forced colors (D3-94): with the reader's system colors forced, no drawing text may print in the ink of the shape under it
async function kitForced(page) {
  return page.evaluate(() => {
    const out = [];
    document.querySelectorAll('figure.oac-fig svg.oac-svg').forEach((svg) => {
      const id = (svg.closest('figure') || {}).id;
      const shapes = Array.from(svg.querySelectorAll('rect, circle, path, polygon')).filter((e) => !e.closest('defs'));
      svg.querySelectorAll('text').forEach((t) => {
        const b = t.getBBox(), m = t.getCTM(), sm = svg.getCTM();
        if (!m || !sm) return;
        const pt = new DOMPoint(b.x + b.width / 2, b.y + b.height / 2).matrixTransform(m).matrixTransform(sm.inverse());
        let ground = getComputedStyle(svg.closest('figure') || svg).backgroundColor, under = null;
        for (const e of shapes) {
          if (e.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_PRECEDING) break;   // painted after the text
          const cs = getComputedStyle(e);
          if (!cs.fill || cs.fill === 'none') continue;
          const em = e.getCTM();
          if (!em) continue;
          const lp = pt.matrixTransform(sm).matrixTransform(em.inverse());
          // a hatch under the text is no single ink: the text's halo carries it, so it is not compared
          if (e.isPointInFill && e.isPointInFill(new DOMPoint(lp.x, lp.y))) { under = cs.fill.indexOf('url') === 0 ? 'pattern' : cs.fill; }
        }
        if (under === 'pattern') return;
        const ink = getComputedStyle(t).fill;
        const g = under || ground;
        if (ink && g && ink === g && !/rgba\(0, 0, 0, 0\)|transparent/.test(g)) out.push(`${id}: forced colors: "${t.textContent.slice(0, 30)}" prints in the ink of its ground (${ink} on ${under ? "a shape" : "the figure"})`);
      });
    });
    return out;
  });
}
async function kitMain(target, widths) {
  const browser = await chromium.launch();
  const report = { page: target, checked: new Date().toISOString(), widths, figures: 0, failures: [] };
  for (const width of widths) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 } });
    const page = await ctx.newPage();
    await page.goto('file://' + target, { waitUntil: 'load', timeout: 120000 });
    await page.evaluate(() => document.fonts.ready);
    // charts draw as they near the screen (D3-97); a check draws them all first
    await page.evaluate(() => window.OAChart && OAChart.draw_all && OAChart.draw_all());
    await page.waitForFunction(() => Array.from(document.querySelectorAll('figure.oac-fig')).every((f) => f.getAttribute('data-oa-drawn') || f.getAttribute('data-oa-error') || f.querySelector('svg.oac-svg')), null, { timeout: 60000 });
    const res = await kitAudit(page);
    report.figures = Math.max(report.figures, res.length);
    res.forEach((r) => r.f.forEach((x) => report.failures.push(`${width}: ${r.id}: ${x}`)));
    await page.emulateMedia({ forcedColors: 'active' });
    (await kitForced(page)).forEach((x) => report.failures.push(`${width}: ${x}`));
    await page.emulateMedia({ forcedColors: 'none' });
    await ctx.close();
  }
  await browser.close();
  return report;
}
async function kitSelfTest() {
  // one clean figure and one figure for each planted fault, drawn as the kit draws (static SVG, no script needed)
  const fig = (id, body, extra, name) => `<figure class="oac-fig" id="${id}" data-oa-drawn="300"><p>Title.${extra || ''}</p><div data-oa-art><svg class="oac-svg" width="300" height="100" viewBox="0 0 300 100" style="display:block" ${name || 'aria-label="A drawing."'}>${body}</svg></div></figure>`;
  const T = (x, y, s, w) => `<text x="${x}" y="${y}" font-size="${s || 15}" font-family="Inter, Arial">${w || 'Label'}</text>`;
  const cases = [
    ['clean', fig('clean', T(10, 30) + '<rect x="10" y="50" width="40" height="20" fill="#121212"/>'), null],
    ['text under 13 px', fig('small', T(10, 30, 11)), 'px'],
    ['text outside its drawing', fig('out', T(270, 30, 15, 'Outside the edge')), 'outside its drawing'],
    ['two texts overlapping', fig('ovl', T(10, 30, 15, 'First label') + T(20, 34, 15, 'Second label')), 'overlap'],
    ['a mark cut by the edge', fig('cut', '<rect x="280" y="10" width="40" height="20" fill="#121212"/>'), 'cut'],
    ['a party mark in red', fig('party', '<rect data-party="Republican" x="10" y="10" width="40" height="20" fill="#E63946"/>'), 'party'],
    ['two working reds', fig('reds', '<circle cx="20" cy="20" r="5" fill="#E63946"/><circle cx="60" cy="20" r="5" fill="#E63946"/>'), 'working-red'],
    ['an em dash', fig('dash', T(10, 30), ' One \u2014 two.'), 'em dash'],
    ['the retired disclosure', fig('disc', T(10, 30), ' The editor works with the Yes on 3 campaign.'), 'disclosure'],
    ['a drawing named by an element not on the page', fig('noname', T(10, 30), '', 'aria-labelledby="not-here"'), 'not on the page'],
  ];
  const tmp = path.join(require('os').tmpdir(), `oa-kit-self-test-${process.pid}.html`);
  fs.writeFileSync(tmp, `<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:20px">${cases.map((c) => c[1]).join('')}</body></html>`);
  const rep = await kitMain(tmp, [1440]);
  fs.unlinkSync(tmp);
  let bad = 0;
  for (const [name, , want] of cases) {
    const id = /id="([^"]+)"/.exec(cases.find((c) => c[0] === name)[1])[1];
    const got = rep.failures.filter((x) => x.includes(`: ${id}: `));
    const ok = want === null ? got.length === 0 : got.some((x) => x.includes(want));
    console.log(`${ok ? (want ? 'caught' : 'pass') : 'MISSED'} ${name}${ok ? '' : ': ' + JSON.stringify(got)}`);
    bad += !ok;
  }
  console.log(bad ? `dataviz_check --kit self-test: ${bad} missed` : 'dataviz_check --kit self-test: every planted fault caught');
  return bad;
}

(async () => {
  if (process.argv.includes('--kit-self-test')) process.exit(await kitSelfTest() ? 1 : 0);
  if (KIT_MODE) {
    const rep = await kitMain(file, [1440, 390]);
    rep.pass = rep.failures.length === 0;
    const outPath = path.join(dir, `${stem}-Kit-Check-Results.json`);
    fs.writeFileSync(outPath, JSON.stringify(rep, null, 1));
    console.log(`${rep.pass ? 'PASS' : 'FAIL'} dataviz_check --kit ${path.relative(ROOT, file)}: ${rep.figures} figures at ${rep.widths.join(' and ')} px, ${rep.failures.length} failures`);
    rep.failures.slice(0, 40).forEach((f) => console.log('  - ' + f));
    console.log('  results: ' + outPath);
    process.exit(rep.pass ? 0 : 1);
  }
  const browser = await chromium.launch();
  const html = fs.readFileSync(file, 'utf8');
  const meta = html.match(/<meta\s+name="chart-views"\s+content="([^"]+)"/) || html.match(/<meta\s+name="atlas-views"\s+content="([^"]+)"/);
  const views = meta ? meta[1].trim().split(/\s+/) : ['overview'];
  const report = { file: path.relative(ROOT, file), checked: new Date().toISOString(), views, runs: [], navigation: null, failures: [] };
  const axeSrc = fs.existsSync(AXE) ? AXE : null;
  // 360 px added November 5 after the interface red team found small-phone failures the 390 px pass missed
  // --mid adds 1024 and 768 px (D2-126): the creative director found a table overprinting between phone and desktop widths
  for (const width of MID ? [1440, 1024, 768, 390, 360] : [1440, 390, 360]) {
    const ctx = await browser.newContext({ viewport: { width, height: width === 1440 ? 900 : width === 390 ? 844 : width === 360 ? 780 : 1000 }, deviceScaleFactor: 1 });
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
      if (a.textCheck.marksOutside.length) report.failures.push(`${tag}: ${a.textCheck.marksOutside.length} marks cut by their drawing's edge (first: ${JSON.stringify(a.textCheck.marksOutside[0])})`);
      if (a.red.unmarked.length) report.failures.push(`${tag}: ${a.red.unmarked.length} red marks without data-red`);
      if (a.red.jobs.length > 1) report.failures.push(`${tag}: ${a.red.jobs.length} working-red jobs (${a.red.jobs.join(', ')})`);
      if (a.red.onPrussian.length) report.failures.push(`${tag}: red over Prussian (${a.red.onPrussian.length})`);
      if (a.scale.bad.length) report.failures.push(`${tag}: ${a.scale.bad.length} marks off their scale (first: ${JSON.stringify(a.scale.bad[0])})`);
      if (a.party.bad.length) report.failures.push(`${tag}: ${a.party.bad.length} party marks in Pillar Red or Prussian`);
      if (axe && axe.length) report.failures.push(`${tag}: axe ${axe.map(v => v.id + 'x' + v.nodes).join(', ')}`);
      if (!axe) report.failures.push(`${tag}: axe-core not found at ${path.relative(ROOT, AXE)}`);
      if (focus && focus.some(f => !f.ring)) report.failures.push(`${tag}: ${focus.filter(f => !f.ring).length} focus stops without a visible ring`);
      if (captures && (width === 1440 || width === 390)) {
        const base = path.join(capDir, `${stem}-${view}-${width}`);
        await page.evaluate(() => window.scrollTo(0, 0));
        if (width === 1440) {
          await page.screenshot({ path: base + '.jpg', fullPage: true, type: 'jpeg', quality: 84 });
          const gray = await page.addStyleTag({ content: 'html{filter:grayscale(1)!important}' });
          await page.screenshot({ path: base + '-grayscale.jpg', fullPage: true, type: 'jpeg', quality: 70 });
          // the views share one document (hash routing), so the filter must go before the next view's capture
          await gray.evaluate((el) => el.remove());
        } else {
          await page.screenshot({ path: base + '.jpg', fullPage: true, type: 'jpeg', quality: 80 });
        }
      }
    }
    if (width === 1440 && !BOARD && views.length > 1) {
      // navigation: the first link into a close-up, then back
      await page.goto('file://' + file + '#' + views[0], { waitUntil: 'networkidle' });
      await page.waitForTimeout(400);
      const target = await page.evaluate((views) => {
        const root = document.querySelector(`[data-view-root="${views[0]}"]`) || document;
        const close = views.slice(1);
        for (const v of close) { const el = root.querySelector(`a[href="#${v}"], [data-goto="${v}"]`); if (el) { el.setAttribute('data-check-click', '1'); return v; } }
        return null;
      }, views);
      const nav = { target, ok: false };
      if (target) {
        await page.click('[data-check-click="1"]');
        await page.waitForTimeout(700);
        nav.afterClick = await page.evaluate((v) => ({ hash: location.hash, visible: !!document.querySelector(`[data-view-root="${v}"]`) && getComputedStyle(document.querySelector(`[data-view-root="${v}"]`)).display !== 'none' }), target);
        await page.goBack(); await page.waitForTimeout(700);
        nav.afterBack = await page.evaluate((v0) => ({ hash: location.hash, visible: !!document.querySelector(`[data-view-root="${v0}"]`) && getComputedStyle(document.querySelector(`[data-view-root="${v0}"]`)).display !== 'none' }), views[0]);
        nav.ok = nav.afterClick.hash === '#' + target && nav.afterClick.visible && nav.afterBack.visible;
      }
      report.navigation = nav;
      if (!nav.ok && views.length > 1) report.failures.push(`navigation: first view to another view and back failed (${JSON.stringify(nav)})`);
    }
    if (outside.size) report.failures.push(`${width}: outside requests to ${[...outside].join(', ')}`);
    if (errors.length) report.failures.push(`${width}: page errors: ${errors.slice(0, 3).join(' | ')}`);
    await ctx.close();
  }
  await browser.close();
  report.pass = report.failures.length === 0;
  const outPath = path.join(dir, `${stem}-Check-Results.json`);
  fs.writeFileSync(outPath, JSON.stringify(report, null, 1));
  console.log(`${report.pass ? 'PASS' : 'FAIL'} ${path.relative(ROOT, file)}: ${views.length} views x ${MID ? 5 : 3} widths, ${report.failures.length} failures`);
  for (const f of report.failures) console.log('  - ' + f);
  console.log('  results: ' + path.relative(ROOT, outPath));
  process.exit(report.pass ? 0 : 1);
})();
