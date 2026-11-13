// Board 2 only: S12 drawn as a stacked tile (the data lead's C-M2 third route, the creative director's RS-1), each tile's
// state code and figure on two lines with board 1's arrow beneath, at the drawing widths the guide gives S12's column at a
// 1440 px window (723 px) and a 1024 px window (558 px). Nothing in work/build/ changes: the script copies the chart kit into
// a scratch folder, links the tokens, fonts, data and atlas extract read-only, drops in its own copy of the form, and draws.
//
//   node 20261113_S12-Stacked-Tile-Build.mjs --repo REPO --form FORM.js --spec SPEC.json --work SCRATCH_DIR --out OUT_DIR
//
// Writes OUT_DIR/20261113_S12-Stacked-Tile-1440.html and -1024.html (standalone: fonts, tokens.css and kit.css inline, no
// script; the figure on Newsprint, then on Charcoal) and OUT_DIR/20261113_S12-Stacked-Tile-Measure.json (every figure the
// notes give, tile by tile). The cartographer, November 13, 2026.
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';
const arg = (k) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : null; };
const REPO = path.resolve(arg('repo')), FORM = path.resolve(arg('form')), SPEC = path.resolve(arg('spec')), WORK = path.resolve(arg('work')), OUT = path.resolve(arg('out'));
// Measured in Chromium on the main session's strict build of November 13 (15:29 UTC, the committed state, D3-1536): the column
// a wide kit chart that does not scroll (S16, S11) is drawn at, and what S12's 1024 px stage shows of its drawing, at each
// window (the cartographer's notes, "S12 stacked tile"). Read here, not typed into the board.
const PICTURES = [{ window: 1440, width: 723, stage_shows: 943 }, { window: 1024, width: 558, stage_shows: 556 }];
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
for (const pic of PICTURES) {
  const secs = [];
  for (const g of ['newsprint', 'charcoal']) {
    const d = K.draw(spec, rows, { width: pic.width, ground: g, tokens: kit.TOK[g] });
    if (g === 'newsprint') measures.pictures.push(Object.assign({ window: pic.window, drawing_px: pic.width, stage_shows_px_of_1024: pic.stage_shows }, measure(d, pic.width)));
    const fig = K.figure(spec, rows, { id: `s12-stacked-${pic.window}-${g}`, svg: d.svg, art_attrs: ' data-oa-static', guide: true }).replace('<figure class="oac-fig"', '<figure class="oac-fig" data-oa-static');
    secs.push(`<section class="oa-surface-${g} pic" id="${g}" data-ground="${g}"><p class="pic-k">Board 2 only, not in the guide: S12 as a stacked tile, drawn at ${pic.width} px, the width the guide gives this chart at a ${pic.window} px window. ${g === 'newsprint' ? 'Newsprint' : 'Charcoal'}.</p><div class="col" style="width:${pic.width}px">${fig}</div></section>`);
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
  fs.writeFileSync(path.join(OUT, `20261113_S12-Stacked-Tile-${pic.window}.html`), html);
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
fs.writeFileSync(path.join(OUT, '20261113_S12-Stacked-Tile-Measure.json'), JSON.stringify(measures, null, 1) + '\n');
console.log('stage drawing', sd.width, 'by', sd.height, sd.svg.indexOf('y="' ) > 0 ? '' : '', 'stacked copy gone:', !/STACK/.test(K.forms['tile-map-shift-arrows'].draw.toString()));
for (const p of measures.pictures) console.log(`${p.window} px window, ${p.drawing_px} px drawing, ${p.tile_px} px tiles: ${p.tiles_hold} of ${p.tiles} hold; least room ${JSON.stringify(p.least_room_px)}; ${p.head_only.length} arrows a head alone; guard ${p.layout_guard.length}`);
console.log('stacked tile fits from a drawing of', fit_from, 'px; stage tiles', stage_size, 'px,', measures.stage_1024.head_only.length, 'arrows a head alone');
