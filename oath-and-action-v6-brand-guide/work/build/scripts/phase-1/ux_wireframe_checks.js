// Phase 1 UX checks on the navigation and template wireframes.
// Usage: node ux_wireframe_checks.js <project-root> [scratch-dir]
// Runs axe-core and a scripted keyboard pass on the guide shell wireframe and on the Gate 1 board,
// saves stills for the board, and writes work/boards/phase-1/navigation/20261021_Wireframe-Check-Results.json.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { launch, launchWithFontSize, newPage, settle } = require('./ux_lib.js');

const ROOT = path.resolve(process.argv[2] || '.');
const SCRATCH = path.resolve(process.argv[3] || fs.mkdtempSync(path.join(os.tmpdir(), 'oa-ux-')));
const NAV = path.join(ROOT, 'work', 'boards', 'phase-1', 'navigation');
const SHELL = 'file://' + path.join(NAV, '20261021_Guide-Shell-Wireframe.html');
const BOARD = 'file://' + path.join(ROOT, 'work', 'boards', '20261021_Navigation-And-Template-Wireframes.html');
const AXE = fs.readFileSync(path.join(ROOT, 'work', 'build', 'node_modules', 'axe-core', 'axe.min.js'), 'utf8');
const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'];
fs.mkdirSync(SCRATCH, { recursive: true });

const R = { date: '2026-10-21', axe: {}, keyboard: {}, layout: {}, notes: [] };
const wait = (p, ms) => p.waitForTimeout(ms);

async function axe(page, label) {
  if (!(await page.evaluate(() => !!window.axe))) await page.addScriptTag({ content: AXE });
  const res = await page.evaluate(async (tags) => {
    const r = await window.axe.run(document, { runOnly: { type: 'tag', values: tags } });
    const pack = (v) => ({ id: v.id, impact: v.impact, wcag: v.tags.filter((t) => /^wcag\d/.test(t)), nodes: v.nodes.length, targets: v.nodes.slice(0, 6).map((n) => n.target.join(' ')), summary: v.nodes[0] ? v.nodes[0].failureSummary : '' });
    return { version: window.axe.version, violations: r.violations.map(pack), incomplete: r.incomplete.map(pack), passes: r.passes.length };
  }, TAGS);
  R.axe[label] = res;
  return res;
}

const active = (p) => p.evaluate(() => {
  const a = document.activeElement;
  if (!a || a === document.body) return { tag: a ? 'body' : null };
  const r = a.getBoundingClientRect(), cs = getComputedStyle(a);
  const head = document.querySelector('.masthead');
  const hb = head && getComputedStyle(head).position === 'sticky' ? head.getBoundingClientRect().bottom : 0;
  const inHead = !!a.closest('.masthead'), inDialog = !!a.closest('dialog');
  // Hit-test five points on the focused element: hidden at all of them is "fully", at some is "partly" (WCAG 2.4.11 and 2.4.12).
  // Points come from each line box, so a link that wraps is tested where its text is. Points outside the viewport are skipped.
  const boxes = [...a.getClientRects()].slice(0, 3);
  const pts = [];
  boxes.forEach((b) => [[.5, .5], [.15, .25], [.85, .25], [.15, .75], [.85, .75]].forEach(([fx, fy]) => pts.push([b.left + b.width * fx, b.top + b.height * fy])));
  const inView = pts.filter(([x, y]) => x >= 0 && y >= 0 && x < innerWidth && y < innerHeight);
  const seen = inView.filter(([x, y]) => { const t = document.elementFromPoint(x, y); return t && (t === a || a.contains(t) || (t.closest && t.closest('label') && t.closest('label').contains(a))); }).length;
  let obscured = r.width <= 1 || !inView.length ? 'n/a' : (seen === 0 ? 'fully' : (seen < inView.length ? 'partly' : 'no'));
  if (a.tagName === 'IFRAME') obscured = 'n/a';
  return {
    tag: a.tagName.toLowerCase(), id: a.id || null, cls: a.className && a.className.baseVal === undefined ? a.className : '',
    name: (a.getAttribute('aria-label') || a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 70),
    current: a.getAttribute('aria-current'), x: Math.round(r.left), y: Math.round(r.top), pageY: Math.round(r.top + scrollY),
    w: Math.round(r.width), h: Math.round(r.height), outlineStyle: cs.outlineStyle, outlineWidth: parseFloat(cs.outlineWidth),
    inViewport: r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth, obscured, inHead, inDialog,
    inMain: !!a.closest('main'), inRail: !!a.closest('.rail'),
  };
});

// Contrast of every visible text element against its composited background, with the WCAG formula.
// Gradient grounds (the striped placeholders) are tested against their darkest stripe.
async function contrastAudit(page, label) {
  const res = await page.evaluate(() => {
    const parse = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
    const over = (top, bot) => ({ r: top.r * top.a + bot.r * (1 - top.a), g: top.g * top.a + bot.g * (1 - top.a), b: top.b * top.a + bot.b * (1 - top.a), a: 1 });
    const L = (c) => { const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
    const ratio = (x, y) => { const a = L(x), b = L(y); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); };
    const bgOf = (el) => {
      const stack = []; let e = el;
      while (e && e.nodeType === 1) {
        const cs = getComputedStyle(e);
        const c = parse(cs.backgroundColor);
        if (/gradient/.test(cs.backgroundImage)) { const m = cs.backgroundImage.match(/rgba?\([^)]+\)/g) || []; m.map(parse).filter((x) => x && x.a > 0).forEach((x) => stack.push(x)); }
        if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break; }
        if (e.tagName === 'DIALOG' && e.open) break;
        e = e.parentElement;
      }
      let base = { r: 255, g: 255, b: 255, a: 1 };
      for (let i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
      return base;
    };
    const out = { checked: 0, failures: [], minSmall: 99, minLarge: 99 };
    const els = [...document.querySelectorAll('body *')].filter((e) => !e.closest('svg') && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()));
    for (const e of els) {
      const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
      if (!r.width || !r.height || cs.visibility === 'hidden' || /inset\(50%\)/.test(cs.clipPath) || e.closest('dialog:not([open])') || e.closest('[hidden]')) continue;
      let hidden = false; for (let p = e; p; p = p.parentElement) { const c = getComputedStyle(p); if (c.display === 'none' || /inset\(50%\)/.test(c.clipPath)) { hidden = true; break; } }
      if (hidden) continue;
      const fg = parse(cs.color); const bg = bgOf(e);
      const col = fg.a < 1 ? over(fg, bg) : fg;
      const ra = ratio(col, bg);
      const px = parseFloat(cs.fontSize), w = parseInt(cs.fontWeight, 10);
      const large = px >= 24 || (px >= 18.66 && w >= 700);
      out.checked++;
      if (large) out.minLarge = Math.min(out.minLarge, ra); else out.minSmall = Math.min(out.minSmall, ra);
      if (ra < (large ? 3 : 4.5)) out.failures.push({ text: e.textContent.trim().slice(0, 40), ratio: +ra.toFixed(2), px, large });
    }
    out.minSmall = +out.minSmall.toFixed(2); out.minLarge = +out.minLarge.toFixed(2);
    out.under13px = els.filter((e) => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); if (!r.width || e.closest('dialog:not([open])') || /inset\(50%\)/.test(cs.clipPath)) return false; for (let p = e; p; p = p.parentElement) if (getComputedStyle(p).display === 'none') return false; return parseFloat(cs.fontSize) < 13; }).map((e) => e.textContent.trim().slice(0, 30) + ' ' + getComputedStyle(e).fontSize);
    return out;
  });
  R.contrast = R.contrast || {};
  R.contrast[label] = res;
}

async function tabPass(page, max, stopWhen) {
  const stops = [];
  for (let i = 0; i < max; i++) {
    await page.keyboard.press('Tab');
    const a = await active(page);
    if (stopWhen && stopWhen(a, stops)) break;
    stops.push(a);
  }
  return stops;
}

function summarizeStops(stops) {
  const real = stops.filter((s) => s.tag && s.tag !== 'body');
  const noRing = real.filter((s) => !(s.outlineStyle !== 'none' && s.outlineWidth >= 2) && s.tag !== 'iframe');
  const obscured = real.filter((s) => s.obscured !== 'no' && s.obscured !== 'n/a');
  const off = real.filter((s) => !s.inViewport);
  // Order: within main, page position should not jump back up by more than 60 px, except into the right-hand chapter list.
  let back = [];
  const mainStops = real.filter((s) => s.inMain);
  for (let i = 1; i < mainStops.length; i++) {
    const a = mainStops[i - 1], b = mainStops[i];
    if (b.pageY < a.pageY - 60 && !(b.x > a.x + 200)) back.push({ from: a.name, to: b.name, dy: b.pageY - a.pageY });
  }
  return { stops: real.length, withoutVisibleRing: noRing.map((s) => s.name || s.tag), obscured: obscured.map((s) => ({ name: s.name, how: s.obscured })), outsideViewport: off.map((s) => s.name), backwardJumps: back };
}

async function shellChecks(browser) {
  const out = {};
  for (const [w, h] of [[1440, 900], [390, 844], [360, 780]]) {
    const k = `shell-${w}`;
    const { ctx, page } = await newPage(browser, ROOT, { width: w, height: h, clipboard: true });
    const errors = []; page.on('pageerror', (e) => errors.push(e.message));
    await page.goto(SHELL); await settle(page);
    await axe(page, `${k}-top`);
    await contrastAudit(page, `${k}-top`);
    const kb = {};

    // Full Tab pass from the top until focus wraps back to the first skip link.
    const stops = await tabPass(page, 700, (a, s) => s.length > 2 && a.cls === 'skip' && a.name === 'Skip to main content');
    kb.firstStops = stops.slice(0, 6).map((s) => s.name);
    kb.tabPass = summarizeStops(stops);

    // Skip links.
    await page.goto(SHELL); await settle(page);
    await page.keyboard.press('Tab');
    const s1 = await active(page);
    await page.keyboard.press('Enter'); await wait(page, 250);
    const afterS1 = await active(page);
    await page.keyboard.press('Tab');
    const afterS1Tab = await active(page);
    await page.goto(SHELL + '?r=1'); await settle(page);
    await page.keyboard.press('Tab'); await page.keyboard.press('Tab');
    const s2 = await active(page);
    await page.keyboard.press('Enter'); await wait(page, 300);
    const afterS2 = await active(page);
    kb.skip = {
      first: { name: s1.name, visible: s1.w > 1 && s1.inViewport, lands: afterS1.id, nextTabInMain: afterS1Tab.inMain },
      second: { name: s2.name, visible: s2.w > 1 && s2.inViewport, lands: afterS2.id },
    };

    // Headings and landmarks.
    kb.outline = await page.evaluate(() => {
      const hs = [...document.querySelectorAll('main h1, main h2, main h3')].map((h) => ({ l: +h.tagName[1], t: h.textContent.replace(/\s+/g, ' ').trim() }));
      const chapterH2 = [...document.querySelectorAll('section.chapter > h2, section.chapter .chapter-head > h2')].map((h) => h.textContent.replace(/\s+/g, ' ').trim());
      const skips = []; for (let i = 1; i < hs.length; i++) if (hs[i].l > hs[i - 1].l + 1) skips.push(hs[i - 1].t + ' -> ' + hs[i].t);
      return { h1: hs.filter((h) => h.l === 1).length, h2: hs.filter((h) => h.l === 2).length, h3: hs.filter((h) => h.l === 3).length, chapterH2Pattern: chapterH2.filter((t) => /^\d\d \S/.test(t)).length, chapterH2: chapterH2.length, levelSkips: skips, sample: chapterH2.slice(3, 6) };
    });
    kb.landmarks = (await page.locator('body').ariaSnapshot()).split('\n').filter((l) => /^\s*- (banner|navigation|main|contentinfo|region|complementary)\b/.test(l)).map((l) => l.trim());

    // Focusing masthead controls (and the desktop rail) must not scroll the page.
    await page.goto(SHELL + '?at=color&r=3'); await settle(page); await wait(page, 200);
    kb.stickyFocusJumps = await page.evaluate(() => {
      const els = [...document.querySelectorAll('.masthead a, .masthead button, .rail a')].filter((e) => e.getBoundingClientRect().width > 0);
      const jumps = [];
      for (const e of els) { const y = scrollY; e.focus(); if (Math.abs(scrollY - y) > 1) { jumps.push((e.textContent || '').trim().slice(0, 30) + ' ' + Math.round(scrollY - y)); window.scrollTo(0, y); } }
      return { checked: els.length, jumps };
    });

    if (w === 1440) {
      // Every chapter, part and the closing: activate its rail link by keyboard and check the markers and focus.
      const ids = await page.evaluate(() => [...document.querySelectorAll('.rail [data-loc]')].map((a) => a.getAttribute('data-loc')));
      const viaLink = [];
      for (const id of ids) {
        await page.focus(`.rail [data-loc="${id}"]`);
        await page.keyboard.press('Enter'); await wait(page, 350);
        viaLink.push(await page.evaluate((id) => {
          const cur = [...document.querySelectorAll('.rail [aria-current]')].map((a) => a.getAttribute('data-loc'));
          const sec = document.getElementById(id);
          const part = sec.getAttribute('data-part');
          const pcur = [...document.querySelectorAll('.partnav [aria-current]')].map((a) => a.getAttribute('data-part-link'));
          const a = document.activeElement, hb = document.querySelector('.masthead').getBoundingClientRect().bottom;
          const r = a.getBoundingClientRect();
          return { id, railCurrent: cur, partCurrent: pcur, expectPart: part || null, focus: a.id, focusClear: r.top >= hb, label: (document.querySelector(`.rail [data-loc="${id}"]`).textContent || '').replace(/\s+/g, ' ').trim() };
        }, id));
      }
      kb.currentMarkerViaRail = {
        targets: viaLink.length,
        ok: viaLink.filter((v) => v.railCurrent.length === 1 && v.railCurrent[0] === v.id && (v.id === 'start' || (v.partCurrent.length === 1 && v.partCurrent[0] === v.expectPart)) && v.focus && v.focusClear).length,
        failures: viaLink.filter((v) => !(v.railCurrent.length === 1 && v.railCurrent[0] === v.id && v.focus && v.focusClear)),
        startHasNoPart: viaLink.filter((v) => v.id === 'start').map((v) => v.partCurrent),
        names: viaLink.slice(0, 4).map((v) => v.label),
      };
      // The same, by scrolling, once the last link's pin has expired.
      await wait(page, 1000);
      const viaScroll = [];
      for (const id of ids.filter((i) => i !== 'start')) {
        await page.evaluate((id) => { const s = document.getElementById(id); const hb = document.querySelector('.masthead').getBoundingClientRect().height; window.scrollTo(0, s.getBoundingClientRect().top + scrollY - hb - 10); }, id);
        await wait(page, 120);
        viaScroll.push(await page.evaluate((id) => ({ id, cur: [...document.querySelectorAll('.rail [aria-current]')].map((a) => a.getAttribute('data-loc')) }), id));
      }
      kb.currentMarkerViaScroll = { targets: viaScroll.length, ok: viaScroll.filter((v) => v.cur.length === 1 && v.cur[0] === v.id).length, failures: viaScroll.filter((v) => !(v.cur.length === 1 && v.cur[0] === v.id)) };

      // Cross-reference and return link.
      await page.goto(SHELL + '#rule-05-2'); await settle(page); await wait(page, 200);
      await page.focus('#rule-05-2 a.xref[href="#type"]');
      await page.keyboard.press('Enter'); await wait(page, 350);
      const landed = await active(page);
      const ret = await page.evaluate(() => { const p = document.querySelector('#type .return'); return { hidden: p.hidden, text: p.textContent }; });
      await page.keyboard.press('Tab');
      const onReturn = await active(page);
      await page.keyboard.press('Enter'); await wait(page, 350);
      const back = await page.evaluate(() => (document.activeElement.textContent || '').replace(/\s+/g, ' ').trim());
      const retAfter = await page.evaluate(() => document.querySelector('#type .return').hidden);
      kb.crossReference = { landedOn: landed.id, returnShown: !ret.hidden, returnText: ret.text, tabReachesReturn: /^Return to/.test(onReturn.name), returnLandsOn: back, returnHiddenAfter: retAfter, hash: await page.evaluate(() => location.hash) };

      // Back to contents from the end of 05 Color.
      await page.focus('#color .chapnav .to-contents');
      await page.keyboard.press('Enter'); await wait(page, 300);
      kb.backToContents = (await active(page)).id;

      // Copy: clipboard granted.
      await page.goto(SHELL + '#rule-05-2'); await settle(page);
      await page.focus('#rule-05-2 button.copy[data-copy="#121212"]');
      await page.keyboard.press('Enter'); await wait(page, 300);
      kb.copy = { status: await page.textContent('#status-05-2'), clipboard: await page.evaluate(() => navigator.clipboard.readText().catch((e) => 'read failed: ' + e.message)), focusStays: (await active(page)).name };

      // Download: enabled, then the disabled one.
      await page.focus('#color-specs button.dl[data-kind="css"]');
      const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 4000 }), page.keyboard.press('Enter')]);
      const saved = path.join(SCRATCH, dl.suggestedFilename()); await dl.saveAs(saved);
      const txt = fs.readFileSync(saved, 'utf8');
      kb.download = { file: dl.suggestedFilename(), bytes: txt.length, hasAllSeven: (txt.match(/--oa-color-[a-z-]+: #[0-9A-F]{6};/g) || []).length, status: await page.textContent('#status-dl') };
      await page.focus('#color-specs button.dl[aria-disabled="true"]');
      let fired = false; page.once('download', () => { fired = true; });
      await page.keyboard.press('Enter'); await wait(page, 1000);
      kb.disabledDownload = { fired, status: await page.textContent('#status-dl'), stillFocused: /ASE/.test((await active(page)).name), describedBy: await page.getAttribute('#color-specs button.dl[aria-disabled="true"]', 'aria-describedby') };
    } else {
      // Phone menu.
      await page.goto(SHELL + '?at=color'); await settle(page); await wait(page, 200);
      const first = await tabPass(page, 4);
      await page.goto(SHELL + '?at=color&r=2'); await settle(page); await wait(page, 200);
      await page.focus('#menubtn');
      const btn = await page.evaluate(() => { const b = document.getElementById('menubtn'); const r = b.getBoundingClientRect(); return { w: Math.round(r.width), h: Math.round(r.height), haspopup: b.getAttribute('aria-haspopup'), where: document.getElementById('where').textContent }; });
      await page.keyboard.press('Enter'); await wait(page, 300);
      const opened = await active(page);
      await page.screenshot({ path: path.join(NAV, `20261021_Nav-${w}-Menu.png`) });
      const menu = await page.evaluate(() => {
        const d = document.getElementById('menu'), sc = d.querySelector('.menu-scroll');
        const links = [...d.querySelectorAll('nav a')];
        const chapterLinks = links.filter((a) => /^\d\d /.test(a.textContent.replace(/\s+/g, ' ').trim()));
        const short = links.filter((a) => a.getBoundingClientRect().height < 44).map((a) => a.textContent.trim());
        const dr = d.getBoundingClientRect();
        const outside = links.filter((a) => { const r = a.getBoundingClientRect(); return r.left < dr.left - 1 || r.right > dr.right + 1; }).map((a) => a.textContent.trim());
        return { open: d.open, modal: d.matches(':modal'), name: document.getElementById(d.getAttribute('aria-labelledby')).textContent, links: links.length, chapterLinks: chapterLinks.length, partLinks: d.querySelectorAll('nav a.menu-partlink').length, under44: short, outsideWidth: outside, sideScroll: sc.scrollWidth > sc.clientWidth, where: document.getElementById('menu-where-text').textContent, current: [...d.querySelectorAll('[aria-current]')].map((a) => a.textContent.replace(/\s+/g, ' ').trim()) };
      });
      const inside = await tabPass(page, 45);
      const back = await tabPass(page, 0);
      // Native modal dialogs let focus pass once to the browser's own controls (recorded as body); page content behind must stay unreachable.
      const leftDialog = inside.filter((s) => !s.inDialog && s.tag !== 'body').map((s) => s.name || s.tag);
      const toBrowser = inside.filter((s) => s.tag === 'body').length;
      const shiftStops = [];
      for (let i = 0; i < 6; i++) { await page.keyboard.press('Shift+Tab'); shiftStops.push(await active(page)); }
      await axe(page, `${k}-menu-open`);
      await contrastAudit(page, `${k}-menu-open`);
      await page.keyboard.press('Escape'); await wait(page, 250);
      const afterEsc = await active(page);
      const closed = await page.evaluate(() => !document.getElementById('menu').open);
      // Choose a chapter from the menu.
      await page.click('#menubtn'); await wait(page, 250);
      await page.focus('#menu a[data-loc="atlas"]');
      await page.keyboard.press('Enter'); await wait(page, 400);
      const chosen = await page.evaluate(() => ({ open: document.getElementById('menu').open, hash: location.hash, focus: document.activeElement.id, where: document.getElementById('where').textContent, current: [...document.querySelectorAll('#menu [aria-current]')].map((a) => a.getAttribute('data-loc')) }));
      // Close button.
      await page.click('#menubtn'); await wait(page, 200);
      await page.focus('#menuclose'); await page.keyboard.press('Enter'); await wait(page, 200);
      const afterClose = await active(page);
      kb.menu = { firstStops: first.map((s) => s.name), button: btn, focusOnOpen: { name: opened.name, current: opened.current, inDialog: opened.inDialog }, dialog: menu, tabStaysInside: leftDialog.length === 0, leftDialog, shiftTabInside: shiftStops.every((s) => s.inDialog || s.tag === 'body'), passesToBrowserChrome: toBrowser, escapeCloses: closed, focusAfterEscape: afterEsc.id, chooseChapter: chosen, focusAfterClose: afterClose.id };
      kb.menu.tabInsideRing = inside.filter((s) => s.tag !== 'body' && !(s.outlineStyle !== 'none' && s.outlineWidth >= 2)).map((s) => s.name);
      // Header still at true width, menu closed, at 05 Color.
      await page.goto(SHELL + '?at=color'); await settle(page); await wait(page, 200);
      await axe(page, `${k}-color`);
    }

    // Targets under 24 by 24 CSS px, with the inline-link exception noted.
    kb.targets = await page.evaluate(() => {
      const els = [...document.querySelectorAll('a[href], button, select, input, [tabindex]:not([tabindex="-1"])')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden' && !e.closest('dialog:not([open])'); });
      const small = els.filter((e) => { const r = e.getBoundingClientRect(); return r.width < 24 || r.height < 24; });
      const inline = (e) => e.tagName === 'A' && e.parentElement && /^(P|LI|FIGCAPTION|SPAN)$/.test(e.parentElement.tagName) && e.parentElement.textContent.trim().length > e.textContent.trim().length + 3;
      return { checked: els.length, under24: small.length, under24NotInline: small.filter((e) => !inline(e)).map((e) => ({ name: e.textContent.trim().slice(0, 40), w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height) })) };
    });
    kb.errors = errors;
    out[k] = kb;
    await ctx.close();
  }
  R.keyboard.shell = out;
}

async function layoutChecks(browser) {
  const L = {};
  // Reflow at 320, and no sideways scroll at the board widths.
  for (const [w, h] of [[320, 640], [360, 780], [390, 844], [1024, 768], [1440, 900]]) {
    const { ctx, page } = await newPage(browser, ROOT, { width: w, height: h });
    await page.goto(SHELL + '?at=color'); await settle(page);
    L[`shell-${w}`] = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const over = [...document.querySelectorAll('main *, header *')].filter((e) => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > vw + 1 && !e.closest('.rail') && getComputedStyle(e).position !== 'fixed'; }).slice(0, 8).map((e) => e.tagName.toLowerCase() + '.' + (e.className || '') + ' ' + Math.round(e.getBoundingClientRect().right));
      return { scrollWidth: document.documentElement.scrollWidth, viewport: vw, overflowing: over, railShown: getComputedStyle(document.querySelector('.rail')).display !== 'none', menuButtonShown: getComputedStyle(document.getElementById('menubtn')).display !== 'none' };
    });
    if (w === 320) await axe(page, 'shell-320-color');
    if (w === 1024) await axe(page, 'shell-1024-color');
    await ctx.close();
  }
  // Page zoom at 200 percent: a 1440 by 900 window seen as 720 by 450 CSS px.
  {
    const { ctx, page } = await newPage(browser, ROOT, { width: 720, height: 450, dsf: 2 });
    await page.goto(SHELL + '?at=color'); await settle(page);
    L['shell-zoom200'] = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, viewport: document.documentElement.clientWidth, menuButtonShown: getComputedStyle(document.getElementById('menubtn')).display !== 'none', headerHeight: Math.round(document.querySelector('.masthead').getBoundingClientRect().height) }));
    await ctx.close();
  }
  // Reduced motion and forced colors on the shell.
  {
    const { ctx, page } = await newPage(browser, ROOT, { width: 1440, height: 900, forced: true });
    await page.goto(SHELL + '?at=color'); await settle(page);
    L['shell-forced-colors'] = await page.evaluate(() => {
      const cur = document.querySelector('.rail [aria-current]'), other = document.querySelector('.rail [data-loc="type"]');
      const pc = document.querySelector('.partnav [aria-current]');
      const s = (e) => { const c = getComputedStyle(e); return { borderLeft: c.borderLeftWidth + ' ' + c.borderLeftStyle + ' ' + c.borderLeftColor, weight: c.fontWeight }; };
      return { forced: matchMedia('(forced-colors: active)').matches, current: s(cur), other: s(other), partUnderline: pc ? getComputedStyle(pc).textDecorationLine : null };
    });
    await page.screenshot({ path: path.join(NAV, '20261021_Nav-1440-Forced-Colors.png') });
    await ctx.close();
  }
  R.layout = L;
}

async function textSizeCheck() {
  // Reader text size set to 32 px in Chromium's preferences, which scales rem and em breakpoints together.
  const dir = path.join(SCRATCH, 'profile-32');
  const ctx = await launchWithFontSize(ROOT, 32, dir);
  const page = await ctx.newPage();
  const res = {};
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    await page.setViewportSize({ width: w, height: h });
    await page.goto(SHELL + '?at=color'); await settle(page); await wait(page, 200);
    res[w] = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const clipped = [...document.querySelectorAll('main *, header *')].filter((e) => { const c = getComputedStyle(e); return (c.overflow === 'hidden' || c.overflowX === 'hidden' || c.textOverflow === 'ellipsis') && e.scrollWidth > e.clientWidth + 1 && e.clientWidth > 0 && !e.classList.contains('vh') && !e.classList.contains('skip') && !/inset\(50%\)/.test(c.clipPath) && !(e.closest && e.closest('thead')); }).map((e) => (e.id || e.className) + ': ' + e.textContent.trim().slice(0, 30));
      return { rootFontSize: getComputedStyle(document.documentElement).fontSize, scrollWidth: document.documentElement.scrollWidth, viewport: vw, railShown: getComputedStyle(document.querySelector('.rail')).display !== 'none', clipped };
    });
    if (w === 1440) await page.screenshot({ path: path.join(NAV, '20261021_Nav-1440-Text-200.png') });
  }
  await ctx.close();
  R.layout['shell-text200'] = res;
}

async function boardChecks(browser) {
  const out = {};
  for (const [w, h] of [[1440, 900], [390, 844], [360, 780]]) {
    const k = `board-${w}`;
    const { ctx, page } = await newPage(browser, ROOT, { width: w, height: h, clipboard: true });
    const errors = []; page.on('pageerror', (e) => errors.push(e.message));
    await page.goto(BOARD); await settle(page); await wait(page, 300);
    await axe(page, `${k}`);
    await contrastAudit(page, `${k}`);
    const kb = {};
    kb.scroll = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, viewport: document.documentElement.clientWidth }));
    kb.frames = await page.evaluate(() => [...document.querySelectorAll('iframe')].map((f) => ({ title: f.title, w: f.getBoundingClientRect().width })));

    // Tab order through the board's own controls, with the frames taken out (the shell is tested on its own).
    await page.evaluate(() => document.querySelectorAll('iframe').forEach((f) => f.remove()));
    const stops = await tabPass(page, 400, (a, s) => s.length > 2 && a.name === 'Skip to main content');
    kb.tabPass = summarizeStops(stops);
    kb.firstStops = stops.slice(0, 4).map((s) => s.name);
    await page.goto(BOARD); await settle(page); await wait(page, 300);

    // Fit toggle keeps its label and flips aria-pressed.
    if (w === 1440) {
      await page.focus('#fit-toggle'); await page.keyboard.press('Enter'); await wait(page, 100);
      kb.fitToggle = await page.evaluate(() => { const b = document.getElementById('fit-toggle'); return { label: b.textContent.trim(), pressed: b.getAttribute('aria-pressed'), scale: document.getElementById('wide-holder').style.transform }; });
      await page.keyboard.press('Enter');
    }

    // 6.1 Report reader.
    const thumb = page.locator('#thumbs button[data-page="5"]');
    await thumb.focus();
    const thumbName = await thumb.evaluate((b) => ({ visible: b.querySelector('span:not(.vh):not(.thumb-page)').textContent, name: b.textContent.replace(/\s+/g, ' ').trim() }));
    await page.keyboard.press('Enter'); await wait(page, 250);
    const rd = {};
    rd.thumbName = thumbName;
    rd.dialogName = (await page.locator('#reader').ariaSnapshot()).split('\n')[0];
    rd.focusOnOpen = (await active(page)).id;
    const title = () => page.textContent('#reader-title');
    await page.keyboard.press('ArrowRight'); await wait(page, 80); rd.arrowOnTitle = await title();
    await page.focus('#rd-next'); await page.keyboard.press('ArrowRight'); await wait(page, 80); rd.arrowOnNext = await title();
    await page.keyboard.press('Enter'); await wait(page, 80); rd.enterOnNext = await title();
    await page.focus('#rd-zoom'); await page.keyboard.press('ArrowRight'); await wait(page, 80);
    rd.arrowRightOnZoom = { title: await title(), zoom: await page.inputValue('#rd-zoom') };
    await page.keyboard.press('ArrowDown'); await wait(page, 120);
    rd.arrowDownOnZoom = { title: await title(), zoom: await page.inputValue('#rd-zoom') };
    await page.selectOption('#rd-zoom', 'full'); await wait(page, 120);
    await page.focus('#rd-page');
    for (let i = 0; i < 6; i++) await page.keyboard.press('ArrowRight');
    await wait(page, 150);
    rd.arrowInPage = { title: await title(), scrollLeft: await page.evaluate(() => document.getElementById('rd-page').scrollLeft), canScroll: await page.evaluate(() => { const p = document.getElementById('rd-page'); return p.scrollWidth > p.clientWidth; }) };
    await page.focus('#rd-next');
    for (let i = 0; i < 6; i++) { await page.keyboard.press('Enter'); await wait(page, 40); }
    rd.atLast = { title: await title(), focus: (await active(page)).id, nextDisabled: await page.getAttribute('#rd-next', 'aria-disabled'), status: await page.textContent('#rd-status') };
    await page.keyboard.press('Enter'); await wait(page, 80);
    rd.pressAtLast = { title: await title(), focus: (await active(page)).id, status: await page.textContent('#rd-status') };
    await page.keyboard.press('Home'); await wait(page, 80);
    rd.home = await title();
    rd.prevAtFirst = await page.getAttribute('#rd-prev', 'aria-disabled');
    const inside = await tabPass(page, 12);
    rd.tabStaysInside = inside.every((s) => s.inDialog || s.tag === 'body');
    rd.passesToBrowserChrome = inside.filter((s) => s.tag === 'body').length;
    rd.tabStops = inside.slice(0, 7).map((s) => s.id || s.name);
    await axe(page, `${k}-reader-open`);
    await contrastAudit(page, `${k}-reader-open`);
    if (w === 390) await page.screenshot({ path: path.join(NAV, '20261021_Reader-390.png') });
    await page.keyboard.press('Escape'); await wait(page, 200);
    rd.afterEscape = { open: await page.evaluate(() => document.getElementById('reader').open), focus: await page.evaluate(() => document.activeElement.getAttribute('data-page')) };
    kb.reader = rd;

    if (w === 1440) {
      // 6.2 Copy and download.
      await page.focus('#copy-demo button.copy[data-copy="#E63946"]'); await page.keyboard.press('Enter'); await wait(page, 250);
      const cp = { status: await page.textContent('#copy-status'), clipboard: await page.evaluate(() => navigator.clipboard.readText().catch((e) => 'read failed: ' + e.message)) };
      await page.focus('#copy-demo button.dl[data-kind="svg"]');
      const [dl] = await Promise.all([page.waitForEvent('download', { timeout: 4000 }), page.keyboard.press('Enter')]);
      const f = path.join(SCRATCH, dl.suggestedFilename()); await dl.saveAs(f);
      const svg = fs.readFileSync(f, 'utf8');
      cp.svg = { file: dl.suggestedFilename(), bytes: svg.length, hasTitle: /<title[ >]/.test(svg), hasDesc: /<desc[ >]/.test(svg), id: (svg.match(/id="(oa-[a-z-]+)"/) || [])[1], circles: (svg.match(/<circle/g) || []).length, path: f };
      cp.svgParses = await page.evaluate((s) => { const d = new DOMParser().parseFromString(s, 'image/svg+xml'); return !d.querySelector('parsererror') && d.documentElement.tagName === 'svg'; }, svg);
      cp.statusAfterDownload = await page.textContent('#copy-status');
      await page.focus('#copy-demo button.dl[aria-disabled="true"]');
      let fired = false; page.once('download', () => { fired = true; });
      await page.keyboard.press('Enter'); await wait(page, 1000);
      cp.disabled = { fired, status: await page.textContent('#copy-status'), focusStays: /PNG/.test((await active(page)).name) };
      kb.copyDownload = cp;

      // 6.3 Pair checker, by keyboard.
      const pr = {};
      pr.initial = await page.textContent('#pair-status');
      await page.focus('#pair-fg'); await page.keyboard.press('ArrowDown'); await wait(page, 120);
      pr.afterArrowDown = { value: await page.inputValue('#pair-fg'), status: await page.textContent('#pair-status') };
      await page.selectOption('#pair-fg', '2'); await wait(page, 80);
      pr.stoneOnNewsprint = await page.textContent('#pair-status');
      await page.focus('#pair-surface input[value="0"]'); await page.keyboard.press('ArrowRight'); await wait(page, 100);
      pr.radioArrow = await page.textContent('#pair-status');
      await page.selectOption('#pair-size', '13'); await wait(page, 80);
      pr.size13 = await page.textContent('#pair-status');
      pr.specimenName = await page.getAttribute('#pair-svg', 'aria-label');
      pr.matchesRendered = await page.evaluate(() => {
        const L = (h) => { const c = [1, 3, 5].map((i) => { const v = parseInt(h.substr(i, 2), 16) / 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
        const a = document.getElementById('pair-text').getAttribute('fill'), b = document.getElementById('pair-bg').getAttribute('fill');
        const r = (Math.max(L(a), L(b)) + 0.05) / (Math.min(L(a), L(b)) + 0.05);
        return { fill: a, bg: b, ratio: r.toFixed(2), inStatus: document.getElementById('pair-status').textContent.includes(r.toFixed(2)) };
      });
      await page.focus('#pair-reset'); await page.keyboard.press('Enter'); await wait(page, 80);
      pr.reset = await page.textContent('#pair-status');
      kb.pairDemo = pr;

      // 6.4 Motion.
      const mvState = () => page.evaluate(() => ({ now: [...document.querySelectorAll('#mv-steps li')].findIndex((l) => l.classList.contains('now')) + 1, status: document.getElementById('mv-status').textContent, still: document.getElementById('mv-still').getAttribute('aria-pressed'), play: document.getElementById('mv-play').getAttribute('aria-disabled'), pause: document.getElementById('mv-pause').getAttribute('aria-disabled'), step: document.getElementById('mv-step').getAttribute('aria-disabled'), transition: getComputedStyle(document.getElementById('mv-marker')).transitionDuration, markerShown: getComputedStyle(document.getElementById('mv-marker')).display !== 'none' }));
      const mv = { initial: await mvState() };
      await page.focus('#mv-play'); await page.keyboard.press('Enter'); await wait(page, 2800);
      mv.afterPlay = await mvState();
      await page.focus('#mv-pause'); await page.keyboard.press('Enter'); await wait(page, 3000);
      mv.afterPause3s = await mvState();
      await page.focus('#mv-step'); await page.keyboard.press('Enter'); await wait(page, 100);
      await page.keyboard.press('Enter'); await wait(page, 100);
      mv.atEnd = await mvState();
      await page.keyboard.press('Enter'); await wait(page, 100);
      mv.stepAtEnd = await mvState();
      await page.focus('#mv-reset'); await page.keyboard.press('Enter'); await wait(page, 100);
      mv.afterReset = await mvState();
      await page.focus('#mv-still'); await page.keyboard.press('Enter'); await wait(page, 100);
      mv.stillOn = await mvState();
      kb.motion = mv;
    }
    kb.errors = errors;
    out[k] = kb;
    await ctx.close();
  }
  // Reduced motion on the board.
  {
    const { ctx, page } = await newPage(browser, ROOT, { width: 1440, height: 900, reduced: true });
    await page.goto(BOARD); await settle(page);
    out.reducedMotion = await page.evaluate(() => ({ still: document.getElementById('mv-still').getAttribute('aria-pressed'), status: document.getElementById('mv-status').textContent, transition: getComputedStyle(document.getElementById('mv-marker')).transitionDuration, markerShown: getComputedStyle(document.getElementById('mv-marker')).display !== 'none' }));
    await page.focus('#mv-play'); await page.keyboard.press('Enter'); await wait(page, 2700);
    out.reducedMotion.playStillWorks = await page.evaluate(() => [...document.querySelectorAll('#mv-steps li')].findIndex((l) => l.classList.contains('now')) + 1);
    await ctx.close();
  }
  R.keyboard.board = out;
}

async function stills(browser) {
  for (const [w, h, name] of [[1440, 900, '20261021_Color-Chapter-1440.jpg'], [360, 780, '20261021_Color-Chapter-360.jpg']]) {
    const { ctx, page } = await newPage(browser, ROOT, { width: w, height: h });
    await page.goto(SHELL); await settle(page);
    await page.addStyleTag({ content: '.masthead{position:static!important}.local-toc{position:static!important}' });
    await (await page.$('#color')).screenshot({ path: path.join(NAV, name), type: 'jpeg', quality: 72 });
    await ctx.close();
  }
}

(async () => {
  const browser = await launch();
  R.chromium = browser.version();
  await shellChecks(browser);
  await layoutChecks(browser);
  await boardChecks(browser);
  await stills(browser);
  await browser.close();
  await textSizeCheck();
  const outFile = path.join(NAV, '20261021_Wireframe-Check-Results.json');
  fs.writeFileSync(outFile, JSON.stringify(R, null, 1));
  const v = Object.fromEntries(Object.entries(R.axe).map(([k, x]) => [k, x.violations.map((y) => `${y.id}(${y.nodes})`).join(' ') || 'none']));
  console.log('axe violations:', JSON.stringify(v, null, 1));
  console.log('wrote', path.relative(ROOT, outFile));
})().catch((e) => { console.error(e); process.exit(1); });
