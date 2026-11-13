// Board 2 only: S12 drawn as a stacked tile (the data lead's C-M2 third route, the creative director's RS-1), each tile's
// state code and figure on two lines with board 1's arrow beneath, at the drawing widths the guide gives S12's column at a
// 1440 px window (723 px) and a 1024 px window (558 px). Nothing in work/build/ changes: the script copies the chart kit into
// a scratch folder, links the tokens, fonts, data and atlas extract read-only, drops in its own copy of the form, and draws.
//
//   node 20261113_S12-Stacked-Tile-Build.mjs --repo REPO --form FORM.js --spec SPEC.json --work SCRATCH_DIR --out OUT_DIR
//        [--guide STRICT_BUILD.html]
//
// Writes OUT_DIR/20261113_S12-Stacked-Tile-1440.html, -1024.html and -618.html (standalone: fonts, tokens.css and kit.css
// inline, no script; the figure on Newsprint, then on Charcoal) and OUT_DIR/20261113_S12-Stacked-Tile-Measure.json (every
// figure the notes give, tile by tile). With --guide (board 2's fix round, B2-M2 and B2-S8) it also photographs, in
// Chromium: each stacked drawing at its own box; S12's as-built frame at a 1440 and a 1024 px window in that strict build;
// and the stacked tile drawn at 618 px in that same frame at a 1024 px window, the guide's own stage swapped for it in the
// page's memory (the file is never written); and it adds each frame's measured widths and what each frame hides to the
// measure file. The cartographer, November 13, 2026.
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';
const arg = (k) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : null; };
const GUIDE = arg('guide') ? path.resolve(arg('guide')) : null;
const REPO = path.resolve(arg('repo')), FORM = path.resolve(arg('form')), SPEC = path.resolve(arg('spec')), WORK = path.resolve(arg('work')), OUT = path.resolve(arg('out'));
// Measured in Chromium on the main session's strict build of November 13 (15:29 UTC, the committed state, D3-1536): the column
// a wide kit chart that does not scroll (S16, S11) is drawn at, and what S12's 1024 px stage shows of its drawing, at each
// window (the cartographer's notes, "S12 stacked tile"). Read here, not typed into the board.
const PICTURES = [{ key: '1440', window: 1440, width: 723, stage_shows: 943 }, { key: '1024', window: 1024, width: 558, stage_shows: 556 },
  // B2-M2: at a 1024 px window, the stacked tile at the narrowest width it holds (618 px), in the guide's sideways frame
  { key: '618', window: 1024, width: 618, stage_shows: 556, framed: true }];
const COLUMN = { from_window_1024: 'the column grows 3 px for every 4 px of window, 558 px at 1024 to 750 at 1280', window_for_618: 1104,
  note: 'measured on S16 at every window width from 1024 to 1440 (8 px steps, then 1 px steps near 618) on the strict build of November 13, 15:29 UTC' };

// 1. a scratch mirror of the kit: its own folder, the repository's tokens, fonts, data and atlas extract linked read-only
const M = path.join(WORK, 'mirror');
fs.rmSync(M, { recursive: true, force: true });
fs.mkdirSync(path.join(M, 'work/build'), { recursive: true });
fs.mkdirSync(path.join(M, 'work/extract'), { recursive: true });
fs.cpSync(path.join(REPO, 'work/build/chart-kit'), path.join(M, 'work/build/chart-kit'), { recursive: true });
for (const d of ['tokens', 'assets', 'data']) fs.symlinkSync(path.join(REPO, 'work/build', d), path.join(M, 'work/build', d));
fs.symlinkSync(path.join(REPO, 'work/extract/atlas-v7-data.json'), path.join(M, 'work/extract/atlas-v7-data.json'));
const KIT = path.join(M, 'work/build/chart-kit');
fs.mkdirSync(OUT, { recursive: true });
const orig_form = fs.readFileSync(path.join(KIT, 'forms/tile-map-shift-arrows.js'), 'utf8');
fs.writeFileSync(path.join(KIT, 'forms/tile-map-shift-arrows.js'), fs.readFileSync(FORM, 'utf8'));

// 2. the kit, as oa-chart.mjs loads it
const kit = await import(pathToFileURL(path.join(KIT, 'oa-chart.mjs')).href);
const K = globalThis.OAChart, G = globalThis.OAChartGeo;
const C = (await import('module')).createRequire(path.join(KIT, 'oa-chart.mjs'))(path.join(KIT, 'checks.js'));
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8'));
const chk = C.check_spec(K, spec, { spec_path: SPEC });
if (chk.faults.length) { console.error(chk.faults.join('\n')); process.exit(1); }
const rows = chk.rows;

// 3. tile by tile: does each tile hold its code, its figure and its arrow with 1 px to spare?
const states = rows.filter((r) => G.tiles[r.code]);
const max = Math.max(...states.map((r) => Math.abs(r.shift_pts)));
const HL = 8;   // tokens.css --oa-chart-arrow-head-length; an arrow shorter than its head plus 2 px draws its head alone
function measure(d, w) {
  const gap = 6, size = Math.min(80, Math.floor((w - 11 * gap) / 12)), pitch = size + gap;
  const tiles = states.map((r) => {
    const t = G.tiles[r.code], x = t[0] * pitch, y = t[1] * pitch;
    const tx = d.texts.filter((b) => b.role === 'tick' && b.x >= x - 0.5 && b.x <= x + size && b.y >= y - 2 && b.y < y + size);
    const cb = tx.find((b) => b.words === r.code), fb = tx.find((b) => b !== cb && /^\d/.test(b.words));
    const ar = d.marks.find((m) => m.kind === 'arrow' && m.data && m.data.key === r.code);
    const room = { code: r.code, figure: fb ? fb.words : null,
      code_right: +(x + size - (cb.x + cb.w)).toFixed(1), figure_right: +(x + size - (fb.x + fb.w)).toFixed(1),
      code_to_figure: +(fb.y - (cb.y + cb.h)).toFixed(1), figure_to_arrow: +(ar.y - (fb.y + fb.h)).toFixed(1),
      arrow_foot: +(y + size - (ar.y + ar.h)).toFixed(1), arrow_right: +(x + size - (ar.x + ar.w)).toFixed(1),
      arrow_px: +((size - 14) * Math.abs(r.shift_pts) / max).toFixed(1), head_only: (size - 14) * Math.abs(r.shift_pts) / max < HL + 2 };
    room.holds = ['code_right', 'figure_right', 'code_to_figure', 'figure_to_arrow', 'arrow_foot', 'arrow_right'].every((k) => room[k] >= 1);
    return room;
  });
  const least = Object.fromEntries(['code_right', 'figure_right', 'code_to_figure', 'figure_to_arrow', 'arrow_foot', 'arrow_right'].map((k) => [k, Math.min(...tiles.map((t) => t[k]))]));
  return { tile_px: size, arrow_px_per_point: +((size - 14) / max).toFixed(2), drawing: [d.width, d.height], tiles_hold: tiles.filter((t) => t.holds).length, tiles: tiles.length,
    tiles_fail: tiles.filter((t) => !t.holds).map((t) => t.code), least_room_px: least,
    head_only: tiles.filter((t) => t.head_only).map((t) => t.code), layout_guard: d.guard, form_warnings: d.warnings, rows: tiles };
}
// the stacked tile's own test (the form copy's c.stack) at every whole drawing width the guide gives a desk drawing
const fit_from = (() => { const s2 = Object.assign({}, spec, { labels: Object.assign({}, spec.labels, { stack: 'fit' }) });
  for (let w = 480; w <= 869; w++) { const d = K.draw(s2, rows, { width: w, ground: 'newsprint', tokens: kit.TOK.newsprint }); if (d.arrangement !== 'phone' && d.svg.indexOf('oac-f-mag-4') < 0) return w; } return null; })();

// 4. the pictures: the kit's own figure (title, measure line, drawing, notes, source, table fold) with the drawing static
const fonts = { 'Inter': ['inter/20261111_Inter-Latin.woff2', 'inter/20261111_Inter-Latin-Ext.woff2'], 'Inter Tight': ['inter-tight/20261111_Inter-Tight-Latin.woff2', 'inter-tight/20261111_Inter-Tight-Latin-Ext.woff2'] };
const font_css = Object.entries(fonts).map(([f, files]) => files.map((x) => `@font-face{font-family:"${f}";src:url(data:font/woff2;base64,${fs.readFileSync(path.join(REPO, 'work/build/assets/fonts', x)).toString('base64')}) format("woff2");font-weight:100 900;font-display:block}`).join('\n')).join('\n');
const tokens = fs.readFileSync(path.join(REPO, 'work/build/tokens/tokens.css'), 'utf8'), kitcss = fs.readFileSync(path.join(KIT, 'kit.css'), 'utf8');
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const measures = { written: new Date().toISOString(), by: 'cartographer, board 2', spec: path.basename(SPEC), form: path.basename(FORM),
  what: 'S12 as a stacked tile: each tile sets its state code (bold) over its figure, with board 1’s arrow beneath on board 1’s scale rule (tile size less 14 px for the largest shift); key, United States arrow, lists and frame as board 1. Board only: nothing in work/build/ changed.',
  leaves_out: 'The phone drawing (unchanged: gray steps under 480 px), the sideways-scrolling stage and its hint, the data island and every script; the table is the kit’s fold, closed.',
  stacked_fits_from_drawing_px: fit_from, guide_column: COLUMN, pictures: [] };
const SVGS = {}, DRAWS = {};
for (const pic of PICTURES) {
  const secs = [];
  SVGS[pic.key] = {};
  for (const g of ['newsprint', 'charcoal']) {
    const d = K.draw(spec, rows, { width: pic.width, ground: g, tokens: kit.TOK[g] });
    SVGS[pic.key][g] = d.svg;
    if (g === 'newsprint') DRAWS[pic.key] = d;
    if (g === 'newsprint') measures.pictures.push(Object.assign({ key: pic.key, window: pic.window, drawing_px: pic.width, in_a_frame: !!pic.framed }, pic.framed ? {} : { stage_shows_px_of_1024: pic.stage_shows }, measure(d, pic.width)));
    const fig = K.figure(spec, rows, { id: `s12-stacked-${pic.window}-${g}`, svg: d.svg, art_attrs: ' data-oa-static', guide: true }).replace('<figure class="oac-fig"', '<figure class="oac-fig" data-oa-static');
    secs.push(`<section class="oa-surface-${g} pic" id="${g}" data-ground="${g}"><p class="pic-k">Board 2 only, not in the guide: S12 as a stacked tile, drawn at ${pic.width} px, ${pic.framed ? 'the narrowest width at which every tile holds, which the guide would show in a frame that scrolls sideways at a 1024 px window' : 'the width the guide gives this chart at a ' + pic.window + ' px window'}. ${g === 'newsprint' ? 'Newsprint' : 'Charcoal'}.</p><div class="col" style="width:${pic.width}px">${fig}</div></section>`);
  }
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>S12 Stacked Tile ${pic.window}</title>
<style>${font_css}</style><style>${tokens}</style><style>${kitcss}</style>
<style>body{margin:0}.pic{padding:32px;box-sizing:border-box;width:${pic.width + 64}px}.pic-k{margin:0 0 16px;font:400 13px/1.4 Inter,sans-serif;color:var(--oa-chart-color-secondary)}.col>.oac-fig{margin:0}</style>
</head><body>
${secs.join('\n')}
</body></html>
`;
  fs.writeFileSync(path.join(OUT, `20261113_S12-Stacked-Tile-${pic.key}.html`), html);
}
// 5. the stage it is compared with: board 1's drawing at 1024 px, drawn by the kit's own form
fs.writeFileSync(path.join(KIT, 'forms/tile-map-shift-arrows.js'), orig_form);
{ const req = (await import('module')).createRequire(path.join(KIT, 'oa-chart.mjs')), fp = path.join(KIT, 'forms/tile-map-shift-arrows.js');
  delete req.cache[fp]; req(fp); }   // the kit's own form registers again, in place of the stacked copy
const spec0 = JSON.parse(fs.readFileSync(path.join(REPO, 'work/build/chart-kit/specs/s12.json'), 'utf8'));
const stage_size = Math.min(80, Math.floor((1024 - 66) / 12));
const sd = K.draw(spec0, rows, { width: 1024, ground: 'newsprint', tokens: kit.TOK.newsprint });
measures.stage_1024 = { drawing_px: 1024, tile_px: stage_size, drawing: [sd.width, sd.height], arrow_px_per_point: +((stage_size - 14) / max).toFixed(2),
  head_only: states.filter((r) => (stage_size - 14) * Math.abs(r.shift_pts) / max < HL + 2).map((r) => r.code),
  note: 'Board 1’s drawing, which the guide draws at 1024 px in a frame that scrolls sideways, drawn here by the kit’s own form' };
// 6. B2-M2 and B2-S8 (board 2's fix round): photographs and the frames' measures, from the strict build --guide names
if (GUIDE) {
  const req = (await import('module')).createRequire(import.meta.url);
  const { chromium } = req('/opt/node-tools/node_modules/playwright');
  const browser = await chromium.launch();
  const shots = [];
  const G2 = (g) => (g === 'newsprint' ? 'Newsprint' : 'Charcoal');
  const shot = async (loc, name, what) => { await loc.screenshot({ path: path.join(OUT, name) }); const b = await loc.boundingBox(); shots.push({ file: name, what, css_px: [Math.round(b.width), Math.round(b.height)] }); };
  try {
    // a) each stacked drawing at its own box, from the standalone pages (1x, true size)
    for (const [key, label, what] of [['1440', '1440-Drawing', 'the stacked tile at 723 px, the guide’s drawing width at a 1440 px window, cropped to its drawing'],
      ['618', '618-Drawing', 'the stacked tile at 618 px, the narrowest width at which every tile holds, its whole drawing'],
      ['1024', '558-Drawing', 'the stacked tile forced into 558 px, the guide’s column at a 1024 px window: every arrow runs past its tile']]) {
      const ctx = await browser.newContext({ viewport: { width: 1000, height: 900 } }); const p = await ctx.newPage();
      await p.goto(pathToFileURL(path.join(OUT, `20261113_S12-Stacked-Tile-${key}.html`)).href, { waitUntil: 'load' });
      await p.evaluate(() => document.fonts.ready);
      for (const g of ['newsprint', 'charcoal']) await shot(p.locator(`#${g} svg.oac-svg`), `20261113_S12-Stacked-Tile-${label}-${G2(g)}.png`, what + ', ' + g);
      await ctx.close();
    }
    // b) the strict build: S12's frame as built at both windows, and at 1024 px the stacked tile at 618 px swapped into that frame
    measures.frames = {};
    for (const win of [1440, 1024]) {
      const ctx = await browser.newContext({ viewport: { width: win, height: 900 } }); const p = await ctx.newPage();
      await p.goto(pathToFileURL(GUIDE).href, { waitUntil: 'load', timeout: 180000 });
      await p.evaluate(() => document.fonts.ready);
      await p.evaluate(async () => { document.getElementById('oac-s-14-s12').scrollIntoView(); await new Promise((r) => setTimeout(r, 500)); if (window.OAChart && OAChart.draw_all) OAChart.draw_all(); await new Promise((r) => setTimeout(r, 500)); });
      const art = p.locator('#oac-s-14-s12 [data-oa-art]');
      const read = () => p.evaluate(() => { const a = document.querySelector('#oac-s-14-s12 [data-oa-art]'), cs = getComputedStyle(a);
        return { box_px: +a.getBoundingClientRect().width.toFixed(2), viewport_px: a.clientWidth, drawing_px: a.scrollWidth, scroll_range_px: a.scrollWidth - a.clientWidth,
          edges_px: [parseFloat(cs.borderLeftWidth), parseFloat(cs.borderRightWidth)], height_px: Math.round(a.getBoundingClientRect().height), stage: a.getAttribute('data-oa-stage') }; });
      const ground = (g) => p.evaluate((g) => { const st = document.querySelector('#oac-s-14-s12').closest('.plate-stage'); st.className = st.className.replace(/oa-surface-\w+/, 'oa-surface-' + g); st.setAttribute('data-surface', g); }, g);
      for (const g of ['newsprint', 'charcoal']) { await ground(g); await shot(art, `20261113_S12-Stage-${win}-Frame-${G2(g)}.png`, `S12 as built, board 1’s 1024 px drawing in its frame at a ${win} px window, as a reader sees it before scrolling, ${g}`); }
      await ground('newsprint');
      measures.frames[`stage_${win}`] = Object.assign({ window: win, what: 'S12 as built: board 1’s drawing at 1024 px in its frame' }, await read());
      if (win === 1024) {
        for (const g of ['newsprint', 'charcoal']) {
          await ground(g);
          await p.evaluate(({ svg }) => { const a = document.querySelector('#oac-s-14-s12 [data-oa-art]'); const old = a.querySelector('svg.oac-svg'); const t = document.createElement('div'); t.innerHTML = svg;
            old.replaceWith(t.firstElementChild); a.setAttribute('data-oa-stage', '618'); a.setAttribute('aria-label', 'The drawing at its full width, 618 px'); a.scrollLeft = 0; }, { svg: SVGS['618'][g] });
          await shot(art, `20261113_S12-Stacked-Tile-1024-Frame-${G2(g)}.png`, `the stacked tile at 618 px in S12’s frame at a 1024 px window, as a reader would see it before scrolling, ${g}`);
        }
        await ground('newsprint');
        measures.frames.stacked_618_in_1024 = Object.assign({ window: 1024, what: 'the stacked tile drawn at 618 px in S12’s frame, swapped in the page’s memory' }, await read());
      }
      await ctx.close();
    }
  } finally { await browser.close(); }
  // what each frame leaves out of view until the reader scrolls: tiles past its viewport, and words that run past it
  const hidden = (tile, vp, d) => { const pitch = tile + 6, cut = [], gone = [];
    for (const [code, t] of Object.entries(G.tiles)) { const x = t[0] * pitch; if (x >= vp) gone.push(code); else if (x + tile > vp) cut.push(code); }
    const words = d.texts.filter((b) => b.x + b.w > vp).map((b) => b.words);
    // a tile the edge cuts still reads where its code, figure and arrow all end inside the viewport
    const reads = cut.filter((code) => { const t = G.tiles[code], x = t[0] * pitch, y = t[1] * pitch;
      const inside = d.texts.filter((b) => b.x >= x - 0.5 && b.x < x + tile && b.y >= y - 2 && b.y < y + tile).concat(d.marks.filter((m) => m.kind === 'arrow' && m.data && m.data.key === code));
      return inside.length >= 2 && inside.every((b) => b.x + b.w <= vp); });
    return { tiles_out_of_view: gone.sort(), tiles_cut_by_the_edge: cut.sort(), cut_tiles_whose_code_figure_and_arrow_show: reads.sort(), words_past_the_edge: words }; };
  Object.assign(measures.frames.stage_1440, hidden(stage_size, measures.frames.stage_1440.viewport_px, sd));
  Object.assign(measures.frames.stage_1024, hidden(stage_size, measures.frames.stage_1024.viewport_px, sd));
  const p618 = measures.pictures.find((x) => x.key === '618');
  Object.assign(measures.frames.stacked_618_in_1024, hidden(p618.tile_px, measures.frames.stacked_618_in_1024.viewport_px, DRAWS['618']),
    { arrows_past_their_tile: p618.tiles_fail });
  measures.frames.note = 'box_px is the frame as laid out (the column); viewport_px is what shows inside its two 1 px edges; scroll_range_px is how far the reader scrolls (the drawing less the viewport). Measured in Chromium on the strict build named in guide_build; nothing was written to it.';
  measures.guide_build = GUIDE.split('/scratchpad/')[1] + ', ' + fs.statSync(GUIDE).size + ' bytes, written ' + fs.statSync(GUIDE).mtime.toISOString();
  measures.photographs = shots;
}
fs.writeFileSync(path.join(OUT, '20261113_S12-Stacked-Tile-Measure.json'), JSON.stringify(measures, null, 1) + '\n');
console.log('stage drawing', sd.width, 'by', sd.height, sd.svg.indexOf('y="' ) > 0 ? '' : '', 'stacked copy gone:', !/STACK/.test(K.forms['tile-map-shift-arrows'].draw.toString()));
for (const p of measures.pictures) console.log(`${p.window} px window, ${p.drawing_px} px drawing, ${p.tile_px} px tiles: ${p.tiles_hold} of ${p.tiles} hold; least room ${JSON.stringify(p.least_room_px)}; ${p.head_only.length} arrows a head alone; guard ${p.layout_guard.length}`);
if (measures.frames) for (const [k, f] of Object.entries(measures.frames)) if (f.window) console.log(k, 'box', f.box_px, 'viewport', f.viewport_px, 'scrolls', f.scroll_range_px, 'out of view', f.tiles_out_of_view.join(' '), '| cut', f.tiles_cut_by_the_edge.join(' '), '| cut but read', f.cut_tiles_whose_code_figure_and_arrow_show.join(' '));
console.log('stacked tile fits from a drawing of', fit_from, 'px; stage tiles', stage_size, 'px,', measures.stage_1024.head_only.length, 'arrows a head alone');
