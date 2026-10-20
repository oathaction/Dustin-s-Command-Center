// Phase 0 UX audit, part 3: accessibility checks on V5 Polished.
// Reflow at 320, text at 200 percent (three methods), forced colors, focus obscured by the sticky nav,
// target sizes, text alternatives, diagram equivalents, color-only meaning, axe at 320.
// Usage: node ux_a11y.js <project-root>
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = path.resolve(process.argv[2] || '.');
const V5 = 'file://' + path.join(ROOT, 'source', '20261018_Oath-And-Action-Brand-Guide_V5-Polished.html');
const OUT = path.join(ROOT, 'work', 'handoffs', 'phase-0', 'ux-data');
const SHOTS = path.join(ROOT, 'work', 'boards', 'screens', 'phase-0-ux');
const AXE = fs.readFileSync(path.join(ROOT, 'work', 'build', 'node_modules', 'axe-core', 'axe.min.js'), 'utf8');
fs.mkdirSync(OUT, { recursive: true });

async function open(browser, width, height, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: opts.dpr || 1, reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  await page.goto(V5);
  await page.waitForTimeout(1200);
  return page;
}

// Elements that stick out of the viewport horizontally and are not clipped by a scrolling or hidden ancestor.
const overflowFn = (vw) => {
  const clipped = (el) => { for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) { const o = getComputedStyle(e).overflowX; if (o !== 'visible') return e; } return null; };
  const out = {};
  for (const sec of document.querySelectorAll('section.chapter')) {
    const rec = { overflowing: 0, maxRight: 0, examples: [], scrollers: [] };
    for (const el of sec.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') continue;
      if (r.right > vw + 1 || r.left < -1) {
        const c = clipped(el);
        if (c) continue;
        rec.overflowing++;
        if (r.right > rec.maxRight) rec.maxRight = Math.round(r.right);
        if (rec.examples.length < 4) rec.examples.push((el.tagName.toLowerCase() + '.' + String(el.className.baseVal ?? el.className).split(' ').join('.')).slice(0, 60) + ' right=' + Math.round(r.right));
      }
      const cs = getComputedStyle(el);
      if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && el.scrollWidth > el.clientWidth + 1 && rec.scrollers.length < 6) rec.scrollers.push(String(el.className).split(' ')[0] + ' ' + el.scrollWidth + '/' + el.clientWidth);
    }
    out[sec.id] = rec;
  }
  out._doc = { scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth };
  return out;
};

// Text clipped by its own box or a hidden-overflow ancestor.
const clipFn = () => {
  const res = { clippedBoxes: 0, examples: [], byChapter: {} };
  for (const el of document.querySelectorAll('section.chapter *')) {
    if (el.closest('svg')) continue;
    const cs = getComputedStyle(el);
    const hidden = ['hidden', 'clip'].includes(cs.overflowX) || ['hidden', 'clip'].includes(cs.overflowY);
    if (!hidden) continue;
    if (!el.textContent.trim()) continue;
    if (el.classList.contains('visually-hidden')) continue;
    const over = el.scrollHeight > el.clientHeight + 3 || el.scrollWidth > el.clientWidth + 3;
    if (over) {
      res.clippedBoxes++;
      const ch = el.closest('section.chapter').id;
      res.byChapter[ch] = (res.byChapter[ch] || 0) + 1;
      if (res.examples.length < 12) res.examples.push(ch + ': ' + (el.tagName.toLowerCase() + '.' + String(el.className).split(' ').join('.')).slice(0, 50) + ' ' + el.scrollWidth + 'x' + el.scrollHeight + ' in ' + el.clientWidth + 'x' + el.clientHeight + ' "' + el.textContent.trim().slice(0, 30) + '"');
    }
  }
  return res;
};

// Tab through the page and record whether the sticky nav covers the focused element.
async function focusObscured(page, maxStops = 70) {
  const out = [];
  await page.evaluate(() => { document.activeElement && document.activeElement.blur(); window.scrollTo({ top: 0, behavior: 'instant' }); });
  for (let i = 0; i < maxStops; i++) {
    await page.keyboard.press('Tab');
    await page.waitForTimeout(40);
    const r = await page.evaluate(() => {
      const a = document.activeElement;
      if (!a || a === document.body) return null;
      const n = document.querySelector('.site-nav').getBoundingClientRect();
      const e = a.getBoundingClientRect();
      const inNav = !!a.closest('.site-nav') || a.classList.contains('skip');
      const covered = inNav ? 0 : Math.max(0, Math.min(e.bottom, n.bottom) - Math.max(e.top, n.top));
      return { name: (a.getAttribute('aria-label') || a.textContent || a.tagName).trim().slice(0, 30), top: Math.round(e.top), h: Math.round(e.height), navBottom: Math.round(n.bottom), coveredPx: Math.round(covered), entirely: !inNav && e.bottom <= n.bottom && e.top >= n.top, belowViewport: e.top >= innerHeight };
    });
    if (!r) break;
    out.push(r);
  }
  return out;
}

const targetFn = () => {
  const els = [...document.querySelectorAll('a[href], button, input, select, summary, [tabindex]:not([tabindex="-1"])')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !e.closest('[hidden]') && !e.closest('dialog:not([open])'); });
  const boxes = els.map((e) => { const r = e.getBoundingClientRect(); return { e, r, cx: r.left + r.width / 2, cy: r.top + r.height / 2 + scrollY }; });
  const small = boxes.filter((b) => b.r.width < 24 || b.r.height < 24);
  const rectCircle = (r, cx, cy, rad) => { const x = Math.max(r.left, Math.min(cx, r.right)); const y = Math.max(r.top + scrollY, Math.min(cy, r.bottom + scrollY)); return (x - cx) ** 2 + (y - cy) ** 2 < rad * rad; };
  return small.map((b) => {
    const inline = b.e.tagName === 'A' && getComputedStyle(b.e).display === 'inline' && b.e.parentElement.textContent.trim().length > b.e.textContent.trim().length + 20;
    const conflict = boxes.some((o) => o !== b && (rectCircle(o.r, b.cx, b.cy, 12) || (small.includes(o) && Math.hypot(o.cx - b.cx, o.cy - b.cy) < 24)));
    return { name: (b.e.getAttribute('aria-label') || b.e.textContent || b.e.tagName).trim().slice(0, 40), w: Math.round(b.r.width), h: Math.round(b.r.height), inline, spacingPasses: !conflict, section: (b.e.closest('section') || {}).id || 'shell' };
  });
};

const altFn = () => {
  const vis = (e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const imgs = [...document.querySelectorAll('img')].map((i) => { const fig = i.closest('figure'); const cap = fig && fig.querySelector('figcaption'); return { alt: i.getAttribute('alt'), w: i.getBoundingClientRect().width, captionSame: !!(cap && cap.textContent.trim() === (i.getAttribute('alt') || '').trim()), chapter: (i.closest('section') || {}).id }; });
  const svgImg = [...document.querySelectorAll('svg[role="img"]')].filter((s) => !s.closest('button') && !s.closest('[aria-hidden="true"]'));
  const labels = {};
  svgImg.forEach((s) => { const l = s.getAttribute('aria-label') || (s.querySelector('title') || {}).textContent || '(none)'; labels[l] = (labels[l] || 0) + 1; });
  const unlabeled = svgImg.filter((s) => !s.getAttribute('aria-label') && !s.getAttribute('aria-labelledby') && !s.querySelector('title')).length;
  const exposedNoRole = [...document.querySelectorAll('body svg')].filter((s) => vis(s) && !s.getAttribute('role') && s.getAttribute('aria-hidden') !== 'true' && !s.closest('[aria-hidden="true"],[role="img"],button,a') && !s.parentElement.closest('svg')).length;
  const divImg = [...document.querySelectorAll('[role="img"]:not(svg)')].map((d) => d.getAttribute('aria-label'));
  const ariaLabelOnGeneric = [...document.querySelectorAll('div[aria-label],span[aria-label],p[aria-label]')].filter((d) => !d.getAttribute('role')).map((d) => d.id || d.className);
  // Diagrams: sizeable images or role=img graphics, and whether a table or description sits in the same figure or chart.
  const diagrams = [...document.querySelectorAll('svg[role="img"], img, [role="img"]:not(svg)')].filter((g) => { const r = g.getBoundingClientRect(); return r.width >= 200 && r.height >= 120 && !g.closest('button'); }).map((g) => {
    const box = g.closest('figure, .chart, .rule, .stage') || g.parentElement;
    return { chapter: (g.closest('section') || {}).id, label: (g.getAttribute('aria-label') || g.getAttribute('alt') || '').slice(0, 60), describedby: !!g.getAttribute('aria-describedby'), tableNearby: !!(box && box.querySelector('table')), detailsNearby: !!(box && box.querySelector('details')) };
  });
  return { imgs, svgImgCount: svgImg.length, unlabeled, topLabels: Object.entries(labels).sort((a, b) => b[1] - a[1]).slice(0, 12), exposedNoRole, divImgCount: divImg.length, divImgSample: divImg.slice(0, 5), ariaLabelOnGeneric, diagrams };
};

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const data = {};

  // 1. Reflow at 320.
  let p = await open(browser, 320, 800);
  data.reflow320 = await p.evaluate(overflowFn, 320);
  data.clip320 = await p.evaluate(clipFn);
  await p.addScriptTag({ content: AXE });
  data.axe320 = await p.evaluate(async () => { const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'] } }); return r.violations.map((v) => ({ id: v.id, count: v.nodes.length, ex: v.nodes.slice(0, 3).map((n) => n.target.join(' ')) })); });
  data.targets320 = await p.evaluate(targetFn);
  data.focus320 = await focusObscured(p);
  // Screenshots of the widest offenders at 320.
  const worst = Object.entries(data.reflow320).filter(([k, v]) => k !== '_doc' && v.overflowing).sort((a, b) => b[1].maxRight - a[1].maxRight).slice(0, 4).map(([k]) => k);
  for (const id of worst) {
    const top = await p.evaluate((i) => { const s = document.getElementById(i); const all = [...s.querySelectorAll('*')].find((e) => e.getBoundingClientRect().right > 322); return all ? all.getBoundingClientRect().top + scrollY - 120 : s.offsetTop; }, id);
    await p.evaluate((t) => window.scrollTo({ top: t, behavior: 'instant' }), top);
    await p.waitForTimeout(200);
    await p.screenshot({ path: path.join(SHOTS, `reflow-320-${id}.png`) });
  }
  await p.context().close();

  // 2a. Root font size doubled: how many text elements respond?
  p = await open(browser, 1440, 900);
  data.rootDouble = await p.evaluate(() => {
    const els = [...document.querySelectorAll('section.chapter *')].filter((e) => !e.closest('svg') && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()));
    const before = els.map((e) => parseFloat(getComputedStyle(e).fontSize));
    document.documentElement.style.fontSize = '200%';
    const after = els.map((e) => parseFloat(getComputedStyle(e).fontSize));
    const changed = after.filter((a, i) => a > before[i] * 1.5).length;
    document.documentElement.style.fontSize = '';
    return { textElements: els.length, scaledToDouble: changed };
  });
  // 2b. Text-only 200 percent: every element's computed font size and px line height doubled, layout width kept at 1440.
  data.text200 = await p.evaluate(() => {
    const els = [...document.querySelectorAll('body *')].filter((e) => !(e.closest('svg') && e.tagName.toLowerCase() !== 'svg'));
    const sizes = els.map((e) => { const cs = getComputedStyle(e); return [parseFloat(cs.fontSize), cs.lineHeight]; });
    els.forEach((e, i) => { e.style.setProperty('font-size', sizes[i][0] * 2 + 'px', 'important'); if (sizes[i][1].endsWith('px')) e.style.setProperty('line-height', parseFloat(sizes[i][1]) * 2 + 'px', 'important'); });
    return { elements: els.length, docScrollWidth: document.documentElement.scrollWidth, navHeight: Math.round(document.querySelector('.site-nav').getBoundingClientRect().height), navLinksOverflow: document.querySelector('.nav-links').scrollWidth - document.querySelector('.nav-links').clientWidth };
  });
  data.text200overflow = await p.evaluate(overflowFn, 1440);
  data.text200clip = await p.evaluate(clipFn);
  for (const id of ['top', 'grid', 'in-use', 'reports']) {
    const el = p.locator(`#${id}`);
    await p.evaluate((i) => window.scrollTo({ top: document.getElementById(i).offsetTop, behavior: 'instant' }), id);
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(SHOTS, `text200-${id}.png`) });
  }
  await p.context().close();

  // 2c. Page zoom 200 percent of a 1440 by 900 window: 720 by 450 CSS px at device scale 2.
  p = await open(browser, 720, 450, { dpr: 2 });
  data.zoom200 = await p.evaluate(overflowFn, 720);
  data.zoom200nav = await p.evaluate(() => { const n = document.querySelector('.site-nav').getBoundingClientRect(); const l = document.querySelector('.nav-links'); return { navHeight: Math.round(n.height), share: Math.round((n.height / innerHeight) * 100), hiddenLinks: [...l.querySelectorAll('a')].filter((a) => a.getBoundingClientRect().right > innerWidth).map((a) => a.textContent) }; });
  data.focus720 = await focusObscured(p);
  await p.screenshot({ path: path.join(SHOTS, 'zoom200-top.png') });
  await p.context().close();

  // 3. Focus obscured, targets and alternatives at 1440 and 390.
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    p = await open(browser, w, h);
    data['focus' + w] = await focusObscured(p);
    data['targets' + w] = await p.evaluate(targetFn);
    if (w === 1440) data.alt = await p.evaluate(altFn);
    await p.context().close();
  }

  // 4. Forced colors.
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce', forcedColors: 'active' });
    p = await ctx.newPage();
    await p.goto(V5); await p.waitForTimeout(1200);
    data.forced = await p.evaluate(() => {
      const q = (s) => document.querySelector(s);
      const cs = (e, prop) => e ? getComputedStyle(e)[prop] : null;
      const sgCircle = q('#c-grid svg circle');
      const swatches = [...document.querySelectorAll('.swatch')].slice(0, 7).map((s) => cs(s, 'backgroundColor'));
      const lever = q('svg.lm.default .lever') || q('svg.lm .lever');
      const keySwatches = [...document.querySelectorAll('.series-key i')].map((i) => cs(i, 'backgroundColor'));
      return { forcedMatches: matchMedia('(forced-colors: active)').matches, bodyBg: cs(document.body, 'backgroundColor'), swatches, keySwatches, sgCircleFill: cs(sgCircle, 'fill'), leverFill: cs(lever, 'fill'), btnBorder: cs(q('#c-reset'), 'borderColor'), modalDisabledBorder: cs(q('#report-prev'), 'borderStyle'), navCurrentBorder: cs(q('.nav-links a'), 'borderBottomColor') };
    });
    for (const id of ['top', 'color', 'grid', 'data', 'reports', 'topic-icons']) {
      await p.evaluate((i) => window.scrollTo({ top: document.getElementById(i).offsetTop, behavior: 'instant' }), id);
      await p.waitForTimeout(150);
      await p.screenshot({ path: path.join(SHOTS, `forced-colors-${id}.png`) });
    }
    // Signal Grid states and composer in forced colors.
    const st = p.locator('#grid .states').first();
    await st.scrollIntoViewIfNeeded(); await st.screenshot({ path: path.join(SHOTS, 'forced-colors-grid-states.png') });
    const ch = p.locator('#data .charts');
    await ch.scrollIntoViewIfNeeded(); await ch.screenshot({ path: path.join(SHOTS, 'forced-colors-charts.png') });
    await ctx.close();
  }

  // 5. Color-only meaning: content-type and progress encodings rendered side by side, in color and grayscale.
  p = await open(browser, 1440, 900);
  await p.evaluate(() => {
    const g = window.oaSignalGrid;
    const wrap = document.createElement('div');
    wrap.id = 'ux-strip';
    wrap.style.cssText = 'position:fixed;inset:0;z-index:9999;background:#DCD9D2;padding:24px;font:600 13px Inter;color:#121212;display:grid;grid-template-columns:repeat(6,150px);gap:16px;align-content:start';
    const cell = (svg, t) => '<div>' + svg + '<div style="margin-top:6px">' + t + '</div></div>';
    const rows = [
      [g({ pillar: 'track', ctype: 'explainer', size: 40 }), 'Track + explainer (Prussian)'], [g({ pillar: 'track', ctype: 'analysis', size: 40 }), 'Track + analysis (Charcoal)'], [g({ pillar: 'track', ctype: 'tracker', size: 40 }), 'Track + tracker (Verdigris)'], [g({ pillar: 'track', ctype: 'step', size: 40 }), 'Track + step (Red)'], [g({ pillar: 'track', size: 40 }), 'Track, no type'], [g({ size: 40 }), 'Plain'],
      [g({ pillar: 'explain', ctype: 'explainer', size: 24 }), '24 px Prussian'], [g({ pillar: 'explain', ctype: 'analysis', size: 24 }), '24 px Charcoal'], [g({ pillar: 'explain', ctype: 'tracker', size: 24 }), '24 px Verdigris'], [g({ pillar: 'explain', ctype: 'step', size: 24 }), '24 px Red'], [g({ stage: 4, size: 40 }), 'Stage 4 of 9'], [g({ stage: 9, final: true, size: 40 }), 'Stage 9, final'],
    ];
    wrap.innerHTML = rows.map((r) => cell(r[0], r[1])).join('');
    document.body.appendChild(wrap);
  });
  await p.screenshot({ path: path.join(SHOTS, 'signal-grid-encodings-color.png'), clip: { x: 0, y: 0, width: 1060, height: 240 } });
  await p.evaluate(() => { document.getElementById('ux-strip').style.filter = 'grayscale(1)'; });
  await p.screenshot({ path: path.join(SHOTS, 'signal-grid-encodings-grayscale.png'), clip: { x: 0, y: 0, width: 1060, height: 240 } });
  await p.evaluate(() => document.getElementById('ux-strip').remove());
  // Charts and tracker ladder in grayscale.
  await p.evaluate(() => { document.querySelector('#data .charts').style.filter = 'grayscale(1)'; });
  const charts = p.locator('#data .charts');
  await charts.scrollIntoViewIfNeeded(); await charts.screenshot({ path: path.join(SHOTS, 'charts-grayscale.png') });
  // Rendered chart label sizes at 1440 and 390.
  data.chartLabels1440 = await p.evaluate(() => [...document.querySelectorAll('#data .chart svg[role="img"]')].map((s) => { const t = s.querySelector('text.lab'); return Math.round(t.getBoundingClientRect().height * 10) / 10; }));
  await p.context().close();
  p = await open(browser, 390, 844);
  data.chartLabels390 = await p.evaluate(() => [...document.querySelectorAll('#data .chart svg[role="img"]')].map((s) => { const t = s.querySelector('text.lab'); const scale = s.getBoundingClientRect().width / s.viewBox.baseVal.width; return { scale: Math.round(scale * 100) / 100, labelPx: Math.round(parseFloat(getComputedStyle(t).fontSize) * scale * 10) / 10 }; }));
  await p.context().close();

  fs.writeFileSync(path.join(OUT, '20261020_UX-Accessibility-Data.json'), JSON.stringify(data, null, 1));
  await browser.close();
  console.log('done');
})();
