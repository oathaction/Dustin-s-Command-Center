// Build the combined reader check page (Oath & Action Edition 06, Phase 2, November 10, 2026).
// Questions: work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md (the editor; DR-143, DR-148, D2-493).
// Built from the first check's tooling (work/boards/phase-2/reader-check/, which stays as it is).
//
// Run from the project root:
//   node work/boards/phase-2/reader-check-2/build_reader_check_2.js               (captures, assets, answer key, page)
//   node work/boards/phase-2/reader-check-2/build_reader_check_2.js --no-capture  (reuse the captures already in img/)
//
// What it writes, all inside this folder:
//   img/                                  the stimuli, under neutral file names. Drawings, charts, the link card and
//                                         the bill rows are captured at phone width; symbols, marks and the drawings
//                                         in the rows are copies of the finals with titles, descriptions and ids
//                                         stripped and their colors baked in, so nothing a reader can open names what
//                                         a symbol means.
//   20261110_Reader-Check-2.html          the page (content only: the publish step wraps it in the skeleton)
//   20261110_Reader-Check-2-Answer-Key.json   what each stimulus is meant to say. The page never carries it.
// The page source is reader_check_2_template.html; this script injects CONFIG into it.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const HERE = __dirname;
const ROOT = path.resolve(HERE, '../../../..');
const IMG = path.join(HERE, 'img');
const PAGE = path.join(HERE, '20261110_Reader-Check-2.html');
const KEY = path.join(HERE, '20261110_Reader-Check-2-Answer-Key.json');
const TEMPLATE = path.join(HERE, 'reader_check_2_template.html');
const FIRST_KEY = JSON.parse(fs.readFileSync(path.join(ROOT, 'work/boards/phase-2/reader-check/20261106_Reader-Check-Answer-Key.json'), 'utf8'));
const CAPTURE = !process.argv.includes('--no-capture');
const LOG = path.join(HERE, '20261110_Reader-Check-2-Capture-Log.json');   // what the captures read; never published

const ATLAS = path.join(ROOT, 'work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer.html');
const EXPLAINER = path.join(ROOT, 'work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html');
const STRETCH = path.join(ROOT, 'work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html');
const ED = JSON.parse(fs.readFileSync(path.join(ROOT, 'work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json'), 'utf8'));
const VOICE = JSON.parse(fs.readFileSync(path.join(ROOT, 'work/boards/phase-2/voice/20261106_Voice-Rules-Content.json'), 'utf8'));
const LABELS = JSON.parse(fs.readFileSync(path.join(ROOT, 'work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json'), 'utf8'));
const V7 = path.join(ROOT, 'work/extract/atlas-v7-data.json');
const A = path.join(ROOT, 'work/build/assets');
const CL = path.join(A, 'civic-line-v6');          // the Civic Line set in use (D2-716)
const PF = path.join(A, 'pillar-icons/svg');       // the pillar fits in use (DR-179)
const ID = path.join(A, 'identity');
const INK = '#121212', RED = '#E63946', STONE = '#5D636D';   // Charcoal; Pillar Red, which is signature red on Newsprint; Stone

const WIDTHS = [390, 360];   // phone widths: 390 px and up gets the 390 capture, narrower phones the 360 capture
const DPR = 2;

// ------------------------------------------------------------------------------------------------ step 3, symbols
// The four symbols the step tests. Change this one line to switch, and the codes, files, key and leak check follow.
//   Dustin's answer (DR-189, November 10, 2026): CL-025 Congress, CL-073 Testify, CL-074 Contact an Official, R-02
//   the editor's first four, built and tested before his answer: ['CL-032', 'CL-063', 'R-02', 'CL-015']
const SYMBOLS = ['CL-025', 'CL-073', 'CL-074', 'R-02'];
// What counts as a pass, from the editor's table. A symbol with no row here builds, and its key entry says the
// editor's row is still to come and reads the answer against the meaning sentence meanwhile (DR-189).
const SYMBOL_PASS = {
  'CL-032': { pass: 'Names local news, a local paper or reporters', partly: 'Names news or a newspaper in general' },
  'CL-063': { pass: 'Names what everyday needs cost a household, such as groceries or bills', partly: 'Names shopping, prices or groceries alone' },
  'R-02': { pass: 'Names ranking candidates or ranked or numbered choices on a ballot', partly: 'Names voting or a ballot alone' },
  'CL-015': { pass: 'Names money going into politics or elections, such as campaign money or donations', partly: 'Names money or voting alone' },
};

// ------------------------------------------------------------------------------------------------ step 2 (kept)
const LOOP_DEFS = {
  R10: { view: 'loop-r10', selector: '[data-view-root="loop-r10"] svg.cyc.ph', from: 'the R10 loop close-up' },
  B4: { view: 'loops', selector: '[data-view-root="loops"] svg.cyc.ph[aria-label^="B4,"]', from: 'the "All loops" catalog card' },
};
const LOOP_WORDS = {
  R10: {
    steps: [
      { value: 'step1', label: '1. raises', from: 'Safe seats', to: 'Seats settled in the primary' },
      { value: 'step2', label: '2. lowers', from: 'Seats settled in the primary', to: 'Risk of losing office' },
      { value: 'step3', label: '3. lowers', from: 'Risk of losing office', to: 'Incumbents control election rules' },
      { value: 'step4', label: '4. raises', from: 'Incumbents control election rules', to: 'Safe seats' },
    ],
    boxes: ['Safe seats', 'Seats settled in the primary', 'Risk of losing office', 'Incumbents control election rules'],
  },
  B4: {
    steps: [
      { value: 'top', label: 'Top arrow, lowers', from: 'Quality of public services', to: 'Risk of losing office' },
      { value: 'right', label: 'Right arrow, raises', from: 'Risk of losing office', to: 'Incumbents defeated' },
      { value: 'left', label: 'Left arrow, raises', from: 'Incumbents defeated', to: 'Quality of public services' },
    ],
    boxes: ['Quality of public services', 'Risk of losing office', 'Incumbents defeated'],
  },
};
const CHARTS = [
  { code: 'S02', page: EXPLAINER, view: 'newsprint', section: 'newsprint-s02', board: 'Data viz board 3, Explainer, Newsprint view' },
  { code: 'S11', page: STRETCH, view: 'newsprint', section: 'newsprint-s11', board: 'Data viz stretch test, Newsprint view' },
  { code: 'S14', page: STRETCH, view: 'newsprint', section: 'newsprint-s14', board: 'Data viz stretch test, Newsprint view' },
];
const PAIRS = ['W02', 'W10', 'W11'];

// ------------------------------------------------------------------------------------------------ steps 4 to 8 (new)
const PILLARS = [['CL-019', 'Explain'], ['CL-020', 'Track'], ['CL-021', 'Connect'], ['CL-022', 'Act']];
const BILLS = { slash: 'Records request fees', square: 'Parking meter fees', dot: 'Public meeting notice' };
const ARTICLE = 'For an investor-owned utility, the state public utility commission sets rates in a rate case; for public power and cooperatives, a city council, utility board or co-op board does. Rates recover the cost of power plants, fuel, transmission lines and local wires, and investor-owned utilities also earn a regulated return on what they invest.';
// chapter 04's end mark (s-04-6-correct, Rule 04.6): the pixel fit at 1x, the 16 px master elsewhere, at these sizes
const ENDS = [
  { px: 17, fit: { file: '20261109_Amp-B-14px-End-Mark-Fit-B.svg', w: 13, h: 13, va: '0' }, smooth: { w: 12.37, h: 14.13, va: '-0.883px' } },
  { px: 15, fit: { file: '20261109_Amp-B-12px-End-Mark-Fit-B.svg', w: 11, h: 11, va: '0' }, smooth: { w: 10.91, h: 12.47, va: '-0.779px' } },
];
const FOOT_TEXT = 'A country that answers to its people.';   // chapter 08's footer place sets the lockmark beside the tagline

// ------------------------------------------------------------------------------------------------ helpers
const rel = (p) => path.relative(ROOT, p);
const clFile = (id, ed) => { const dir = path.join(CL, ed === 'red' ? 'red-black' : 'black'); const f = fs.readdirSync(dir).find((n) => n.includes(`-${id}-`) && n.endsWith(ed === 'red' ? '-Red-Black.svg' : '-Black.svg') && (ed === 'red' || !n.endsWith('-Red-Black.svg'))); if (!f) throw new Error(`no ${ed || 'black'} file for ${id} in ${rel(dir)}`); return path.join(dir, f); };
const fitFile = (id, px) => { const f = fs.readdirSync(PF).find((n) => n.includes(`-${id}-`) && n.includes(`-${px}px-Black.svg`)); if (!f) throw new Error(`no ${px} px fit for ${id}`); return path.join(PF, f); };
function cleanSvg(svg, colors) {
  let s = svg.replace(/<\?xml[^>]*\?>\s*/g, '').replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<title>[\s\S]*?<\/title>/g, '').replace(/<desc>[\s\S]*?<\/desc>/g, '')
    .replace(/\s(id|data-[a-z-]+|aria-[a-z-]+|focusable)="[^"]*"/g, '');
  for (const [from, to] of colors) s = s.split(from).join(to);
  if (/url\(#|href="#/.test(s)) throw new Error('an SVG kept an internal reference after its ids were stripped');
  if (/var\(|currentColor/.test(s)) throw new Error('an SVG kept an unbaked color: ' + (s.match(/var\([^)]*\)|currentColor/) || [])[0]);
  return s.trim() + '\n';
}
function setSize(svg, w, h) { return svg.replace(/<svg\b([^>]*)>/, (m, a) => `<svg${a.replace(/\s(width|height)="[^"]*"/g, '')} width="${w}" height="${h}">`); }
function put(name, svg) { fs.writeFileSync(path.join(IMG, name), svg); return 'img/' + name; }
function pngSize(p) { const b = fs.readFileSync(p); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; }
function plainBefore(s) { return s.replace(/\[-([\s\S]*?)-\]/g, '$1').replace(/\[\+([\s\S]*?)\+\]/g, ''); }
function plainAfter(s) { return s.replace(/\[-([\s\S]*?)-\]/g, '').replace(/\[\+([\s\S]*?)\+\]/g, '$1'); }
const label = (id) => LABELS.rows.find((r) => r.id === id) || {};
const ONE = [['currentColor', INK], ['var(--amp,#E63946)', INK], ['var(--lever,#E63946)', INK], ['var(--link,#5D636D)', INK]];

// ------------------------------------------------------------------------------------------------ captures
async function capture() {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const log = [];
  const titles = {};
  // the guide, built fresh, for the link card and chapter 11's bills
  const tmp = fs.mkdtempSync(path.join(process.env.TMPDIR || os.tmpdir(), 'rc2-guide-'));
  const guide = path.join(tmp, 'guide.html');
  execFileSync('python3', ['-I', path.join(ROOT, 'work/build/scripts/phase-2/guide_build.py'), '--quiet', '--out', guide], { stdio: 'pipe' });
  for (const W of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: W, height: 900 }, deviceScaleFactor: DPR });
    const page = await ctx.newPage();
    // the atlas: the overview's first screens and the two loops, as in the first check
    await page.goto('file://' + ATLAS + '#overview', { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({ content: 'header.mast, nav.tabs, nav.ak-crumbs { display: none !important; }' });
    await page.waitForTimeout(500);
    const ov = await page.evaluate(() => {
      const root = document.querySelector('[data-view-root="overview"]');
      const top = root.querySelector('p.eyebrow').getBoundingClientRect().top + scrollY;
      const svg = root.querySelector('svg.sysp').getBoundingClientRect();
      return { x: svg.left - 2, y: top - 16, width: svg.width + 4, height: svg.bottom + scrollY - top + 20 };
    });
    await page.screenshot({ path: path.join(IMG, `drawing-overview-${W}.png`), clip: ov, fullPage: true });
    log.push(['overview', W, ov.width]);
    for (const k of ['R10', 'B4']) {
      const d = LOOP_DEFS[k];
      await page.goto('file://' + ATLAS + '#' + d.view, { waitUntil: 'networkidle' });
      await page.addStyleTag({ content: 'header.mast, nav.tabs, nav.ak-crumbs { display: none !important; }' });
      await page.waitForTimeout(500);
      await page.locator(d.selector).scrollIntoViewIfNeeded();
      const box = await page.evaluate((sel) => { const r = document.querySelector(sel).getBoundingClientRect(); return { x: r.left - 2, y: r.top + scrollY - 12, width: r.width + 4, height: r.height + 24 }; }, d.selector);
      await page.screenshot({ path: path.join(IMG, `drawing-${k.toLowerCase()}-${W}.png`), clip: box, fullPage: true });
      // the words printed on the drawing must still match the choices (System 1's finishing pass, DR-121)
      // the drawing breaks box names over lines, so the words are compared with their spaces taken out
      const words = await page.evaluate((sel) => document.querySelector(sel).textContent.replace(/\s+/g, ''), d.selector);
      for (const b of LOOP_WORDS[k].boxes) if (!words.includes(b.replace(/\s+/g, ''))) throw new Error(`${k}: the drawing no longer prints "${b}"`);
      for (const s of LOOP_WORDS[k].steps) if (!words.includes(s.label.replace(/^(Top|Right|Left) arrow, /, '').replace(/\s+/g, ''))) throw new Error(`${k}: the drawing no longer prints "${s.label}"`);
      log.push([k, W, box.width]);
    }
    // the charts, as in the first check; each title is read so the key can say whether it changed since November 6
    for (const c of CHARTS) {
      await page.goto('file://' + c.page + '#' + c.view, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.addStyleTag({ content: `#${c.section} figure > .fnotes, #${c.section} figure > .srcrow, #${c.section} figure > details { display: none !important; }` });
      await page.waitForTimeout(500);
      const fig = page.locator(`#${c.section} figure`);
      await fig.scrollIntoViewIfNeeded();
      titles[c.code] = await fig.evaluate((el) => el.innerText.replace(/\s+/g, ' ').trim());
      await fig.screenshot({ path: path.join(IMG, `chart-${c.code.toLowerCase()}-${W}.png`) });
      log.push([c.code, W, 0]);
    }
    await ctx.close();
  }
  // From the guide: a stimulus is cloned out of its plate into a box of its own at the top of the page, inside an
  // element carrying its specimen's id, so the specimen's scoped style still applies, and captured there.
  {
    // the link card's face alone, at its own 1200 by 630 (the page shows it at the phone column's width)
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    await page.goto('file://' + guide, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => {
      const card = [...document.querySelectorAll('[data-specimen="s-proofs-social"] .oai-s-newsprint')].find((e) => e.style.width === '1200px');
      const box = document.createElement('div');
      box.setAttribute('data-specimen', 's-proofs-social'); box.id = 'rc2-lift';
      box.style.cssText = 'position:absolute;left:0;top:0;z-index:2147483647;line-height:0';
      box.append(card.cloneNode(true)); document.body.append(box); window.scrollTo(0, 0);
    });
    await page.waitForTimeout(300);
    await page.locator('#rc2-lift > div').screenshot({ path: path.join(IMG, 'card.png') });
    log.push(['card', 1200, 1200]);
    await ctx.close();
  }
  {
    // chapter 11's list of five bills (Rule 11.5) at its own 360 px, and three bills' rows of step marks alone
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: DPR });
    const page = await ctx.newPage();
    await page.goto('file://' + guide, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const lifted = async (fn, arg, name) => {
      await page.evaluate(({ fn, arg }) => {
        const src = document.querySelector('[data-specimen="s-11-5-correct"]');
        // eslint-disable-next-line no-new-func
        const el = new Function('src', 'arg', fn)(src, arg);
        if (!el) throw new Error('nothing to lift for ' + arg);
        document.querySelectorAll('#rc2-lift').forEach((x) => x.remove());
        const box = document.createElement('div');
        box.setAttribute('data-specimen', 's-11-5-correct'); box.id = 'rc2-lift';
        box.style.cssText = 'position:absolute;left:0;top:0;z-index:2147483647;background:var(--oa-color-surface-newsprint);width:' + (arg ? 'auto' : '360px');
        box.append(el.cloneNode(true)); document.body.append(box); window.scrollTo(0, 0);
      }, { fn, arg });
      await page.waitForTimeout(200);
      await page.locator('#rc2-lift').screenshot({ path: path.join(IMG, name) });
    };
    await lifted("return src.querySelector('.sx-pc');", null, 'bills-list.png');
    const rowFn = "const li = [...src.querySelectorAll('li.sx-row')].find((r) => r.querySelector('.sx-bill').textContent.includes(arg)); return li && li.querySelector('.sx-mkw');";
    let n = 1;
    for (const [k, bill] of Object.entries(BILLS)) { await lifted(rowFn, bill, `bills-row-${n}.png`); log.push(['bill row ' + k, 0, 0]); n++; }
    const words = await page.evaluate(() => document.querySelector('[data-specimen="s-11-5-correct"]').innerText);
    for (const b of Object.values(BILLS)) if (!words.includes(b)) throw new Error(`chapter 11's list no longer holds "${b}"`);
    await ctx.close();
  }
  fs.rmSync(tmp, { recursive: true, force: true });
  await browser.close();
  fs.writeFileSync(LOG, JSON.stringify({ captured: new Date().toISOString(), chart_figures: titles }, null, 1));
  return log;
}

// ------------------------------------------------------------------------------------------------ vector assets
function vectorAssets() {
  const icons = SYMBOLS.map((id, i) => {
    const f = clFile(id);
    const src = put(`icon-${i + 1}.svg`, cleanSvg(fs.readFileSync(f, 'utf8'), []));
    return { code: `i${i + 1}`, id, src, source: rel(f), label: label(id).label, word: label(id).civic_line_word, meaning: label(id).meaning };
  });
  // R-46, red-black edition, at 96 px
  const houseFile = clFile('R-46', 'red');
  const house = { src: put('drawing-5.svg', setSize(cleanSvg(fs.readFileSync(houseFile, 'utf8'), []), 96, 96)), w: 96, h: 96, source: rel(houseFile) };
  // the four in the rows: the 24 px fit (1x) and the master (2x) one color; the masters at 48, Track's in two colors
  const rows = PILLARS.map(([id, word], i) => {
    const g = `g${i + 1}`;
    return {
      word,
      fit24: put(`${g}-24.svg`, setSize(cleanSvg(fs.readFileSync(fitFile(id, 24), 'utf8'), []), 24, 24)),
      master: put(`${g}.svg`, cleanSvg(fs.readFileSync(clFile(id), 'utf8'), [])),
      two: word === 'Track' ? put(`${g}-two.svg`, cleanSvg(fs.readFileSync(clFile(id, 'red'), 'utf8'), [])) : null,
      sources: { fit24: rel(fitFile(id, 24)), master: rel(clFile(id)), two: word === 'Track' ? rel(clFile(id, 'red')) : null },
    };
  });
  // the sheet of 12 marks, one color; 9 to 12 draw fit B on a 1x screen and the master on a 2x screen
  const MARKS = [
    { code: 'm1', src: 'wordmark/20261028_Wordmark-16px-Master.svg', name: "Wordmark, today's width, 16 px master", w: 152, h: 16, row: 1 },
    { code: 'm2', src: 'ampersand/20261028_Amp-B-16px-Master.svg', name: 'Ampersand B, 16 px master', w: 14, h: 16, row: 1 },
    { code: 'm3', src: 'lockmark/20261028_Lockmark-16px-Master.svg', name: 'Lockmark, 16 px master, in use (DR-181)', w: 16, h: 16, row: 1 },
    ...PILLARS.map(([id, word], i) => ({ code: `m${4 + i}`, fit: fitFile(id, 16), name: `${word} (${id}), the 16 px pixel fit (DR-179)`, w: 16, h: 16, row: 1 })),
    { code: 'm8', src: 'lockmark/20261109_Lockmark-24px-Master-Outline.svg', name: 'Lockmark, the rebuilt 24 px master (DR-181)', w: 24, h: 24, row: 2 },
    ...PILLARS.map(([id, word], i) => ({ code: `m${9 + i}`, fit: fitFile(id, 24), master: clFile(id), name: `${word} (${id}) at 24 px: fit B on a 1x screen, the master on a 2x screen (DR-179)`, w: 24, h: 24, row: 2 })),
  ];
  const marks = MARKS.map((m, i) => {
    const file = m.src ? path.join(ID, m.src) : m.fit;
    const out = { code: m.code, src: put(`mark-${i + 1}.svg`, setSize(cleanSvg(fs.readFileSync(file, 'utf8'), ONE), m.w, m.h)), w: m.w, h: m.h, row: m.row, name: m.name, source: rel(file) };
    if (m.master) { out.src2x = put(`mark-${i + 1}-b.svg`, setSize(cleanSvg(fs.readFileSync(m.master, 'utf8'), ONE), m.w, m.h)); out.source2x = rel(m.master); }
    return out;
  });
  // the bottom of a page: the rebuilt 24 px master with its red lever
  const footFile = path.join(ID, 'lockmark/20261109_Lockmark-24px-Master-Outline.svg');
  const foot = { src: put('foot.svg', setSize(cleanSvg(fs.readFileSync(footFile, 'utf8'), [['currentColor', INK], ['var(--lever,#E63946)', RED], ['var(--link,#5D636D)', STONE]]), 24, 24)), w: 24, h: 24, text: FOOT_TEXT, source: rel(footFile) };
  // the article's ending: the end mark's fit at its size and the 16 px master, as chapter 04 sets them
  const smoothFile = path.join(ID, 'ampersand/20261028_Amp-B-16px-Master.svg');
  const smooth = put('t-16.svg', cleanSvg(fs.readFileSync(smoothFile, 'utf8'), ONE));
  const ends = ENDS.map((e) => ({ px: e.px, fit: { src: put(`t-${e.fit.h + 1}.svg`, cleanSvg(fs.readFileSync(path.join(ID, 'ampersand', e.fit.file), 'utf8'), ONE)), w: e.fit.w, h: e.fit.h, va: e.fit.va, source: rel(path.join(ID, 'ampersand', e.fit.file)) },
    smooth: { src: smooth, w: e.smooth.w, h: e.smooth.h, va: e.smooth.va, source: rel(smoothFile) } }));
  return { icons, house, rows, marks, foot, ends };
}

// ------------------------------------------------------------------------------------------------ config, checks, key
function imgPair(stem) {
  const out = {};
  for (const W of WIDTHS) { const p = path.join(IMG, `${stem}-${W}.png`); const s = pngSize(p); out[W === 390 ? 'lg' : 'sm'] = { src: `img/${stem}-${W}.png`, w: s.w / DPR, h: s.h / DPR }; }
  return out;
}
function oneImg(file, scale, widths) {   // one capture shown at a set width on each phone size
  const s = pngSize(path.join(IMG, file));
  const at = (w) => ({ src: 'img/' + file, w, h: +(s.h * w / s.w).toFixed(1) });
  return widths ? { lg: at(widths[0]), sm: at(widths[1]) } : { lg: at(s.w / scale), sm: at(s.w / scale) };
}

function build() {
  const v = vectorAssets();
  const rules = Object.fromEntries(VOICE.groups.flatMap((g) => g.rules).map((r) => [r.id, r]));
  const parts = ['X', 'A', 'B', 'C', 'D', 'E', 'EC', 'TC'].map((id) => ED.parts.find((p) => p.id === id).plain_name);
  const model = JSON.parse(fs.readFileSync(V7, 'utf8'));
  const pw = model.pathways.find((p) => p.id === 'PW03') || model.pathways[2];
  if (!pw.short_answer.includes(ARTICLE)) throw new Error('the article lines are no longer in Atlas V7 PW03 word for word');
  const CONFIG = {
    version: '20261110-1',
    exposure: { drawing: 10, icon: 10, card: 10, row: 10, marks: 10, foot: 10, chart: 15 },
    overview: { img: imgPair('drawing-overview'), parts },
    loops: ['R10', 'B4'].map((k) => ({ code: k.toLowerCase(), img: imgPair(`drawing-${k.toLowerCase()}`), steps: LOOP_WORDS[k].steps, boxes: LOOP_WORDS[k].boxes })),
    icons: v.icons.map((ic) => ({ code: ic.code, src: ic.src })),
    card: { img: oneImg('card.png', 1, [358, 328]) },
    house: { src: v.house.src, w: v.house.w, h: v.house.h },
    rows: { words: PILLARS.map(([, w]) => w), r24: v.rows.map((r) => ({ word: r.word, fit: r.fit24, master: r.master })), r48: v.rows.map((r) => ({ word: r.word, master: r.master, two: r.two })), current24: 'Connect', current48: 'Track' },
    bills: { rows: { slash: oneImg('bills-row-1.png', DPR), square: oneImg('bills-row-2.png', DPR), dot: oneImg('bills-row-3.png', DPR) }, list: oneImg('bills-list.png', DPR), names: Object.values({ a: 'Public meeting notice', b: 'School bus contracts', c: 'Library hours', d: 'Records request fees', e: 'Parking meter fees' }) },
    marks: v.marks.map((m) => ({ code: m.code, src: m.src, src2x: m.src2x || null, w: m.w, h: m.h, row: m.row })),
    foot: { src: v.foot.src, w: v.foot.w, h: v.foot.h, text: v.foot.text },
    article: { text: ARTICLE, ends: v.ends.map((e) => ({ px: e.px, fit: { src: e.fit.src, w: e.fit.w, h: e.fit.h, va: e.fit.va }, smooth: { src: e.smooth.src, w: e.smooth.w, h: e.smooth.h, va: e.smooth.va } })) },
    charts: CHARTS.map((c) => ({ code: c.code, img: imgPair(`chart-${c.code.toLowerCase()}`) })),
    pairs: PAIRS.map((id) => ({ code: id, before: plainBefore(rules[id].before), after: plainAfter(rules[id].after) })),
  };

  const tpl = fs.readFileSync(TEMPLATE, 'utf8');
  if (!tpl.includes('/*CONFIG*/{}')) throw new Error('template has no /*CONFIG*/ slot');
  const html = tpl.replace('/*CONFIG*/{}', JSON.stringify(CONFIG));

  // The leak check: the page never names what a stimulus means. Symbols' labels, words and IDs; R-46; the identity's
  // names; and "party" outside the questions and choices that ask about party.
  const banned = [...v.icons.flatMap((ic) => [ic.label, ic.word, ic.id]), 'Expand the House', 'R-46', 'end mark', 'lockmark', 'pillar', 'Pillar Red', 'Ranked', 'Local news', 'Local Reporting', 'Political Money', 'Essential Costs', 'Cost of essentials'].filter(Boolean);
  for (const w of banned) if (html.toLowerCase().includes(w.toLowerCase())) throw new Error(`the page names "${w}"`);
  const partyOk = ['Does it seem to favor a party or side?', 'Does this card seem to favor a party or side?', 'Does this drawing seem to favor a party or side?', 'Seats one party holds', 'It shows a party or side', 'It marks one party', "['party', "];   // the last is the choices' code, which the editor names for the record
  let rest = html; for (const ok of partyOk) rest = rest.split(ok).join('');
  if (/part(y|ies)\b/i.test(rest)) throw new Error('the page says "party" outside the questions that ask about it: ' + rest.match(/.{40}part(y|ies)\b.{20}/i)[0]);
  if (/Oath\s*(&|&amp;|and)\s*Action/i.test(html)) throw new Error('page text names the brand');
  if (/—/.test(html)) throw new Error('page text carries an em dash');
  for (const f of fs.readdirSync(IMG).filter((n) => n.endsWith('.svg'))) {
    const t = fs.readFileSync(path.join(IMG, f), 'utf8');
    if (/<title|<desc|\sid=|data-|Oath|Civic/i.test(t)) throw new Error(`img/${f} still carries a title, id or name`);
  }
  fs.writeFileSync(PAGE, html);

  // ---------------------------------------------------------------- answer key
  const titles = fs.existsSync(LOG) ? JSON.parse(fs.readFileSync(LOG, 'utf8')).chart_figures : {};
  const charts = FIRST_KEY.charts.map((c) => {
    const now = titles[c.code] || '';
    const same = now.includes(c.title);
    return { ...c, title_check: now ? (same ? 'The title printed today matches the first check\'s, word for word.' : 'CHANGED since November 6: the figure now reads: ' + now.slice(0, 600)) : 'not read' };
  });
  const changed = charts.filter((c) => /^CHANGED/.test(c.title_check)).map((c) => c.code);
  const favors = { right: 'no', to_dustin: ['left', 'right'] };
  const key = {
    title: 'Combined reader check answer key',
    date: 'November 10, 2026',
    page: rel(PAGE),
    questions: 'work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md (the editor)',
    private: 'Never publish this file with the page. The page carries neutral codes only (i1 to i4, m1 to m12).',
    group_reading: 'For each question: how many readers chose each answer, and what they typed. A question needs a look when fewer than half the readers who answered it pass. Any reader who reads a party into a drawing or a page goes to Dustin with their own words, whatever the count.',
    overview: FIRST_KEY.overview,
    loops: { r10: FIRST_KEY.loops.r10, b4: FIRST_KEY.loops.b4, choice_values: FIRST_KEY.loops.choice_values, words_check: 'The box words the choices quote were read from today\'s drawings when the page was built, and all match.' },
    icons: v.icons.map((ic) => ({ code: ic.code, file: ic.src, id: ic.id, chapter_10_label: ic.label, civic_line_word: ic.word, meaning: ic.meaning, source: ic.source,
      pass: (SYMBOL_PASS[ic.id] || {}).pass || 'The editor\'s row is still to come (DR-189). Until it lands, read the answer against the meaning sentence above.', partly: (SYMBOL_PASS[ic.id] || {}).partly || 'The editor\'s row is still to come (DR-189).' })),
    symbols_in_use: SYMBOLS,
    red_card: { stimulus: 'img/card.png, the link card face from the guide\'s proofs (s-proofs-social), 1200 by 630, shown 358 px wide on a 390 px phone and 328 px on a 360 px phone, Newsprint', look_seconds: 10,
      questions: { favors: { ...favors, partial: [], why: 'Pillar Red stays the lead color (DR-114), and red is the color many readers link to one party. The card is the brand at its most common size in a reader\'s day, with red in two places and nothing about party in its words.' },
        why: { shown_after: ['left', 'right', 'unsure'], pass: 'none (optional)', finding: 'A Yes or Not sure whose follow-up names the red, the color or the ampersand is the finding DR-114 asks for.' } } },
    house: { stimulus: v.house.src + ', R-46 Expand the House of Representatives, Red Black edition, 96 px, Newsprint, no label', source: v.house.source, look_seconds: 10,
      questions: { red: { right: 'added', partial: [], to_dustin: ['party'], shuffled: 'the first four', why: 'DR-152 keeps R-46 as drawn and asks this check whether readers take its red seats, at one side of a chamber, as a party\'s. Chapter 10 always sets R-46 beside its label, "Expand the House of Representatives", so showing it bare is the hard case: a pass here holds for the page.' },
        favors: { ...favors, why: 'As red_card:favors, for a drawing with red on one side.' } } },
    row_24: { stimulus: 'The compact row under 48 px at phone width: the four icons at 24 px, one color, each with its word, Explain, Track, Connect, Act joined by arrows; Connect bold and underlined; no red. Fit B under 2 device pixels per CSS pixel, the master from 2 (DR-179, the guide\'s switch)', sources: v.rows.map((r) => r.sources), look_seconds: 10,
      questions: { current: { right: 'Connect', partial: [], why: 'Chapter 09 marks the current pillar by underlining its word at every size, with no red under 48 px (DR-111, R10). This asks whether the underline alone tells a reader where they are.' } } },
    row_48: { stimulus: 'The section opener at 48 px, stacked in one column, Track underlined and Track\'s icon in its Red Black edition (the pin and the magnifier\'s handle); the others one color', look_seconds: 10,
      questions: { current: { right: 'Track', partial: [] }, red: { right: 'current', partial: [], to_dustin: ['party'], shuffled: 'the first four', why: 'From 48 px, red on the current icon is a second sign beside the underline (DR-111, DR-133). This asks whether readers take that red to mean "you are here".' } } },
    steps_slash: { stimulus: 'img/bills-row-1.png: the row for Records request fees (H.99004) from s-11-5-correct, alone: 1 done, 2 never happened (slash), 3 done, 4 now, 5 and 6 not yet', question: 'meaning', right: 'skipped', partial: [], shuffled: 'the first four', why: 'A step that never happened keeps its number with a slash (DR-108), and chapter 11 draws each state as a shape so the set reads without color (Rule 11.2). The list prints the reason in words beside the row; this asks what the shape says before the words do.' },
    steps_square: { stimulus: 'img/bills-row-2.png: the row for Parking meter fees (S.99005), alone: 1 to 5 done, 6 a filled square', question: 'meaning', right: 'stopped', partial: [], shuffled: 'the first four', why: 'A bill that stops ends its line on a square, and a signed bill reads as law in words (DR-108, Rule 11.3). A reader who takes the square for law reads the opposite of the record.' },
    steps_dot: { stimulus: 'img/bills-row-3.png: the row for Public meeting notice (H.99001), alone: 1 done, 2 now with the small red take-part disc, 3 to 6 not yet', question: 'meaning', right: 'take_part', partial: ['unsure'], to_dustin: ['party'], watch: ['error'], shuffled: 'the first four', why: 'The take-part mark is one of the three things that may claim a view\'s working red (Rule 05.3), and chapter 11 decides which yields when an error mark sits beside it. A reader who sees an error or a party here shows where the words must carry the meaning.' },
    steps_list: { stimulus: 'img/bills-list.png: chapter 11\'s whole list of five bills at 360 px with every status line, the key and the Illustrative label', question: 'take_part', right: 'Public meeting notice', partial: [], why: 'The tracker\'s job is to show a reader where a decision stands and when they can act. This asks whether a newcomer finds the one bill open to them in a list of five.' },
    steps_names: { stimulus: 'the same list', question: 'clear', right: ['all', 'most'], follow_up: { which: { shown_after: ['most', 'few', 'unsure'], pass: 'none (optional)' } }, why: 'DR-108 gave the tracker six plain step names in place of nine stages. This is the first time a reader outside the studio judges them.' },
    marks: v.marks.map((m) => ({ code: m.code, file: m.src, file_2x: m.src2x || null, mark: m.name, size_px: `${m.w} by ${m.h}`, source: m.source, source_2x: m.source2x || null, pass: 'clear' })),
    marks_note: 'One color, Charcoal #121212 on Newsprint, at true CSS size, in two rows, 16 px then 24 px. m9 to m12 draw fit B on screens under 2 device pixels per CSS pixel and the master from 2, as the guide does; the record\'s device_pixel_ratio says which drawing each reader saw. A mark half the readers call blurry or can\'t tell goes to the identity designer with each reader\'s screen sharpness.',
    foot_24: { editor_code: 'lockmark_24 (the page records it as foot_24, since the page may not print the word lockmark)', stimulus: v.foot.src + ', the rebuilt 24 px master with its red lever and Stone links, beside the footer line "' + FOOT_TEXT + '" at phone width on Newsprint', source: v.foot.source, look_seconds: 10, question: 'seen', right: 'dots', partial: [], shuffled: 'the first three', why: 'DR-145 rebuilt the 24 px master so each node and the lever draw as one outline, because the old file could part into stripes. This asks whether readers see the grid of nodes it is meant to show.' },
    end_17: { stimulus: 'The two lines below in 17 px Inter on Newsprint at the phone column\'s width, with ampersand B half an em after the final period in the text\'s ink, at the text\'s cap height: fit B at 14 px (13 by 13) at exactly 1 device pixel per CSS pixel, the 16 px master at 12.37 by 14.13 elsewhere (s-04-6-correct, Rule 04.6, DR-180)', text: ARTICLE, text_source: 'Atlas V7, pathway PW03, short answer, sentences 2 and 3, word for word (checked at build)', sources: v.ends[0],
      questions: { meaning: { right: 'ends', partial: ['sign'], shuffled: 'the first four' }, clear: { right: ['clear', 'barely'] }, sits: { right: 'fits', partial: [], shuffled: 'the first three' } },
      why: 'DR-130 set the end mark at the text\'s cap height because B at 16 px read louder than the line it ends, and DR-142 and DR-180 drew it on whole pixels at 14 and 12 px so its edges stay crisp. These questions ask whether readers see it, whether it sits quietly, and whether they read it as the end.' },
    end_15: { stimulus: 'The same lines in 15 px text, with fit B at 12 px (11 by 11) at 1x and the 16 px master at 10.91 by 12.47 elsewhere', sources: v.ends[1], questions: { clear: { right: ['clear', 'barely'] }, sits: { right: 'fits', partial: [], shuffled: 'the first three' } } },
    charts,
    charts_note: changed.length ? `Chart titles changed since November 6: ${changed.join(', ')}. Their findings above are the first key's and need the data viz owner's check.` : 'Every chart title printed today matches the first check\'s, so the titles and findings stand.',
    pairs: FIRST_KEY.pairs,
    favors_questions: 'red_card:favors, house:favors and each chart\'s favors pass on "no"; "left" and "right" go to Dustin with the reader\'s own words, whatever the count.',
    record_fields: {
      path: FIRST_KEY.record_fields.path.replace('reader-check', 'reader-check-2'),
      run: 'initials, mode ("saved" or "copy"), mode_note, started_at, finished_at (ISO, UTC), viewport_width, device_pixel_ratio (window.devicePixelRatio at the start), resumed, position, orders, items',
      orders: 'loops, icons (i codes in order), charts, pairs (per pair: which of A and B was the before), choices (for each question that shuffles its choices, the codes in the order shown)',
      items: 'overview, loop_r10, loop_b4, icon_i1 to icon_i4, red_card (favors, why), house (red, favors), row_24 (current), row_48 (current, red), steps_slash (meaning), steps_square (meaning), steps_dot (meaning), steps_list (take_part), steps_names (clear, which), marks (m1 to m12), foot_24 (seen; the editor\'s lockmark_24), end_17 (meaning, clear, sits), end_15 (clear, sits), chart_S02, chart_S11, chart_S14, pair_W02, pair_W10, pair_W11. Each: show_again, shown_seconds, again_seconds, interrupted, load_failed, questions: { <q>: { answer, seconds, skipped } }. A follow-up that was not asked is absent.',
    },
  };
  fs.writeFileSync(KEY, JSON.stringify(key, null, 1) + '\n');
  return { CONFIG, v, changed };
}

(async () => {
  fs.mkdirSync(IMG, { recursive: true });
  if (CAPTURE) {
    for (const f of fs.readdirSync(IMG)) fs.rmSync(path.join(IMG, f));
    const log = await capture();
    for (const [what, W, w] of log) console.log(`captured ${what}${W ? ' at ' + W : ''}${w ? ': ' + Math.round(w) + ' px wide' : ''}`);
  } else {
    for (const f of fs.readdirSync(IMG).filter((n) => n.endsWith('.svg'))) fs.rmSync(path.join(IMG, f));
  }
  const out = build();
  const files = fs.readdirSync(IMG).filter((f) => !f.startsWith('.'));
  const bytes = files.reduce((a, f) => a + fs.statSync(path.join(IMG, f)).size, 0);
  console.log(`wrote ${rel(PAGE)} (${fs.statSync(PAGE).size} bytes), ${rel(KEY)}, ${files.length} files in img/ (${(bytes / 1048576).toFixed(2)} MB)`);
  console.log(`symbols in step 3: ${SYMBOLS.join(', ')}${SYMBOLS.some((s) => !SYMBOL_PASS[s]) ? ' (the key marks the pass lines the editor owes)' : ''}`);
  if (out.changed.length) console.log(`chart titles changed since November 6: ${out.changed.join(', ')}`);
})().catch((e) => { console.error(e); process.exit(1); });
