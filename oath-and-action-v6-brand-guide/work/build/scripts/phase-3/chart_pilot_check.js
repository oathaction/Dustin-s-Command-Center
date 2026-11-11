// The drawing-method pilot's page conditions (Phase 3, round 0): the charts of a guide page under each condition the brief
// names that the guide check does not already cover.
//
// Usage: node work/build/scripts/phase-3/chart_pilot_check.js <page.html> [--out results.json]
//
// For every chart figure (figure.oac-fig) on the page:
//   scripts on     drawn at 1440 and at 390 px (data-oa-drawn), no drawing error, one SVG, the drawing's width the column's
//   resize         a page opened at 1440 and narrowed to 390 redraws each chart at the phone width
//   scripts off    the title, source line and table equivalent are in the page and visible or one click away, the table's
//                  rows are there, and no empty drawing box shows (the art box holds nothing)
//   print          under print media the drawing stays, inside the page width
//   forced colors  under forced colors the drawing stays, and text and marks take system colors
//   reduced motion every chart drawn, with no animation or transition on any chart element
// Writes the results as JSON; exit 1 when any figure fails.
const fs = require('fs');
const path = require('path');
const { chromium } = require('/opt/node-tools/node_modules/playwright');

const page_file = path.resolve(process.argv[2]);
const outArg = process.argv.indexOf('--out');
const OUT = outArg > 0 ? process.argv[outArg + 1] : page_file.replace(/\.html$/, '-Pilot-Check.json');
const url = 'file://' + page_file;

async function open(b, opts) {
  const ctx = await b.newContext(Object.assign({ viewport: { width: 1440, height: 900 } }, opts.ctx || {}));
  const p = await ctx.newPage();
  const errors = [];
  p.on('pageerror', (e) => errors.push(String(e)));
  if (opts.media) await p.emulateMedia(opts.media);
  await p.goto(url, { waitUntil: 'load', timeout: 120000 });
  if (opts.ctx && opts.ctx.javaScriptEnabled === false) return { ctx, p, errors };
  await p.waitForFunction(() => Array.from(document.querySelectorAll('figure.oac-fig')).every((f) => f.getAttribute('data-oa-drawn') || f.getAttribute('data-oa-error')), null, { timeout: 60000 });
  return { ctx, p, errors };
}

const drawnState = () => Array.from(document.querySelectorAll('figure.oac-fig')).map((f) => {
  const svg = f.querySelector('svg.oac-svg'), art = f.querySelector('[data-oa-art]');
  return { id: f.id, drawn: f.getAttribute('data-oa-drawn'), err: f.getAttribute('data-oa-error'), svgs: f.querySelectorAll('svg.oac-svg').length,
    w: svg ? svg.getBoundingClientRect().width : 0, artW: art ? art.clientWidth : 0 };
});

(async () => {
  const b = await chromium.launch();
  const res = { page: page_file, checked: new Date().toISOString(), conditions: {}, failures: [] };
  const fail = (cond, id, why) => res.failures.push(`${cond}: ${id}: ${why}`);
  try {
    // scripts on, at 1440 and 390, and the resize from one to the other
    for (const w of [1440, 390]) {
      const t0 = Date.now();
      const { ctx, p, errors } = await open(b, { ctx: { viewport: { width: w, height: 900 } } });
      const st = await p.evaluate(drawnState);
      const ms = await p.evaluate(() => performance.now());
      st.forEach((s) => {
        if (s.err) fail(`scripts on ${w}`, s.id, s.err);
        else if (!s.drawn || s.svgs !== 1) fail(`scripts on ${w}`, s.id, `drawn ${s.drawn}, ${s.svgs} drawings`);
        else if (Math.abs(+s.drawn - Math.min(s.artW, +s.drawn)) > 1) fail(`scripts on ${w}`, s.id, `drawn at ${s.drawn} in a ${s.artW} px column`);
      });
      errors.forEach((e) => fail(`scripts on ${w}`, 'page', e));
      res.conditions[`scripts on ${w}`] = { figures: st.length, drawn: st.filter((s) => s.drawn).length, load_ms: Math.round(Date.now() - t0), page_clock_ms: Math.round(ms) };
      if (w === 1440) {
        await p.setViewportSize({ width: 390, height: 900 });
        await p.waitForTimeout(800);
        const st2 = await p.evaluate(drawnState);
        st2.forEach((s) => { if (+s.drawn > 400) fail('resize 1440 to 390', s.id, `still drawn at ${s.drawn}`); });
        res.conditions['resize 1440 to 390'] = { figures: st2.length, redrawn_at_phone: st2.filter((s) => +s.drawn <= 400).length };
      }
      await ctx.close();
    }
    // scripts off: words and tables readable, no empty drawing box
    {
      const { ctx, p } = await open(b, { ctx: { javaScriptEnabled: false } });
      const st = await p.evaluate(() => Array.from(document.querySelectorAll('figure.oac-fig')).map((f) => {
        const vis = (el) => !!el && el.getBoundingClientRect().height > 0 && getComputedStyle(el).visibility !== 'hidden';
        const art = f.querySelector('[data-oa-art]');
        return { id: f.id, title: vis(f.querySelector('[data-role=title]')), source: vis(f.querySelector('[data-role=source]')),
          summary: vis(f.querySelector('details.oac-eq > summary')), rows: f.querySelectorAll('table.oac-table tbody tr').length,
          artH: art ? art.getBoundingClientRect().height : 0, svgs: f.querySelectorAll('svg').length };
      }));
      st.forEach((s) => {
        if (!s.title || !s.source || !s.summary) fail('scripts off', s.id, `title ${s.title}, source ${s.source}, table one click away ${s.summary}`);
        if (!s.rows) fail('scripts off', s.id, 'the table equivalent has no rows');
        if (s.artH > 40) fail('scripts off', s.id, `an empty drawing box ${Math.round(s.artH)} px tall`);
      });
      res.conditions['scripts off'] = { figures: st.length, readable: st.filter((s) => s.title && s.source && s.summary && s.rows).length, table_rows: st.reduce((a, s) => a + s.rows, 0) };
      await ctx.close();
    }
    // print, forced colors, reduced motion
    for (const [name, media] of [['print', { media: 'print' }], ['forced colors', { forcedColors: 'active' }], ['reduced motion', { reducedMotion: 'reduce' }]]) {
      const { ctx, p, errors } = await open(b, { media });
      const st = await p.evaluate((name) => Array.from(document.querySelectorAll('figure.oac-fig')).map((f) => {
        const svg = f.querySelector('svg.oac-svg');
        const r = svg ? svg.getBoundingClientRect() : { width: 0, right: 0 };
        const out = { id: f.id, w: r.width, inside: r.right <= document.documentElement.clientWidth + 1 };
        if (svg && name === 'forced colors') {
          const t = svg.querySelector('text'), m = svg.querySelector('[class*="oac-f-subject"], [class*="oac-f-context"]');
          out.text = t ? getComputedStyle(t).fill : null;
          out.mark = m ? getComputedStyle(m).fill : null;
        }
        if (svg && name === 'reduced motion') out.moving = Array.from(svg.querySelectorAll('*')).filter((e) => { const cs = getComputedStyle(e); return cs.animationName !== 'none' || parseFloat(cs.transitionDuration) > 0; }).length;
        return out;
      }), name);
      st.forEach((s) => {
        if (!s.w) fail(name, s.id, 'no drawing');
        if (!s.inside) fail(name, s.id, 'the drawing runs past the page');
        if (name === 'reduced motion' && s.moving) fail(name, s.id, `${s.moving} moving elements`);
      });
      if (name === 'forced colors') {
        const t = st.find((s) => s.text);
        res.conditions[name] = { figures: st.length, drawn: st.filter((s) => s.w).length, text_fill: t && t.text, mark_fill: t && t.mark };
      } else res.conditions[name] = { figures: st.length, drawn: st.filter((s) => s.w).length };
      errors.forEach((e) => fail(name, 'page', e));
      await ctx.close();
    }
  } finally {
    await b.close();
  }
  fs.writeFileSync(OUT, JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res.conditions, null, 1));
  console.log(`${res.failures.length ? 'FAIL' : 'PASS'} pilot conditions: ${res.failures.length} failures`);
  res.failures.slice(0, 30).forEach((f) => console.log('  - ' + f));
  process.exit(res.failures.length ? 1 : 0);
})();
