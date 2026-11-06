// Captures for stage board A (November 6, 2026), run by stage_a_board_build.py on every build.
// Usage: node work/build/scripts/phase-2/stage_a_board_capture.js <job.json>
//
// The job names the chapters page, the views to capture and where to write. The script reads the page as it is now:
//   - every chapter's number, title, instruction line and rules, the proof groups, and every anchor a decision may cite;
//   - each view at 1440 and 390 px, device scale 2, after the page's own anchor jump: at 1440 the chapter column under
//     the masthead (the rail left out), at 390 the whole phone screen under the masthead;
//   - each comparison plate of the wordmark proofs, the stage alone, at true size and device scale 2;
//   - the letter spacing the page renders for the tagline, a chapter title and a rule title, measured at 1440 px.
// It writes JPEG captures to job.out and the facts to job.facts. It never edits the page.
// Exit code 1 when an anchor is missing or a capture fails; the facts file still lists what was found.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const PAGE = job.page;
const OUT = job.out;
const Q = job.quality || 80;
fs.mkdirSync(OUT, { recursive: true });
const facts = { page: PAGE, page_mtime: fs.statSync(PAGE).mtime.toISOString(), captured: new Date().toISOString(),
  chapters: [], anchors: {}, views: [], proofs: null, tracking: null, errors: [] };

async function open(ctx) {
  const page = await ctx.newPage();
  page.on('pageerror', (e) => facts.errors.push('page error: ' + String(e.message || e).slice(0, 160)));
  await page.goto('file://' + PAGE, { waitUntil: 'networkidle', timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
  return page;
}

// the page's own anchor jump, as a reader's link lands; the heading the shell focuses is blurred so no ring shows
async function jump(page, anchor) {
  await page.evaluate((a) => { location.hash = ''; window.scrollTo(0, 0); location.hash = a; }, anchor);
  await page.waitForTimeout(450);
  await page.evaluate(async () => {
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    const vis = [...document.images].filter((i) => { const r = i.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; });
    await Promise.all(vis.map((i) => (i.decode ? i.decode().catch(() => {}) : null)));
  });
  await page.waitForTimeout(150);
}

async function readFacts(page) {
  return page.evaluate(() => {
    const txt = (el) => (el ? el.textContent.replace(/\s+/g, ' ').trim() : '');
    // like txt, with the shell's Illustrative label kept as a marker the board sets as its own label
    const rich = (el) => { if (!el) return ''; const c = el.cloneNode(true); c.querySelectorAll('.illus').forEach((i) => i.replaceWith('{{illus}}')); return txt(c); };
    const chapters = [...document.querySelectorAll('section.chapter[data-chapter]')].map((s) => ({
      number: s.getAttribute('data-chapter'), anchor: s.id, label: s.getAttribute('data-label') || '',
      title: txt(s.querySelector('.ch-title .t')) || txt(s.querySelector('.ch-title')),
      instruction: txt(s.querySelector('.ch-head .instr')),
      intro: [...s.querySelectorAll('.ch-head > .intro')].map(txt),
      rules: [...s.querySelectorAll('.rule[id][data-rule]')].map((r) => ({ id: r.getAttribute('data-rule'), anchor: r.id, title: txt(r.querySelector('.rule-h .rt')) || txt(r.querySelector('h3')) })),
    }));
    // every anchor a decision may cite, with the words a link should carry; specimen internals left out
    const anchors = {};
    for (const s of chapters) {
      anchors[s.anchor] = { kind: 'chapter', chapter: s.number, label: `Chapter ${s.number} ${s.title}` };
      for (const r of s.rules) anchors[r.anchor] = { kind: 'rule', chapter: s.number, label: `Rule ${r.id} ${r.title}` };
    }
    for (const el of document.querySelectorAll('main [id], .colophon[id]')) {
      if (anchors[el.id] || el.closest('.plate-stage')) continue;
      const sec = el.closest('section[id]');
      const chapter = sec && sec.getAttribute('data-chapter');
      let label = '';
      if (el.matches('.rule-group')) label = txt(el.querySelector('.rg-head'));
      else if (el.matches('.proof-group')) label = 'Wordmark proofs, ' + txt(el.querySelector('.proof-h'));
      else if (el.matches('section')) label = el.getAttribute('data-label') || txt(el.querySelector('h1, h2'));
      else if (el.matches('.closer')) label = txt(el.querySelector('h3')) + (sec ? ', ' + (sec.getAttribute('data-label') || '') : '');
      else if (el.matches('tr')) label = txt(el.querySelector('th')) || txt(el).slice(0, 60);
      else if (el.matches('figure.plate')) label = txt(el.querySelector('.plate-label')) + (sec ? ', ' + (sec.getAttribute('data-label') || '') : '');
      else if (el.matches('h1, h2, h3, h4')) continue;
      else continue;
      anchors[el.id] = { kind: el.matches('.proof-group') ? 'proof' : el.matches('section') ? 'section' : 'other', chapter: chapter || null, label: label.replace(/[.:]$/, '') };
    }
    const app = document.querySelector('section.appendix#proofs');
    const proofs = app ? {
      anchor: app.id, title: txt(app.querySelector('.ch-title')), instruction: txt(app.querySelector('.ch-head .instr')),
      intro: [...app.querySelectorAll('.ch-head > .intro')].map(rich),
      groups: [...app.querySelectorAll('.proof-group[id]')].map((g) => {
        const fig = g.querySelector('figure.plate');
        const stage = fig && fig.querySelector('.plate-stage');
        const notes = [...g.children].filter((c) => c.tagName === 'P' && !c.classList.contains('return')).map(rich).filter(Boolean);
        return { anchor: g.id, title: txt(g.querySelector('.proof-h')), notes,
          plate_label: txt(fig && fig.querySelector('.plate-label')),
          size: fig ? ((fig.querySelector('.plate-size') || {}).getAttribute ? fig.querySelector('.plate-size').getAttribute('data-true') || txt(fig.querySelector('.plate-size')) : '') : '',
          caption: rich(fig && fig.querySelector('.plate-cap')),
          alt: stage ? (stage.getAttribute('aria-label') || '') : '', figure: fig ? fig.id : null,
          specimen: stage ? stage.getAttribute('data-specimen') : null, width: stage ? +stage.getAttribute('data-width') || null : null };
      }),
    } : null;
    return { chapters, anchors, proofs };
  });
}

// letter spacing as rendered, in percent of the font size, for the three styles DR-95 changed
async function measureTracking(page) {
  return page.evaluate(() => {
    const m = (sel) => {
      const el = document.querySelector(sel); if (!el) return null;
      const cs = getComputedStyle(el); const size = parseFloat(cs.fontSize); const ls = parseFloat(cs.letterSpacing) || 0;
      return { selector: sel, text: el.textContent.replace(/\s+/g, ' ').trim().slice(0, 80), size_px: +size.toFixed(2), spacing_px: +ls.toFixed(3), percent: +(100 * ls / size).toFixed(2), family: cs.fontFamily, weight: cs.fontWeight };
    };
    return { title: m('.cover .tagline'), section: m('section.chapter .ch-title'), h3: m('section.chapter .rule .rule-h') };
  });
}

(async () => {
  const browser = await chromium.launch();
  let ok = true;
  // ---------------------------------------------------------------- facts, tracking and the 1440 views
  for (const width of job.widths || [1440, 390]) {
    const height = width >= 1024 ? 900 : 844;
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 2 });
    const page = await open(ctx);
    if (width === (job.widths || [1440])[0]) {
      const f = await readFacts(page);
      Object.assign(facts, f);
      facts.tracking = await measureTracking(page);
      facts.tracking.width = width;
    }
    for (const v of job.views || []) {
      if (v.opening) v.anchor = await page.evaluate((n) => { const s = document.querySelector(`section.chapter[data-chapter="${n}"]`); return s ? s.id : null; }, v.chapter);
      if (!v.anchor) { facts.errors.push(`no chapter ${v.chapter} on the page`); ok = false; continue; }
      const exists = await page.evaluate((a) => !!document.getElementById(a), v.anchor);
      if (!exists) { facts.errors.push(`missing anchor #${v.anchor} (chapter ${v.chapter})`); ok = false; continue; }
      await jump(page, v.anchor);
      const box = await page.evaluate(({ anchor, width }) => {
        const head = document.querySelector('header.masthead, .masthead');
        const top = head ? Math.ceil(head.getBoundingClientRect().bottom) : 0;
        const t = document.getElementById(anchor);
        const sec = t.closest('section[id]') || t;
        const sr = sec.getBoundingClientRect();
        const toc = sec.querySelector('.local-toc');
        let left = 0, right = innerWidth;
        if (width >= 1024) {             // the chapter column and its local contents, without the rail
          const rail = document.querySelector('nav.rail');
          const rr = rail && getComputedStyle(rail).display !== 'none' ? rail.getBoundingClientRect() : null;
          left = Math.max(0, Math.floor(sr.left) - 24, rr && rr.width ? Math.ceil(rr.right) + 1 : 0);
          right = Math.min(innerWidth, Math.ceil(Math.max(sr.right, toc ? toc.getBoundingClientRect().right : 0)) + 24);
        }
        return { x: left, y: top, width: right - left, height: innerHeight - top, targetTop: Math.round(t.getBoundingClientRect().top) };
      }, { anchor: v.anchor, width });
      const file = `${v.stem || v.key}-${width}.jpg`;
      try {
        await page.screenshot({ path: path.join(OUT, file), type: 'jpeg', quality: Q, clip: { x: box.x, y: box.y, width: box.width, height: box.height } });
        facts.views.push({ key: v.key, chapter: v.chapter, anchor: v.anchor, width, file, css_w: box.width, css_h: box.height, target_top: box.targetTop });
      } catch (e) { facts.errors.push(`capture ${file}: ${String(e.message || e).slice(0, 160)}`); ok = false; }
    }
    await ctx.close();
  }
  // ---------------------------------------------------------------- the comparison plates, at true size
  if (job.proofs && facts.proofs) {
    const widest = Math.max(1440, ...facts.proofs.groups.map((g) => (g.width || 0) + 240));
    const ctx = await browser.newContext({ viewport: { width: widest, height: 900 }, deviceScaleFactor: 2 });
    const page = await open(ctx);
    // the page chrome stays out of the way of a plate taller than the screen; plates stay at true size
    await page.addStyleTag({ content: '.masthead,.rail,.skip,.menu{visibility:hidden!important}.plate-scroll{overflow:visible!important}' });
    for (const g of facts.proofs.groups) {
      if (!g.figure) { facts.errors.push(`proof ${g.anchor} has no plate`); ok = false; continue; }
      const fit = await page.$(`#${g.figure} .fit-btn[data-fit="true"]`);
      if (fit) { const pressed = await fit.getAttribute('aria-pressed'); if (pressed !== 'true') await fit.click(); }
      const stage = page.locator(`#${g.figure} .plate-stage`).first();
      await stage.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      const bb = await stage.boundingBox();
      const words = g.anchor.replace(/^proofs-/, '').split('-').map((w) => w.charAt(0).toUpperCase() + w.slice(1));
      const file = `${job.proof_prefix || 'proof-'}${words.join('-')}.jpg`;
      try {
        await stage.screenshot({ path: path.join(OUT, file), type: 'jpeg', quality: Math.min(92, Q + 6) });
        g.file = file; g.css_w = Math.round(bb.width); g.css_h = Math.round(bb.height);
      } catch (e) { facts.errors.push(`capture ${file}: ${String(e.message || e).slice(0, 160)}`); ok = false; }
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(job.facts, JSON.stringify(facts, null, 1));
  console.log(`captured ${facts.views.length} views and ${facts.proofs ? facts.proofs.groups.filter((g) => g.file).length : 0} plates; ${facts.errors.length} errors`);
  for (const e of facts.errors) console.log('  - ' + e);
  process.exit(ok ? 0 : 1);
})();
