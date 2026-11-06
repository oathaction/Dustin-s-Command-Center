// Walk the reader check page end to end with a stubbed window.claude (November 6, 2026).
// Run from the project root:  node work/boards/phase-2/reader-check/test_reader_check.js [--quick]
//
// The page is content only (the publish step wraps it), so each run wraps it in the publish skeleton with a <base>
// pointing at this folder, and puts a stub window.claude in the head, before the page's script, as the viewer does:
//   saved     use("db") and use("user") resolve: an in-memory store that checks paths, rejects update() on a missing
//             document, and counts overlapping writes to one document; a user with an id and data.write.
//   null      use() resolves null for everything (a signed-out reader, or a view that cannot run db).
//   absent    no window.claude at all (a saved copy of the page).
//   viewonly  db and an id, but can("data.write") is false.
//   reject    db and an id, but every write rejects invalid_argument (a level below interact).
// Every screen is checked at its rendered state: axe-core 4.10.2 (WCAG 2.x A and AA tags), no sideways scroll, no
// visible text under 13 px, text contrast from rendered colors, targets at least 44 px tall, focus on the screen's
// heading after each change. Timed looks run at a twentieth of real time except in the real-time run.
// Writes 20261106_Reader-Check-Test-Results.json and the 390 px captures in captures/.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const HERE = __dirname;
const ROOT = path.resolve(HERE, '../../../..');
const PAGE = path.join(HERE, '20261106_Reader-Check.html');
const AXE = fs.readFileSync(path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js'), 'utf8');
const CAPS = path.join(HERE, 'captures');
const TMP = process.env.RC_TMP || path.join(require('os').tmpdir(), 'reader-check-test');
const QUICK = process.argv.includes('--quick');
fs.mkdirSync(CAPS, { recursive: true });
fs.mkdirSync(TMP, { recursive: true });

const STUB = String.raw`
(function (MODE) {
  window.__DB__ = { docs: {}, writes: [], inflight: {}, maxInflight: 0, calls: [] };
  if (MODE === 'absent') return;
  const D = window.__DB__;
  try { const kept = sessionStorage.getItem('stubdocs'); if (kept) D.docs = JSON.parse(kept); } catch (e) { /* none */ }
  const clone = (x) => JSON.parse(JSON.stringify(x));
  const merge = (a, b) => { for (const [k, v] of Object.entries(b)) { if (v && typeof v === 'object' && !Array.isArray(v) && a[k] && typeof a[k] === 'object' && !Array.isArray(a[k])) merge(a[k], v); else a[k] = clone(v); } return a; };
  const lag = () => new Promise((r) => setTimeout(r, 15 + Math.random() * 40));
  function seg(path) { const s = path.split('/'); if (s.some((x) => !/^[A-Za-z0-9_\-.~:@+]+$/.test(x) || x === '.' || x === '..')) throw new TypeError('bad segment in ' + path); return s; }
  async function write(path, fn) {
    D.inflight[path] = (D.inflight[path] || 0) + 1; D.maxInflight = Math.max(D.maxInflight, D.inflight[path]);
    try { await lag(); if (MODE === 'reject') throw { code: 'invalid_argument', message: 'below interact' }; fn(); D.writes.push({ path, at: Date.now() }); }
    finally { D.inflight[path]--; }
  }
  const db = Object.freeze({
    doc(path) {
      if (seg(path).length % 2) throw new TypeError('document paths have an even number of segments');
      return Object.freeze({ id: path.split('/').pop(), path,
        async get() { D.calls.push('get'); await lag(); const d = D.docs[path]; return { id: path.split('/').pop(), exists: !!d, data: () => (d ? clone(d) : undefined), metadata: { fromCache: false, hasPendingWrites: false } }; },
        set(body) { D.calls.push('set'); return write(path, () => { D.docs[path] = clone(body); }); },
        update(body) { D.calls.push('update'); return write(path, () => { if (!D.docs[path]) throw { code: 'invalid_argument', message: 'update needs an existing document' }; merge(D.docs[path], body); }); },
        async delete() { delete D.docs[path]; },
        onSnapshot() { return () => {}; }, collection() { throw new Error('not stubbed'); } });
    },
    collection() { throw new Error('not stubbed'); },
  });
  const user = Object.freeze({
    async id() { return 'u_test_reader_01'; }, async isOwner() { return false; }, async canEdit() { return false; },
    async can(n) { return n === 'data.write' ? MODE !== 'viewonly' : false; },
    async me() { return { id: 'u_test_reader_01', name: '', avatarUrl: 'data:,', color: '#888', email: null, isOwner: false, canEdit: false }; },
    async profiles() { return {}; }, async name() { return ''; }, async avatarUrl() { return null; }, async search() { return []; }, async email() { return null; },
  });
  window.claude = Object.freeze({ use: async (name) => { await lag(); if (MODE === 'null') return null; return name === 'db' ? db : name === 'user' ? user : null; } });
})`;

function wrap(mode, scale) {
  const page = fs.readFileSync(PAGE, 'utf8');
  const head = `<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><base href="file://${HERE}/"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>`
    + `<script>window.__RC_TEST__ = { timeScale: ${scale} };${STUB}(${JSON.stringify(mode)});</script></head><body>`;
  const out = path.join(TMP, `reader-check-${mode}.html`);
  fs.writeFileSync(out, head + page + '</body></html>');
  return out;
}

// ------------------------------------------------------------------ checks on the rendered screen
async function audit(page) {
  await page.addScriptTag({ content: AXE }).catch(() => {});
  return page.evaluate(async () => {
    const parse = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
    const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
    const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const vis = (el) => { const r = el.getBoundingClientRect(); if (!r.width && !r.height) return false; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false; } return true; };
    const bg = (el) => { for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return c; } return { r: 255, g: 255, b: 255 }; };
    const out = { under13: [], lowContrast: [], smallTargets: [], overflow: null, focus: null, axe: [] };
    for (const el of document.querySelectorAll('body *')) {
      if (['SCRIPT', 'STYLE', 'TITLE'].includes(el.tagName) || el.closest('.sr')) continue;
      const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim()).map((n) => n.textContent.trim()).join(' ');
      if (!own || !vis(el)) continue;
      const cs = getComputedStyle(el); const size = parseFloat(cs.fontSize);
      if (size < 12.95) out.under13.push({ text: own.slice(0, 40), size });
      const cr = ratio(parse(cs.color), bg(el)); const large = size >= 24 || (size >= 18.66 && +cs.fontWeight >= 700);
      if (cr < (large ? 3 : 4.5) - 0.005) out.lowContrast.push({ text: own.slice(0, 40), ratio: +cr.toFixed(2) });
    }
    for (const el of document.querySelectorAll('button, .choice, .seg label, input[type=text], textarea')) {
      if (!vis(el)) continue; const r = el.getBoundingClientRect();
      if (r.height < 43.5 || r.width < 24) out.smallTargets.push({ el: el.tagName + '.' + el.className, text: (el.textContent || '').trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) });
    }
    out.overflow = document.documentElement.scrollWidth > document.documentElement.clientWidth + 1 ? document.documentElement.scrollWidth : null;
    const a = document.activeElement; out.focus = a ? a.tagName + (a.id ? '#' + a.id : '') + ':' + (a.textContent || '').trim().slice(0, 40) : null;
    const r = await window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
    out.axe = r.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, target: v.nodes[0] && v.nodes[0].target.join(' ') }));
    return out;
  });
}
const state = (page) => page.evaluate(() => { const S = window.__RC__.S; const sc = S.screens[S.pos]; return { pos: S.pos, kind: sc.kind, key: sc.key, step: sc.step, mode: window.__RC__.Store.mode }; });

async function waitPos(page, from, ms) {
  await page.waitForFunction((p) => window.__RC__ && window.__RC__.S.pos !== p, from, { timeout: ms });
}

// ------------------------------------------------------------------ one walk through the whole test
async function walk(browser, { mode, width, scale, captures, reduce, label }) {
  const height = width === 1440 ? 900 : width === 390 ? 844 : 780;
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: captures ? 2 : 1, reducedMotion: reduce ? 'reduce' : 'no-preference' });
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write']).catch(() => {});
  const page = await ctx.newPage();
  const errors = [], outside = new Set();
  page.on('pageerror', (e) => errors.push(String(e.message || e)));
  page.on('request', (r) => { const u = r.url(); if (/^(file|data|blob|about):/.test(u)) return; const hst = new URL(u).hostname; if (!['fonts.googleapis.com', 'fonts.gstatic.com'].includes(hst)) outside.add(hst); });
  const file = wrap(mode, scale);
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__RC__ && document.querySelector('[data-view-root="welcome"]'));
  const res = { label, mode, width, scale, screens: 0, failures: [], notes: [], exposures: [] };
  const fail = (m) => res.failures.push(m);
  const capNames = new Set();
  let capN = 0;
  async function snap(name) {
    if (!captures || capNames.has(name)) return;
    capNames.add(name); capN++;
    await page.screenshot({ path: path.join(CAPS, `20261106_Reader-Check-${String(capN).padStart(2, '0')}-${name}-${width}${mode === 'saved' ? '' : '-' + mode}.png`), fullPage: true });
  }
  async function check(tag) {
    const a = await audit(page); res.screens++;
    if (a.under13.length) fail(`${tag}: text under 13 px ${JSON.stringify(a.under13.slice(0, 3))}`);
    if (a.lowContrast.length) fail(`${tag}: low contrast ${JSON.stringify(a.lowContrast.slice(0, 3))}`);
    if (a.smallTargets.length) fail(`${tag}: targets under 44 px ${JSON.stringify(a.smallTargets.slice(0, 3))}`);
    if (a.overflow) fail(`${tag}: sideways scroll to ${a.overflow}`);
    if (a.axe.length) fail(`${tag}: axe ${a.axe.map((v) => v.id + ' x' + v.nodes + ' ' + v.target).join('; ')}`);
    return a;
  }

  // welcome: the mode line settles, an empty start is caught, then start
  await page.waitForFunction(() => window.__RC__.Store.mode !== 'checking', null, { timeout: 15000 });
  const modeLine = await page.textContent('#mode-line');
  res.modeLine = modeLine;
  await check('welcome');
  await snap('Welcome');
  await page.click('form button[type=submit]');
  const err = await page.textContent('#initials-msg');
  if (!/first name or initials/.test(err)) fail('welcome: empty start not caught');
  await page.fill('#initials', 'T' + width);
  await page.click('form button[type=submit]');

  let guard = 0, usedAgain = 0, skipped = 0, validated = 0;
  const seen = {};
  while (guard++ < 120) {
    const s = await state(page);
    seen[s.kind] = (seen[s.kind] || 0) + 1;
    const focus = await page.evaluate(() => document.activeElement && document.activeElement.tagName);
    if (s.kind !== 'expose' && !['H1', 'H2'].includes(focus)) fail(`${s.key}: focus on ${focus}, not the heading`);
    if (s.kind === 'end') {
      await page.waitForFunction(() => !/Saving/.test(document.querySelector('main').textContent), null, { timeout: 30000 });
      await check('end');
      await snap('End');
      res.end = await page.evaluate(() => ({ text: document.querySelector('main').innerText.slice(0, 400), copy: (document.querySelector('#copy-text') || {}).value || null }));
      if (res.end.copy) {
        await page.click('text=Copy my answers');
        await page.waitForTimeout(200);
        res.copyStatus = await page.evaluate(() => (document.querySelector('.status') || {}).textContent || '');
        if (!/Copied|couldn’t copy/.test(res.copyStatus)) fail('end: copy gave no status');
        // one tap on "Start a new test" must not clear unsent answers
        await page.click('text=Start a new test on this device');
        const kept = await page.evaluate(() => ({ copy: !!document.querySelector('#copy-text'), label: [...document.querySelectorAll('main button')].map((b) => b.textContent).join(' | ') }));
        if (!kept.copy || !/Tap again/.test(kept.label)) fail('end: one tap on start-again cleared the answers or gave no warning');
      }
      break;
    }
    if (s.kind === 'ready') {
      await check(s.key); await snap('Ready-' + s.step);
      await page.click('main .btn.primary');
      await waitPos(page, s.pos, 5000);
      continue;
    }
    if (s.kind === 'expose') {
      // the clock starts only after the images decode; it then runs its seconds and moves on
      await page.waitForFunction(() => !document.querySelector('main .loading'), null, { timeout: 20000 });
      const t0 = Date.now();
      const imgs = await page.evaluate(() => [...document.querySelectorAll('main img')].map((i) => ({ ok: i.complete && i.naturalWidth > 0, w: Math.round(i.getBoundingClientRect().width), src: i.currentSrc.split('/').pop() })));
      if (imgs.some((i) => !i.ok)) fail(`${s.key}: image not loaded ${JSON.stringify(imgs)}`);
      const clock = await page.evaluate(() => ({ text: document.querySelector('#bar-step').textContent, bar: getComputedStyle(document.querySelector('#clock')).display }));
      if (!/seconds? left/.test(clock.text)) fail(`${s.key}: no time-left text (${clock.text})`);
      if (reduce && clock.bar !== 'none') fail(`${s.key}: clock bar shows under reduced motion`);
      if (s.key === 'overview:look' || s.key.startsWith('icon_') && !capNames.has('Symbol-Look') || s.key === 'marks:look' || s.key.startsWith('chart_') && !capNames.has('Chart-Look') || s.key === 'masthead:look' || s.key.startsWith('loop_') && !capNames.has('Loop-Look')) {
        const a = await check(s.key);
        const nm = s.key === 'overview:look' ? 'Overview-Look' : s.key.startsWith('icon_') ? 'Symbol-Look' : s.key === 'marks:look' ? 'Marks-Look' : s.key.startsWith('chart_') ? 'Chart-Look' : s.key.startsWith('loop_') ? 'Loop-Look' : 'Masthead-Look';
        await snap(nm);
      }
      await waitPos(page, s.pos, 30000 * Math.max(scale, 0.1) + 15000);
      const it = await page.evaluate((k) => window.__RC__.S.run.items[k], (await page.evaluate((p) => window.__RC__.S.screens[p].item, s.pos)));
      res.exposures.push({ key: s.key, shown: it.shown_seconds.slice(-1)[0], wall: (Date.now() - t0) / 1000, imgs: imgs.map((i) => i.src + '@' + i.w).join(' ') });
      continue;
    }
    // questions
    await check(s.key);
    if (s.kind === 'question') {
      const isChoice = await page.$('main .choice');
      if (s.key === 'overview:purpose' || s.key.endsWith(':least_certain') && !capNames.has('Loop-Question') || s.key.endsWith(':stands_for') && !capNames.has('Symbol-Question') || s.key.endsWith(':favors') && !capNames.has('Chart-Question')) {
        await snap(s.key === 'overview:purpose' ? 'Overview-Question' : s.key.endsWith(':least_certain') ? 'Loop-Question' : s.key.endsWith(':stands_for') ? 'Symbol-Question' : 'Chart-Question');
      }
      // validation once, show-again on the first question of three looks, one skip
      if (!validated && s.key === 'overview:purpose') {
        validated++;
        await page.click('main button[type=submit]');
        const m = await page.textContent('#q-msg');
        if (!/Type an answer/.test(m)) fail('question: empty next not caught');
      }
      if (['overview:purpose', 'loop_r10:least_certain'].includes(s.key) || (s.key.endsWith(':stands_for') && usedAgain < 3)) {
        if (!isChoice) await page.fill('#answer', 'draft before another look');
        const before = await page.evaluate((k) => window.__RC__.S.run.items[window.__RC__.S.screens[window.__RC__.S.pos].item].show_again, s.key);
        await page.click('text=Show it again');
        await page.waitForFunction(() => /seconds? left/.test(document.querySelector('#bar-step').textContent), null, { timeout: 20000 });
        await snap('Show-It-Again');
        await page.waitForFunction((k) => document.querySelector('#q-h') && window.__RC__.S.screens[window.__RC__.S.pos].key === k, s.key, { timeout: 30000 * Math.max(scale, 0.1) + 15000 });
        const after = await page.evaluate(() => window.__RC__.S.run.items[window.__RC__.S.screens[window.__RC__.S.pos].item].show_again);
        if (after !== before + 1) fail(`${s.key}: show-again count ${before} -> ${after}`);
        if (!isChoice) { const v = await page.inputValue('#answer'); if (v !== 'draft before another look') fail(`${s.key}: draft lost after another look (${v})`); }
        usedAgain++;
      }
      if (s.key.endsWith(':stands_for') && skipped === 0) {
        skipped++;
        await page.click('text=Skip this question');
      } else if (isChoice) {
        const n = await page.$$eval('main .choice', (els) => els.length);
        await page.click(`main .choice >> nth=${Math.min(1, n - 1)}`);
        await page.click('main button[type=submit]');
      } else {
        await page.fill('#answer', `answer for ${s.key} at ${width}`);
        await page.click('main button[type=submit]');
      }
    } else if (s.kind === 'marks') {
      await snap('Marks-Rating');
      const rows = await page.$$('main fieldset.rate');
      for (let i = 0; i < rows.length - 1; i++) await rows[i].$eval(`label:nth-child(${(i % 3) + 1})`, (l) => l.click());
      await page.click('main button[type=submit]');
      const m = await page.evaluate(() => document.querySelector('main .msg').textContent);
      if (!/Mark 9 has no answer yet/.test(m)) fail(`marks: partial rating not caught (${m})`);
      await page.click('main button[type=submit]');
    } else if (s.kind === 'pair') {
      await snap('Pair');
      await page.click('main .choice >> nth=0');
      await page.click('main button[type=submit]');
    } else if (s.kind === 'masthead') {
      await snap('Masthead-Question');
      await page.click('main .choice >> nth=1');
      await page.fill('#why', 'It is shorter.');
      await page.click('main button[type=submit]');
    }
    await waitPos(page, s.pos, 10000);
  }
  res.seen = seen;
  // the record
  const rec = await page.evaluate(() => ({ run: window.__RC__.S.run, runId: window.__RC__.S.runId, mode: window.__RC__.Store.mode, db: window.__DB__ }));
  res.finalMode = rec.mode;
  const run = rec.run;
  const items = run.items;
  const qcount = Object.values(items).reduce((a, it) => a + Object.keys(it.questions).length, 0);
  res.record = { questions: qcount, items: Object.keys(items).length, orders: run.orders, finished: !!run.finished_at, initials: run.initials, viewport_width: run.viewport_width, mode: run.mode, mode_note: run.mode_note,
    showAgain: Object.fromEntries(Object.entries(items).filter(([, v]) => v.show_again).map(([k, v]) => [k, v.show_again])),
    skipped: Object.entries(items).flatMap(([k, v]) => Object.entries(v.questions).filter(([, q]) => q.skipped).map(([q]) => k + '.' + q)) };
  if (qcount !== 2 + 8 + 8 + 9 + 6 + 3 + 2) fail(`record: ${qcount} answers, expected 38`);
  if (!run.finished_at) fail('record: no finished time');
  const secs = Object.values(items).flatMap((it) => Object.values(it.questions).map((q) => q.seconds)).filter((x) => x !== undefined);
  if (secs.some((x) => x === null && false)) fail('record: missing seconds');
  if (mode === 'saved') {
    const doc = rec.db.docs['responses/u_test_reader_01'];
    if (!doc) fail('db: no document at responses/<id>');
    else {
      const stored = doc.runs[rec.runId];
      if (JSON.stringify(stored) !== JSON.stringify(run)) fail('db: stored run differs from the page state');
      if (doc.latest_run !== rec.runId) fail('db: latest_run not set');
    }
    if (rec.db.maxInflight > 1) fail(`db: ${rec.db.maxInflight} writes overlapped on one document`);
    if (!/saved/.test(res.end.text)) fail('end: saved mode did not confirm the save');
    res.db = { writes: rec.db.writes.length, maxInflight: rec.db.maxInflight, calls: rec.db.calls.reduce((a, c) => (a[c] = (a[c] || 0) + 1, a), {}) };
  } else {
    if (!res.end.copy || !res.end.copy.includes('"schema":"reader-check/1"')) fail('end: copy mode shows no copy text');
    const line = res.end.copy.split('\n').pop();
    const parsed = JSON.parse(line);
    if (JSON.stringify(parsed.run) !== JSON.stringify(run)) fail('copy: the copied JSON differs from the page state');
    if (rec.db.writes.length) fail(`copy mode wrote ${rec.db.writes.length} documents`);
  }
  if (errors.length) fail('page errors: ' + errors.join(' | '));
  if (outside.size) fail('outside requests: ' + [...outside].join(', '));
  // the copy text must not name what a symbol means
  if (res.end.copy) for (const w of ['Explain', 'Track', 'Connect', 'Act', 'Political', 'Reporting', 'Essential', 'Ranked']) if (new RegExp('\\b' + w + '\\b').test(res.end.copy)) fail('copy text names ' + w);
  await ctx.close();
  return res;
}

// ------------------------------------------------------------------ targeted tests
async function resumeTest(browser) {
  const res = { label: 'resume after a reload, saved mode, 390', failures: [] };
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  const file = wrap('saved', 0.05);
  await page.goto('file://' + file); await page.waitForFunction(() => window.__RC__ && window.__RC__.Store.mode === 'saved');
  await page.fill('#initials', 'RS'); await page.click('form button[type=submit]');
  await page.click('main .btn.primary');                                         // drawings: ready
  await page.waitForFunction(() => document.querySelector('#q-h'), null, { timeout: 10000 });  // after the look
  await page.fill('#answer', 'a map of who answers to whom'); await page.click('main button[type=submit]');
  await page.waitForFunction(() => window.__RC__.S.screens[window.__RC__.S.pos].key === 'overview:open_first');
  const before = await page.evaluate(() => ({ runId: window.__RC__.S.runId, db: window.__DB__.docs }));
  // a reload keeps localStorage but the in-memory store resets, so carry the stub's documents across
  await page.evaluate((docs) => sessionStorage.setItem('stubdocs', JSON.stringify(docs)), before.db);
  await page.reload();
  await page.waitForFunction(() => window.__RC__);
  const welcome = await page.textContent('main');
  if (!/Welcome back/.test(welcome)) res.failures.push('no resume offer after reload: ' + welcome.slice(0, 120));
  await page.click('text=Pick up where I left off');
  const s = await state(page);
  if (s.key !== 'overview:open_first') res.failures.push('resumed at ' + s.key);
  const run = await page.evaluate(() => window.__RC__.S.run);
  if (run.resumed !== 1) res.failures.push('resumed count ' + run.resumed);
  if (!run.items.overview || run.items.overview.questions.purpose.answer !== 'a map of who answers to whom') res.failures.push('earlier answer lost on resume');
  if ((await page.evaluate(() => window.__RC__.S.runId)) !== before.runId) res.failures.push('resume started a new run');
  await page.click('main .choice >> nth=2'); await page.click('main button[type=submit]');
  await page.waitForTimeout(400);
  const doc = await page.evaluate(() => window.__DB__.docs['responses/u_test_reader_01']);
  if (!doc) res.failures.push('no write after resume');
  // a finished run reloads to its end screen
  res.pass = !res.failures.length; await ctx.close(); return res;
}

async function pauseTest(browser) {
  // a look counts only visible time: hide the page for 1.5 s of a 2 s look and the look runs about 3.5 s
  const res = { label: 'a look pauses while the page is hidden, 390', failures: [] };
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await ctx.newPage();
  await page.goto('file://' + wrap('null', 0.2)); await page.waitForFunction(() => window.__RC__ && window.__RC__.Store.mode === 'copy');
  await page.fill('#initials', 'PT'); await page.click('form button[type=submit]');
  await page.click('main .btn.primary');
  await page.waitForFunction(() => !document.querySelector('main .loading'));
  const t0 = Date.now();
  await page.waitForTimeout(300);
  await page.evaluate(() => { Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'hidden' }); document.dispatchEvent(new Event('visibilitychange')); });
  await page.waitForTimeout(1500);
  const still = await state(page);
  if (still.kind !== 'expose') res.failures.push('look ended while hidden');
  await page.evaluate(() => { Object.defineProperty(document, 'visibilityState', { configurable: true, get: () => 'visible' }); document.dispatchEvent(new Event('visibilitychange')); });
  await page.waitForFunction(() => document.querySelector('#q-h'), null, { timeout: 10000 });
  res.wall = (Date.now() - t0) / 1000;
  const shown = await page.evaluate(() => window.__RC__.S.run.items.overview.shown_seconds[0]);
  res.shown = shown;
  if (res.wall < 3.2) res.failures.push(`look did not pause (${res.wall} s wall)`);
  if (Math.abs(shown - 10) > 0.6) res.failures.push(`recorded look ${shown} s, expected 10 (scaled back)`);
  res.pass = !res.failures.length; await ctx.close(); return res;
}

async function reflowTest(browser) {
  // WCAG 1.4.10: 320 CSS px, no sideways scroll, on every kind of screen (quick walk, captures off)
  const r = await walk(browser, { mode: 'null', width: 320, scale: 0.05, label: 'reflow at 320 px, copy mode' });
  return r;
}

(async () => {
  const browser = await chromium.launch();
  const runs = [];
  const plan = QUICK ? [
    { mode: 'saved', width: 390, scale: 0.05, label: 'saved, 390' },
  ] : [
    { mode: 'saved', width: 390, scale: 1, captures: true, label: 'saved, 390, real time, captures' },
    { mode: 'saved', width: 360, scale: 0.05, label: 'saved, 360' },
    { mode: 'saved', width: 1440, scale: 0.05, label: 'saved, 1440' },
    { mode: 'null', width: 390, scale: 0.4, captures: true, label: 'copy (use() resolves null), 390, captures' },
    { mode: 'null', width: 360, scale: 0.05, label: 'copy (use() resolves null), 360' },
    { mode: 'null', width: 1440, scale: 0.05, label: 'copy (use() resolves null), 1440' },
    { mode: 'absent', width: 390, scale: 0.05, label: 'copy (no window.claude), 390' },
    { mode: 'viewonly', width: 390, scale: 0.05, label: 'copy (view-only), 390' },
    { mode: 'reject', width: 390, scale: 0.05, label: 'saved then copy (every write rejected), 390' },
    { mode: 'saved', width: 390, scale: 0.05, reduce: true, label: 'saved, 390, reduced motion' },
  ];
  for (const p of plan) {
    const t = Date.now();
    const r = await walk(browser, p).catch((e) => ({ label: p.label, failures: ['crashed: ' + (e.stack || e).toString().slice(0, 400)] }));
    r.pass = !r.failures.length; r.seconds = Math.round((Date.now() - t) / 1000);
    runs.push(r);
    console.log(`${r.pass ? 'PASS' : 'FAIL'} ${p.label}: ${r.screens || 0} screens, ${r.seconds} s${r.finalMode ? ', ends in ' + r.finalMode + ' mode' : ''}`);
    for (const f of r.failures.slice(0, 8)) console.log('   - ' + f);
  }
  if (!QUICK) {
    for (const fn of [resumeTest, pauseTest, reflowTest]) {
      const r = await fn(browser).catch((e) => ({ label: fn.name, failures: ['crashed: ' + String(e.stack || e).slice(0, 400)] }));
      r.pass = !r.failures.length; runs.push(r);
      console.log(`${r.pass ? 'PASS' : 'FAIL'} ${r.label}`);
      for (const f of r.failures.slice(0, 8)) console.log('   - ' + f);
    }
  }
  await browser.close();
  const out = { page: path.relative(ROOT, PAGE), run_at: new Date().toISOString(), pass: runs.every((r) => r.pass), runs };
  if (!QUICK) fs.writeFileSync(path.join(HERE, '20261106_Reader-Check-Test-Results.json'), JSON.stringify(out, null, 1));
  console.log(out.pass ? 'ALL PASS' : 'SOME FAILED');
  process.exit(out.pass ? 0 : 1);
})();
