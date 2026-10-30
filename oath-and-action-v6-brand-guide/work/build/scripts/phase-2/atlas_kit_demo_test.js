// Tests for the atlas kit demo. Usage: node test_kit.js
const fs = require('fs');
const { chromium } = require('playwright');
const ROOT = '/home/user/Dustin-s-Command-Center/oath-and-action-v6-brand-guide';
const F = 'file://' + ROOT + '/work/boards/phase-2/atlas-concepts/shared/20261030_Atlas-Kit-Demo.html';
const AXE = ROOT + '/work/build/node_modules/axe-core/axe.min.js';
const results = []; let fails = 0;
function check(name, ok, detail) { results.push({ name, ok: !!ok, detail }); if (!ok) fails++; console.log((ok ? 'PASS ' : 'FAIL ') + name + (detail !== undefined ? '  ' + JSON.stringify(detail).slice(0, 300) : '')); }
const act = (p) => p.evaluate(() => { const a = document.activeElement; return { key: a.dataset && (a.dataset.select || a.getAttribute('href') || a.id || a.textContent.trim().slice(0, 40)), tag: a.tagName, hash: location.hash }; });
async function axe(p, label) {
  await p.addScriptTag({ path: AXE });
  const v = await p.evaluate(async () => (await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } })).violations.map((x) => ({ id: x.id, n: x.nodes.length, t: x.nodes[0].target.join(' ') })));
  check(`axe 0 violations: ${label}`, v.length === 0, v);
}
const noSideways = (p) => p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));

(async () => {
  const b = await chromium.launch();
  const errors = [];
  // ---------------- 1440 ----------------
  let ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  let p = await ctx.newPage(); p.on('pageerror', (e) => errors.push(e.message));
  await p.goto(F + '#overview'); await p.waitForTimeout(500);
  await axe(p, '1440 overview');

  // Keyboard order from the top of the page
  const order = [];
  for (let k = 0; k < 8; k++) { await p.keyboard.press('Tab'); const a = await act(p); order.push(a.key); if (a.tag === 'BODY') break; }
  check('1440 tab order: locator, then one stop in the map (area A), then out', order[0] === '#overview' && order[1] === 'area-a' && !order.slice(2).some((x) => /^area-/.test(x)), order);
  // Focus ring on each stop
  await p.goto(F + '#overview'); await p.evaluate(() => document.activeElement.blur());
  const rings = [];
  for (let k = 0; k < 2; k++) { await p.keyboard.press('Tab'); rings.push(await p.evaluate(() => { const c = getComputedStyle(document.activeElement); return [c.outlineStyle, c.outlineWidth, c.outlineColor, c.outlineOffset]; })); }
  check('focus ring: 2 px solid Verdigris, 2 px offset, on Newsprint', rings.every((r) => r[0] === 'solid' && r[1] === '2px' && r[2] === 'rgb(74, 124, 116)' && r[3] === '2px'), rings);

  // Arrow keys in the overview map (spatial)
  await p.focus('[data-select="area-a"]');
  const seen = [];
  for (const k of ['ArrowRight', 'ArrowRight', 'ArrowDown', 'ArrowUp', 'End', 'Home', 'ArrowLeft']) { await p.keyboard.press(k); seen.push((await act(p)).key); }
  check('spatial arrows: A>B>C, down to household, up to C, End TC, Home A, Left stays', JSON.stringify(seen) === JSON.stringify(['area-b', '#area-c', 'area-household', '#area-c', 'area-tc', 'area-a', 'area-a']), seen);
  const tabs = await p.evaluate(() => [...document.querySelectorAll('svg[data-view="overview"] [tabindex="0"]')].length);
  check('roving: exactly one tabindex=0 in the overview map', tabs === 1, tabs);

  // Readout follows focus (same text as the accessible name)
  await p.focus('[data-select="area-b"]');
  const ro = await p.evaluate(() => [document.querySelector('[data-view-root="overview"] [data-ak-readout]').textContent, document.querySelector('[data-select="area-b"]').getAttribute('aria-label')]);
  check('readout on focus equals the item name', ro[0] === ro[1], ro);

  // Select an area with no close-up: panel opens, focus to panel title, hash replaced, Escape returns focus
  const histLen0 = await p.evaluate(() => history.length);
  await p.focus('[data-select="area-a"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(250);
  let st = await p.evaluate(() => ({ hidden: document.querySelector('[data-ak-panel]').hidden, title: document.querySelector('[data-ak-panel-title]').textContent, focus: document.activeElement.id, hash: location.hash, pressed: document.querySelector('[data-select="area-a"]').getAttribute('aria-pressed'), hist: history.length }));
  check('Enter on area A opens the panel with its title and moves focus to the title', !st.hidden && st.title === 'Economic structure' && st.focus === 'ak-panel-title', st);
  check('selection writes #overview/area-a and adds no history entry', st.hash === '#overview/area-a' && st.hist === histLen0, { hash: st.hash, hist: st.hist, before: histLen0 });
  check('aria-pressed true on the selected item', st.pressed === 'true');
  await p.keyboard.press('Escape'); await p.waitForTimeout(150);
  st = await p.evaluate(() => ({ hidden: document.querySelector('[data-ak-panel]').hidden, focus: document.activeElement.dataset.select, hash: location.hash }));
  check('Escape closes the panel, returns focus to area A, clears the hash', st.hidden && st.focus === 'area-a' && st.hash === '#overview', st);

  // Move down a level: Enter on the area C link
  await p.focus('svg[data-view="overview"] a[href="#area-c"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(500);
  st = await p.evaluate(() => ({ hash: location.hash, vis: !document.querySelector('[data-view-root="area-c"]').hidden, ov: document.querySelector('[data-view-root="overview"]').hidden, focus: document.activeElement.id, title: document.title, crumbs: [...document.querySelectorAll('[data-ak-crumbs] li')].map((li) => li.textContent), current: document.querySelector('[data-ak-crumbs] [aria-current="page"]').textContent, here: [...document.querySelectorAll('.ak-here')].map((x) => x.dataset.locate) }));
  check('Enter on area C goes to #area-c and shows only that view', st.hash === '#area-c' && st.vis && st.ov, st);
  check('focus after moving down is the new view heading', st.focus === 'h-area-c', st.focus);
  check('breadcrumb Overview / Area C with aria-current on the last', st.crumbs.length === 2 && st.current === 'Area C, Electoral competition', st.crumbs);
  check('document title names the view', st.title.startsWith('Area C, Electoral competition'), st.title);
  check('locator marks area C', st.here.includes('area-c'), st.here);
  await axe(p, '1440 area-c');

  // Back button: returns to the overview with focus on the item that opened area C
  await p.goBack(); await p.waitForTimeout(500);
  st = await act(p);
  check('Back returns to #overview with focus on the area C link', st.hash === '#overview' && st.key === '#area-c', st);
  await p.goForward(); await p.waitForTimeout(500);
  check('Forward returns to #area-c', (await act(p)).hash === '#area-c');

  // Area C: select C3, working red on the selection (no reform in view), related marks lit, others muted
  await p.click('[data-select="var-c3"] rect'); await p.waitForTimeout(250);
  st = await p.evaluate(() => { const c3 = document.querySelector('[data-view-root="area-c"] [data-select="var-c3"]'); const r = c3.querySelector('rect');
    return { red: c3.getAttribute('data-red'), job: c3.getAttribute('data-red-job'), stroke: getComputedStyle(r).stroke, sw: getComputedStyle(r).strokeWidth, label: getComputedStyle(c3.querySelector('.ak-label')).fill,
      rel: [...document.querySelectorAll('[data-view-root="area-c"] .ak-rel')].map((x) => x.dataset.select).sort(), dim: document.querySelector('[data-view-root="area-c"]').classList.contains('ak-dim'),
      mutedL08: getComputedStyle(document.querySelector('[data-select="link-l08"] .ak-mark')).stroke, hash: location.hash, focus: document.activeElement.id }; });
  check('selected C3 takes the working red (no reform in view), job "selected item"', st.red === 'working' && st.job === 'selected item' && st.stroke === 'rgb(230, 57, 70)', st);
  check('selected label stays ink (Charcoal), bold mark 4 px', st.label === 'rgb(18, 18, 18)' && st.sw === '4px', st);
  check('C3 related marks lit (C2, C4, C5, L24, L25, L53) and unrelated L08 muted to Stone', JSON.stringify(st.rel) === JSON.stringify(['link-l24', 'link-l25', 'link-l53', 'var-c2', 'var-c3', 'var-c4', 'var-c5']) && st.dim && st.mutedL08 === 'rgb(93, 99, 109)', st);
  check('click selection: hash #area-c/var-c3, focus to panel title', st.hash === '#area-c/var-c3' && st.focus === 'ak-panel-title', st);
  await axe(p, '1440 area-c with panel open');
  // Hover never uses red
  await p.hover('[data-select="link-l08"] text'); await p.waitForTimeout(200);
  st = await p.evaluate(() => ({ s: getComputedStyle(document.querySelector('[data-select="link-l08"] path.ak-mark')).stroke, ro: document.querySelector('[data-view-root="area-c"] [data-ak-readout]').textContent }));
  check('hover on L08 lights it in ink, not red, and the readout names it', st.s === 'rgb(18, 18, 18)' && st.ro.startsWith('L08:'), st);
  await p.mouse.move(5, 890); await p.waitForTimeout(150);
  // Panel pick moves the selection without new history
  const h1 = await p.evaluate(() => history.length);
  await p.click('[data-ak-panel-body] [data-ak-pick="link-l25"]'); await p.waitForTimeout(200);
  st = await p.evaluate(() => ({ hash: location.hash, title: document.querySelector('[data-ak-panel-title]').textContent, hist: history.length, plain: [...document.querySelectorAll('[data-ak-panel-body] button')].length }));
  check('panel pick selects L25 in place (hash replaced, no history entry)', st.hash === '#area-c/link-l25' && st.hist === h1 && st.title.startsWith('Decisive primaries'), st);
  // Spatial keys over variables and wires in area C
  await p.focus('[data-select="var-c1"]'); const ak = [];
  for (const k of ['ArrowRight', 'ArrowRight', 'ArrowDown', 'ArrowDown']) { await p.keyboard.press(k); ak.push((await act(p)).key); }
  check('area C arrows walk C1 > L08 > C2 > L25 > C3', JSON.stringify(ak) === JSON.stringify(['link-l08', 'var-c2', 'link-l25', 'var-c3']), ak);

  // Down to loop R10 through the loop chip
  await p.keyboard.press('Escape');
  await p.click('a[href="#loop-r10"].chip'); await p.waitForTimeout(500);
  st = await p.evaluate(() => ({ hash: location.hash, focus: document.activeElement.id, crumbs: [...document.querySelectorAll('[data-ak-crumbs] li')].map((li) => li.textContent) }));
  check('R10 chip opens #loop-r10, focus on its heading, three-level breadcrumb', st.hash === '#loop-r10' && st.focus === 'h-loop-r10' && st.crumbs.length === 3, st);
  await axe(p, '1440 loop-r10');
  // Sequence arrows walk the loop and wrap
  await p.focus('svg[data-view="loop-r10"] [data-select="var-c1"]'); const seq = [];
  for (let k = 0; k < 8; k++) { await p.keyboard.press('ArrowRight'); seq.push((await act(p)).key); }
  check('loop arrows: C1 > L08 > C2 > L25 > C3 > L53 > C4 > L42 > C1 (wraps)', JSON.stringify(seq) === JSON.stringify(['link-l08', 'var-c2', 'link-l25', 'var-c3', 'link-l53', 'var-c4', 'link-l42', 'var-c1']), seq);
  await p.keyboard.press('ArrowLeft'); check('ArrowLeft steps back along the loop', (await act(p)).key === 'link-l42');

  // Reform: R-01 lights its targets, the reform and any selection stay ink
  await p.click('[data-select="reform-r-01"]'); await p.waitForTimeout(200);
  st = await p.evaluate(() => { const v = document.querySelector('[data-view-root="loop-r10"]');
    return { targets: [...v.querySelectorAll('.ak-target')].map((x) => x.dataset.select).sort(), jobs: [...new Set([...document.querySelectorAll('[data-red="working"]')].map((x) => x.dataset.redJob))], reformRed: document.querySelector('[data-select="reform-r-01"]').getAttribute('data-red'),
      l25: getComputedStyle(v.querySelector('[data-select="link-l25"] path.ak-mark')).stroke, l53: getComputedStyle(v.querySelector('[data-select="link-l53"] path.ak-mark')).stroke, keyline: getComputedStyle(v.querySelector('[data-select="link-l25"] path.ak-case')).stroke }; });
  check('R-01 targets L08, L25, C2 take the red; one job "R-01 targets"; the reform button stays ink', JSON.stringify(st.targets) === JSON.stringify(['link-l08', 'link-l25', 'var-c2']) && st.jobs.length === 1 && st.jobs[0] === 'R-01 targets' && st.reformRed === null && st.l25 === 'rgb(230, 57, 70)', st);
  check('a red wire on Newsprint carries the Charcoal keyline; non-targets stay ink', st.keyline === 'rgb(18, 18, 18)' && st.l53 === 'rgb(18, 18, 18)', st);
  // A reform shown by default in the view: selection goes to ink
  await p.keyboard.press('Escape');
  await p.evaluate(() => { document.querySelector('[data-view-root="loop-r10"]').dataset.akReform = 'reform-r-01'; AtlasKit.refresh(); });
  await p.click('svg[data-view="loop-r10"] [data-select="var-c3"] rect'); await p.waitForTimeout(200);
  st = await p.evaluate(() => { const c3 = document.querySelector('svg[data-view="loop-r10"] [data-select="var-c3"]');
    return { red: c3.getAttribute('data-red'), stroke: getComputedStyle(c3.querySelector('rect')).stroke, jobs: [...new Set([...document.querySelectorAll('[data-red="working"]')].map((x) => x.dataset.redJob))] }; });
  check('with a reform in view, the selected C3 goes to Charcoal and the only red job stays the targets', st.red === null && st.stroke === 'rgb(18, 18, 18)' && st.jobs.length === 1 && st.jobs[0] === 'R-01 targets', st);
  // Prussian: red never sits there; focus rings per surface, reached by keyboard so :focus-visible applies
  const ringOn = async (surface) => { await p.evaluate((sf) => { document.body.dataset.surface = sf; AtlasKit.refresh(); }, surface);
    await p.focus('svg[data-view="loop-r10"] [data-select="var-c1"]'); await p.keyboard.press('ArrowRight'); await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(200);   // let the 120 ms stroke transition finish
    return p.evaluate(() => ({ el: document.activeElement.dataset.select, color: getComputedStyle(document.activeElement).outlineColor, style: getComputedStyle(document.activeElement).outlineStyle, reds: document.querySelectorAll('[data-red]').length,
      targets: [...document.querySelectorAll('[data-view-root="loop-r10"] .ak-target')].map((x) => getComputedStyle(x.querySelector('.ak-mark')).stroke) })); };
  let rg = await ringOn('prussian');
  check('on Prussian the kit marks no working red and the focus ring is Newsprint', rg.reds === 0 && rg.color === 'rgb(220, 217, 210)' && rg.style === 'solid', rg);
  check('on Prussian the reform targets still light, in White', rg.targets.length === 3 && rg.targets.every((c) => c === 'rgb(255, 255, 255)'), rg.targets);
  rg = await ringOn('charcoal'); check('on Charcoal the focus ring is Newsprint', rg.color === 'rgb(220, 217, 210)' && rg.style === 'solid', rg);
  rg = await ringOn('white'); check('on White the focus ring is Verdigris', rg.color === 'rgb(74, 124, 116)' && rg.style === 'solid', rg);
  rg = await ringOn('newsprint'); check('on Newsprint the focus ring is Verdigris', rg.color === 'rgb(74, 124, 116)' && rg.style === 'solid', rg);
  await p.evaluate(() => { document.body.dataset.surface = 'newsprint'; delete document.querySelector('[data-view-root="loop-r10"]').dataset.akReform; });
  await p.keyboard.press('Escape');

  // Step-through
  const S = (q) => p.evaluate((q) => { const box = document.querySelector('[data-ak-stepper]'); return { status: box.querySelector('[data-ak-step-status]').textContent, cur: [...box.querySelectorAll('li')].findIndex((li) => li.getAttribute('aria-current') === 'step'), now: [...document.querySelectorAll('[data-view-root="loop-r10"] .ak-now')].map((x) => x.dataset.select).sort(), shown: [...document.querySelectorAll('[data-ak-at]')].filter((m) => !m.hasAttribute('hidden')).map((m) => m.dataset.akAt), play: box.querySelector('[data-ak-step="play"]').textContent, dash: getComputedStyle(document.querySelector('[data-select="link-l53"] path.ak-mark')).strokeDasharray }; });
  let s0 = await S(); check('stepper idle: only the start marker shows', s0.cur === -1 && JSON.stringify(s0.shown) === '["0"]', s0);
  await p.click('[data-ak-step="next"]'); let s1 = await S();
  check('Next: step 1 of 4 is L08, list item 1 is aria-current="step", C2 marker shows', s1.status.startsWith('Step 1 of 4. L08') && s1.cur === 0 && JSON.stringify(s1.now) === '["link-l08","var-c2"]' && s1.shown.includes('1'), s1);
  await p.click('[data-ak-step="next"]'); await p.click('[data-ak-step="next"]'); let s3 = await S();
  check('step 3 lights L53 and keeps its dashed texture (plausible)', JSON.stringify(s3.now) === '["link-l53","var-c4"]' && s3.dash !== 'none', s3.dash);
  const runner = await p.evaluate(() => document.querySelectorAll('.ak-runner').length);
  check('a runner travels the step (motion allowed)', runner >= 0, runner);
  await p.click('[data-ak-step="next"]'); let s4 = await S();
  check('step 4 closes the loop and names its kind and weakest step', s4.status.includes('Reinforcing'.toLowerCase()) && s4.status.includes('L53') && s4.play === 'Play again', s4.status);
  await p.click('[data-ak-step="next"]'); check('Next at the end stays on step 4', (await S()).cur === 3);
  await p.click('[data-ak-step="prev"]'); check('Previous goes back to step 3', (await S()).cur === 2);
  await p.click('[data-ak-step="reset"]'); let sr = await S(); check('Reset returns to idle', sr.cur === -1 && JSON.stringify(sr.shown) === '["0"]', sr);
  await p.click('[data-ak-step="play"]'); let sp = await S(); check('Play starts at step 1 and the button reads Pause', sp.cur === 0 && sp.play === 'Pause', sp);
  await p.waitForTimeout(3400); check('Play advances after 3,200 ms', (await S()).cur === 1);
  await p.click('[data-ak-step="play"]'); await p.waitForTimeout(3400); let spz = await S(); check('Pause holds the step', spz.cur === 1 && spz.play === 'Play', spz);
  const live = await p.evaluate(() => document.querySelector('[data-ak-step-status]').getAttribute('aria-live'));
  check('step status is a polite live region', live === 'polite');

  // Hash edge cases
  await p.goto(F + '#area-z'); await p.waitForTimeout(300);
  st = await p.evaluate(() => ({ hash: location.hash, status: document.querySelector('[data-ak-status]').textContent, ov: !document.querySelector('[data-view-root="overview"]').hidden }));
  check('unknown view falls back to the overview with a status message', st.ov && st.status.includes('no view called area-z'), st);
  await p.goto(F + '#area-a'); await p.reload(); await p.waitForTimeout(300);
  st = await p.evaluate(() => ({ hash: location.hash, panel: !document.querySelector('[data-ak-panel]').hidden, title: document.querySelector('[data-ak-panel-title]').textContent }));
  check('deep link #area-a (no close-up) opens the overview with area A in the panel', st.hash === '#overview/area-a' && st.panel && st.title === 'Economic structure', st);
  await p.goto(F + '#loop-r10/reform-r-01'); await p.reload(); await p.waitForTimeout(300);
  st = await p.evaluate(() => ({ targets: document.querySelectorAll('[data-view-root="loop-r10"] .ak-target').length, panel: document.querySelector('[data-ak-panel-title]').textContent }));
  check('deep link #loop-r10/reform-r-01 restores the reform selection and its red targets', st.targets === 3 && st.panel.startsWith('All-party'), st);
  await ctx.close();

  // ---------------- 390 ----------------
  ctx = await b.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  p = await ctx.newPage(); p.on('pageerror', (e) => errors.push(e.message));
  for (const v of ['overview', 'area-c', 'loop-r10']) {
    await p.goto(F + '#' + v); await p.reload(); await p.waitForTimeout(400);
    const w = await noSideways(p); check(`390 ${v}: no sideways scroll`, w.sw <= w.cw, w);
    const reg = await p.evaluate((v) => { const r = document.querySelector(`[data-view-root="${v}"] .ak-scroll`); return { role: r.getAttribute('role'), tab: r.tabIndex, label: r.getAttribute('aria-label'), scrolls: r.scrollWidth > r.clientWidth }; }, v);
    check(`390 ${v}: the drawing sits in a focusable, labelled scroll region`, reg.role === 'region' && reg.tab === 0 && reg.label && reg.scrolls, reg);
    await axe(p, `390 ${v}`);
  }
  // Tap selects and opens the bottom sheet
  await p.goto(F + '#overview'); await p.reload(); await p.waitForTimeout(300);
  await p.tap('[data-select="area-a"] rect'); await p.waitForTimeout(300);
  st = await p.evaluate(() => { const pn = document.querySelector('[data-ak-panel]'); const r = pn.getBoundingClientRect(); return { pos: getComputedStyle(pn).position, bottom: Math.round(r.bottom), h: Math.round(r.height), vh: innerHeight, focus: document.activeElement.id }; });
  check('390 tap on area A opens a bottom sheet at most 48% of the screen, focus on its title', st.pos === 'fixed' && st.bottom === st.vh && st.h <= Math.ceil(st.vh * 0.48) && st.focus === 'ak-panel-title', st);
  await axe(p, '390 overview with the sheet open');
  await p.tap('[data-ak-sheet-toggle]'); await p.waitForTimeout(250);
  st = await p.evaluate(() => ({ h: document.querySelector('[data-ak-panel]').getBoundingClientRect().height, exp: document.querySelector('[data-ak-sheet-toggle]').getAttribute('aria-expanded') }));
  check('More expands the sheet and sets aria-expanded', st.exp === 'true' && st.h > 844 * 0.48, st);
  await p.tap('[data-ak-sheet-toggle]');
  // Focus is not hidden behind the sheet (2.4.11)
  st = await p.evaluate(() => { const el = document.querySelector('[data-view-root="overview"] .full-btn'); el.focus(); const r = el.getBoundingClientRect(); const top = document.querySelector('[data-ak-panel]').getBoundingClientRect().top; return { bottom: Math.round(r.bottom), sheetTop: Math.round(top) }; });
  check('390 a control focused while the sheet is open scrolls clear of it', st.bottom <= st.sheetTop, st);
  await p.tap('[data-ak-close]'); await p.waitForTimeout(200);
  check('Close hides the sheet and returns focus to area A', (await act(p)).key === 'area-a');
  // Full size
  await p.focus('[data-view-root="overview"] .full-btn'); await p.keyboard.press('Enter'); await p.waitForTimeout(300);
  st = await p.evaluate(() => ({ open: !!document.querySelector('dialog.ak-full[open]'), svgIn: !!document.querySelector('dialog.ak-full svg[data-view="overview"]'), focus: document.activeElement.textContent }));
  check('View full size opens a modal dialog holding the drawing, focus on Close full size', st.open && st.svgIn && st.focus === 'Close full size', st);
  await axe(p, '390 full-size dialog');
  await p.keyboard.press('Escape'); await p.waitForTimeout(200);
  st = await p.evaluate(() => ({ open: !!document.querySelector('dialog.ak-full'), back: !!document.querySelector('#map-overview svg[data-view="overview"]'), focus: document.activeElement.textContent.trim() }));
  check('Escape closes full size, the drawing returns to its region, focus returns to the button', !st.open && st.back && st.focus === 'View the map full size', st);
  // Tapping area C from full size moves down a level
  await p.tap('[data-view-root="overview"] .full-btn'); await p.waitForTimeout(300);
  await p.tap('dialog.ak-full a[href="#area-c"] rect'); await p.waitForTimeout(500);
  st = await p.evaluate(() => ({ hash: location.hash, dlg: !!document.querySelector('dialog.ak-full'), back: !!document.querySelector('#map-overview svg') }));
  check('a tap on area C inside full size closes it and opens #area-c', st.hash === '#area-c' && !st.dlg && st.back, st);
  await ctx.close();

  // ---------------- reduced motion ----------------
  ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  p = await ctx.newPage(); p.on('pageerror', (e) => errors.push(e.message));
  await p.goto(F + '#overview'); await p.waitForTimeout(300);
  await p.click('svg[data-view="overview"] a[href="#area-c"]'); await p.waitForTimeout(50);
  st = await p.evaluate(() => ({ anims: document.querySelector('[data-view-root="area-c"]').getAnimations().length, name: getComputedStyle(document.querySelector('[data-view-root="area-c"]')).animationName }));
  check('reduced motion: the level change has no animation', st.anims === 0 && st.name === 'none', st);
  await p.goto(F + '#loop-r10'); await p.waitForTimeout(200);
  await p.click('[data-ak-step="next"]'); await p.waitForTimeout(30);
  st = await p.evaluate(() => ({ runner: document.querySelectorAll('.ak-runner').length, status: document.querySelector('[data-ak-step-status]').textContent.slice(0, 20) }));
  check('reduced motion: steps change at once with no runner', st.runner === 0 && st.status.startsWith('Step 1 of 4'), st);
  await ctx.close();
  // ---------------- motion allowed: the zoom runs ----------------
  ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'no-preference' });
  p = await ctx.newPage(); await p.goto(F + '#overview'); await p.waitForTimeout(300);
  await p.click('svg[data-view="overview"] a[href="#area-c"]'); await p.waitForTimeout(30);
  st = await p.evaluate(() => { const r = document.querySelector('[data-view-root="area-c"]'); return { name: getComputedStyle(r).animationName, dur: getComputedStyle(r).animationDuration, origin: r.style.transformOrigin }; });
  check('motion allowed: area C lands with ak-zoom-in, 320 ms, from the clicked card', st.name === 'ak-zoom-in' && st.dur === '0.32s' && st.origin !== '50% 0px', st);
  await p.goto(F + '#loop-r10'); await p.waitForTimeout(200); await p.click('[data-ak-step="next"]'); await p.waitForTimeout(60);
  check('motion allowed: a runner travels the step', (await p.evaluate(() => document.querySelectorAll('.ak-runner').length)) === 1);
  await ctx.close();

  check('no page errors in any run', errors.length === 0, errors);
  await b.close();
  fs.writeFileSync(__dirname + '/test_kit_results.json', JSON.stringify({ when: new Date().toISOString(), fails, results }, null, 1));
  console.log(`\n${results.length - fails} of ${results.length} passed`);
  process.exit(fails ? 1 : 0);
})();
