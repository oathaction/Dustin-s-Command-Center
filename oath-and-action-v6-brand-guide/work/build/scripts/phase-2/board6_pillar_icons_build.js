// Board 6, section 2 (November 7, 2026): four pillar icons from the Civic Line, in three sets of four.
//
// Usage:
//   node work/build/scripts/phase-2/board6_pillar_icons_build.js
//
// Reads the Civic Line inventory and masters in work/build/assets/civic-line/ (read and place only: every icon is the
// supplied SVG of its edition, inlined with its ids made unique per placement and its box set to the size shown).
// Measures every one of the 122 black masters in Chromium (Playwright): pixels that reach 3:1 against Newsprint at 16 and
// 24 px, size at 128 px (square root of the convex hull's area), and silhouette likeness at 24 px for all 7,381 pairs
// (Pearson correlation of slightly blurred ink maps, best over shifts of up to one pixel), ranked as percentiles.
// Writes:
//   work/boards/phase-2/board-6/pillar-icons/20261107_Board-6-Pillar-Icons.html
//   work/boards/phase-2/board-6/pillar-icons/20261107_Board-6-Pillar-Icons-Measurements.json
// The page loads Inter, Inter Tight and Lora from Google Fonts and nothing else; every SVG is inline. Every red mark sits
// under data-red="signature" (Rule 05.3, DR-66); the page carries no working red.
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const CL = path.join(ROOT, 'work/build/assets/civic-line');
const OUTDIR = path.join(ROOT, 'work/boards/phase-2/board-6/pillar-icons');
const OUT = path.join(OUTDIR, '20261107_Board-6-Pillar-Icons.html');
const MEAS = path.join(OUTDIR, '20261107_Board-6-Pillar-Icons-Measurements.json');
const INV = JSON.parse(fs.readFileSync(path.join(CL, '20261029_Civic-Line-Inventory.json'), 'utf8'));
const BY = Object.fromEntries(INV.icons.map((i) => [i.id, i]));
const STROKE = 3.3508;   // every candidate here exports at this line, in units of the 128 box

// ---------- placing masters ----------
const EDS = { 'red-black': 'svg_red_black', black: 'svg_black', 'red-newsprint': 'svg_red_newsprint', newsprint: 'svg_newsprint' };
const RED_EDS = new Set(['red-black', 'red-newsprint']);
const src = (id, ed) => fs.readFileSync(path.join(CL, ed, BY[id].exports[EDS[ed]]), 'utf8');
const tileSrc = (id) => fs.readFileSync(path.join(CL, BY[id].tiles.find((t) => t.includes('/rounded-charcoal/') && t.endsWith('Two-Color.svg'))), 'utf8');
let uid = 0;
function inline(svg, px, cls) {
  const n = ++uid;
  let s = svg.replace(/<\?xml[^>]*>\s*/, '');
  s = s.replace(/\bid="([^"]+)"/g, (m, v) => `id="${v}-p${n}"`)
    .replace(/url\(#([^)]+)\)/g, (m, v) => `url(#${v}-p${n})`)
    .replace(/href="#([^"]+)"/g, (m, v) => `href="#${v}-p${n}"`);
  s = s.replace(/(<svg\b[^>]*?)\swidth="128" height="128"/, `$1 width="${px}" height="${px}" aria-hidden="true" focusable="false" class="${cls || 'ic'}"`);
  if (!s.includes(`width="${px}" height="${px}"`)) throw new Error('could not size an SVG');
  return s.trim();
}
// An icon at a size in an edition, wrapped so the check can find every red (signature red, R11 and DR-66).
function icon(id, ed, px) {
  const red = RED_EDS.has(ed) ? ' data-red="signature"' : '';
  return `<span class="ico" style="width:${px}px;height:${px}px"${red} data-icon="${id}" data-edition="${ed}">${inline(src(id, ed), px)}</span>`;
}
function tile(id, px) {
  return `<span class="ico" style="width:${px}px;height:${px}px" data-red="signature" data-icon="${id}" data-edition="tile-rounded-charcoal-two-color">${inline(tileSrc(id), px)}</span>`;
}

// ---------- content ----------
const PILLARS = [
  { key: 'explain', word: 'Explain', n: '01', job: 'Make the rules and their effects understandable.' },
  { key: 'track', word: 'Track', n: '02', job: 'Follow the decision and keep its record within reach.' },
  { key: 'connect', word: 'Connect', n: '03', job: 'Help people reach the office that decides and the evidence it decides on.' },
  { key: 'act', word: 'Act', n: '04', job: 'Give the reader a useful next step.' },
];

// What each drawing says for its pillar, and what to watch. Studio judgment, written for Dustin.
const NOTES = {
  'CL-019': { fit: 'An open book with three rays rising from its spine. A reader sees something opened up and understood, which is Explain’s job: making the rules and their effects understandable.', watch: 'The same book appears in CL-068 Education and R-13 Congressional Capacity, so on a page about schools two books would sit close together.', read: 'a book, reading or learning', leads: 'Yes' },
  'CL-020': { fit: 'A route winds from a map pin to a magnifier, the way a parcel is tracked from place to place. Track follows a decision and keeps its record within reach.', watch: 'It holds three subjects, the most of the four. Its magnifier is the Civic Line’s sign for oversight, so a newcomer may give it to Explain. It is the faintest of the four at 16 px.', read: 'a route on a map, tracking a delivery', leads: 'Likely' },
  'CL-021': { fit: 'Two equal rings overlap, and the lens they share is red: a reader and the office that decides, meeting where they overlap.', watch: 'Many readers will call it a Venn diagram first. Its rings are drawn as outlines, which keeps it apart from payment-card logos built from two filled circles.', read: 'a Venn diagram, overlap or a link', leads: 'Likely' },
  'CL-022': { fit: 'A finger presses a round control, with short rays where it lands. It says do it now, which suits a next step of any kind.', watch: 'It is the tap gesture from phone screens, so on a website Act can read as a button to press. Its drawing measures about a fifth smaller than Explain’s in the same box.', read: 'press, tap or do it now', leads: 'Yes' },
  'CL-048': { fit: 'A folder with one page lifted out, its top line in red. It draws the second half of Track’s job, keeping the record within reach.', watch: 'Many apps use a folder for files. A newcomer may give it to Explain, since the book and the folder both hold things to read. It already names the Public Records topic.', read: 'files, a folder or an archive', leads: 'At risk' },
  'CL-061': { fit: 'A person, an arrow and an envelope: a reader writes to the office that decides.', watch: 'In the economy pages this drawing stands for a household’s income, so one drawing would carry two meanings. Many sites use an envelope for “contact us”. It is wide and low, so at 24 px in a kicker it shrinks to a thin strip. Connect and Act would both show writing.', read: 'sending mail or a message', leads: 'Likely' },
  'CL-004': { fit: 'A page with a pen across it, the pen in red. A reader signs, comments or puts their name to a step.', watch: 'A pen on a page is the edit sign in many apps. Petitions are a campaign tool, so Act may read as advocacy. It already names the Petition topic.', read: 'writing, signing or edit', leads: 'Likely' },
  'CL-006': { fit: 'Three people joined by three red arcs. Connect brings readers to the people making a decision, and of the twelve icons on this page it is the one that shows people joined to each other.', watch: 'It reads as a group or a team. It is the faintest icon on this page at 16 px. It already names the Civic Ties topic.', read: 'a group, a community or a team', leads: 'Yes' },
  'CL-001': { fit: 'A ballot going into a box, the public act every reader knows.', watch: 'Most Act pieces ask for a comment, a call or a turn at the microphone, and a ballot narrows Act to elections. In all three earlier icon tests, raters took other ballot-box drawings for printers or trays. It already names the Voting topic.', read: 'voting or a ballot box', leads: 'Yes' },
};

const SETS = [
  {
    key: 'a', letter: 'A', name: 'Drawn for the pillars', ids: ['CL-019', 'CL-020', 'CL-021', 'CL-022'], rec: true,
    short: 'Today’s marks, drawn as one row for the pillars, each with one red part doing the work.',
    family: 'These four were drawn as one row for the pillars on the first Civic Line sheet, and you approved them on October 29. Each holds one idea, with one red part doing the pillar’s work: the rays over the book, the pin and the handle, the shared lens and the pressed ring. They hold together through the line and the red, since their subjects differ.',
    use: 'Set A keeps today’s drawings and changes how they are used, as the recommendation lists.',
  },
  {
    key: 'b', letter: 'B', name: 'The reader’s paper', ids: ['CL-019', 'CL-048', 'CL-061', 'CL-004'],
    short: 'Paper a reader holds: the book they read, the file they keep, the letter they send and the page they sign.',
    kept: { 'CL-019': 'Kept from Set A. The book is paper too, so it sits with the file, the letter and the signed page.' },
    family: 'Every mark is paper a reader holds: the book they read, the file they keep, the letter they send and the page they sign. One material ties the four together, and each red part is the reader’s own move.',
    use: 'Set B keeps the book and changes Track, Connect and Act.',
  },
  {
    key: 'c', letter: 'C', name: 'Civic life', ids: ['CL-019', 'CL-020', 'CL-006', 'CL-001'],
    short: 'Set A’s book and route where a reader learns, then people and the vote where a reader takes part.',
    kept: { 'CL-019': 'Kept from Set A for the first pillar where a reader learns.', 'CL-020': 'Kept from Set A for the second pillar where a reader learns, which follows the decision.' },
    family: 'Set C keeps Set A’s book and route for the two pillars where a reader learns, and turns to people and the vote for the two where a reader takes part. The change falls at the hinge between Track and Connect, where chapter 01 says a reader stops learning about a decision and starts taking part in it.',
    use: 'Set C keeps Explain and Track and changes Connect and Act.',
  },
];

const SHORTLIST = [
  { p: 'Explain', items: [
    ['CL-019', 'Drawn for this pillar. The open book with rays reads as learning at 24 px and up.', 'Sets A, B and C'],
    ['CL-068', 'The same book with a bulb. It already names the Education topic and sits too close to CL-019.', ''],
    ['CL-023', 'A page under a magnifier with a check. It shares the magnifier with Track and the watchdog drawings.', ''],
    ['CL-032', 'A newspaper. It names local news, and every pillar publishes.', ''],
    ['CL-071', 'A page with one slider, which reads as a settings control.', ''],
  ] },
  { p: 'Track', items: [
    ['CL-020', 'Drawn for this pillar. A route runs from a pin to a magnifier.', 'Sets A and C'],
    ['CL-048', 'A folder with a page lifted out: the record kept within reach.', 'Set B'],
    ['CL-028', 'A page under a magnifier with a red handle, the Civic Line’s sign for oversight.', ''],
    ['CL-039', 'A ranked list beside a slider. It names how platforms rank posts.', ''],
    ['CL-072', 'Three routes, one turned. The atlas uses it for reform in general.', ''],
  ] },
  { p: 'Connect', items: [
    ['CL-021', 'Drawn for this pillar. Two rings overlap, and their shared lens is red.', 'Set A'],
    ['CL-061', 'A person, an arrow and an envelope. For Connect it reads as writing to an office.', 'Set B'],
    ['CL-006', 'Three people joined by red arcs.', 'Set C'],
    ['CL-050', 'Two people across a table with a two-way arrow. It draws a labor negotiation, which the economy pages use.', ''],
    ['CL-031', 'A town hall with a red door. It names local government, a topic of its own.', ''],
    ['CL-047', 'A page and a key. The key reads as a password or a lock.', ''],
  ] },
  { p: 'Act', items: [
    ['CL-022', 'Drawn for this pillar. A finger presses a round control.', 'Set A'],
    ['CL-004', 'A page with a red pen.', 'Set B'],
    ['CL-001', 'A ballot going into a box.', 'Set C'],
  ] },
];

// The four pieces from chapter 01 (s-01-pieces), kicker and headline as approved. Connect and Act are invented.
const PIECES = [
  { label: 'Explainer', part: 'Utility rates', head: 'Why is my electric bill going up?', ill: false },
  { label: 'Tracker', part: 'Congress', head: 'Stop Insider Trading Act Tracker', ill: false },
  { label: 'Guide', part: 'Field Notes', head: 'Who answers for the repair on your street?', ill: true },
  { label: 'Act · How to take part', part: '', head: 'Alder County votes on backyard cottages March 9.', ill: true },
];

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const name = (id) => BY[id].label;
const fmt = (x, d = 2) => Number(x).toFixed(d);
const ordinal = (n) => { const v = Math.round(n); const s = (v % 100 >= 11 && v % 100 <= 13) ? 'th' : ({ 1: 'st', 2: 'nd', 3: 'rd' }[v % 10] || 'th'); return v + s; };

// ---------- measurement ----------
async function measure() {
  const ids = INV.icons.map((i) => i.id);
  const svgs = Object.fromEntries(ids.map((id) => [id, src(id, 'black')]));
  const zoomIds = [...new Set(SETS.flatMap((s) => s.ids))];
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent('<!doctype html><html><body></body></html>');
  const res = await page.evaluate(async ({ svgs, zoomIds }) => {
    const NP = [220, 217, 210];
    const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    const lum = (r, g, b) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
    const Lbg = lum(...NP), Lch = lum(18, 18, 18);
    const imgs = {};
    for (const [id, s] of Object.entries(svgs)) {
      const img = new Image(); img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(s); await img.decode(); imgs[id] = img;
    }
    const raster = (img, px) => {
      const c = document.createElement('canvas'); c.width = c.height = px; const g = c.getContext('2d');
      g.fillStyle = '#DCD9D2'; g.fillRect(0, 0, px, px); g.drawImage(img, 0, 0, px, px);
      return { c, d: g.getImageData(0, 0, px, px).data };
    };
    const ink = (d, px) => { const m = new Float64Array(px * px); for (let i = 0; i < px * px; i++) { const L = lum(d[4 * i], d[4 * i + 1], d[4 * i + 2]); m[i] = Math.max(0, Math.min(1, (Lbg - L) / (Lbg - Lch))); } return m; };
    const blur = (m, px, s) => {
      const r = Math.ceil(3 * s), k = []; let t = 0; for (let i = -r; i <= r; i++) { const v = Math.exp(-i * i / (2 * s * s)); k.push(v); t += v; } for (let i = 0; i < k.length; i++) k[i] /= t;
      const a = new Float64Array(px * px), b = new Float64Array(px * px);
      for (let y = 0; y < px; y++) for (let x = 0; x < px; x++) { let v = 0; for (let i = -r; i <= r; i++) { const xx = x + i; if (xx >= 0 && xx < px) v += k[i + r] * m[y * px + xx]; } a[y * px + x] = v; }
      for (let y = 0; y < px; y++) for (let x = 0; x < px; x++) { let v = 0; for (let i = -r; i <= r; i++) { const yy = y + i; if (yy >= 0 && yy < px) v += k[i + r] * a[yy * px + x]; } b[y * px + x] = v; }
      return b;
    };
    const corr = (A, B, px, sh) => {
      let best = -1;
      for (let dy = -sh; dy <= sh; dy++) for (let dx = -sh; dx <= sh; dx++) {
        let n = 0, sa = 0, sb = 0, saa = 0, sbb = 0, sab = 0;
        for (let y = Math.max(0, dy); y < px + Math.min(0, dy); y++) for (let x = Math.max(0, dx); x < px + Math.min(0, dx); x++) {
          const a = A[y * px + x], b = B[(y - dy) * px + (x - dx)]; n++; sa += a; sb += b; saa += a * a; sbb += b * b; sab += a * b;
        }
        const cov = sab - sa * sb / n, va = saa - sa * sa / n, vb = sbb - sb * sb / n;
        if (va > 0 && vb > 0) best = Math.max(best, cov / Math.sqrt(va * vb));
      }
      return best;
    };
    const hull = (pts) => {
      pts.sort((p, q) => p[0] - q[0] || p[1] - q[1]);
      const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
      const lo = [], up = [];
      for (const p of pts) { while (lo.length >= 2 && cross(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
      for (let i = pts.length - 1; i >= 0; i--) { const p = pts[i]; while (up.length >= 2 && cross(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
      const h = lo.slice(0, -1).concat(up.slice(0, -1)); let a = 0;
      for (let i = 0; i < h.length; i++) { const p = h[i], q = h[(i + 1) % h.length]; a += p[0] * q[1] - q[0] * p[1]; }
      return Math.abs(a) / 2;
    };
    const per = {}, maps = {};
    for (const [id, img] of Object.entries(imgs)) {
      per[id] = {};
      for (const px of [16, 24]) {
        const { d } = raster(img, px); let n3 = 0, peak = 1;
        for (let i = 0; i < px * px; i++) { const L = lum(d[4 * i], d[4 * i + 1], d[4 * i + 2]); const cr = (Lbg + 0.05) / (L + 0.05); if (cr >= 3) n3++; peak = Math.max(peak, cr); }
        per[id]['px3_' + px] = n3; per[id]['peak_' + px] = +peak.toFixed(2);
        if (px === 24) maps[id] = blur(ink(d, 24), 24, 1.2);
      }
      const { d } = raster(img, 128); const m = ink(d, 128); const pts = [];
      for (let y = 0; y < 128; y++) for (let x = 0; x < 128; x++) if (m[y * 128 + x] > 0.5) pts.push([x + 0.5, y + 0.5]);
      per[id].hull128 = +Math.sqrt(hull(pts)).toFixed(1);
    }
    const ids = Object.keys(maps), pairs = {};
    for (let i = 0; i < ids.length; i++) for (let j = i + 1; j < ids.length; j++) pairs[ids[i] + '|' + ids[j]] = +corr(maps[ids[i]], maps[ids[j]], 24, 1).toFixed(4);
    const zoom = {};
    for (const id of zoomIds) {
      zoom[id] = {};
      for (const px of [16, 24]) {
        const { c } = raster(imgs[id], px); const z = document.createElement('canvas'); z.width = z.height = px * 4;
        const g = z.getContext('2d'); g.imageSmoothingEnabled = false; g.drawImage(c, 0, 0, px * 4, px * 4); zoom[id][px] = z.toDataURL('image/png');
      }
    }
    return { per, pairs, zoom, ua: navigator.userAgent };
  }, { svgs, zoomIds });
  await browser.close();
  return res;
}

// ---------- page parts ----------
function pillarRow(ids, opts) {
  const { px = 48, ed = 'black', current = null, size = 'm', ids: showIds = false } = opts || {};
  const items = PILLARS.map((p, i) => {
    const cur = current === p.key;
    const e = cur && px >= 48 ? 'red-black' : ed;
    const word = showIds ? `<span class="pwrap"><span class="pw">${p.word}</span><span class="pid">${ids[i]}${name(ids[i]) !== p.word ? ' ' + esc(name(ids[i])) : ''}</span></span>` : `<span class="pw">${p.word}</span>`;
    return `<li class="pi${cur ? ' cur' : ''}"${cur ? ' aria-current="true"' : ''}>${icon(ids[i], e, px)}${word}</li>`;
  }).join('');
  return `<ol class="prow prow-${size}${showIds ? ' prow-grid' : ''}" aria-label="The four pillars in order">${items}</ol>`;
}

function compareSection(M) {
  const rows = SETS.map((s) => `<div class="cmp-row" id="cmp-${s.key}">
<div class="cmp-h"><p class="setid">Set ${s.letter}${s.rec ? ' <span class="chip solid">Recommended</span>' : ''}</p><h3>${esc(s.name)}</h3>
<p class="ids">${esc(s.short)}</p></div>
${pillarRow(s.ids, { px: 48, ids: true })}</div>`).join('');
  const big = SETS.map((s) => `<div class="big-row"><p class="setid">Set ${s.letter}</p><div class="big-cells">${s.ids.map((id, i) => `<figure class="big-cell">${icon(id, 'red-black', 128)}<figcaption><b>${PILLARS[i].word}</b><span>${id} ${esc(name(id))}</span></figcaption></figure>`).join('')}</div></div>`).join('');
  return `<section id="compare" aria-labelledby="compare-h">
<p class="secnum">01</p><h2 id="compare-h">The three sets in the pillar row</h2>
<p>Each row reads Explain, Track, Connect and Act, with each word beside its icon. The icons are the Civic Line masters at 48 px in one color, as the guide sets any row of icons, with each icon’s ID under its word. The same twelve follow at 128 px in two colors.</p>
<div class="cmp">${rows}</div>
<h3 class="sub">The same twelve at 128 px, in two colors</h3>
<div class="big">${big}</div>
</section>`;
}

function recommendation(M) {
  const a = SETS[0];
  const h = (id) => M.per[id].hull128;
  return `<section id="rec" class="decision" aria-labelledby="rec-h">
<p class="secnum">02</p><h2 id="rec-h">Our recommendation: keep Set A and change how it is used</h2>
<div class="rec-grid"><div>
<p>Set A is the four marks you approved on October 29. We would keep them because they are the only four of the 122 drawn for the pillars, so no topic page or reform page uses the same drawing. Sets B and C each borrow two or three drawings that already name a topic, such as Voting or Public Records, and a reader would meet one drawing with two meanings. Set A’s hand also covers any next step a reader takes, where a ballot or a signed page names one kind of step.</p>
<h3>Five changes in how Set A is used</h3>
<ol class="changes">
<li>The word sits beside the icon in every row, and always below 48 px.</li>
<li>In a row the four icons go one color, and the current pillar keeps its red from 48 px up. Below 48 px, bold type and an underline mark the current pillar’s word.</li>
<li>At 16 px the icon is decoration beside its word. Its line is ${fmt(STROKE * 16 / 128)} px wide there, and no drawing on this page keeps a clear shape at that size.</li>
<li>The grid corner retires, and the icon takes its place in kickers and on section openers.</li>
<li>The app icon and avatars use the two-color tile on Charcoal, from 76 px.</li>
</ol>
<p>You would accept two weaknesses. Track is the busiest of the four and the faintest at 16 px. Act measures about a fifth smaller than Explain in the same box (${fmt(h('CL-022'), 1)} against ${fmt(h('CL-019'), 1)} px at 128 px). If you would rather the pillars show people and public acts, Set C is our second choice. Set B ties its four together best, at the cost of three topic drawings and two pillars that both show writing.</p>
<h3>One question for you</h3>
<p>Below 48 px a pillar mark sits with its word. In a kicker the content label sits beside the icon instead: Explainer, Tracker and Act carry the pillar’s word, and Guide does not name Connect. We recommend the label counts as the word in a kicker, because it already tells the reader what kind of piece it is, and the pillar’s own word stands on its section opener and in the pillar row. If you would rather, the kicker keeps a topic icon and the pillar mark stays out of it.</p>
</div>
<div class="rec-marks" aria-label="Set A in Newsprint on Prussian">${pillarRow(a.ids, { px: 48, ed: 'newsprint' })}</div></div>
</section>`;
}

function shortlist() {
  const groups = SHORTLIST.map((g) => `<div class="sl-g"><h3>${g.p}</h3><ul class="sl">${g.items.map(([id, why, used]) => `<li class="${used ? 'used' : ''}">${icon(id, 'red-black', 48)}<div><p class="sl-id"><b>${id}</b> ${esc(name(id))}</p><p>${esc(why)}</p>${used ? `<p class="sl-used">${esc(used)}</p>` : ''}</div></li>`).join('')}</ul></div>`).join('');
  return `<section id="how" aria-labelledby="how-h">
<p class="secnum">03</p><h2 id="how-h">How we chose from the 122</h2>
<p>We read all 122 drawings on the five contact sheets, then narrowed them in three steps.</p>
<ol class="steps">
<li>We kept the 72 drawings on sheets 01 to 03. The 50 reform drawings on sheets 04 and 05 each stand for a proposal the atlas weighs, and a pillar mark on a proposal would look like an endorsement.</li>
<li>We kept the 29 of those that still read at 24 px, the kicker size, in the October 29 trace review.</li>
<li>We set aside ten whose subject names a harm or one policy area, such as Market Power or Healthcare, and Feedback Loop, which raters took for a refresh sign in all three earlier icon tests.</li>
</ol>
<p>That left the 19 below, sorted by the pillar each could serve. Icons in the three sets carry the set’s name.</p>
<div class="sl-wrap">${groups}</div>
</section>`;
}

function whyCards(s, M) {
  return `<div class="why4">${s.ids.map((id, i) => {
    const n = NOTES[id]; const p = PILLARS[i];
    const kept = s.kept && s.kept[id];
    return `<article class="why"><div class="why-ic">${icon(id, 'red-black', 128)}</div>
<h4><span class="pw">${p.word}</span><span class="why-id">${id} ${esc(name(id))}</span></h4>
<p class="fit">${esc(kept || n.fit)}</p>
<p class="watch"><b>Watch.</b> ${esc(n.watch)}</p></article>`;
  }).join('')}</div>`;
}

function sizes(s, M) {
  const cell = (id, ed, px, label) => `<figure class="lc">${icon(id, ed, px)}<figcaption>${label}</figcaption></figure>`;
  const cards = s.ids.map((id, i) => `<div class="ladp"><p class="lad-w"><b>${PILLARS[i].word}</b><span>${id}</span></p>
<div class="ladrow">${cell(id, 'black', 16, '16 px')}${cell(id, 'black', 24, '24 px')}${cell(id, 'red-black', 48, '48 px')}${cell(id, 'red-black', 128, '128 px')}</div>
<div class="zm-i"><img src="${M.zoom[id][16]}" width="64" height="64" alt="${esc(PILLARS[i].word)}, ${id}, as Chrome draws it at 16 px, enlarged four times"><img src="${M.zoom[id][24]}" width="96" height="96" alt="${esc(PILLARS[i].word)}, ${id}, as Chrome draws it at 24 px, enlarged four times"></div>
<p class="zmcap">${M.per[id].px3_16} ${M.per[id].px3_16 === 1 ? 'pixel reaches' : 'pixels reach'} 3:1 at 16 px, and ${M.per[id].px3_24} at 24 px.</p></div>`).join('');
  return `<h3 class="sub">Sizes</h3>
<p>Each icon at 16 and 24 px in one color, and at 48 and 128 px in two colors. The line is ${fmt(STROKE * 16 / 128)} px wide at 16 px and ${fmt(STROKE * 24 / 128)} px at 24 px, and red under a full pixel reads as pink, so both small sizes stay one color. Under each ladder, the 16 and 24 px icons appear as the screen draws them, enlarged four times.</p>
<div class="lad4">${cards}</div>`;
}

function rows(s) {
  return `<h3 class="sub">In the pillar row</h3>
<p>At 48 px in one color, with Track as the current pillar keeping its red. Below it, the compact row at 24 px, where bold type and an underline mark the current pillar.</p>
<div class="rowdemo">${pillarRow(s.ids, { px: 48, current: 'track' })}</div>
<div class="rowdemo compact">${pillarRow(s.ids, { px: 24, current: 'track', size: 's' })}</div>`;
}

function opener(s) {
  const i = 2; const p = PILLARS[i]; const id = s.ids[i];
  return `<h3 class="sub">On a section opener</h3>
<p>Connect’s opener at true size. It is a Charcoal panel, as the guide’s part openers are, with the icon at 128 px in Newsprint and red.</p>
<div class="opener"><div class="op-ic">${icon(id, 'red-newsprint', 128)}</div><div class="op-t"><p class="op-l">Section ${p.n}</p><p class="op-w">${p.word}</p><p class="op-j">${esc(p.job)}</p></div></div>`;
}

function kickers(s) {
  const cards = PIECES.map((k, i) => `<div class="card"><p class="kick">${icon(s.ids[i], 'black', 24)}<span class="lb">${esc(k.label)}</span>${k.part ? `<span class="dot" aria-hidden="true">·</span><span class="sx">${esc(k.part)}</span>` : ''}${k.ill ? '<span class="chip ill">Illustrative</span>' : ''}</p>
<p class="hl">${esc(k.head)}</p><p class="cap">${PILLARS[i].word} piece</p></div>`).join('');
  return `<h3 class="sub">In a kicker</h3>
<p>The tops of the four story cards from chapter 01 at true size, 340 px wide. The icon takes the place the grid held, at 24 px in one color, with 12 px before the content label.</p>
<div class="cards">${cards}</div>`;
}

function tiles(s) {
  const t = s.ids.map((id, i) => `<figure class="tl"><div class="tl-i">${tile(id, 128)}${tile(id, 76)}</div><figcaption>${PILLARS[i].word}</figcaption></figure>`).join('');
  return `<h3 class="sub">As a tile on Charcoal</h3>
<p>The two-color rounded tiles, the default for the app icon and avatars, at 128 px and at 76 px, the smallest size where the rounded tile keeps its red.</p>
<div class="tiles">${t}</div>`;
}

function setSection(s, M, n) {
  const pairs = closePairs(s, M);
  return `<section class="set" id="set-${s.key}" aria-labelledby="set-${s.key}-h">
<div class="set-head"><span class="setnum" aria-hidden="true">${s.letter}</span><div><p class="secnum">${n}</p><h2 id="set-${s.key}-h">Set ${s.letter}, ${esc(s.name.toLowerCase())}${s.rec ? ' <span class="chip solid">Recommended</span>' : ''}</h2>
<p class="ids">${s.ids.map((id, i) => `${PILLARS[i].word}: ${id}${name(id) !== PILLARS[i].word ? ' ' + esc(name(id)) : ''}`).join(' · ')}</p>
<p>${esc(s.family)} ${esc(s.use)}</p>
<p class="small">Closest pair in shape at 24 px: ${pairs[0].a} and ${pairs[0].b}, more alike than ${Math.round(pairs[0].pct)} percent of the 7,381 pairs in the Civic Line.</p></div></div>
<h3 class="sub">Why each icon fits</h3>${whyCards(s, M)}
${sizes(s, M)}${rows(s)}${opener(s)}${kickers(s)}${tiles(s)}
</section>`;
}

function pct(M, v) { const all = M.sorted; let lo = 0, hi = all.length; while (lo < hi) { const m = (lo + hi) >> 1; if (all[m] < v) lo = m + 1; else hi = m; } return 100 * lo / all.length; }
function pairVal(M, a, b) { return M.pairs[a + '|' + b] ?? M.pairs[b + '|' + a]; }
function closePairs(s, M) {
  const out = [];
  for (let i = 0; i < 4; i++) for (let j = i + 1; j < 4; j++) {
    const v = pairVal(M, s.ids[i], s.ids[j]);
    out.push({ a: PILLARS[i].word, b: PILLARS[j].word, ida: s.ids[i], idb: s.ids[j], v, pct: pct(M, v) });
  }
  return out.sort((x, y) => y.v - x.v);
}

const RISKS = {
  a: ['Track and Explain: the magnifier in Track reads as “look into”, which a newcomer may give to Explain.', 'Explain and Connect: they are the most alike in shape in Set A, and a newcomer who reads the rings as “compare” may give them to Explain.'],
  b: ['Connect and Act: the letter and the signed page both show writing, and either could be the other.', 'Track and Explain: the folder and the book both hold reading, and a newcomer may give the folder to Explain.'],
  c: ['Connect and Act match at once, but a newcomer may read the ballot as Act meaning “vote” and nothing else.', 'Track and Explain keep Set A’s small risk with the magnifier.'],
};

function naming(M) {
  const rowsHtml = SETS.map((s) => s.ids.map((id, i) => `<tr><th scope="row">${s.letter}</th><td>${PILLARS[i].word}</td><td class="ni">${icon(id, 'black', 24)}<span>${id} ${esc(name(id))}</span></td><td>${esc(NOTES[id].read)}</td><td>${NOTES[id].leads}</td></tr>`).join('')).join('');
  const pairs = SETS.map((s) => {
    const cp = closePairs(s, M).slice(0, 2);
    return `<div class="np"><h3>Set ${s.letter}</h3><ul>${RISKS[s.key].map((r) => `<li>${esc(r)}</li>`).join('')}</ul>
<p class="small">Most alike in shape at 24 px: ${cp.map((c) => `${c.a} and ${c.b}, ${ordinal(c.pct)} percentile`).join('; ')}.</p></div>`;
  }).join('');
  return `<section id="naming" aria-labelledby="naming-h">
<p class="secnum">07</p><h2 id="naming-h">Could a newcomer match each icon to its word?</h2>
<p>We ran a quick test of our own. For each icon we wrote down what a newcomer would likely call it, then asked whether that name leads to its word. This is the studio’s reading, and no outside reader has seen these sets. The reader check you approved for Gate 2 can test the pick with five or more people.</p>
<div class="tw narrow" role="region" aria-label="Naming test table" tabindex="0"><table class="nt"><thead><tr><th scope="col">Set</th><th scope="col">Word</th><th scope="col">Icon</th><th scope="col">A newcomer would likely say</th><th scope="col">Leads to the word</th></tr></thead><tbody>${rowsHtml}</tbody></table></div>
<h3 class="sub">Pairs that risk confusion</h3>
<div class="nps">${pairs}</div>
<p class="small">Likeness in shape: we drew all 122 icons at 24 px, blurred each slightly and compared every pair, 7,381 in all. A pair at the 90th percentile looks more alike than nine pairs in ten.</p>
<h3 class="sub">What raters confused in the earlier icon tests</h3>
<ul class="facts">
<li>Lids and opened boxes read as cameras and notification badges. No set here uses a lid.</li>
<li>Boxes holding a card read as printers or trays, in all three tests. Set C’s ballot box and Set B’s folder carry that risk.</li>
<li>Loops with arrows read as a refresh or sync sign, in all three tests. We left Feedback Loop out.</li>
<li>Two halves facing each other read as a no-entry sign or a broadcast signal. Set A’s rings overlap and close, and a newcomer names them a Venn diagram.</li>
<li>A house with a red door competed with Act’s door. No set here uses a house or a door.</li>
</ul>
<p class="small">Those tests used other drawings, from the three concepts before the Civic Line, and agent raters in place of people.</p>
</section>`;
}

function measures(M) {
  const ids = [...new Set(SETS.flatMap((s) => s.ids))];
  const rowsHtml = ids.map((id) => {
    const inSets = SETS.filter((s) => s.ids.includes(id)).map((s) => s.letter).join(', ');
    const p = M.per[id];
    return `<tr><th scope="row">${id} ${esc(name(id))}</th><td>${inSets}</td><td class="num">${p.px3_16}</td><td class="num">${p.px3_24}</td><td class="num">${fmt(p.hull128, 1)}</td></tr>`;
  }).join('');
  const setRows = SETS.map((s) => { const c = closePairs(s, M)[0]; return `<tr><th scope="row">Set ${s.letter}</th><td>${c.a} and ${c.b}</td><td class="num">${fmt(c.v, 3)}</td><td class="num">${ordinal(c.pct)}</td></tr>`; }).join('');
  return `<section id="measure" aria-labelledby="measure-h">
<p class="secnum">08</p><h2 id="measure-h">Measurements</h2>
<p>Chrome drew each black master on Newsprint. The line is ${fmt(STROKE * 16 / 128)} px at 16 px and ${fmt(STROKE * 24 / 128)} px at 24 px for all nine icons. Size is the square root of the area inside the outline around all the ink, at 128 px.</p>
<div class="tw narrow" role="region" aria-label="Measurements for each icon" tabindex="0"><table><thead><tr><th scope="col">Icon</th><th scope="col">In sets</th><th scope="col" class="num">Pixels at 3:1 or more, 16 px</th><th scope="col" class="num">Pixels at 3:1 or more, 24 px</th><th scope="col" class="num">Size at 128 px</th></tr></thead><tbody>${rowsHtml}</tbody></table></div>
<div class="tw narrow" role="region" aria-label="Closest pair in each set" tabindex="0"><table><thead><tr><th scope="col">Set</th><th scope="col">Closest pair in shape at 24 px</th><th scope="col" class="num">Likeness</th><th scope="col" class="num">Percentile of 7,381 pairs</th></tr></thead><tbody>${setRows}</tbody></table></div>
<p class="small">A 16 px icon has 256 pixels. A Civic Line master at 16 px reaches 3:1 against Newsprint in a handful of them, so at that size the icon needs a small drawing of its own, which this round does not make.</p>
</section>`;
}

const CSS = `
:root{color-scheme:light;--np:#DCD9D2;--ch:#121212;--stone:#5D636D;--deep:#4E535B;--dim:#A3A19C;--pr:#1F2D5A;--white:#FFFFFF;--surface:#E6E3DD;--hair:#C9C6BF;
--display:"Inter Tight","Helvetica Neue",Arial,sans-serif;--body:"Inter","Helvetica Neue",Arial,sans-serif;--quote:"Lora",Georgia,serif}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--np);color:var(--ch);font:400 1rem/1.6 var(--body)}
a{color:inherit;text-underline-offset:3px}a:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--ch);outline-offset:3px}
.board{max-width:1280px;margin:0 auto;padding-block:40px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--ch);padding-bottom:14px;flex-wrap:wrap}
.mast b{font:800 1.25rem/1 var(--display);letter-spacing:-.02em;white-space:nowrap}.mast span{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--deep)}
.eyebrow{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--deep);margin:28px 0 0}
h1,h2,h3,h4{font-family:var(--display);letter-spacing:-.02em;text-wrap:balance;margin:0}
h1{font-weight:800;font-size:clamp(2.5rem,6vw,4.5rem);line-height:1;margin-top:10px;max-width:16ch;letter-spacing:-.03em}
h2{font-weight:800;font-size:clamp(1.5rem,3vw,2.25rem);line-height:1.08;margin:0 0 12px;letter-spacing:-.025em}
h3{font-weight:700;font-size:1.25rem;line-height:1.25}
h4{font-weight:700;font-size:1.0625rem;line-height:1.3}
p{margin:0 0 12px;max-width:70ch}.deck{font-size:1.25rem;line-height:1.5;max-width:60ch;margin-top:18px}
section{border-top:1px solid var(--stone);margin-top:56px;padding-top:32px}
.toc+section{border-top:0;margin-top:24px;padding-top:24px}
.secnum{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;color:var(--deep);margin:0 0 6px}
.sub{margin:40px 0 10px}
.lab{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--deep);margin:24px 0 10px}
.small{font-size:.875rem;color:var(--deep)}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.chip{display:inline-block;font:700 .8125rem/1 var(--body);letter-spacing:.06em;text-transform:uppercase;padding:5px 8px;border:1px solid var(--ch);vertical-align:middle;white-space:nowrap}
.chip.solid{background:var(--ch);color:var(--np)}.chip.ill{border-style:dashed;color:var(--deep);border-color:var(--deep)}
.toc{display:flex;flex-wrap:wrap;gap:4px 22px;margin:22px 0 0;padding:8px 0;border-top:1px solid var(--stone);border-bottom:1px solid var(--stone)}
.toc a{font:600 .9375rem/1.4 var(--body);text-decoration:none;display:inline-flex;align-items:center;min-height:44px;white-space:nowrap}.toc a:hover{text-decoration:underline}
.ico{display:inline-block;flex:none;line-height:0}.ico svg{display:block}
/* pillar rows */
.prow{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;gap:12px 0}
.prow .pi{display:flex;align-items:center;gap:12px}
.prow .pi:not(:last-child)::after{content:"→";color:var(--stone);font:400 1.25rem/1 var(--body);margin:0 18px}
.prow-m .pw{font:700 1.375rem/1 var(--display);letter-spacing:-.01em}
.pwrap{display:flex;flex-direction:column;gap:4px;min-width:0}.pid{font:500 .8125rem/1.3 var(--body);color:var(--deep)}
.prow-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px 0;align-items:center}
.prow-grid .pi{position:relative;padding-right:36px}
.prow-grid .pi:not(:last-child)::after{position:absolute;right:8px;top:50%;transform:translateY(-50%);margin:0}
.prow-s .pi{gap:8px}.prow-s .pw{font:500 1rem/1 var(--body)}.prow-s .pi:not(:last-child)::after{margin:0 12px;font-size:1rem}
.prow-s .cur .pw{font-weight:700;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:5px}
/* comparison */
.cmp{border-top:2px solid var(--ch);margin-top:20px}
.cmp-row{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:16px 40px;align-items:center;padding:24px 0;border-bottom:1px solid var(--stone)}
.cmp-h h3{font-size:1.375rem}.setid{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--deep);margin:0 0 4px}
.ids{font-size:.875rem;color:var(--deep);margin:6px 0 0}
.big{display:grid;gap:8px}
.big-row{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:16px 40px;align-items:center;border-top:1px solid var(--hair);padding:20px 0}
.big-cells{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.big-cell{margin:0;display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.big-cell figcaption{display:flex;flex-direction:column;font-size:.875rem;color:var(--deep);line-height:1.4}.big-cell figcaption b{font:700 1.0625rem/1.3 var(--display);color:var(--ch)}
/* decision band */
.decision{background:var(--pr);color:var(--np);border-top:0;padding:32px max(20px,3vw);margin-top:56px}
.decision h2,.decision h3{color:var(--white)}.decision .secnum{color:var(--np)}
.decision h3{margin:20px 0 8px}
.rec-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,auto);gap:32px 48px;align-items:start}
.changes{margin:0 0 16px;padding-left:1.3em}.changes li{margin:0 0 8px;max-width:72ch}
.rec-marks{border:1px solid var(--np);padding:20px 24px}
.rec-marks .prow{flex-direction:column;align-items:flex-start;gap:14px}
.rec-marks .prow .pi:not(:last-child)::after{content:none}
.rec-marks .pw{color:var(--np)}
/* shortlist */
.steps{padding-left:1.3em;margin:0 0 16px}.steps li{margin:0 0 8px;max-width:76ch}
.sl-wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr));gap:28px 32px;margin-top:16px}
.sl-g h3{border-bottom:2px solid var(--ch);padding-bottom:6px;margin-bottom:4px}
.sl{list-style:none;margin:0;padding:0}
.sl li{display:grid;grid-template-columns:48px minmax(0,1fr);gap:14px;padding:12px 0;border-bottom:1px solid var(--hair);font-size:.9375rem;line-height:1.45}
.sl li p{margin:0 0 4px}.sl-id b{font-weight:700}.sl-used{font:700 .8125rem/1.4 var(--body);letter-spacing:.06em;text-transform:uppercase}
.sl li:not(.used) .ico{opacity:1}
/* set sections */
.set{border-top:2px solid var(--ch);margin-top:72px}
.set-head{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 28px;align-items:start}
.setnum{font:800 clamp(4rem,9vw,7rem)/.82 var(--display);letter-spacing:-.04em}
.why4{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr));gap:20px}
.why{background:var(--surface);border:1px solid var(--hair);padding:20px}
.why-ic{margin-bottom:12px}
.why h4{display:flex;flex-direction:column;gap:2px;margin-bottom:10px}.why h4 .pw{font:800 1.375rem/1.1 var(--display)}.why-id{font:500 .875rem/1.4 var(--body);color:var(--deep);letter-spacing:0}
.why p{font-size:.9375rem;line-height:1.5}.why .watch{margin:0}
.lad4{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:28px 24px;border-top:1px solid var(--stone);padding-top:16px}
.lad-w{margin:0 0 10px;display:flex;align-items:baseline;gap:10px}.lad-w b{font:700 1.125rem/1.3 var(--display)}.lad-w span{font-size:.875rem;color:var(--deep)}
.ladrow{display:flex;align-items:flex-end;gap:8px;padding-bottom:12px;border-bottom:1px solid var(--hair)}
.lc{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px;min-width:34px}.lc figcaption{font:500 .8125rem/1.2 var(--body);color:var(--deep);white-space:nowrap}
.zm-i{display:flex;align-items:flex-end;gap:12px;margin:14px 0 8px}
.zm-i img{image-rendering:pixelated;image-rendering:crisp-edges;display:block;outline:1px solid var(--hair)}
.zmcap{font-size:.875rem;color:var(--deep);line-height:1.4;margin:0}
.rowdemo{border:1px solid var(--hair);padding:20px 24px;background:var(--np);margin:0 0 12px}
.opener{background:var(--ch);color:var(--np);display:grid;grid-template-columns:128px minmax(0,1fr);gap:40px;align-items:center;padding:48px max(24px,4vw)}
.op-l{font:700 .8125rem/1.4 var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:0 0 8px}
.op-w{font:800 clamp(3rem,7vw,5.5rem)/1 var(--display);letter-spacing:-.035em;margin:0 0 14px;color:var(--np)}
.op-j{font-size:1.25rem;line-height:1.45;margin:0;max-width:40ch}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,340px));gap:24px 40px}
.card{background:var(--np);border-top:2px solid var(--ch);padding:14px 0 0;max-width:340px}
.kick{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:0 0 10px;font:700 .8125rem/1.3 var(--body);letter-spacing:.06em;text-transform:uppercase}
.kick .ico{margin-right:4px}.kick .dot,.kick .sx{color:var(--deep)}
.hl{font:800 1.5rem/1.15 var(--display);letter-spacing:-.02em;margin:0 0 8px}
.cap{font-size:.875rem;color:var(--deep);margin:0}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:24px}
.tl{margin:0}.tl-i{display:flex;align-items:flex-end;gap:12px;margin-bottom:8px}.tl figcaption{font:700 1.0625rem/1.3 var(--display)}
/* naming and measures */
.tw{overflow-x:auto;border:1px solid var(--stone);background:var(--white);margin:12px 0 16px}
table{border-collapse:collapse;width:100%;font-size:.9375rem;font-variant-numeric:tabular-nums}
th,td{text-align:left;vertical-align:middle;padding:10px 14px;border-bottom:1px solid var(--hair)}
thead th{font:700 .8125rem/1.3 var(--body);letter-spacing:.02em;text-transform:uppercase;color:var(--deep);background:var(--surface)}
td.num,th.num{text-align:right}
.tw table{min-width:560px}.tw.narrow{max-width:960px}
.ni{display:flex;align-items:center;gap:10px}
.nps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:20px}
.np ul,.facts{margin:0 0 8px;padding-left:1.1em}.np li,.facts li{margin:0 0 6px;max-width:72ch}
.foot{border-top:1px solid var(--stone);margin-top:56px;padding-top:16px}
@media (max-width:900px){.cmp-row{grid-template-columns:minmax(0,1fr)}.rec-grid{grid-template-columns:minmax(0,1fr)}
.big-row{grid-template-columns:minmax(0,1fr)}.big-cells{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.prow{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 0}.prow .pi{position:relative;padding-right:28px}
.prow .pi:not(:last-child)::after{position:absolute;right:6px;top:50%;transform:translateY(-50%);margin:0}.prow .pi:nth-child(2n)::after{content:none}
.rec-marks .prow{display:flex}.rec-marks .prow .pi{padding-right:0}
.prow-m .pi:not(:last-child)::after{margin:0}.prow-m .pw{font-size:1.125rem}.prow .pi{gap:8px}
.rowdemo{padding:16px}.opener{grid-template-columns:minmax(0,1fr);gap:20px;padding:32px 20px}
.set-head{grid-template-columns:minmax(0,1fr)}.tiles{padding:20px}.big-cells{gap:12px}}
@media (max-width:760px){.cards{grid-template-columns:minmax(0,340px)}.prow-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 0}.prow-grid .pi:nth-child(2n)::after{content:none}.prow-grid .pi{padding-right:28px}}
`;

function page(M) {
  const toc = [['compare', 'The three sets'], ['rec', 'Recommendation'], ['how', 'How we chose'], ['set-a', 'Set A'], ['set-b', 'Set B'], ['set-c', 'Set C'], ['naming', 'Naming test'], ['measure', 'Measurements']]
    .map(([h, t]) => `<a href="#${h}">${t}</a>`).join('');
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="chart-views" content="board">
<title>Board 6 Pillar Icons</title>
<meta name="description" content="Three sets of four pillar icons drawn from the 122 Civic Line icons, compared in the pillar row and in use, with a recommendation.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>${CSS}</style></head>
<body><main class="board" data-view-root="board">
<header class="mast"><b>Oath &amp; Action</b><span>Edition 06 · Board 6, section 2 · November 7, 2026</span></header>
<p class="eyebrow">Board 6 · Pillar icons</p>
<h1>Four pillar icons from the Civic Line</h1>
<p class="deck">You asked us to revisit the civic icons and show a few thoughts on the four pillar icons. We read all 122 Civic Line drawings and drew three sets of four from them. Each set stands first in the pillar row, so you can compare them in one view, and then in use. Each pillar is now its icon with its word, with no grid corner.</p>
<p>Every icon on this page is a Civic Line master as supplied, in one of its four editions or its Charcoal tile, placed at the size shown. Nothing is redrawn or recolored.</p>
<nav class="toc" aria-label="On this page">${toc}</nav>
${compareSection(M)}
${recommendation(M)}
${shortlist()}
${SETS.map((s, i) => setSection(s, M, String(4 + i).padStart(2, '0'))).join('\n')}
${naming(M)}
${measures(M)}
<footer class="foot"><p class="small">Built on November 7, 2026 by <code>work/build/scripts/phase-2/board6_pillar_icons_build.js</code> from the Civic Line masters in <code>work/build/assets/civic-line/</code>. The measurements are in <code>20261107_Board-6-Pillar-Icons-Measurements.json</code> beside this page.</p></footer>
</main></body></html>
`;
}

(async () => {
  const M = await measure();
  M.sorted = Object.values(M.pairs).sort((a, b) => a - b);
  fs.mkdirSync(OUTDIR, { recursive: true });
  const html = page(M);
  if (/—/.test(html)) throw new Error('em dash in page');
  fs.writeFileSync(OUT, html);
  const setsOut = SETS.map((s) => ({ set: s.letter, name: s.name, ids: s.ids, pairs: closePairs(s, M).map((c) => ({ a: c.ida, b: c.idb, likeness: c.v, percentile: +c.pct.toFixed(1) })) }));
  const ids = [...new Set(SETS.flatMap((s) => s.ids))];
  const meas = {
    built: '2026-11-07', script: 'work/build/scripts/phase-2/board6_pillar_icons_build.js', renderer: M.ua,
    method: {
      pixels_at_3to1: 'Black master drawn by Chrome on a Newsprint (#DCD9D2) canvas at 16 and 24 px; count of pixels whose contrast with Newsprint is 3:1 or more.',
      size_128: 'Square root of the convex hull area of pixels with ink coverage over one half, black master at 128 px.',
      likeness_24: 'Ink maps at 24 px blurred with a Gaussian of sigma 1.2 px; Pearson correlation, best over shifts of up to 1 px; percentile among all 7,381 pairs of the 122 masters.',
      line_px: { '16': +(STROKE * 16 / 128).toFixed(3), '24': +(STROKE * 24 / 128).toFixed(3), '48': +(STROKE * 48 / 128).toFixed(3) },
    },
    pair_distribution: { pairs: M.sorted.length, p50: M.sorted[Math.floor(M.sorted.length * 0.5)], p90: M.sorted[Math.floor(M.sorted.length * 0.9)], p95: M.sorted[Math.floor(M.sorted.length * 0.95)] },
    icons: Object.fromEntries(ids.map((id) => [id, { label: name(id), ...M.per[id] }])),
    all_icons: M.per,
    sets: setsOut,
  };
  fs.writeFileSync(MEAS, JSON.stringify(meas, null, 1));
  console.log('wrote', path.relative(ROOT, OUT), (html.length / 1024).toFixed(0) + ' KB');
  console.log('wrote', path.relative(ROOT, MEAS));
  for (const s of setsOut) console.log('Set', s.set, s.pairs.slice(0, 2).map((p) => `${p.a}/${p.b} ${p.likeness} (${p.percentile})`).join('; '));
  for (const id of ids) console.log(id, JSON.stringify(M.per[id]));
})().catch((e) => { console.error(e); process.exit(1); });
