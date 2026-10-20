// Phase 0 UX audit, part 2: every control in V5 Polished, tested with keyboard and pointer.
// Usage: node ux_interaction.js <project-root>
// Writes work/handoffs/phase-0/ux-data/20261020_UX-Interaction-Data.json and screenshots in work/boards/screens/phase-0-ux/.
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

const active = (p) => p.evaluate(() => {
  const a = document.activeElement;
  if (!a) return null;
  return { tag: a.tagName.toLowerCase(), id: a.id || null, name: (a.getAttribute('aria-label') || a.textContent || '').trim().slice(0, 40), inDialog: !!a.closest('dialog'), disabled: !!a.disabled };
});
const reader = (p) => p.evaluate(() => ({ open: document.getElementById('report-dialog').open, counter: document.getElementById('report-counter').textContent, zoom: document.getElementById('report-zoom').value, prevDisabled: document.getElementById('report-prev').disabled, nextDisabled: document.getElementById('report-next').disabled }));

async function open(browser, width, height, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width, height }, reducedMotion: opts.reduced ? 'reduce' : 'no-preference' });
  const page = await ctx.newPage();
  await page.goto(V5);
  await page.waitForTimeout(1200);
  return page;
}

async function readerTests(browser, width, height) {
  const r = {};
  const p = await open(browser, width, height);
  // Open from the main button.
  await p.focus('#report-first');
  await p.keyboard.press('Enter');
  await p.waitForTimeout(400);
  r.afterOpen = { state: await reader(p), focus: await active(p) };
  r.dialogSemantics = await p.evaluate(() => { const d = document.getElementById('report-dialog'); return { role: d.getAttribute('role'), ariaModal: d.getAttribute('aria-modal'), ariaLabel: d.getAttribute('aria-label'), ariaLabelledby: d.getAttribute('aria-labelledby'), matchesModal: d.matches(':modal'), headingInside: !!d.querySelector('h1,h2'), bodyTabIndex: document.getElementById('report-body').tabIndex, bodyRole: document.getElementById('report-body').getAttribute('role') }; });
  r.snapshot = await p.locator('#report-dialog').ariaSnapshot();
  // Tab cycle: 12 presses forward, 6 back.
  r.tabForward = [];
  for (let i = 0; i < 12; i++) { await p.keyboard.press('Tab'); r.tabForward.push(await active(p)); }
  r.tabBack = [];
  for (let i = 0; i < 6; i++) { await p.keyboard.press('Shift+Tab'); r.tabBack.push(await active(p)); }
  // Arrow keys with focus on Close.
  await p.focus('#report-close');
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  r.arrowRightOnClose = await reader(p);
  await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(150);
  r.arrowLeftOnClose = await reader(p);
  // Arrow keys with focus on the zoom select: does the page change and the select value change too?
  await p.focus('#report-zoom');
  await p.keyboard.press('ArrowDown'); await p.waitForTimeout(150);
  r.arrowDownOnZoom = await reader(p);
  await p.keyboard.press('ArrowRight'); await p.waitForTimeout(150);
  r.arrowRightOnZoom = await reader(p);
  await p.selectOption('#report-zoom', 'fit');
  // Full size on this width: horizontal overflow of the page body and whether the keyboard can reach it.
  await p.selectOption('#report-zoom', 'full'); await p.waitForTimeout(300);
  r.fullSize = await p.evaluate(() => { const b = document.getElementById('report-body'); return { scrollW: b.scrollWidth, clientW: b.clientWidth, scrollH: b.scrollHeight, clientH: b.clientHeight, focusable: b.tabIndex >= 0 }; });
  await p.screenshot({ path: path.join(SHOTS, `reader-fullsize-${width}.png`) });
  await p.selectOption('#report-zoom', 'fit'); await p.waitForTimeout(200);
  // axe on the open dialog.
  await p.addScriptTag({ content: AXE });
  r.axeOpen = await p.evaluate(async () => { const res = await axe.run(document.getElementById('report-dialog'), { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } }); return res.violations.map((v) => ({ id: v.id, impact: v.impact, count: v.nodes.length, ex: v.nodes.slice(0, 2).map((n) => n.target.join(' ') + ' | ' + n.failureSummary.split('\n')[1]) })); });
  r.dupIdsOpen = await p.evaluate(() => { const c = {}; document.querySelectorAll('[id]').forEach((e) => { c[e.id] = (c[e.id] || 0) + 1; }); return Object.entries(c).filter(([, n]) => n > 1).slice(0, 10); });
  // Next to the last page with the Next button: where does focus go when Next becomes disabled?
  await p.focus('#report-next');
  for (let i = 0; i < 12; i++) await p.keyboard.press('Enter');
  await p.waitForTimeout(200);
  r.atLastPage = { state: await reader(p), focus: await active(p) };
  await p.keyboard.press('Tab');
  r.tabAfterLast = await active(p);
  // Escape closes; focus returns to the opener.
  await p.keyboard.press('Escape'); await p.waitForTimeout(250);
  r.afterEscape = { state: await reader(p), focus: await active(p) };
  // Open from thumbnail 5 by keyboard, close with the Close button, check focus return.
  await p.focus('[data-report="4"]');
  await p.keyboard.press('Enter'); await p.waitForTimeout(300);
  r.thumb5 = { state: await reader(p), focus: await active(p) };
  await p.click('#report-close'); await p.waitForTimeout(250);
  r.afterCloseButton = { state: await reader(p), focus: await active(p) };
  // Backdrop click.
  await p.focus('[data-report="0"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(300);
  await p.mouse.click(4, 4); await p.waitForTimeout(250);
  r.afterBackdropClick = await reader(p);
  await p.context().close();
  return r;
}

async function motionTests(browser) {
  const out = {};
  for (const reduced of [false, true]) {
    const k = reduced ? 'reduced' : 'normal';
    const p = await open(browser, 1440, 900, { reduced });
    const m = {};
    // Running animations right after load.
    m.runningOnLoad = await p.evaluate(() => document.getAnimations().map((a) => ({ name: a.animationName || a.constructor.name, target: (a.effect && a.effect.target && (a.effect.target.closest('svg')?.getAttribute('aria-label') || a.effect.target.className?.baseVal || a.effect.target.className)) || null, iterations: a.effect && a.effect.getComputedTiming().iterations, state: a.playState })));
    m.loadingLever = await p.evaluate(() => { const l = document.querySelector('svg.lm.loading .lever'); if (!l) return null; const s = []; return { opacity: getComputedStyle(l).opacity, anim: getComputedStyle(l).animationName, iter: getComputedStyle(l).animationIterationCount }; });
    m.trackerLoading = await p.evaluate(() => { const st = document.querySelector('.stage.loading'); if (!st) return null; const lev = st.querySelector('circle[r="4.75"], .lever'); const all = [...st.querySelectorAll('circle')].map((c) => getComputedStyle(c).opacity + '/' + getComputedStyle(c).animationName); return { label: st.querySelector('svg')?.getAttribute('aria-label'), circles: all.slice(-3) }; });
    // Hinge.
    await p.locator('#hinge-play').scrollIntoViewIfNeeded();
    m.hingeBefore = await p.evaluate(() => document.getElementById('hinge-anim').className);
    await p.click('#hinge-play');
    await p.waitForTimeout(60);
    m.hingeDuring = await p.evaluate(() => ({ cls: document.getElementById('hinge-anim').className, w1opacity: getComputedStyle(document.querySelector('#hinge-anim .w1')).opacity, anims: document.getAnimations().filter((a) => a.effect.target.closest && a.effect.target.closest('#hinge-anim')).length }));
    await p.waitForTimeout(900);
    m.hingeAfter = await p.evaluate(() => ({ cls: document.getElementById('hinge-anim').className, w1opacity: getComputedStyle(document.querySelector('#hinge-anim .w1')).opacity, ampOpacity: getComputedStyle(document.querySelector('#hinge-anim svg')).opacity }));
    m.hingeA11y = await p.locator('#hinge-anim').ariaSnapshot();
    // Lever reveal.
    await p.locator('#lever-play').scrollIntoViewIfNeeded();
    m.leverBefore = await p.evaluate(() => document.getElementById('lever-anim').getAttribute('class'));
    await p.click('#lever-play');
    await p.waitForTimeout(60);
    m.leverDuring = await p.evaluate(() => ({ cls: document.getElementById('lever-anim').getAttribute('class'), anims: document.getAnimations().filter((a) => a.effect.target.closest && a.effect.target.closest('#lever-anim')).length }));
    await p.waitForTimeout(800);
    // Tracker.
    m.tracker = [];
    m.trackerLive = await p.evaluate(() => ({ labelLive: document.getElementById('tracker-label').getAttribute('aria-live'), gridLive: document.getElementById('tracker-grid').getAttribute('aria-live'), role: document.getElementById('tracker-label').getAttribute('role') }));
    for (let i = 0; i < 9; i++) { await p.click('#tracker-next'); m.tracker.push(await p.evaluate(() => document.getElementById('tracker-label').textContent + ' | ' + document.querySelector('#tracker-grid svg').getAttribute('aria-label'))); }
    await p.click('#tracker-reset');
    m.trackerAfterReset = await p.evaluate(() => document.getElementById('tracker-label').textContent);
    if (!reduced) {
      // Screenshot the loading state twice, 600 ms apart, to show the pulse.
      const st = p.locator('svg.lm.loading').first();
      await st.scrollIntoViewIfNeeded();
      await p.waitForTimeout(100);
      await st.screenshot({ path: path.join(SHOTS, 'loading-pulse-a.png') });
      await p.waitForTimeout(600);
      await st.screenshot({ path: path.join(SHOTS, 'loading-pulse-b.png') });
    }
    out[k] = m;
    await p.context().close();
  }
  return out;
}

async function controlTests(browser) {
  const out = {};
  const p = await open(browser, 1440, 900);
  // View on dark.
  const t = p.locator('#surface-toggle');
  await t.scrollIntoViewIfNeeded();
  out.toggleBefore = await t.ariaSnapshot();
  await t.focus(); await p.keyboard.press('Enter'); await p.waitForTimeout(150);
  out.toggleAfter = await t.ariaSnapshot();
  out.toggleState = await p.evaluate(() => { const b = document.getElementById('surface-toggle'); const cs = getComputedStyle(b); return { pressed: b.getAttribute('aria-pressed'), text: b.textContent, dark: document.getElementById('icon-browser').classList.contains('dark'), outline: cs.outlineColor + ' ' + cs.outlineStyle + ' ' + cs.outlineWidth, browserBg: getComputedStyle(document.getElementById('icon-browser')).backgroundColor, btnBg: cs.backgroundColor, btnColor: cs.color, btnBorder: cs.borderColor }; });
  await p.locator('#icon-browser').screenshot({ path: path.join(SHOTS, 'icons-dark-toggle.png') });
  // Text contrast inside the dark library.
  out.darkContrast = await p.evaluate(() => {
    const lum = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); const [r, g, b] = m[1].split(',').map(Number); const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
    const bgOf = (el) => { for (let e = el; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor; const a = c.match(/rgba?\(([^)]+)\)/)[1].split(',').map(Number); if (a.length < 4 || a[3] > 0.5) return c; } return 'rgb(255,255,255)'; };
    const res = {};
    for (const el of document.querySelectorAll('#icon-browser *')) {
      if (!el.childNodes.length || ![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
      const cs = getComputedStyle(el); const fg = cs.color, bg = bgOf(el);
      const L1 = lum(fg), L2 = lum(bg); const ratio = ((Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05)).toFixed(2);
      const key = fg + ' on ' + bg + ' = ' + ratio + ' @' + cs.fontSize; res[key] = (res[key] || 0) + 1;
    }
    return res;
  });
  // Icon graphics on dark: stroke colors used.
  out.darkIconColors = await p.evaluate(() => { const c = {}; document.querySelectorAll('#icon-browser .icon-tile svg').forEach((s) => { const cs = getComputedStyle(s); c[cs.color] = (c[cs.color] || 0) + 1; }); return c; });
  await t.click();
  // Icon search empty state.
  await p.fill('#icon-search', 'zzzz'); await p.waitForTimeout(100);
  out.searchEmpty = await p.evaluate(() => ({ results: document.getElementById('icon-results').textContent, emptyShown: !document.getElementById('icon-empty').hidden, emptyText: document.getElementById('icon-empty').textContent, emptyLive: document.getElementById('icon-empty').getAttribute('aria-live') }));
  await p.fill('#icon-search', 'vote'); await p.waitForTimeout(100);
  out.searchVote = await p.evaluate(() => document.getElementById('icon-results').textContent);
  await p.fill('#icon-search', '');
  out.searchLabel = await p.locator('#icon-search').ariaSnapshot();
  await p.selectOption('#icon-size', '16'); await p.waitForTimeout(100);
  out.size16 = await p.evaluate(() => { const s = document.querySelector('.icon-tile svg'); const r = s.getBoundingClientRect(); return { w: r.width, h: r.height, vb: s.getAttribute('viewBox') }; });
  // Composer: change selects and read decode, warning, live regions.
  out.composerLive = await p.evaluate(() => ({ grid: document.getElementById('c-grid').getAttribute('aria-live'), decode: document.getElementById('c-decode').getAttribute('aria-live'), warn: document.getElementById('c-warn').getAttribute('aria-live'), warnRole: document.getElementById('c-warn').getAttribute('role') }));
  await p.selectOption('#c-stage', '9'); await p.selectOption('#c-type', 'step'); await p.waitForTimeout(100);
  out.composerConflict = await p.evaluate(() => ({ decode: document.getElementById('c-decode').textContent, warn: document.getElementById('c-warn').textContent, warnColor: getComputedStyle(document.getElementById('c-warn')).color, warnSize: getComputedStyle(document.getElementById('c-warn')).fontSize, svgLabel: document.querySelector('#c-grid svg').getAttribute('aria-label') }));
  await p.locator('#composer').screenshot({ path: path.join(SHOTS, 'composer-conflict.png') });
  await p.click('#c-reset');
  out.composerReset = await p.evaluate(() => document.getElementById('c-decode').textContent);
  // Standards details: keyboard toggling.
  const s = p.locator('#standards summary').first();
  await s.scrollIntoViewIfNeeded(); await s.focus();
  out.detailsBefore = await p.evaluate(() => document.querySelector('#standards details').open);
  await p.keyboard.press('Enter');
  out.detailsAfterEnter = await p.evaluate(() => document.querySelector('#standards details').open);
  await p.keyboard.press('Space');
  out.detailsAfterSpace = await p.evaluate(() => document.querySelector('#standards details').open);
  await p.context().close();
  return out;
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const data = {};
  data.reader1440 = await readerTests(browser, 1440, 900);
  data.reader390 = await readerTests(browser, 390, 844);
  data.motion = await motionTests(browser);
  data.controls = await controlTests(browser);
  fs.writeFileSync(path.join(OUT, '20261020_UX-Interaction-Data.json'), JSON.stringify(data, null, 1));
  await browser.close();
  console.log('done');
})();
