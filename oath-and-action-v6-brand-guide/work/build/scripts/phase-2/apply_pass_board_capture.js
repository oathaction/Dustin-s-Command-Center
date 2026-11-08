// Captures for the apply pass changes board (November 7, 2026), run by apply_pass_board_build.py on every build.
// Usage: node work/build/scripts/phase-2/apply_pass_board_capture.js <job.json>
//
// The job names two copies of the chapters page, "before" (the page at commit 3130c5b, saved outside the repository)
// and "after" (the page as it stands now), the views to capture and where to write. The script never edits a page.
//   - A view is a place on one page at 1440 or 390 px, captured at device scale 2 as JPEG after the page's own anchor
//     jump, with the focus ring the shell gives a heading cleared (D2-310). At 1440 px it holds the chapter column, from
//     24 px left of the column to 24 px past it (the rail and the local contents left out); at 390 px the whole phone
//     screen. Both start under the masthead. "find" moves the view to the first element under the anchor whose text
//     holds the words; "offset" moves it further down by that many CSS px; "height" sets the view's height in CSS px,
//     and "until" ends it 12 px above the first block under the anchor that holds those words, such as a rule's "Tokens".
//   - A view with "stage": true is a plate's stage alone, at true size, in a window wide enough for it, with the page's
//     chrome hidden (D2-311), as stage board A captured the proofs.
//   - Each plate in job.plates is an element of an identity designer's plate page, captured at true size as PNG.
//   - job.compare draws two SVG files at several sizes on Newsprint, side by side, and captures the result as PNG.
// It writes the files to job.out and the facts to job.facts: each view's size, the rule, figure and chapter it shows,
// and every anchor of the after page with its words, so the board can link to the published copy.
// Exit code 1 when an anchor or a find text is missing or a capture fails; the facts file still lists what was found.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = job.out;
const Q = job.quality || 80;
fs.mkdirSync(OUT, { recursive: true });
const facts = { captured: new Date().toISOString(), pages: {}, anchors: {}, views: [], plates: [], errors: [] };
for (const [k, p] of Object.entries(job.pages)) facts.pages[k] = { path: p, mtime: fs.statSync(p).mtime.toISOString(), bytes: fs.statSync(p).size };

async function open(ctx, file) {
  const page = await ctx.newPage();
  page.on('pageerror', (e) => facts.errors.push('page error: ' + String(e.message || e).slice(0, 160)));
  await page.goto('file://' + file, { waitUntil: 'networkidle', timeout: 120000 });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
  return page;
}

async function settle(page) {
  await page.evaluate(async () => {
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    const vis = [...document.images].filter((i) => { const r = i.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; });
    await Promise.all(vis.map((i) => (i.decode ? i.decode().catch(() => {}) : null)));
  });
  await page.waitForTimeout(200);
}

// what a view shows, in words the board can print: the rule, the figure's label and the chapter
async function describe(page, anchor) {
  return page.evaluate((a) => {
    const txt = (el) => (el ? el.textContent.replace(/\s+/g, ' ').trim() : '');
    const el = document.getElementById(a);
    if (!el) return null;
    const sec = el.closest('section[id]');
    const rule = el.closest('.rule[id]');
    const fig = el.matches('figure') ? el : null;
    const group = el.closest('.proof-group[id]');
    let figLabel = fig ? txt(fig.querySelector('.plate-label')).replace(/^[✓×→]\s*/, '') : '';
    return {
      chapter: sec ? sec.getAttribute('data-chapter') : null,
      chapter_title: sec ? txt(sec.querySelector('.ch-title .t')) || txt(sec.querySelector('.ch-title')) : '',
      chapter_anchor: sec ? sec.id : null,
      rule: rule ? rule.getAttribute('data-rule') || rule.id.replace(/^rule-(\d\d)-(\d+)$/, '$1.$2') : null,
      rule_title: rule ? txt(rule.querySelector('.rule-h .rt')) || '' : '',
      figure: figLabel,
      proof: group ? txt(group.querySelector('.proof-h')) : '',
      kind: el.matches('section') ? 'chapter' : el.matches('.rule') ? 'rule' : el.matches('figure') ? 'figure' : el.matches('.proof-group') ? 'proof' : 'other',
    };
  }, anchor);
}

async function readAnchors(page) {
  return page.evaluate(() => {
    const txt = (el) => (el ? el.textContent.replace(/\s+/g, ' ').trim() : '');
    const out = {};
    for (const el of document.querySelectorAll('main [id]')) {
      if (el.closest('.plate-stage')) continue;
      const sec = el.closest('section[id]');
      const chapter = sec && sec.getAttribute('data-chapter');
      let label = '', kind = 'other';
      if (el.matches('section.chapter, section.appendix')) { kind = 'chapter'; label = el.getAttribute('data-label') || txt(el.querySelector('.ch-title')); }
      else if (el.matches('.rule')) { kind = 'rule'; label = `Rule ${el.getAttribute('data-rule') || ''} ${txt(el.querySelector('.rule-h .rt'))}`.trim(); }
      else if (el.matches('.proof-group')) { kind = 'proof'; label = 'Identity proofs, ' + txt(el.querySelector('.proof-h')); }
      else if (el.matches('figure.plate')) {
        kind = 'figure';
        const rule = el.closest('.rule[id]');
        const pl = txt(el.querySelector('.plate-label')).replace(/^[✓×→]\s*/, '');
        label = rule ? `Rule ${rule.getAttribute('data-rule')}, ${pl}` : chapter ? `${pl}, in chapter ${chapter}` : `${pl}, in the ${(sec && sec.getAttribute('data-label')) || 'page'}`;
      } else if (el.matches('.rule-group')) { kind = 'group'; label = txt(el.querySelector('.rg-head')); }
      else continue;
      out[el.id] = { kind, chapter: chapter || null, label: label.replace(/[.:]$/, '') };
    }
    return out;
  });
}

// Position the view: the page's own jump to the anchor, then, for find or offset, the element's top under the masthead.
async function place(page, v) {
  await page.evaluate((a) => { location.hash = ''; window.scrollTo(0, 0); location.hash = a; }, v.anchor);
  await page.waitForTimeout(450);
  const r = await page.evaluate(({ anchor, find, offset, until }) => {
    const head = document.querySelector('header.masthead, .masthead');
    const top = head ? Math.ceil(head.getBoundingClientRect().bottom) : 0;
    const root = document.getElementById(anchor);
    if (!root) return { error: `missing anchor #${anchor}` };
    let target = root;
    if (find) {
      const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let n, hit = null;
      const norm = (s) => s.replace(/\s+/g, ' ').replace(/[’‘]/g, "'");
      // the first place a reader can see the words: a visually hidden description (1 by 1 px) is skipped
      const seen = (e) => { const r = e.getBoundingClientRect(); return r.width > 2 && r.height > 2 && !e.closest('.vh, [hidden]'); };
      while ((n = w.nextNode())) { if (norm(n.textContent).includes(norm(find)) && seen(n.parentElement)) { hit = n.parentElement; break; } }
      if (!hit) {   // the words may span elements: the smallest element whose text holds them
        const all = [...root.querySelectorAll('*')].filter((e) => seen(e) && norm(e.textContent).includes(norm(find)));
        hit = all.length ? all[all.length - 1] : null;
      }
      if (!hit) return { error: `no "${find}" under #${anchor}` };
      target = hit;   // the element that holds the words, or its nearest block when that element is inline
      while (target !== root && getComputedStyle(target).display.startsWith('inline')) target = target.parentElement;
    }
    if (find || offset) {
      const y = target.getBoundingClientRect().top + window.scrollY + (offset || 0) - top - 16;
      window.scrollTo(0, Math.max(0, y));
    }
    // "until": the view ends 12 px above the first block under the anchor, below the view's top, that holds these words
    let untilTop = null;
    if (until) {
      const norm = (s) => s.replace(/\s+/g, ' ').replace(/[’‘]/g, "'");
      const cands = [...root.querySelectorAll('*')].filter((e) => !getComputedStyle(e).display.startsWith('inline') &&
        [...e.childNodes].some((n) => n.nodeType === 3 && norm(n.textContent).includes(norm(until))) && e.getBoundingClientRect().top > top + 24);
      if (!cands.length) return { error: `no "${until}" under #${anchor} below the view's top` };
      untilTop = Math.floor(cands[0].getBoundingClientRect().top) - 12;
    }
    return { top, untilTop };
  }, { anchor: v.anchor, find: v.find || null, offset: v.offset || 0, until: v.until || null });
  await settle(page);
  return r;
}

async function clipBox(page, v, width, mastTop, height) {
  return page.evaluate(({ anchor, width, top, height }) => {
    const t = document.getElementById(anchor);
    const body = t.closest('.ch-body') || (t.closest('section[id]') || t).querySelector('.ch-body') || t.closest('section[id]') || t;
    const br = body.getBoundingClientRect();
    let left = 0, right = innerWidth;
    if (width >= 1024) {   // the chapter column, 24 px either side: the rail and the local contents left out
      left = Math.max(0, Math.floor(br.left) - 24);
      right = Math.min(innerWidth, Math.ceil(br.right) + 24);
    }
    const h = Math.min(height, innerHeight - top);
    return { x: left, y: top, width: right - left, height: h, targetTop: Math.round(t.getBoundingClientRect().top) };
  }, { anchor: v.anchor, width, top: mastTop, height });
}

(async () => {
  const browser = await chromium.launch();
  let ok = true;
  // ---------------------------------------------------------------- the after page's anchors
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await open(ctx, job.pages.after);
    facts.anchors = await readAnchors(page);
    await ctx.close();
  }
  // ---------------------------------------------------------------- views in the column or on the phone
  const flow = (job.views || []).filter((v) => !v.stage);
  for (const side of Object.keys(job.pages)) {
    for (const width of [1440, 390]) {
      const vs = flow.filter((v) => v.page === side && v.width === width);
      if (!vs.length) continue;
      const baseH = width >= 1024 ? 900 : 844;
      const ctx = await browser.newContext({ viewport: { width, height: baseH }, deviceScaleFactor: 2 });
      const page = await open(ctx, job.pages[side]);
      for (const v of vs) {
        const mast = await page.evaluate(() => { const h = document.querySelector('header.masthead, .masthead'); return h ? Math.ceil(h.getBoundingClientRect().bottom) : 0; });
        const want = v.height || (baseH - mast);
        const needH = Math.max(baseH, mast + want);
        if (needH !== page.viewportSize().height) { await page.setViewportSize({ width, height: needH }); await page.waitForTimeout(250); }
        const pos = await place(page, v);
        if (pos.error) { facts.errors.push(`${v.key}: ${pos.error} on the ${side} page`); ok = false; continue; }
        const box = await clipBox(page, v, width, pos.top, pos.untilTop ? Math.min(want, pos.untilTop - pos.top) : want);
        const file = `${v.stem}.jpg`;
        try {
          await page.screenshot({ path: path.join(OUT, file), type: 'jpeg', quality: Q, clip: { x: box.x, y: box.y, width: box.width, height: box.height } });
          facts.views.push({ key: v.key, page: side, width, anchor: v.anchor, find: v.find || null, file, css_w: box.width, css_h: box.height, about: await describe(page, v.anchor) });
        } catch (e) { facts.errors.push(`capture ${file}: ${String(e.message || e).slice(0, 160)}`); ok = false; }
      }
      await ctx.close();
    }
  }
  // ---------------------------------------------------------------- plate stages alone, at true size
  const stages = (job.views || []).filter((v) => v.stage);
  for (const side of Object.keys(job.pages)) {
    const vs = stages.filter((v) => v.page === side);
    if (!vs.length) continue;
    const ctx = await browser.newContext({ viewport: { width: 1760, height: 900 }, deviceScaleFactor: 2 });
    const page = await open(ctx, job.pages[side]);
    await page.addStyleTag({ content: '.masthead,.rail,.skip,.menu{visibility:hidden!important}.plate-scroll{overflow:visible!important}' });
    for (const v of vs) {
      const fig = await page.evaluate((a) => { const e = document.getElementById(a); if (!e) return null; const f = e.matches('figure') ? e : e.querySelector('figure.plate[id]'); return f ? f.id : null; }, v.anchor);
      if (!fig) { facts.errors.push(`${v.key}: no plate under #${v.anchor} on the ${side} page`); ok = false; continue; }
      const fit = await page.$(`#${fig} .fit-btn[data-fit="true"]`);
      if (fit && (await fit.getAttribute('aria-pressed')) !== 'true' && await fit.isVisible()) await fit.click();
      const stage = page.locator(`#${fig} .plate-stage`).first();
      await stage.scrollIntoViewIfNeeded();
      await page.waitForTimeout(250);
      const bb = await stage.boundingBox();
      const file = `${v.stem}.jpg`;
      try {
        await stage.screenshot({ path: path.join(OUT, file), type: 'jpeg', quality: Math.min(92, Q + 6) });
        facts.views.push({ key: v.key, page: side, width: 'stage', anchor: v.anchor, file, css_w: Math.round(bb.width), css_h: Math.round(bb.height), about: await describe(page, fig) });
      } catch (e) { facts.errors.push(`capture ${file}: ${String(e.message || e).slice(0, 160)}`); ok = false; }
    }
    await ctx.close();
  }
  // ---------------------------------------------------------------- the identity designer's plates
  for (const p of job.plates || []) {
    const ctx = await browser.newContext({ viewport: { width: p.viewport || 1960, height: 1200 }, deviceScaleFactor: 2 });
    const page = await open(ctx, p.page);
    const loc = page.locator(p.selector).first();
    if (!(await loc.count())) { facts.errors.push(`plate ${p.key}: no ${p.selector} in ${path.basename(p.page)}`); ok = false; await ctx.close(); continue; }
    const fonts = await page.evaluate(() => [...new Set([...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family.replace(/"/g, '')} ${f.weight}`))]);
    const bb = await loc.boundingBox();
    const file = `${p.stem}.png`;
    try {
      await loc.screenshot({ path: path.join(OUT, file), type: 'png' });
      facts.plates.push({ key: p.key, file, css_w: Math.round(bb.width), css_h: Math.round(bb.height), source: path.basename(p.page), selector: p.selector, fonts });
    } catch (e) { facts.errors.push(`plate ${file}: ${String(e.message || e).slice(0, 160)}`); ok = false; }
    await ctx.close();
  }
  // ---------------------------------------------------------------- two SVG files side by side at several sizes
  if (job.compare) {
    const c = job.compare;
    const css = fs.readFileSync(c.tokens, 'utf8');
    const svg = (f) => fs.readFileSync(f, 'utf8').replace(/<title>.*?<\/title>/s, '').replace('<svg ', '<svg aria-hidden="true" ');
    const cell = (f, s) => `<div class="c"><div class="m" style="width:${s}px;height:${s}px">${svg(f).replace('<svg ', `<svg width="${s}" height="${s}" `)}</div><p>${s} px</p></div>`;
    const rows = c.rows.map((r) => `<div class="row"><p class="h">${r.label}</p><div class="cells">${c.sizes.map((s) => cell(r.file, s)).join('')}</div></div>`).join('');
    const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet"><style>${css}
      body{margin:0;background:var(--oa-color-surface-newsprint)}
      #plate{display:inline-block;padding:24px;background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);font-family:Inter,sans-serif}
      .row+.row{margin-top:24px;padding-top:20px;border-top:1px solid var(--oa-color-border-hairline-on-newsprint)}
      .h{margin:0 0 14px;font:600 13px/1.3 Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase}
      .cells{display:flex;align-items:flex-end;gap:48px}.m{line-height:0;color:var(--oa-color-palette-charcoal)}
      .m svg{display:block;--link:var(--oa-color-palette-stone);--lever:var(--oa-color-palette-pillar-red)}
      .c p{margin:10px 0 0;font:400 13px/1.3 Inter,sans-serif;color:var(--oa-color-text-secondary-on-newsprint)}</style></head>
      <body><div id="plate">${rows}</div></body></html>`;
    const ctx = await browser.newContext({ viewport: { width: 1200, height: 900 }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const loc = page.locator('#plate');
    const bb = await loc.boundingBox();
    const file = `${c.stem}.png`;
    await loc.screenshot({ path: path.join(OUT, file), type: 'png' });
    facts.plates.push({ key: c.key, file, css_w: Math.round(bb.width), css_h: Math.round(bb.height), source: 'drawn by the board builder from ' + c.rows.map((r) => path.basename(r.file)).join(' and '), sizes: c.sizes });
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(job.facts, JSON.stringify(facts, null, 1));
  console.log(`captured ${facts.views.length} views and ${facts.plates.length} plates; ${facts.errors.length} errors`);
  for (const e of facts.errors) console.log('  - ' + e);
  process.exit(ok ? 0 : 1);
})();
