// Build the reader check page (Oath & Action Edition 06, Phase 2, November 6, 2026).
// Brief: work/handoffs/phase-2/20261106_Reader-Check-Brief.md (DR-68, DR-84 to DR-87).
//
// Run from the project root:
//   node work/boards/phase-2/reader-check/build_reader_check.js            (captures, assets, answer key, page)
//   node work/boards/phase-2/reader-check/build_reader_check.js --no-capture   (reuse the captures already in img/)
//
// What it writes, all inside this folder:
//   img/                     the stimuli. Drawings and charts are captured from the boards at phone width and twice
//                            size; icons, 16 px marks and mastheads are copies of the vector masters with their titles,
//                            descriptions and ids stripped and their colors baked in, under neutral file names, so
//                            nothing a reader can open names what a symbol means.
//   20261106_Reader-Check.html                the page (content only: the publish step wraps it in the skeleton)
//   20261106_Reader-Check-Answer-Key.json     what each symbol is meant to say, the loop answers and chart findings.
//                                             The page never carries it.
// The page source is reader_check_template.html; this script injects CONFIG into it.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const HERE = __dirname;
const ROOT = path.resolve(HERE, '../../../..');
const IMG = path.join(HERE, 'img');
const PAGE = path.join(HERE, '20261106_Reader-Check.html');
const KEY = path.join(HERE, '20261106_Reader-Check-Answer-Key.json');
const TEMPLATE = path.join(HERE, 'reader_check_template.html');
const CAPTURE = !process.argv.includes('--no-capture');

const ATLAS = path.join(ROOT, 'work/boards/phase-2/atlas-editorial/01-times-explainer/20261105_Editorial-01-Times-Explainer.html');
const EXPLAINER = path.join(ROOT, 'work/boards/phase-2/data-viz/01-explainer/20261106_Data-Viz-01-Explainer.html');
const STRETCH = path.join(ROOT, 'work/boards/phase-2/data-viz/stretch/20261106_Data-Viz-Stretch.html');
const ED = JSON.parse(fs.readFileSync(path.join(ROOT, 'work/boards/phase-2/atlas-editorial/shared/20261105_Atlas-Editorial-Data.json'), 'utf8'));
const VOICE = JSON.parse(fs.readFileSync(path.join(ROOT, 'work/boards/phase-2/voice/20261106_Voice-Rules-Content.json'), 'utf8'));
const CL = path.join(ROOT, 'work/build/assets/civic-line/black');
const ID = path.join(ROOT, 'work/build/assets/identity');

// Phone widths the stimuli are captured at. A viewport of 390 px and up gets the 390 capture; narrower phones get the
// 360 capture, drawn for that width, so nothing is scaled up and chart text stays at its 14 px phone floor.
const WIDTHS = [390, 360];
const DPR = 2;   // twice size for sharpness (brief, step 5)

// ------------------------------------------------------------------------------------------------ the loops (DR-84)
// The third loop: R8, because System 1 draws it (on its "All loops" view) and the brief asks for R8 when the page draws
// it. B4, the balancing loop, is ready below as a one-line swap (see the notes: both R8 and R10 feed themselves).
const THIRD_LOOP = 'R8';
const LOOP_DEFS = {
  R10: { view: 'loop-r10', selector: '[data-view-root="loop-r10"] svg.cyc.ph', from: 'the R10 loop close-up' },
  R8: { view: 'loops', selector: '[data-view-root="loops"] svg.cyc.ph[aria-label^="R8,"]', from: 'the "All loops" catalog card' },
  B4: { view: 'loops', selector: '[data-view-root="loops"] svg.cyc.ph[aria-label^="B4,"]', from: 'the "All loops" catalog card' },
};
// Words printed on each drawing, read from the captures (step labels as printed, boxes as printed).
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
  R8: {
    steps: [
      { value: 'top', label: 'Top arrow, raises', from: 'Housing scarcity', to: "Homeowners' equity" },
      { value: 'bottom', label: 'Bottom arrow, raises', from: "Homeowners' equity", to: 'Housing scarcity' },
    ],
    boxes: ['Housing scarcity', "Homeowners' equity"],
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

// ------------------------------------------------------------------------------------------------ icons (DR-84)
// The four pillar marks and four topic icons, one from each of the set's other sheets. File numbers are a fixed
// scramble, so a file name says nothing about the set's order; readers see them in a random order anyway.
const ICONS = [
  { file: 'icon-5.svg', id: 'CL-019', sheet: '01', group: 'pillar mark' },
  { file: 'icon-2.svg', id: 'CL-020', sheet: '01', group: 'pillar mark' },
  { file: 'icon-7.svg', id: 'CL-021', sheet: '01', group: 'pillar mark' },
  { file: 'icon-3.svg', id: 'CL-022', sheet: '01', group: 'pillar mark' },
  { file: 'icon-8.svg', id: 'CL-015', sheet: '01', group: 'topic: participation and accountability' },
  { file: 'icon-1.svg', id: 'CL-032', sheet: '02', group: 'topic: government, information and technology' },
  { file: 'icon-6.svg', id: 'CL-063', sheet: '03', group: 'topic: economy and public issues' },
  { file: 'icon-4.svg', id: 'R-02', sheet: '04', group: 'reform' },
];
// Meanings in the words of voice line B (W13's rewrite, DR-76): "We'll explain the rules and track what happens to
// them. When a decision is coming, we'll connect you with the people making it, so you can act in time."
const PILLAR_MEANING = {
  'CL-019': 'Explain, pillar 1: we explain the rules and how a decision is made.',
  'CL-020': 'Track, pillar 2: we track what happens to the rules as a decision moves.',
  'CL-021': 'Connect, pillar 3: when a decision is coming, we connect readers with the people making it.',
  'CL-022': 'Act, pillar 4: the reader acts in time, taking part in the decision.',
};

// ------------------------------------------------------------------------------------------------ 16 px marks (DR-84, R10 of DR-67)
// The identity's 16 px masters, both wordmark widths, and the four pillar marks drawn at 16 px, all one color.
const MARKS = [
  { code: 'm1', file: 'mark-1.svg', src: 'wordmark/20261028_Wordmark-16px-Master.svg', name: "Wordmark, today's width, 16 px master", w: 152, h: 16, row: 1 },
  { code: 'm2', file: 'mark-2.svg', src: 'wordmark-condensed/20261028_Wordmark-Condensed-16px-Master.svg', name: 'Wordmark, condensed, 16 px master', w: 120, h: 16, row: 2 },
  { code: 'm3', file: 'mark-3.svg', src: 'ampersand/20261028_Amp-B-16px-Master.svg', name: 'Ampersand B, 16 px master', w: 14, h: 16, row: 3 },
  { code: 'm4', file: 'mark-4.svg', src: 'lockmark/20261028_Lockmark-16px-Master.svg', name: 'Lockmark, 16 px master', w: 16, h: 16, row: 3 },
  { code: 'm5', file: 'mark-5.svg', src: 'badge/20261028_Hinge-Badge-16px-Master.svg', name: 'Hinge-circle badge, 16 px master', w: 16, h: 16, row: 3 },
  { code: 'm6', file: 'mark-6.svg', cl: 'CL-019', name: 'Pillar mark Explain (CL-019) at 16 px', w: 16, h: 16, row: 4 },
  { code: 'm7', file: 'mark-7.svg', cl: 'CL-020', name: 'Pillar mark Track (CL-020) at 16 px', w: 16, h: 16, row: 4 },
  { code: 'm8', file: 'mark-8.svg', cl: 'CL-021', name: 'Pillar mark Connect (CL-021) at 16 px', w: 16, h: 16, row: 4 },
  { code: 'm9', file: 'mark-9.svg', cl: 'CL-022', name: 'Pillar mark Act (CL-022) at 16 px', w: 16, h: 16, row: 4 },
];

// ------------------------------------------------------------------------------------------------ mastheads (DR-86)
// L3 at one scale for both widths, as the minimum-size table sets them (196 and 164 px wide share 0.1533 px a unit).
const MAST_SCALE = 0.17;
const MASTHEADS = [
  { code: 'L3-today', file: 'masthead-1.svg', src: 'lockups/20261028_L3-Horizontal-Master.svg', name: "L3 horizontal lockup, today's width" },
  { code: 'L3-condensed', file: 'masthead-2.svg', src: 'lockups/20261028_L3-Horizontal-Condensed-Master.svg', name: 'L3 horizontal lockup, condensed' },
];

// ------------------------------------------------------------------------------------------------ charts (DR-85)
const CHARTS = [
  { code: 'S02', page: EXPLAINER, view: 'newsprint', section: 'newsprint-s02', board: 'Data viz board 3, Explainer, Newsprint view' },
  { code: 'S11', page: STRETCH, view: 'newsprint', section: 'newsprint-s11', board: 'Data viz stretch test, Newsprint view' },
  { code: 'S14', page: STRETCH, view: 'newsprint', section: 'newsprint-s14', board: 'Data viz stretch test, Newsprint view' },
];

// ------------------------------------------------------------------------------------------------ sentence pairs (DR-86)
// W02, W10 and W11: short, with befores quoted from real Oath & Action copy. W10 stands in for the brief's W05, whose
// county is invented and would need an Illustrative label beside that one pair only (house rule H03).
const PAIRS = ['W02', 'W10', 'W11'];

// ------------------------------------------------------------------------------------------------ helpers
const rel = (p) => path.relative(ROOT, p);
function sha(p) { return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex').slice(0, 16); }
function cleanSvg(svg, colors) {
  let s = svg.replace(/<\?xml[^>]*\?>\s*/g, '')
    .replace(/<title>[\s\S]*?<\/title>/g, '')
    .replace(/<desc>[\s\S]*?<\/desc>/g, '')
    .replace(/\s(id|data-id|data-part|data-[a-z-]+)="[^"]*"/g, '');
  for (const [from, to] of colors) s = s.split(from).join(to);
  if (/url\(#|href="#/.test(s)) throw new Error('an SVG kept an internal reference after its ids were stripped');
  if (/var\(|currentColor/.test(s)) throw new Error('an SVG kept an unbaked color: ' + (s.match(/var\([^)]*\)|currentColor/) || [])[0]);
  return s.trim() + '\n';
}
function setSize(svg, w, h) {
  return svg.replace(/<svg\b([^>]*)>/, (m, attrs) => {
    attrs = attrs.replace(/\s(width|height)="[^"]*"/g, '');
    return `<svg${attrs} width="${w}" height="${h}">`;
  });
}
function plain(s) { return s.replace(/\[-([\s\S]*?)-\]/g, '$1').replace(/\[\+([\s\S]*?)\+\]/g, '$1'); }
function beforeText(s) { return s.replace(/\[-([\s\S]*?)-\]/g, '$1').replace(/\[\+([\s\S]*?)\+\]/g, ''); }
function afterText(s) { return s.replace(/\[-([\s\S]*?)-\]/g, '').replace(/\[\+([\s\S]*?)\+\]/g, '$1'); }
function pngSize(p) { const b = fs.readFileSync(p); return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) }; }

// ------------------------------------------------------------------------------------------------ captures
async function capture() {
  const { chromium } = require('playwright');
  const browser = await chromium.launch();
  const log = [];
  for (const W of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: W, height: 900 }, deviceScaleFactor: DPR });
    const page = await ctx.newPage();
    // The atlas: the overview's first screens (kicker, headline, deck and whole-system drawing), with no wordmark,
    // tabs or breadcrumb; then the two loop drawings on their own.
    await page.goto('file://' + ATLAS + '#overview', { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({ content: 'header.mast, nav.tabs, nav.ak-crumbs { display: none !important; }' });
    await page.waitForTimeout(500);
    const ov = await page.evaluate(() => {
      const root = document.querySelector('[data-view-root="overview"]');
      const top = root.querySelector('p.eyebrow').getBoundingClientRect().top + scrollY;
      const svg = root.querySelector('svg.sysp').getBoundingClientRect();
      // 16 px of White above the kicker and 4 px under the drawing, which stops short of the caption below it
      return { x: svg.left - 2, y: top - 16, width: svg.width + 4, height: svg.bottom + scrollY - top + 20 };
    });
    await page.screenshot({ path: path.join(IMG, `drawing-overview-${W}.png`), clip: ov, fullPage: true });
    log.push(['overview', W, ov]);
    for (const k of ['R10', THIRD_LOOP]) {
      const d = LOOP_DEFS[k];
      await page.goto('file://' + ATLAS + '#' + d.view, { waitUntil: 'networkidle' });
      await page.addStyleTag({ content: 'header.mast, nav.tabs, nav.ak-crumbs { display: none !important; }' });
      await page.waitForTimeout(500);
      await page.locator(d.selector).scrollIntoViewIfNeeded();
      const box = await page.evaluate((sel) => { const r = document.querySelector(sel).getBoundingClientRect(); return { x: r.left - 2, y: r.top + scrollY - 12, width: r.width + 4, height: r.height + 24 }; }, d.selector);
      await page.screenshot({ path: path.join(IMG, `drawing-${k.toLowerCase()}-${W}.png`), clip: box, fullPage: true });
      log.push([k, W, box]);
    }
    // The charts: evidence line, title, measure line and the phone drawing. Notes, source line and the table toggle
    // stay off, so the exposure is the figure a phone reader meets first.
    for (const c of CHARTS) {
      await page.goto('file://' + c.page + '#' + c.view, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.addStyleTag({ content: `#${c.section} figure > .fnotes, #${c.section} figure > .srcrow, #${c.section} figure > details { display: none !important; }` });
      await page.waitForTimeout(500);
      const fig = page.locator(`#${c.section} figure`);
      await fig.scrollIntoViewIfNeeded();
      const w = await fig.evaluate((el) => el.getBoundingClientRect().width);
      await fig.screenshot({ path: path.join(IMG, `chart-${c.code.toLowerCase()}-${W}.png`) });
      log.push([c.code, W, { width: w }]);
    }
    await ctx.close();
  }
  await browser.close();
  return log;
}

// ------------------------------------------------------------------------------------------------ vector assets
function vectorAssets() {
  const icons = [];
  const clFile = (id) => fs.readdirSync(CL).find((f) => f.includes(`-${id}-`) && f.endsWith('-Black.svg'));
  for (const ic of ICONS) {
    const f = clFile(ic.id);
    const svg = cleanSvg(fs.readFileSync(path.join(CL, f), 'utf8'), []);
    fs.writeFileSync(path.join(IMG, ic.file), svg);
    const inv = INVENTORY.icons.find((i) => i.id === ic.id);
    icons.push({ ...ic, source: rel(path.join(CL, f)), label: inv.label });
  }
  const one = [['currentColor', '#121212'], ['var(--amp,#E63946)', '#121212'], ['var(--lever,#E63946)', '#121212'], ['var(--link,#5D636D)', '#121212']];
  const marks = [];
  for (const m of MARKS) {
    const src = m.src ? path.join(ID, m.src) : path.join(CL, clFile(m.cl));
    let svg = cleanSvg(fs.readFileSync(src, 'utf8'), one);
    svg = setSize(svg, m.w, m.h);
    fs.writeFileSync(path.join(IMG, m.file), svg);
    marks.push({ ...m, source: rel(src) });
  }
  const masts = [];
  for (const m of MASTHEADS) {
    const src = path.join(ID, m.src);
    const raw = fs.readFileSync(src, 'utf8');
    const vb = raw.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    const w = +(vb[2] * MAST_SCALE).toFixed(1), h = +(vb[3] * MAST_SCALE).toFixed(1);
    let svg = cleanSvg(raw, [['currentColor', '#121212'], ['var(--amp,#E63946)', '#E63946'], ['var(--lever,#E63946)', '#E63946'], ['var(--link,#5D636D)', '#5D636D']]);
    svg = setSize(svg, w, h);
    fs.writeFileSync(path.join(IMG, m.file), svg);
    masts.push({ ...m, source: rel(src), w, h, units_wide: vb[2] });
  }
  return { icons, marks, masts };
}
const INVENTORY = JSON.parse(fs.readFileSync(path.join(ROOT, 'work/build/assets/civic-line/20261029_Civic-Line-Inventory.json'), 'utf8'));

// ------------------------------------------------------------------------------------------------ config and key
function imgPair(stem) {
  const out = {};
  for (const W of WIDTHS) {
    const p = path.join(IMG, `${stem}-${W}.png`);
    const s = pngSize(p);
    out[W === 390 ? 'lg' : 'sm'] = { src: `img/${stem}-${W}.png`, w: s.w / DPR, h: s.h / DPR };
  }
  return out;
}

function build() {
  const { icons, marks, masts } = vectorAssets();
  const rules = Object.fromEntries(VOICE.groups.flatMap((g) => g.rules).map((r) => [r.id, r]));
  const parts = ['X', 'A', 'B', 'C', 'D', 'E', 'EC', 'TC'].map((id) => ED.parts.find((p) => p.id === id).plain_name);
  const loops = ['R10', THIRD_LOOP].map((k) => ({ code: k.toLowerCase(), img: imgPair(`drawing-${k.toLowerCase()}`), steps: LOOP_WORDS[k].steps, boxes: LOOP_WORDS[k].boxes }));
  const CONFIG = {
    version: '20261106-1',
    exposure: { drawing: 10, icon: 10, marks: 10, chart: 15, masthead: 10 },
    overview: { img: imgPair('drawing-overview'), parts },
    loops,
    icons: icons.map((ic) => ({ code: ic.file.replace('.svg', '').replace('icon-', 'i'), src: 'img/' + ic.file })).sort((a, b) => a.code.localeCompare(b.code)),
    marks: marks.map((m) => ({ code: m.code, src: 'img/' + m.file, w: m.w, h: m.h, row: m.row })),
    charts: CHARTS.map((c) => ({ code: c.code, img: imgPair(`chart-${c.code.toLowerCase()}`) })),
    pairs: PAIRS.map((id) => ({ code: id, before: beforeText(rules[id].before), after: afterText(rules[id].after) })),
    mastheads: masts.map((m) => ({ code: m.code, src: 'img/' + m.file, w: m.w, h: m.h })),
  };
  // Nothing in CONFIG may name what a symbol means.
  const leak = JSON.stringify(CONFIG);
  for (const ic of icons) for (const word of [ic.label, ic.id]) if (leak.includes(word)) throw new Error(`CONFIG names ${word}`);

  const tpl = fs.readFileSync(TEMPLATE, 'utf8');
  if (!tpl.includes('/*CONFIG*/')) throw new Error('template has no /*CONFIG*/ slot');
  const html = tpl.replace('/*CONFIG*/{}', JSON.stringify(CONFIG));
  for (const ic of icons) if (html.includes(ic.label)) throw new Error(`page text names ${ic.label}`);
  if (/Oath\s*(&|&amp;|and)\s*Action/i.test(html)) throw new Error('page text names the brand');
  if (/—/.test(html)) throw new Error('page text carries an em dash');
  fs.writeFileSync(PAGE, html);

  // ---------------------------------------------------------------- answer key
  const loopKey = {
    r10: {
      loop: 'R10, Safe-seat loop (V7), reinforcing, "feeds itself"',
      drawing: `System 1 phone drawing from ${LOOP_DEFS.R10.from}, with reform R-01's targets in the working red`,
      image: 'img/drawing-r10-390.png and img/drawing-r10-360.png',
      comes_back: { answer: 'yes', why: 'Four steps run C1 to C2 to C3 to C4 and step 4 (L42) returns to Safe seats.' },
      feeds_or_pushes: { answer: 'feeds', why: 'Two plus and two minus signs: an even number of minus signs makes the loop reinforcing.' },
      least_certain: { answer: 'step3', why: 'Step 3, L53 "Officials safe from defeat write rules for themselves", graded plausible and drawn dashed; the drawing prints "weakest step" under it. Steps 1 and 4 are documented, step 2 well supported.' },
      reform_acts: { answer: 'Seats settled in the primary', partial: ['Safe seats', 'Risk of losing office'], why: 'R-01 (all-party primaries) targets L08, L25 and C2; the red marks are arrow 1, arrow 2 and the box "Seats settled in the primary". Safe seats and Risk of losing office each touch one red arrow. The drawing shows no key, so this question tests whether red reads as "where a reform acts" without one; the loop page sets the key line above the drawing.' },
    },
    [THIRD_LOOP.toLowerCase()]: THIRD_LOOP === 'R8' ? {
      loop: 'R8, Housing-scarcity loop (V7), reinforcing, "feeds itself"',
      drawing: `System 1 phone drawing from ${LOOP_DEFS.R8.from}; the catalog draws no reform marks`,
      image: 'img/drawing-r8-390.png and img/drawing-r8-360.png',
      comes_back: { answer: 'yes', why: 'Two steps: L38 runs from Housing scarcity to Homeowners\' equity and L39 returns.' },
      feeds_or_pushes: { answer: 'feeds', why: 'Both steps carry a plus sign.' },
      least_certain: { answer: 'same', why: 'Both steps, L38 and L39, are graded well supported and drawn with the same solid line; no weakest step is marked.' },
      reform_acts: { answer: 'none', why: 'R-30 (more homes allowed by right near jobs) aims at R8, but the catalog drawing shows no reform marks. A reader who names a box is reading in a reform the drawing does not show.' },
    } : { loop: THIRD_LOOP, note: 'Write this key from the model before publishing.' },
    choice_values: 'least_certain: step1 to step4 (R10) or top and bottom (R8), "same" for "They look about the same", "unsure" for "Not sure". reform_acts: the box name as printed, "none" for "No reform is shown", "unsure".',
  };
  const key = {
    title: 'Reader check answer key',
    date: 'November 6, 2026',
    page: rel(PAGE),
    private: 'Never publish this file with the page. The page carries neutral codes only (i1 to i8, m1 to m9).',
    overview: {
      image: 'img/drawing-overview-390.png and -360.png: System 1 overview kicker, headline "Who do they answer to?", deck and whole-system phone drawing',
      purpose_pass: 'Names who officials answer to, or how economic and public life connect (civic education memo, section 7, Q1). A party or a single issue fails.',
      open_first: 'No right answer. The choices are the eight parts as the drawing prints them, in its order.',
    },
    loops: loopKey,
    icons: icons.map((ic) => ({
      code: ic.file.replace('.svg', '').replace('icon-', 'i'), file: 'img/' + ic.file, id: ic.id, label: ic.label, group: ic.group,
      intended_meaning: PILLAR_MEANING[ic.id] || ({
        'CL-015': 'Political money: money spent to influence politics (atlas B1, "Money spent on influence"). The drawing: a coin with a dollar sign wired to a ballot box.',
        'CL-032': 'Local reporting: the availability of local news about local government and elections (atlas B2). The drawing: a folded newspaper.',
        'CL-063': 'Essential costs: the cost of necessities a household must buy (atlas EC9, "Cost of essentials"). The drawing: a house holding a shopping bag with a price tag.',
        'R-02': 'Ranked-choice voting (reform R-02): voters rank candidates in order of preference. The drawing: a ballot with numbered choices 1, 2 and 3.',
      })[ic.id],
      source: ic.source,
    })),
    marks: marks.map((m) => ({ code: m.code, file: 'img/' + m.file, mark: m.name, size_px: `${m.w} by ${m.h}`, source: m.source })),
    marks_note: 'One color, Charcoal #121212 on Newsprint, at true CSS size. The Civic Line set has no 16 px drawing of the pillar marks, so m6 to m9 are the black edition scaled to 16 px, below the set\'s 32 px bare floor (D2-42); their strokes fall to about 0.4 px.',
    charts: CHARTS.map((c) => {
      const t = { S02: { title: 'Child poverty fell to 5.1 percent in 2021, the lowest since the series began in 2009, and more than doubled the next year.', finding: 'Child poverty under the Supplemental Poverty Measure fell to its series low of 5.1 percent in 2021 and rose to 12.0 percent in 2022; in 2025 both measures stood at 13.4 percent.', evidence: 'Finding, official statistic (Census Bureau)' },
        S11: { title: 'The margin in every state and DC moved toward the Republican nominee from 2020 to 2024, by 1.0 point in Washington to 10.5 points in New York.', finding: 'Every state and DC shifted toward the Republican nominee between 2020 and 2024, from 1.0 point (Washington) to 10.5 points (New York); the phone drawing ranks the shifts as arrows from zero.', evidence: 'Finding, documented official results (FEC)' },
        S14: { title: 'The three-month average of monthly job change stood at 51,000 in September 2026, a preliminary figure, and payrolls shrank in seven of the 57 months charted.', finding: 'Monthly payroll change from January 2022 to September 2026 with its three-month average, 51,000 in September 2026 (preliminary); seven of the 57 months show a loss.', evidence: 'Finding, official statistic (BLS via FRED)' } }[c.code];
      return { code: c.code, board: c.board, file: rel(c.page), section: '#' + c.section, image: `img/chart-${c.code.toLowerCase()}-390.png and -360.png`, ...t, favors_intended: 'no', telling_pass: 'The sentence carries the finding\'s direction and subject (what moved, which way, over what period). Numbers are a bonus.' };
    }),
    pairs: PAIRS.map((id) => ({ code: id, rule: rules[id].name, before: beforeText(rules[id].before), after: afterText(rules[id].after), before_source: rules[id].before_source, expected: 'after' })),
    mastheads: masts.map((m) => ({ code: m.code, file: 'img/' + m.file, lockup: m.name, css_px: `${m.w} by ${m.h}`, scale: MAST_SCALE, source: m.source })),
    record_fields: {
      path: 'responses/<viewer id>: { schema, latest_run, updated_at, runs: { <run id>: run } }. Copy mode sends the same run as text.',
      run: 'initials, mode ("saved" or "copy"), mode_note, started_at, finished_at (ISO, UTC), viewport_width, resumed, position, orders, items',
      orders: 'loops (codes in the order shown), icons (i codes in order), charts, pairs (per pair: which of A and B was the before), mastheads (A then B)',
      items: 'one per stimulus: show_again (count of "Show it again"), shown_seconds (each exposure as measured, visible time only), interrupted (exposures cut short by a reload), load_failed, questions: { <q>: { answer, seconds (visible seconds on the question screen, re-shows excluded), skipped } }',
    },
  };
  fs.writeFileSync(KEY, JSON.stringify(key, null, 1) + '\n');
  return { CONFIG, icons, marks, masts };
}

(async () => {
  fs.mkdirSync(IMG, { recursive: true });
  if (CAPTURE) {
    const log = await capture();
    for (const [what, W, box] of log) console.log(`captured ${what} at ${W}: ${Math.round(box.width)} px wide`);
  }
  const out = build();
  const bytes = fs.readdirSync(IMG).reduce((a, f) => a + fs.statSync(path.join(IMG, f)).size, 0);
  console.log(`wrote ${rel(PAGE)} (${fs.statSync(PAGE).size} bytes), ${rel(KEY)}, ${fs.readdirSync(IMG).length} files in img/ (${(bytes / 1048576).toFixed(2)} MB)`);
})().catch((e) => { console.error(e); process.exit(1); });
