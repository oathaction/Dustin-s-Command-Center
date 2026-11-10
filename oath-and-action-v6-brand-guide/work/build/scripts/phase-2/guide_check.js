// Rendered checks for an Oath & Action guide page built by guide_build.py (November 6, 2026, guide engineer).
// The chart checks stay in dataviz_check.js; this script holds the tests guide pages need, and ports the text, red,
// overflow, axe and focus checks so one run covers a guide page.
//
// Usage:
//   node work/build/scripts/phase-2/guide_check.js <page.html> [--quick] [--no-captures]
//   node work/build/scripts/phase-2/guide_check.js --self-test [--results out.json]   plants each fault in a demo build and proves
//                                                                the test catches it (results default to the stage A board folder)
//
// Widths: 1440, 1024, 390 and 360 px (--quick: 1440 and 390). At every width it checks:
//   structure  exactly one h1; no skipped heading level; no heading inside a specimen; every h3 in a chapter is a rule
//              h3 or one of the closers (Specifications, Related chapters, For builders); every rule h3 starts with
//              "Rule NN.n", NN is its chapter's number, and its rule block carries id="rule-NN-n" (map sections 4 and 5)
//   anchors    unique ids; every same-page link lands on an id; every Related chapters link lands on a chapter; V5 aliases
//              (#grid and the rest) sit inside their new chapter when that chapter is in the page
//   specimens  every plate stage named by its alt (15 characters or more) or described when interactive; no pending
//              specimen; every <img> has alt; every inline <svg> is named or hidden
//   text       nothing under 13 px; text contrast 4.5 to 1, or 3 to 1 for large text, from rendered colors
//   red        Rule 05.3: every Pillar Red mark under data-red; one working-red job at most outside specimens and inside
//              each specimen; no red on Prussian
//   writing    locked lines character for character wherever a fragment of one appears; pillars in order; no em dash
//              outside [data-allow-emdash] (DR-79)
//   page       no sideways scroll outside a scrolling frame; axe-core 4.10.2 (WCAG 2.2 AA tags); outside requests other
//              than Google Fonts; script errors; at 1440, a visible focus ring on the first 60 Tab stops
// Added in the stage A fix pass (November 6, 2026):
//   specimenLandmarks  no <nav>, <article>, <header>, <footer>, <main>, <aside>, named <section> or <form>, or
//                      landmark role inside a stage (AX-S8)
//   nameEntities       no accessible name (aria-label, alt, title, SVG title and desc, the text an aria-labelledby or
//                      aria-describedby points at) holds an entity such as "&amp;", and no visible text outside code
//                      shows "&amp;" (AX-M2, RP-M4)
//   typeScale          every font size inside a stage is one D2-254 allows: the phone floor up to 600 px wide, the desktop
//                      ceiling from 1,200 px, either between, plus each style's fluid size at the checked width for a
//                      stage with no width and the chart system's own sizes; a stage with data-scale also passes at
//                      size divided by its scale; check_exempt "scale" skips the stage (D2-254, C-M7)
//   codes              no decision code (DR-, D1-, D2-, G1-, T-, R9, R13, I6, I8, S5, S9) and none of "Master Brief",
//                      "Phase", "Gate", "gate" where it names the studio's gate, "Board 5" or any "Board N" or "board A" to "F", "stage A" to
//                      "stage C", "stage board", "the studio", "V5", "V4.2", "Atlas V7" in reader text, alt text and
//                      accessible names (D2-253; the case-free "gate" and the board and stage names from the apply pass)
// Added in the apply pass (November 7, 2026):
//   retiredWords       none of "Signal Grid" (D2-326), "Stage n of 9" or "nine stages" (the six-step tracker, DR-108)
//                      and "condensed width, proposed" (DR-115, D2-328) in reader text, alt text, accessible names or
//                      the document title, failure plates included
//   retiredClasses     no element carries a class the makers' grid specimens used for a retired grid job (the coded
//                      grid, its key and nine-stage sheet, grid states, the composer: DR-110), except inside a labeled
//                      failure plate, where chapter 08 shows one retired use on purpose
//   partOrder          every chapter sits under its own part's opener, and that opener links to it (D2-324)
//   ruleRefs           every rule a citation names ("Rule 05.2", "Rules 05.3 and 05.5", "Rules 08.4 to 08.8") exists
//                      when its chapter's rules are in the page, so an old chapter 08 number cannot hide (D2-325)
// Added in the apply pass's fix pass (November 7, 2026):
//   fitFloor           every plate whose True size / Fit to window switch shows is set to Fit to window, and its
//                      smallest rendered text (HTML text times the fit scale, SVG text at its drawn size) must stay at
//                      13 px or more; the switch is then set back (CA-M1). Plates with no switch showing are skipped.
//   illusOnce          a plate carries the Illustrative label once: never in both the piece and its caption (DR-97,
//                      CD-N1, CA-N11)
// Added in the Q1 to Q4 pass (November 8, 2026), both read at true size before fitFloor runs:
//   scrollHint         a plate frame says it scrolls only when it does: a frame that holds its stage whole shows no
//                      "Wider than this column" hint, no tab stop and no "Scroll sideways" name, and a frame that
//                      scrolls shows all three (CD-S9, AX-S3, AX-S12)
//   frameFit           no frame scrolls with sides over 32 px when 32 px sides would hold its stage whole, and a stage
//                      in a frame that does not scroll sits centered, within 1 px, at true size (CD-S9)
// A plate whose stage carries data-check-exempt="contrast size red locked" skips that test inside it; every exemption
// is listed in the results. Writes <page stem>-Guide-Check-Results.json beside the page, and one capture per section at
// 1440 and 390 px to captures/. Exit code 1 when any check fails.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '../../../..');
const AXE_CANDIDATES = [process.env.AXE_PATH, path.join(ROOT, 'work/build/node_modules/axe-core/axe.min.js'),
  path.join(process.env.TMPDIR || os.tmpdir(), 'oa-axe/node_modules/axe-core/axe.min.js')].filter(Boolean);
const AXE = AXE_CANDIDATES.find((p) => fs.existsSync(p)) || null;
const ALLOWED_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com'];
const RED = [230, 57, 70];
const PRUSSIAN = [31, 45, 90];
const LOCKED = [
  { name: 'tagline', full: 'A country that answers to its people.', frags: ['answers to its people', 'A country that answers'] },
  { name: 'mission', full: 'Help people understand and improve the rules that shape their lives.', frags: ['rules that shape their lives', 'understand and improve the rules'] },
  { name: 'reader promise', full: 'We explain how a decision is made and give you a practical way to take part.', frags: ['practical way to take part', 'how a decision is made and give'] },
  { name: 'editorial commitment', full: 'Clarity is our duty. Action is our promise.', frags: ['Clarity is our duty', 'Action is our promise'] },
];
const ALIASES = [['grid', 'lockmark'], ['topic-icons', 'symbols'], ['data', 'data-visualization'], ['motion', 'motion-and-states'],
  ['atlas-system', 'systems-graphics'], ['in-use', 'part-applications']];
const CLOSERS = ['Specifications', 'Related chapters', 'For builders'];
// D2-254: fixed artboards up to 600 px take each style's phone floor; from 1,200 px its desktop ceiling.
const SCALE_FLOOR = [56, 44, 48, 26, 20, 24, 19, 17, 15, 14, 13];
const SCALE_CEIL = [110, 80, 104, 32, 24, 22, 19, 17, 15, 14, 13];
const TYPE_STYLES = ['title', 'section', 'h3', 'h4', 'quote', 'intro', 'body', 'body-small', 'ui', 'caption', 'label', 'data-label', 'figure', 'ask'];
const CHART_SIZES = ['--oa-chart-type-label', '--oa-chart-type-tick', '--oa-chart-type-note', '--oa-chart-type-phone-min', '--oa-chart-type-tile-code-phone',
  '--oa-chart-type-big', '--oa-chart-type-big-phone', '--oa-chart-type-eyebrow', '--oa-chart-type-title-size', '--oa-chart-type-title-phone-size', '--oa-chart-type-measure-size'];
// D2-253: words and codes that never reach a reader. Each entry: [pattern source, flags, what it is].
const CODE_PATTERNS = [
  ['\\b(?:DR|D1|D2|G1)-\\d+', 'g', 'decision code'],
  ['\\bT-\\d+\\b', 'g', 'decision code'],
  ['(?<![Ll]oop )\\b(?:R9|R13|I6|I8|S5|S9)\\b', 'g', 'decision code'],
  ['\\bMaster Brief\\b', 'g', 'internal document'],
  ['\\bPhase\\b', 'g', 'studio word'],
  // "Gate" with a capital always; "gate" where it names the studio's gate (the next gate, this gate, a gate report), not
  // a gate drawn in a symbol, such as R-42's parcel at a gate (round 2, November 10, 2026)
  ['\\bGates?\\b', 'g', 'studio word'],
  ['\\b(?:next|last|this|that|each|every|later|final|first|second|third|phase|stage|the)\\s+gates?\\b(?!\\s+(?:with|of|in|on|across|that|which)\\b)', 'gi', 'studio word'],
  ['\\bgates?\\s+(?:reports?|reviews?|approvals?|rules?|questions?|meetings?)\\b', 'gi', 'studio word'],
  ['\\b[Bb]oards?[\\s\\u00a0]+(?:\\d+|[A-F])\\b', 'g', 'studio word'],   // Board 6, board A; not "the board I serve on"
  ['\\b[Ss]tages?[\\s\\u00a0]+[A-C]\\b', 'g', 'studio word'],
  ['\\bstage board\\b', 'gi', 'studio word'],
  ['\\bthe studio\\b', 'gi', 'studio word'],
  ['\\bV5\\b', 'g', 'internal edition name'],
  ['\\bV4\\.2\\b', 'g', 'internal edition name'],
  ['\\bAtlas V7', 'g', 'internal document'],
];

// Apply pass (November 7, 2026). Words that left reader pages: [pattern source, flags, what it is].
const RETIRED_WORDS = [
  ['\\bSignal[\\s\\u00a0-]*Grid', 'gi', 'the name "Signal Grid" (D2-326: the drawing is the lockmark)'],
  ['\\bstages?[\\s\\u00a0]+(?:\\d+|one|two|three|four|five|six|seven|eight|nine)[\\s\\u00a0]+of[\\s\\u00a0]+(?:9|nine)\\b', 'gi', 'a nine-stage tracker (DR-108: six steps)'],
  ['\\b(?:nine|9)[\\s\\u00a0-]+stages?\\b', 'gi', 'a nine-stage tracker (DR-108: six steps)'],
  ['\\bcondensed[\\s\\u00a0]+width,?[\\s\\u00a0]+proposed\\b', 'gi', 'a condensed width proof (DR-115, D2-328)'],
];
// Class names the stage A grid specimens used for jobs DR-110 retires: the coded grid (oai-grid), its key (oai-lg), the
// nine-stage sheet and glossary (oai-st, oai-gl, oai-gl-d), the grid states (oai-pulse) and the composer (oai-comp,
// oai-compwrap). Read from stage_a_identity_lib.py and stage_a_identity_s08.py at commit 3130c5b.
const RETIRED_CLASSES = ['oai-grid', 'oai-lg', 'oai-st', 'oai-gl', 'oai-gl-d', 'oai-pulse', 'oai-comp', 'oai-compwrap'];

// ------------------------------------------------------------------------------------------------ in-page audit
function audit(page) {
  return page.evaluate(({ RED, PRUSSIAN, LOCKED, ALIASES, CLOSERS, SCALE_FLOOR, SCALE_CEIL, TYPE_STYLES, CHART_SIZES, CODE_PATTERNS, RETIRED_WORDS, RETIRED_CLASSES }) => {
    const parse = (c) => { const m = c && c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
    const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
    const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const near = (c, t, tol = 3) => c && c.a > 0.3 && Math.abs(c.r - t[0]) <= tol && Math.abs(c.g - t[1]) <= tol && Math.abs(c.b - t[2]) <= tol;
    const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
    const visible = (el) => {
      const r = el.getBoundingClientRect(); if (r.width === 0 && r.height === 0) return false;
      if (el.closest('dialog:not([open])')) return false;
      for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false; }
      return !(el.closest('details:not([open])') && !el.closest('summary'));
    };
    const exempt = (el, kind) => !!el.closest(`[data-check-exempt~="${kind}"]`);
    const where = (el) => { const s = el.closest('[data-specimen]'); if (s) return 'specimen ' + s.getAttribute('data-specimen'); const r = el.closest('.rule[id], .closer[id], [data-track]'); return r ? '#' + r.id : (el.id ? '#' + el.id : el.tagName.toLowerCase()); };
    const out = {};

    // ---------------- structure
    const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role="heading"]')]
      .filter((h) => !h.closest('dialog:not([open])') && !h.closest('[aria-hidden="true"]') && !h.closest('[data-specimen]') && visible(h));
    const lvl = (h) => h.getAttribute('role') === 'heading' ? parseInt(h.getAttribute('aria-level') || '2', 10) : parseInt(h.tagName[1], 10);
    const st = { headings: hs.length, h1: hs.filter((h) => lvl(h) === 1).map((h) => norm(h.textContent)), skips: [], inSpecimen: [], badH3: [], ruleIds: [], ruleAnchors: [], rulesWithoutH3: [], rules: 0 };
    let prev = 0;
    hs.forEach((h, i) => {
      const l = lvl(h);
      if (i === 0 && l !== 1) st.skips.push({ text: norm(h.textContent).slice(0, 50), from: 0, to: l });
      else if (i > 0 && l > prev + 1) st.skips.push({ text: norm(h.textContent).slice(0, 50), from: prev, to: l });
      prev = l;
    });
    document.querySelectorAll('[data-specimen] :is(h1,h2,h3,h4,h5,h6,[role="heading"])').forEach((h) => st.inSpecimen.push({ specimen: h.closest('[data-specimen]').getAttribute('data-specimen'), text: norm(h.textContent).slice(0, 40) }));
    document.querySelectorAll('section.chapter').forEach((sec) => {
      const num = sec.getAttribute('data-chapter');
      sec.querySelectorAll('h3').forEach((h) => {
        if (h.closest('[data-specimen]')) return;
        const t = norm(h.textContent);
        const m = t.match(/^Rule (\d{2})\.(\d{1,2})(?=\s|$)/);
        if (m) {
          st.rules++;
          if (m[1] !== num) st.ruleIds.push({ chapter: num, text: t.slice(0, 50), problem: `Rule ${m[1]}.${m[2]} sits in chapter ${num}` });
          const block = h.closest('[id^="rule-"]');
          const want = `rule-${m[1]}-${m[2]}`;
          if (!(h.id === want || (block && block.id === want))) st.ruleAnchors.push({ text: t.slice(0, 50), want, got: block ? block.id : (h.id || null) });
          return;
        }
        if (CLOSERS.includes(t)) {
          const c = h.closest('.closer[id]');
          if (!c) st.badH3.push({ chapter: num, text: t, problem: 'a closer h3 outside its closer block' });
          return;
        }
        if (/^Rule\b/.test(t)) st.ruleIds.push({ chapter: num, text: t.slice(0, 50), problem: 'starts with "Rule" but not with an ID of the form NN.n' });
        else st.badH3.push({ chapter: num, text: t.slice(0, 50), problem: 'an h3 that is neither a rule (Rule NN.n) nor a closer' });
      });
      sec.querySelectorAll('.rule').forEach((r) => { const h = r.querySelector('h3'); if (!h || !/^Rule \d{2}\.\d{1,2}(?=\s|$)/.test(norm(h.textContent))) st.rulesWithoutH3.push(r.id || '(no id)'); });
    });
    out.structure = st;

    // ---------------- anchors
    const counts = new Map();
    document.querySelectorAll('[id]').forEach((el) => counts.set(el.id, (counts.get(el.id) || 0) + 1));
    const an = { ids: counts.size, duplicates: [...counts].filter(([, n]) => n > 1).map(([id, n]) => ({ id, n })).slice(0, 20), links: 0, broken: [], relatedLinks: 0, relatedBad: [], aliases: [] };
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      const href = a.getAttribute('href'); if (href === '#') return; an.links++;
      if (!document.getElementById(decodeURIComponent(href.slice(1)))) an.broken.push({ href, text: norm(a.textContent).slice(0, 40), where: where(a) });
    });
    document.querySelectorAll('.rel-inline a, ul.related a').forEach((a) => {
      an.relatedLinks++;
      const t = document.getElementById(decodeURIComponent((a.getAttribute('href') || '').slice(1)));
      if (!t || !t.matches('section.chapter')) an.relatedBad.push({ href: a.getAttribute('href'), text: norm(a.textContent).slice(0, 40), where: where(a) });
    });
    for (const [alias, target] of ALIASES) {
      const t = document.getElementById(target); if (!t) continue;
      const al = document.getElementById(alias);
      if (!al || !t.contains(al)) an.aliases.push({ alias, target, problem: al ? 'outside its chapter' : 'missing' });
    }
    out.anchors = an;

    // ---------------- specimens and alt text
    const sp = { stages: 0, pending: [], noAlt: [], imgNoAlt: [], svgUnnamed: [], exemptions: [] };
    document.querySelectorAll('[data-specimen]').forEach((s) => {
      const id = s.getAttribute('data-specimen'); sp.stages++;
      if (s.hasAttribute('data-pending')) { sp.pending.push(id); return; }
      const ex = s.getAttribute('data-check-exempt'); if (ex) sp.exemptions.push({ specimen: id, skips: ex });
      const role = s.getAttribute('role');
      if (role === 'img') { const l = norm(s.getAttribute('aria-label')); if (l.length < 15) sp.noAlt.push({ specimen: id, label: l }); }
      else { const d = (s.getAttribute('aria-describedby') || '').split(/\s+/).map((x) => document.getElementById(x)).filter(Boolean).map((x) => norm(x.textContent)).join(' '); if (d.length < 15) sp.noAlt.push({ specimen: id, label: d, role }); }
    });
    document.querySelectorAll('img').forEach((im) => { if (!im.hasAttribute('alt')) sp.imgNoAlt.push({ src: (im.getAttribute('src') || '').slice(0, 60), where: where(im) }); });
    document.querySelectorAll('svg').forEach((s) => {
      if (s.parentElement && s.parentElement.closest('svg')) return;
      const anc = s.parentElement && s.parentElement.closest('[role="img"], [aria-hidden="true"]');
      if (anc) return;
      if (s.getAttribute('aria-hidden') === 'true') return;
      const r = s.getBoundingClientRect(); if (r.width === 0 && r.height === 0 && !s.querySelector('use, path, rect, circle, text')) return;   // a sprite of symbols
      const named = (s.getAttribute('role') === 'img' || s.getAttribute('role') === 'graphics-document') && (norm(s.getAttribute('aria-label')) || s.getAttribute('aria-labelledby') || s.querySelector(':scope > title'));
      if (!named) sp.svgUnnamed.push({ where: where(s), cls: String(s.className && s.className.baseVal || '').slice(0, 30) });
    });
    // AX-S8: a stage holds no landmark or article, so the page's landmark list stays the page's own
    sp.landmarks = [];
    const LANDMARK = 'nav, article, header, footer, main, aside, section[aria-label], section[aria-labelledby], form[aria-label], form[aria-labelledby], '
      + ['banner', 'complementary', 'contentinfo', 'form', 'main', 'navigation', 'region', 'search', 'article', 'feed'].map((r) => `[role~="${r}"]`).join(', ');
    document.querySelectorAll('[data-specimen]').forEach((s) => {
      s.querySelectorAll(LANDMARK).forEach((el) => sp.landmarks.push({ specimen: s.getAttribute('data-specimen'), element: el.tagName.toLowerCase() + (el.getAttribute('role') ? `[role=${el.getAttribute('role')}]` : '') }));
    });
    out.specimens = sp;

    // ---------------- accessible names: no entity text (AX-M2, RP-M4)
    const ENT = /&(?:[a-z][a-z0-9]{1,31}|#\d+|#x[0-9a-f]+);/i;
    const nm = [];
    const NAME_ATTRS = ['aria-label', 'alt', 'title', 'aria-description', 'aria-roledescription', 'placeholder'];
    document.querySelectorAll(NAME_ATTRS.map((a) => `[${a}]`).join(',')).forEach((el) => {
      for (const a of NAME_ATTRS) { const v = el.getAttribute(a); if (v && ENT.test(v)) nm.push({ attribute: a, value: norm(v).slice(0, 60), where: where(el) }); }
    });
    document.querySelectorAll('svg title, svg desc').forEach((t) => { if (ENT.test(t.textContent)) nm.push({ attribute: t.tagName, value: norm(t.textContent).slice(0, 60), where: where(t) }); });
    document.querySelectorAll('[aria-labelledby], [aria-describedby]').forEach((el) => {
      for (const a of ['aria-labelledby', 'aria-describedby']) {
        const v = (el.getAttribute(a) || '').split(/\s+/).map((x) => document.getElementById(x)).filter(Boolean).map((x) => x.textContent).join(' ');
        if (ENT.test(v)) nm.push({ attribute: a, value: norm(v).slice(0, 60), where: where(el) });
      }
    });
    {
      const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n = tw.nextNode(); n; n = tw.nextNode()) {
        const p = n.parentElement; if (!p || p.closest('script,style,code,pre')) continue;
        if (n.textContent.includes('&amp;')) nm.push({ attribute: 'text', value: norm(n.textContent).slice(0, 60), where: where(p) });
      }
    }
    out.names = { entities: nm.slice(0, 30), count: nm.length };

    // ---------------- type scale inside specimens (D2-254)
    const probe = document.createElement('span'); probe.textContent = 'x'; probe.style.position = 'absolute'; probe.style.visibility = 'hidden';
    document.body.append(probe);
    const fluid = TYPE_STYLES.map((st) => { probe.style.font = `var(--oa-type-${st})`; return parseFloat(getComputedStyle(probe).fontSize); }).filter((x) => x > 0);
    const chart = CHART_SIZES.map((v) => { probe.style.font = ''; probe.style.fontSize = `var(${v})`; return parseFloat(getComputedStyle(probe).fontSize); }).filter((x) => x > 0);
    probe.remove();
    const ts = { stages: 0, exempt: 0, off: [], fluid: [...new Set(fluid.map((x) => +x.toFixed(2)))] };
    document.querySelectorAll('[data-specimen]:not([data-pending])').forEach((stage) => {
      const id = stage.getAttribute('data-specimen');
      if (stage.matches('[data-check-exempt~="scale"]')) { ts.exempt++; return; }
      ts.stages++;
      const w = parseFloat(stage.getAttribute('data-width')) || null;
      const sc = parseFloat(stage.getAttribute('data-scale')) || 1;
      let allowed = w === null ? [...SCALE_FLOOR, ...SCALE_CEIL, ...fluid] : w <= 600 ? SCALE_FLOOR : w >= 1200 ? SCALE_CEIL : [...SCALE_FLOOR, ...SCALE_CEIL];
      allowed = allowed.concat(chart);
      const ok = (size) => allowed.some((a) => Math.abs(size - a) <= 0.3 || (sc !== 1 && Math.abs(size / sc - a) <= 0.3 / sc));
      const offHere = new Map();
      stage.querySelectorAll('*').forEach((el) => {
        if (['SCRIPT', 'STYLE', 'TITLE', 'DESC', 'DEFS', 'OPTION'].includes(el.tagName.toUpperCase()) || el.closest('title,desc,defs,.vh')) return;
        const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim()).map((n) => n.textContent.trim()).join(' ');
        if (!own || !visible(el)) return;
        const r = el.getBoundingClientRect(); if (r.width <= 1 && r.height <= 1) return;
        let size = parseFloat(getComputedStyle(el).fontSize);
        if (el instanceof SVGElement) { const s = el.closest('svg'); const vb = s && s.viewBox && s.viewBox.baseVal; if (vb && vb.width) size = +(size * s.getBoundingClientRect().width / vb.width).toFixed(2); }
        if (!ok(size)) { const k = +size.toFixed(2); if (!offHere.has(k)) offHere.set(k, own.slice(0, 40)); }
      });
      if (offHere.size) ts.off.push({ specimen: id, width: w, scale: sc === 1 ? undefined : sc, sizes: [...offHere.keys()], sample: [...offHere.values()][0] });
    });
    out.typeScale = ts;

    // ---------------- D2-253: no codes or studio words in reader text, alt text or accessible names
    const codeRes = CODE_PATTERNS.map(([src, flags, kind]) => [new RegExp(src, flags), kind]);
    const hits = [];
    const scan = (txt, w, how) => {
      for (const [re, kind] of codeRes) { re.lastIndex = 0; let m; while ((m = re.exec(txt))) { hits.push({ found: m[0], kind, how, where: w, text: norm(txt.slice(Math.max(0, m.index - 30), m.index + m[0].length + 30)) }); } }
    };
    {
      const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n = tw.nextNode(); n; n = tw.nextNode()) { const p = n.parentElement; if (!p || p.closest('script,style')) continue; scan(n.textContent, where(p), 'text'); }
    }
    scan(document.title, 'document title', 'title');
    document.querySelectorAll(NAME_ATTRS.map((a) => `[${a}]`).join(',')).forEach((el) => { for (const a of NAME_ATTRS) { const v = el.getAttribute(a); if (v) scan(v, where(el), a); } });
    out.codes = { hits: hits.slice(0, 40), count: hits.length, where: [...new Set(hits.map((h) => h.where))] };

    // ---------------- apply pass: retired words, retired grid classes, parts, cross-references
    {
      const res = RETIRED_WORDS.map(([src, flags, kind]) => [new RegExp(src, flags), kind]);
      const rh = [];
      const rscan = (txt, w, how) => {
        for (const [re, kind] of res) { re.lastIndex = 0; let m; while ((m = re.exec(txt))) rh.push({ found: m[0], kind, how, where: w, text: norm(txt.slice(Math.max(0, m.index - 30), m.index + m[0].length + 30)) }); }
      };
      const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n = tw.nextNode(); n; n = tw.nextNode()) { const p = n.parentElement; if (!p || p.closest('script,style')) continue; rscan(n.textContent, where(p), 'text'); }
      rscan(document.title, 'document title', 'title');
      document.querySelectorAll(NAME_ATTRS.map((a) => `[${a}]`).join(',')).forEach((el) => { for (const a of NAME_ATTRS) { const v = el.getAttribute(a); if (v) rscan(v, where(el), a); } });
      out.retiredWords = { hits: rh.slice(0, 40), count: rh.length, where: [...new Set(rh.map((h) => h.where))] };

      const rc = { hits: [], exempt: [] };
      document.querySelectorAll(RETIRED_CLASSES.map((c) => '.' + c).join(',')).forEach((el) => {
        const cls = RETIRED_CLASSES.filter((c) => el.classList.contains(c));
        const item = { classes: cls, element: el.tagName.toLowerCase(), where: where(el) };
        if (el.closest('.plate--failure')) rc.exempt.push(item); else rc.hits.push(item);
      });
      out.retiredClasses = { hits: rc.hits.slice(0, 30), count: rc.hits.length, where: [...new Set(rc.hits.map((h) => h.where))], exemptInFailurePlates: [...new Set(rc.exempt.map((h) => h.where))] };

      const po = [];
      let opener = null;
      document.querySelectorAll('main > section').forEach((sec) => {
        if (sec.matches('section.part')) { opener = sec; return; }
        if (!sec.matches('section.chapter')) return;
        const part = sec.getAttribute('data-part'), num = sec.getAttribute('data-chapter');
        if (!opener || opener.getAttribute('data-part') !== part) po.push({ chapter: num, part, under: opener ? opener.getAttribute('data-part') : null, problem: 'sits under another part\'s opener' });
        else if (!opener.querySelector(`.part-list a[href="#${sec.id}"]`)) po.push({ chapter: num, part, problem: 'its part opener does not link to it' });
      });
      out.partOrder = po;

      // rules held, by chapter, where a chapter's rules are in the page (a placeholder holds none and is skipped)
      const held = new Map();
      document.querySelectorAll('section.chapter[data-chapter]').forEach((sec) => {
        const ids = [...sec.querySelectorAll('.rule[id^="rule-"]')].map((r) => r.id);
        if (ids.length) held.set(sec.getAttribute('data-chapter'), new Set(ids));
      });
      const XREF = /\bRules?(?:\s|\u00a0)+\d{2}\.\d{1,2}\b(?:\s*(?:,|and|or|to|through)\s*\d{2}\.\d{1,2}\b)*/g;
      const refs = []; const seen = new Set();
      const cite = (txt, w, how) => {
        XREF.lastIndex = 0; let m;
        while ((m = XREF.exec(txt))) {
          const toks = [...m[0].matchAll(/(\d{2})\.(\d{1,2})|\b(to|through)\b/g)];
          let prev = null, rng = false; const got = [];
          for (const t of toks) {
            if (t[3]) { rng = true; continue; }
            const cur = [t[1], parseInt(t[2], 10)];
            if (rng && prev && prev[0] === cur[0] && cur[1] > prev[1]) for (let k = prev[1] + 1; k < cur[1]; k++) got.push([cur[0], k]);
            got.push(cur); prev = cur; rng = false;
          }
          for (const [ch, k] of got) {
            if (!held.has(ch) || held.get(ch).has(`rule-${ch}-${k}`)) continue;
            const key = `${ch}.${k}|${w}`; if (seen.has(key)) continue; seen.add(key);
            refs.push({ rule: `${ch}.${k}`, how, where: w, text: norm(m[0]) });
          }
        }
      };
      document.querySelectorAll('p, li, dd, dt, td, th, figcaption, caption, h2, h3, label, legend, blockquote, span').forEach((el) => {
        if (el.closest('script,style')) return;
        const t = norm(el.textContent); if (t.includes('Rule')) cite(t, where(el), 'text');
      });
      document.querySelectorAll(NAME_ATTRS.map((a) => `[${a}]`).join(',')).forEach((el) => { for (const a of NAME_ATTRS) { const v = el.getAttribute(a); if (v && v.includes('Rule')) cite(norm(v), where(el), a); } });
      out.ruleRefs = refs.slice(0, 30);
      out.ruleRefCount = refs.length;

      // DR-97, CD-N1: one Illustrative label per plate, at the head of the piece or, for a piece that shows none, in
      // the caption; never both
      out.illusTwice = [...document.querySelectorAll('figure.plate')].filter((f) => {
        const st = f.querySelector('.plate-stage'), cap = f.querySelector('.plate-cap');
        return st && cap && st.querySelector('.illus') && cap.querySelector('.illus');
      }).map((f) => (f.querySelector('[data-specimen]') || f).getAttribute('data-specimen') || f.id);
    }

    // ---------------- text size and contrast
    const svgUnder = (el) => {
      if (!(el instanceof SVGElement)) return null;
      const bb = el.getBoundingClientRect(); const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
      for (let node = el; node && !(node instanceof SVGSVGElement); node = node.parentElement) {
        for (let sib = node.previousElementSibling; sib; sib = sib.previousElementSibling) {
          const shapes = [sib, ...sib.querySelectorAll('circle,rect,polygon,path,ellipse')].filter((s) => ['circle', 'rect', 'polygon', 'path', 'ellipse'].includes(s.tagName)).reverse();
          for (const sh of shapes) { const f = parse(getComputedStyle(sh).fill); if (!f || f.a < 0.5 || getComputedStyle(sh).fill === 'none') continue; const b = sh.getBoundingClientRect(); if (b.width < 8 || b.height < 8) continue; if (cx >= b.x && cx <= b.right && cy >= b.y && cy <= b.bottom) return f; }
        }
      }
      return null;
    };
    const bgOf = (el) => { const u = svgUnder(el); if (u) return u; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { if (!(e instanceof SVGElement)) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return c; } } return parse(getComputedStyle(document.body).backgroundColor) || { r: 255, g: 255, b: 255, a: 1 }; };
    const all = [...document.querySelectorAll('body *')].filter((el) => !['SCRIPT', 'STYLE', 'TITLE', 'DESC', 'DEFS', 'NOSCRIPT'].includes(el.tagName.toUpperCase()) && !el.closest('title,desc,defs'));
    const tx = { texts: 0, minSize: 99, under13: [], lowContrast: [], skipped: 0 };
    for (const el of all) {
      const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim()).map((n) => n.textContent.trim()).join(' ');
      if (!own || !visible(el) || (el.closest('[aria-hidden="true"]') && !(el instanceof SVGElement))) continue;
      const cs = getComputedStyle(el); let size = parseFloat(cs.fontSize);
      const isSvg = el instanceof SVGElement;
      if (isSvg) { const s = el.closest('svg'); const vb = s && s.viewBox && s.viewBox.baseVal; if (vb && vb.width) size = +(size * s.getBoundingClientRect().width / vb.width).toFixed(2); }
      const fg = parse(isSvg ? cs.fill : cs.color); if (!fg) continue;
      tx.texts++;
      if (!exempt(el, 'size')) { tx.minSize = Math.min(tx.minSize, size); if (size < 12.95) tx.under13.push({ text: own.slice(0, 40), size, where: where(el) }); } else tx.skipped++;
      if (!exempt(el, 'contrast')) {
        const cr = ratio(fg, bgOf(el)); const large = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight, 10) >= 700);
        if (cr < (large ? 3 : 4.5) - 0.005) tx.lowContrast.push({ text: own.slice(0, 50), size, ratio: +cr.toFixed(2), where: where(el) });
      }
    }
    tx.under13 = tx.under13.slice(0, 20); tx.lowContrast = tx.lowContrast.slice(0, 20);
    out.text = tx;

    // ---------------- overflow
    const vw = document.documentElement.clientWidth;
    const ov = { scrollWidth: document.documentElement.scrollWidth, clientWidth: vw, overflowing: [] };
    for (const el of all) {
      if (!visible(el)) continue;
      const box = el.closest('[data-plate-scroll], [role="region"][tabindex]'); if (box && box !== el) continue;
      if (el.closest('.skip')) continue;
      const r = el.getBoundingClientRect(); if (r.right > vw + 0.5) ov.overflowing.push({ tag: el.tagName, cls: String(el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className).slice(0, 40), right: Math.round(r.right), where: where(el) });
    }
    ov.overflowing = ov.overflowing.slice(0, 15);
    out.overflow = ov;

    // ---------------- Rule 05.3
    const red = { marks: 0, unmarked: [], pageJobs: [], specimenJobs: [], onPrussian: [] };
    const pageJobs = new Set(); const specJobs = new Map();
    for (const el of all) {
      if (!visible(el)) continue;
      const cs = getComputedStyle(el); const isSvg = el instanceof SVGElement;
      const hasOwnText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
      const cands = [];
      if (isSvg) { if (cs.fill !== 'none') cands.push(parse(cs.fill)); if (cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0) cands.push(parse(cs.stroke)); }
      else {
        if (hasOwnText) cands.push(parse(cs.color));
        cands.push(parse(cs.backgroundColor));
        ['Top', 'Right', 'Bottom', 'Left'].forEach((s) => { if (parseFloat(cs['border' + s + 'Width']) > 0) cands.push(parse(cs['border' + s + 'Color'])); });
      }
      if (!cands.some((c) => near(c, RED))) continue;
      if (isSvg && ['svg', 'g'].includes(el.tagName)) continue;
      red.marks++;
      if (exempt(el, 'red')) continue;
      const tag = el.closest('[data-red]');
      if (!tag) { red.unmarked.push({ tag: el.tagName, cls: String(el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className).slice(0, 30), text: (el.textContent || '').trim().slice(0, 30), where: where(el) }); continue; }
      const stage = el.closest('[data-specimen]');
      if (tag.getAttribute('data-red') === 'working') {
        const job = tag.getAttribute('data-red-job') || '(no job named)';
        if (stage) { const k = stage.getAttribute('data-specimen'); if (!specJobs.has(k)) specJobs.set(k, new Set()); specJobs.get(k).add(job); }
        else pageJobs.add(job);
      }
      // the ground behind a red fill or border is the parent's; behind red text it is the element's own
      const behind = (!isSvg && (near(parse(cs.backgroundColor), RED) || !hasOwnText) && el.parentElement) ? bgOf(el.parentElement) : bgOf(el);
      if (near(behind, PRUSSIAN, 4)) red.onPrussian.push({ tag: el.tagName, where: where(el) });
    }
    red.pageJobs = [...pageJobs];
    red.specimenJobs = [...specJobs].filter(([, s]) => s.size > 1).map(([k, s]) => ({ specimen: k, jobs: [...s] }));
    red.unmarked = red.unmarked.slice(0, 20);
    out.red = red;

    // ---------------- writing: locked lines and em dashes
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: (n) => {
      const p = n.parentElement; if (!p || p.closest('script,style,title,desc')) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT; } });
    let text = ''; const dashes = [];
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const p = n.parentElement;
      if (n.textContent.includes('—') && !p.closest('[data-allow-emdash]')) dashes.push({ text: norm(n.textContent).slice(0, 60), where: where(p) });
      if (!p.closest('[data-check-exempt~="locked"]')) text += n.textContent;
    }
    document.querySelectorAll('[aria-label], [alt]').forEach((el) => {
      const v = (el.getAttribute('aria-label') || '') + ' ' + (el.getAttribute('alt') || '');
      if (v.includes('—') && !el.closest('[data-allow-emdash]')) dashes.push({ text: norm(v).slice(0, 60), where: where(el), attribute: true });
    });
    text = norm(text);
    const wr = { emDashes: dashes.slice(0, 20), locked: [], nearMisses: [], pillarOrder: [] };
    for (const L of LOCKED) {
      let found = 0;
      for (const f of L.frags) {
        const off = L.full.indexOf(f);
        for (let i = text.indexOf(f); i !== -1; i = text.indexOf(f, i + 1)) {
          const span = text.slice(Math.max(0, i - off), Math.max(0, i - off) + L.full.length);
          if (span === L.full) found++;
          else wr.nearMisses.push({ line: L.name, found: text.slice(Math.max(0, i - off - 10), i - off + L.full.length + 10) });
        }
      }
      wr.locked.push({ line: L.name, exact: found });
    }
    const seq = /\b(Explain|Track|Connect|Act)\b(?:\s*(?:→|,|, then|then|and|->)\s*\b(Explain|Track|Connect|Act)\b){3}/g;
    for (let m; (m = seq.exec(text));) {
      const words = m[0].match(/Explain|Track|Connect|Act/g);
      if (words.join(' ') !== 'Explain Track Connect Act') wr.pillarOrder.push(m[0]);
    }
    wr.nearMisses = wr.nearMisses.slice(0, 20);
    out.writing = wr;
    out.height = document.documentElement.scrollHeight;
    out.fonts = [...new Set([...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, '')))];
    return out;
  }, { RED, PRUSSIAN, LOCKED, ALIASES, CLOSERS, SCALE_FLOOR, SCALE_CEIL, TYPE_STYLES, CHART_SIZES, CODE_PATTERNS, RETIRED_WORDS, RETIRED_CLASSES });
}

function failuresFrom(a, width) {
  const f = [];
  const add = (key, msg) => f.push({ key, msg: `${width}: ${msg}` });
  const s = a.structure;
  if (s.h1.length !== 1) add('h1', `${s.h1.length} h1 headings (${s.h1.map((t) => JSON.stringify(t.slice(0, 40))).join(', ')}); the page has exactly one`);
  if (s.skips.length) add('headingOrder', `${s.skips.length} skipped heading level(s), first: ${JSON.stringify(s.skips[0])}`);
  if (s.inSpecimen.length) add('specimenHeadings', `${s.inSpecimen.length} heading(s) inside specimens, first: ${JSON.stringify(s.inSpecimen[0])}`);
  if (s.badH3.length) add('chapterH3', `${s.badH3.length} chapter h3(s) that are neither rules nor closers, first: ${JSON.stringify(s.badH3[0])}`);
  if (s.ruleIds.length) add('ruleIds', `${s.ruleIds.length} rule h3(s) with a bad Rule ID, first: ${JSON.stringify(s.ruleIds[0])}`);
  if (s.ruleAnchors.length) add('ruleAnchors', `${s.ruleAnchors.length} rule h3(s) without their #rule-NN-n anchor, first: ${JSON.stringify(s.ruleAnchors[0])}`);
  if (s.rulesWithoutH3.length) add('ruleIds', `${s.rulesWithoutH3.length} rule block(s) without a Rule NN.n h3: ${s.rulesWithoutH3.slice(0, 5).join(', ')}`);
  const an = a.anchors;
  if (an.duplicates.length) add('duplicateIds', `${an.duplicates.length} duplicate id(s), first: ${JSON.stringify(an.duplicates[0])}`);
  if (an.broken.length) add('brokenLinks', `${an.broken.length} same-page link(s) to no id, first: ${JSON.stringify(an.broken[0])}`);
  if (an.relatedBad.length) add('relatedLinks', `${an.relatedBad.length} Related chapters link(s) that do not land on a chapter, first: ${JSON.stringify(an.relatedBad[0])}`);
  if (an.aliases.length) add('aliases', `V5 alias problem(s): ${JSON.stringify(an.aliases)}`);
  const sp = a.specimens;
  if (sp.pending.length) add('pendingSpecimens', `${sp.pending.length} specimen file(s) missing: ${sp.pending.slice(0, 6).join(', ')}`);
  if (sp.noAlt.length) add('specimenAlt', `${sp.noAlt.length} specimen(s) without alt text, first: ${JSON.stringify(sp.noAlt[0])}`);
  if (sp.imgNoAlt.length) add('imgAlt', `${sp.imgNoAlt.length} <img> without alt, first: ${JSON.stringify(sp.imgNoAlt[0])}`);
  if (sp.svgUnnamed.length) add('svgNames', `${sp.svgUnnamed.length} inline SVG(s) neither named nor hidden, first: ${JSON.stringify(sp.svgUnnamed[0])}`);
  if (sp.landmarks.length) add('specimenLandmarks', `${sp.landmarks.length} landmark or article element(s) inside stages, in ${[...new Set(sp.landmarks.map((x) => x.specimen))].join(', ')}; first: ${JSON.stringify(sp.landmarks[0])}`);
  if (a.names.count) add('nameEntities', `${a.names.count} accessible name(s) or text(s) holding an entity, first: ${JSON.stringify(a.names.entities[0])}`);
  if (a.typeScale.off.length) add('typeScale', `${a.typeScale.off.length} specimen(s) with type off the D2-254 sizes: ${a.typeScale.off.map((x) => `${x.specimen} (${x.sizes.join(', ')} px)`).join('; ')}`);
  if (a.retiredWords.count) add('retiredWords', `${a.retiredWords.count} retired word(s) in reader text or names, in ${a.retiredWords.where.slice(0, 25).join(', ')}${a.retiredWords.where.length > 25 ? ' and more' : ''}; first: ${JSON.stringify(a.retiredWords.hits[0])}`);
  if (a.retiredClasses.count) add('retiredClasses', `${a.retiredClasses.count} element(s) with a retired grid class outside a failure plate, in ${a.retiredClasses.where.slice(0, 25).join(', ')}; first: ${JSON.stringify(a.retiredClasses.hits[0])}`);
  if (a.partOrder.length) add('partOrder', `${a.partOrder.length} chapter(s) out of their part, first: ${JSON.stringify(a.partOrder[0])}`);
  if (a.ruleRefCount) add('ruleRefs', `${a.ruleRefCount} citation(s) of a rule the page does not hold, first: ${JSON.stringify(a.ruleRefs[0])}`);
  if (a.frames) {
    const fr = a.frames, ids = (xs) => xs.slice(0, 12).map((x) => x.specimen).join(', ');
    if (fr.hintNoScroll.length) add('scrollHint', `${fr.hintNoScroll.length} frame(s) that hold their stage whole but show a scroll hint, tab stop or "Scroll sideways" name: ${ids(fr.hintNoScroll)}; first: ${JSON.stringify(fr.hintNoScroll[0])}`);
    if (fr.scrollNoHint.length) add('scrollHint', `${fr.scrollNoHint.length} frame(s) that scroll without their hint, tab stop and name: ${ids(fr.scrollNoHint)}; first: ${JSON.stringify(fr.scrollNoHint[0])}`);
    if (fr.couldFit.length) add('frameFit', `${fr.couldFit.length} frame(s) that scroll though ${fr.snugPx} px sides would hold the stage whole: ${ids(fr.couldFit)}; first: ${JSON.stringify(fr.couldFit[0])}`);
    if (fr.offCenter.length) add('frameFit', `${fr.offCenter.length} stage(s) in a frame that does not scroll, off center or not at true size: ${ids(fr.offCenter)}; first: ${JSON.stringify(fr.offCenter[0])}`);
  }
  if (a.illusTwice.length) add('illusOnce', `${a.illusTwice.length} plate(s) with the Illustrative label in both the piece and its caption: ${a.illusTwice.slice(0, 12).join(', ')}`);
  if (a.codes.count) add('codes', `${a.codes.count} decision code(s) or studio word(s) in reader text, in ${a.codes.where.slice(0, 25).join(', ')}${a.codes.where.length > 25 ? ' and more' : ''}; first: ${JSON.stringify(a.codes.hits[0])}`);
  if (a.text.under13.length) add('under13', `${a.text.under13.length} text item(s) under 13 px, first: ${JSON.stringify(a.text.under13[0])}`);
  if (a.text.lowContrast.length) add('contrast', `${a.text.lowContrast.length} text item(s) under contrast, first: ${JSON.stringify(a.text.lowContrast[0])}`);
  if (a.overflow.scrollWidth > a.overflow.clientWidth + 1) add('overflow', `sideways scroll (${a.overflow.scrollWidth} > ${a.overflow.clientWidth}), first: ${JSON.stringify(a.overflow.overflowing[0] || null)}`);
  const r = a.red;
  if (r.unmarked.length) add('redUnmarked', `${r.unmarked.length} Pillar Red mark(s) without data-red, first: ${JSON.stringify(r.unmarked[0])}`);
  if (r.pageJobs.length > 1) add('redJobs', `${r.pageJobs.length} working-red jobs outside specimens (${r.pageJobs.join(', ')})`);
  if (r.specimenJobs.length) add('redJobsSpecimen', `specimen(s) with more than one working-red job: ${JSON.stringify(r.specimenJobs)}`);
  if (r.onPrussian.length) add('redOnPrussian', `${r.onPrussian.length} red mark(s) on Prussian, first: ${JSON.stringify(r.onPrussian[0])}`);
  const w = a.writing;
  if (w.emDashes.length) add('emDash', `${w.emDashes.length} em dash(es) outside data-allow-emdash, first: ${JSON.stringify(w.emDashes[0])}`);
  if (w.nearMisses.length) add('lockedLines', `${w.nearMisses.length} near miss(es) of a locked line, first: ${JSON.stringify(w.nearMisses[0])}`);
  if (w.pillarOrder.length) add('pillarOrder', `pillars out of order: ${JSON.stringify(w.pillarOrder.slice(0, 3))}`);
  return f;
}

// CD-S9 (Q1 to Q4 pass): read every plate frame at true size. A frame scrolls when its content runs more than 1 px past
// it, the shell's own threshold. The narrow side is the --oa-space-400 token (32 px at the default text size). A plate
// set to Fit to window, or a pending one, is skipped; the page opens every plate at true size.
async function frameAudit(page) {
  return page.evaluate(() => {
    const rootCs = getComputedStyle(document.documentElement);
    const tok = rootCs.getPropertyValue('--oa-space-400').trim();
    const snugPx = /rem$/.test(tok) ? parseFloat(tok) * parseFloat(rootCs.fontSize) : (parseFloat(tok) || 32);
    const out = { snugPx, frames: 0, scrolling: 0, snug: [], hintNoScroll: [], scrollNoHint: [], couldFit: [], offCenter: [] };
    for (const fig of document.querySelectorAll('figure.plate')) {
      const box = fig.querySelector(':scope > .plate-scroll'); const st = box && box.querySelector('.plate-stage');
      if (!st || st.hasAttribute('data-pending') || fig.getAttribute('data-fit') === 'fit') continue;
      const r = box.getBoundingClientRect(); if (r.width === 0 && r.height === 0) continue;
      out.frames++;
      const id = st.getAttribute('data-specimen');
      const cs = getComputedStyle(box); const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight);
      const scrolls = box.scrollWidth > box.clientWidth + 1;
      const hint = fig.querySelector('.plate-hint');
      const hintOn = !!hint && !hint.hidden && getComputedStyle(hint).display !== 'none';
      const tabStop = box.getAttribute('tabindex') === '0';
      const named = /scroll sideways/i.test(box.getAttribute('aria-label') || '');
      const need = Math.max(st.offsetWidth, st.scrollWidth);
      if (box.classList.contains('is-snug')) out.snug.push({ specimen: id, sides: pl, hint: hintOn, scrolls });
      if (scrolls) {
        out.scrolling++;
        if (!hintOn || !tabStop || !named) out.scrollNoHint.push({ specimen: id, over: box.scrollWidth - box.clientWidth, hint: hintOn, tabStop, named });
        if (Math.max(pl, pr) > snugPx + 0.5 && need + 2 * snugPx <= box.clientWidth) out.couldFit.push({ specimen: id, need, frame: box.clientWidth, sides: [pl, pr] });
      } else {
        if (hintOn || tabStop || named) out.hintNoScroll.push({ specimen: id, hint: hintOn, tabStop, named });
        const s = st.getBoundingClientRect();
        const gaps = [+(s.left - r.left).toFixed(2), +(r.right - s.right).toFixed(2)];
        const scaled = Math.abs(s.width - st.offsetWidth) > 1;
        if (Math.abs(gaps[0] - gaps[1]) > 1 || scaled) out.offCenter.push({ specimen: id, gaps, drawn: +s.width.toFixed(2), trueWidth: st.offsetWidth });
      }
    }
    return out;
  });
}

// CA-M1 (fix pass): set each plate whose switch shows to Fit to window, measure its smallest rendered text, set it back.
async function fitAudit(page) {
  return page.evaluate(async () => {
    const settle = () => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    const out = { offered: [], under: [] };
    for (const fig of document.querySelectorAll('figure.plate')) {
      const sw = fig.querySelector('.fit-switch');
      if (!sw || sw.hidden || getComputedStyle(sw).display === 'none') continue;
      const stage = fig.querySelector('.plate-stage'); if (!stage) continue;
      const id = stage.getAttribute('data-specimen');
      const fitBtn = sw.querySelector('[data-fit="fit"]'), trueBtn = sw.querySelector('[data-fit="true"]');
      const was = fig.getAttribute('data-fit') === 'fit';
      fitBtn.click(); await settle();
      const scale = stage.getBoundingClientRect().width / (stage.offsetWidth || 1);
      let min = Infinity, sample = '';
      stage.querySelectorAll('*').forEach((el) => {
        if (/^(script|style|title|desc|defs)$/i.test(el.tagName) || el.closest('title, desc, defs, .vh')) return;
        const own = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim()).map((n) => n.textContent.trim()).join(' ');
        if (!own) return;
        const r = el.getBoundingClientRect(); if (r.width === 0 && r.height === 0) return;
        const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') return;
        let size = parseFloat(cs.fontSize);
        if (el instanceof SVGElement) { const svg = el.closest('svg'); const vb = svg && svg.viewBox && svg.viewBox.baseVal; size = vb && vb.width ? size * svg.getBoundingClientRect().width / vb.width : size * scale; }
        else size *= scale;
        if (size < min) { min = size; sample = own.slice(0, 40); }
      });
      out.offered.push({ specimen: id, scale: +scale.toFixed(3), smallest: Number.isFinite(min) ? +min.toFixed(2) : null });
      if (min < 12.95) out.under.push({ specimen: id, scale: +scale.toFixed(3), smallest: +min.toFixed(2), sample });
      (was ? fitBtn : trueBtn).click(); await settle();
    }
    return out;
  });
}

// ------------------------------------------------------------------------------------------------ stage B
// Stage B (November 9, 2026): the accessibility audit's requirements that run on today's page
// (20261109_Stage-B-Accessibility-Audit.md, section 2), found by data-icon and data-icon-family (D2-517), plus the
// mark tokens' parity (D2-402). A stage with role="img" is a picture and is skipped; a live specimen (D2-516) is not.
const GLYPH_ONLY_OK = ['clear the search'];                 // A-4: the one control that may show a glyph and no word
// D2-517: a glyph without data-icon-family fails. true: everywhere; a list of chapter anchors: only there, listed
// elsewhere. Round 2 (November 10, 2026): on everywhere, since every glyph on the page with chapters 01 to 11 carries it.
const REQUIRE_FAMILY = true;
// B-3: the 41 drawings that read at 24 px (DR-136), from 20261110_Stage-B-Ch10-Construction.md, section 10: 37 topic
// and atlas drawings and the four pillar icons.
const READS_AT_24 = ['CL-001', 'CL-004', 'CL-006', 'CL-010', 'CL-013', 'CL-019', 'CL-020', 'CL-021', 'CL-022', 'CL-023', 'CL-024', 'CL-028', 'CL-031', 'CL-032',
  'CL-039', 'CL-040', 'CL-047', 'CL-048', 'CL-050', 'CL-051', 'CL-054', 'CL-057', 'CL-060', 'CL-061', 'CL-067', 'CL-068', 'CL-070', 'CL-071', 'CL-072',
  'R-05', 'R-06', 'R-08', 'R-09', 'R-14', 'R-15', 'R-17', 'R-19', 'R-23', 'R-27', 'R-37', 'R-45'];
const ICON_SIZES = { utility: [16, 24], pillar: [16, 24], status: [24, 26, 28, 30] };   // B-3; topic and atlas: 48 up, or 24 for the 41
// The mark tokens' readers: each mark by its classes and its width attribute, which the plates keep while their own
// CSS sets the width from the token (round 2; the shell's bridge rules went), and each mark kind for the parity
// outside failure plates.
const MARKS = [
  { token: 'ring-now', prop: 'stroke-width', expr: 'var(--oa-component-mark-ring-now)', reader: 'circle:is(.fb.si, .sx-fb.sx-si)[stroke-width="3"]', kind: 'circle:is(.fb.si, .sx-fb.sx-si)' },
  { token: 'ring-ahead', prop: 'stroke-width', expr: 'var(--oa-component-mark-ring-ahead)', reader: 'circle:is(.fb.ss, .sx-fb.sx-ss)[stroke-width="1.5"]', kind: 'circle:is(.fb.ss, .sx-fb.sx-ss)' },
  { token: 'slash', prop: 'stroke-width', expr: 'var(--oa-component-mark-slash)', reader: 'line:is(.si, .sx-si)[stroke-width="2"]', kind: 'line:is(.si, .sx-si)' },
  { token: 'halo', prop: 'stroke-width', expr: 'var(--oa-component-mark-halo)', reader: 'text:is(.halo, .sx-halo)', kind: 'text:is(.halo, .sx-halo)' },
  { token: 'line-reached', prop: 'height', expr: 'var(--oa-component-mark-line-reached)', reader: 'rect:is(.fi, .fr, .sx-fi, .sx-fr)[height="2"]' },
  { token: 'line-ahead', prop: 'height', expr: 'var(--oa-component-mark-line-ahead)', reader: 'rect:is(.fs, .sx-fs)[height="1"]', kind: 'rect:is(.fs, .sx-fs)' },
  { token: 'take-part-disc', prop: 'r', expr: 'calc(var(--oa-component-mark-take-part-disc) / 2)', reader: 'circle:is(.fr, .sx-fr)[r="5.5"]', kind: 'circle:is(.fr, .sx-fr)' },
  { token: 'take-part-keyline', prop: 'stroke-width', expr: 'var(--oa-component-mark-take-part-keyline)', reader: 'circle:is(.sk.nf, .sx-sk.sx-nf)[stroke-width="1"]', kind: 'circle:is(.sk.nf, .sx-sk.sx-nf)' },
  { token: 'take-part-cut', prop: 'r', expr: 'calc(var(--oa-component-mark-take-part-disc) / 2 + var(--oa-component-mark-take-part-cut))', reader: 'circle:is(.fb, .sx-fb):not(.si, .ss, .sx-si, .sx-ss)[r="7"]', kind: 'circle:is(.fb, .sx-fb):not(.si, .ss, .sx-si, .sx-ss)' },
];

// Helpers shared by the stage B page functions, installed once per page.
const SB_HELPERS = `
window.__sb = (() => {
  const parse = (c) => { const m = c && c.match(/rgba?\\(([^)]+)\\)/); if (!m) return null; const p = m[1].split(/[\\s,\\/]+/).filter(Boolean).map(parseFloat); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const bgBehind = (el) => {
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const c = parse(getComputedStyle(e).backgroundColor); if (c && c.a > 0.5) return c; }
    return parse(getComputedStyle(document.documentElement).backgroundColor) || { r: 255, g: 255, b: 255, a: 1 };
  };
  const rendered = (el) => {
    const r = el.getBoundingClientRect(); if (r.width === 0 && r.height === 0) return false;
    if (el.closest('dialog:not([open])')) return false;
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; }
    return true;
  };
  const picture = (el) => !!el.closest('[data-specimen][role="img"]');
  const vhidden = (e) => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return (r.width <= 1 && r.height <= 1) || /inset\\(50%\\)/.test(cs.clipPath) || cs.display === 'none' || cs.visibility === 'hidden'; };
  // The words a sighted reader sees in an element: text not under aria-hidden, a data-icon or a visually hidden box.
  const seen = (root) => {
    let out = ''; const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (let n = w.nextNode(); n; n = w.nextNode()) {
      const p = n.parentElement; if (!p || !n.textContent.trim()) continue;
      let skip = false;
      for (let e = p; e && e !== root.parentElement; e = e.parentElement) { if (e.getAttribute('aria-hidden') === 'true' || e.hasAttribute('data-icon') || vhidden(e)) { skip = true; break; } }
      if (!skip) out += ' ' + n.textContent;
    }
    return out.replace(/\\s+/g, ' ').trim();
  };
  const key = (s) => (s || '').toLowerCase().replace(/[\\u2018\\u2019]/g, "'").replace(/[^a-z0-9' ]+/g, ' ').replace(/\\s+/g, ' ').trim();
  const CONTROLS = 'a[href], button, summary, select, textarea, input:not([type="hidden"]), [role="button"], [role="link"], [role="tab"], [role="switch"], [role="menuitem"], [role="checkbox"], [role="radio"]';
  const where = (el) => { const st = el.closest('[data-specimen]'); const sec = el.closest('section[id]'); return st ? st.getAttribute('data-specimen') : (sec ? '#' + sec.id : el.tagName.toLowerCase()); };
  const desc = (el) => ({ where: where(el), tag: el.tagName.toLowerCase(), text: (el.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 50), label: el.getAttribute('aria-label') || null });
  // The paints a <use> draws (promotion, November 10, 2026). Its symbol's shapes sit in a closed shadow tree, so each
  // shape's fill and stroke is read from the symbol's own markup, nearest declaration first, and resolved as the use
  // would draw it: currentColor and var(--oa-icon-accent, currentColor) against the use's computed style, a literal
  // color through a probe beside the use (Chromium keeps a literal SVG paint in forced colors), and a paint the symbol
  // leaves unset from the use itself.
  const usePaints = (u) => {
    const ref = (u.getAttribute('href') || u.getAttribute('xlink:href') || '').replace(/^#/, '');
    const sym = ref && document.getElementById(ref);
    if (!sym) return [];
    const cs = getComputedStyle(u);
    const own = (el, prop) => {
      for (let e = el; e && e.nodeType === 1; e = e.parentNode) {
        const v = (e.style && e.style.getPropertyValue(prop)) || e.getAttribute(prop);
        if (v) return v.trim();
        if (e === sym) break;
      }
      return null;
    };
    const literal = (v) => {
      const probe = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      probe.setAttribute('fill', v); u.parentNode.appendChild(probe);
      const c = getComputedStyle(probe).fill; probe.remove(); return parse(c);
    };
    const resolve = (v, depth = 0) => {
      if (!v || v === 'none' || depth > 4) return null;
      if (/^currentcolor$/i.test(v)) return parse(cs.color);
      const m = v.match(/^var\\(\\s*(--[\\w-]+)\\s*(?:,\\s*(.+))?\\)$/);
      if (m) { const set = cs.getPropertyValue(m[1]).trim(); return resolve(set || (m[2] || '').trim(), depth + 1); }
      return literal(v);
    };
    const out = [];
    for (const el of sym.querySelectorAll('path, line, circle, rect, polyline, polygon, ellipse, text')) {
      if (el.closest('mask, clipPath, defs, pattern, marker')) continue;
      for (const prop of ['fill', 'stroke']) {
        const v = own(el, prop);
        const c = v === null ? parse(cs.getPropertyValue(prop)) : resolve(v);
        if (c) out.push(c);
      }
    }
    return out;
  };
  // The best contrast a glyph part's paint (its fill, stroke or CSS background) has against the ground behind it.
  window.__sbContrast = (el) => {
    const svgPart = el.namespaceURI === 'http://www.w3.org/2000/svg';
    const behind = bgBehind(svgPart ? el.closest('svg').parentElement : el.parentElement);
    const cs = getComputedStyle(el); const paints = [];
    if (!svgPart) paints.push(parse(cs.backgroundColor));
    else if (el.tagName.toLowerCase() === 'use') paints.push(...usePaints(el));
    else { if (cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0) paints.push(parse(cs.stroke)); if (cs.fill !== 'none') paints.push(parse(cs.fill)); }
    const ok = paints.filter((c) => c && c.a > 0.5);
    return ok.length ? Math.max(...ok.map((c) => ratio(c, behind))) : 1;
  };
  return { parse, ratio, bgBehind, rendered, picture, seen, key, CONTROLS, where, desc, vhidden };
})();`;

async function sbInstall(page) { await page.evaluate((src) => { if (!window.__sb) (0, eval)(src); }, SB_HELPERS); }

// Normal mode: names, targets, sizes, label in name, glyph-only controls, titles, disabled controls, state cues, motion
// with motion allowed, and the mark tokens.
async function sbAudit(page) {
  await sbInstall(page);
  return page.evaluate(({ GLYPH_ONLY_OK, READS_AT_24, ICON_SIZES, MARKS }) => {
    const { parse, ratio, rendered, picture, seen, key, CONTROLS, desc } = window.__sb;
    const out = { icons: 0, missingFamily: [], switchHeights: [], iconNames: [], iconTwice: [], iconTargets: [], iconSizes: [], labelInName: [], controlNames: [], titleOnly: [], disabled: [], stateCues: [], motion: [], stateWords: [], stateStages: 0, marks: { readers: {}, off: [], unread: [], held: false } };
    const icons = [...document.querySelectorAll('[data-icon]')].filter((el) => !picture(el) && !el.parentElement.closest('[data-icon]'));
    out.icons = icons.length;
    const nameOf = (el) => (el.getAttribute('aria-label') || el.getAttribute('alt') || el.getAttribute('title') || (el.querySelector(':scope > title') || {}).textContent || '').trim();
    for (const el of icons) {
      const box = el.closest(CONTROLS + ', li, label, figcaption, dt, dd, td, th, p, h1, h2, h3, h4, h5, h6, legend') || el.parentElement;
      const words = seen(box);
      const hidden = el.closest('[aria-hidden="true"]') && (el.tagName.toLowerCase() !== 'svg' || el.getAttribute('focusable') === 'false')
        || (el.tagName.toLowerCase() === 'img' && el.getAttribute('alt') === '');
      if (words && !hidden) out.iconNames.push({ ...desc(el), icon: el.getAttribute('data-icon'), words: words.slice(0, 40) });   // A-1
      const nm = nameOf(el);
      if (nm && words && key(words).includes(key(nm))) out.iconTwice.push({ ...desc(el), icon: el.getAttribute('data-icon'), name: nm });   // A-2
      const ctl = el.closest(CONTROLS);
      // B-1's inline exception (WCAG 2.5.8, round 2): a link set inline in a paragraph's running text, with words of the
      // paragraph outside it, may stand at the line's height
      const inText = ctl && ctl.matches('a[href]') && getComputedStyle(ctl).display === 'inline' && !!ctl.closest('p')
        && key(seen(ctl.closest('p'))).length > key(seen(ctl)).length + 2;
      if (inText) out.inlineTargets = (out.inlineTargets || 0) + 1;
      if (ctl && rendered(ctl) && !inText) {                                                               // B-1
        const r = ctl.getBoundingClientRect();
        if (r.width < 43.5 || r.height < 43.5) out.iconTargets.push({ ...desc(ctl), icon: el.getAttribute('data-icon'), w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10 });
      }
      if (rendered(el)) {                                                                                  // B-3
        const id = el.getAttribute('data-icon');
        let fam = el.getAttribute('data-icon-family');
        if (!fam) {
          out.missingFamily.push({ ...desc(el), icon: id, chapter: (el.closest('section.chapter[id]') || {}).id || null });
          fam = /^U-/.test(id) ? 'utility' : /^CL-0(19|20|21|22)$/.test(id) ? 'pillar' : /^CL-/.test(id) ? 'topic' : /^R-/.test(id) ? 'atlas' : null;
        }
        const px = Math.round(el.getBoundingClientRect().width);
        let ok;
        if (!fam) ok = false;
        else if (ICON_SIZES[fam]) ok = ICON_SIZES[fam].includes(px) || (fam === 'pillar' && px >= 48);
        else if (fam === 'topic' || fam === 'atlas') ok = px >= 48 || (px === 24 && READS_AT_24.includes(id));
        else ok = true;   // encoding glyphs follow System 1's own constants
        if (!ok) out.iconSizes.push({ ...desc(el), icon: id, family: fam || '(none)', px });
      }
    }
    // DR-153: the Fit to window switch stands 44 px tall, measured where it shows and from its minimum height where hidden.
    out.switchHeights = [];
    for (const el of document.querySelectorAll('.fit-switch button')) {
      const h = rendered(el) ? el.getBoundingClientRect().height : parseFloat(getComputedStyle(el).minHeight) || 0;
      if (h < 43.5) out.switchHeights.push({ ...desc(el), h: Math.round(h * 10) / 10, shown: rendered(el) });
    }
    const controls = [...document.querySelectorAll(CONTROLS)].filter((el) => !picture(el) && rendered(el) && !window.__sb.vhidden(el));
    for (const el of controls) {
      const vis = seen(el);
      const lb = el.getAttribute('aria-labelledby');
      const name = lb ? lb.split(/\s+/).map((id) => (document.getElementById(id) || {}).textContent || '').join(' ') : el.getAttribute('aria-label');
      if (name !== null && vis && !key(name).startsWith(key(vis))) out.labelInName.push({ ...desc(el), visible: vis.slice(0, 50), name: name.slice(0, 80) });   // A-3
      const namedImage = el.querySelector('img:not([alt=""]), svg[aria-label], svg[aria-labelledby], [role="img"][aria-label]');
      if (!vis && !namedImage && !['input', 'select', 'textarea'].includes(el.tagName.toLowerCase())) {          // A-4
        const nm = key(name || el.getAttribute('title') || '');
        if (!GLYPH_ONLY_OK.includes(nm)) out.controlNames.push({ ...desc(el), name: nm || '(none)' });
      }
    }
    for (const el of document.querySelectorAll('[title]')) {                                                  // A-8
      if (picture(el) || el.namespaceURI === 'http://www.w3.org/2000/svg' && el.tagName.toLowerCase() === 'title') continue;
      const t = el.getAttribute('title').trim(); if (!t) continue;
      const other = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || el.getAttribute('alt') || seen(el) || (el.querySelector(':scope > title') || {}).textContent;
      const isNamed = el.matches(CONTROLS + ', img, [role="img"], svg');
      if (isNamed && !other) out.titleOnly.push({ ...desc(el), title: t.slice(0, 60), why: 'its only name is its title' });
      else if (!key(document.body.innerText).includes(key(t)) && !key(other || '').includes(key(t))) out.titleOnly.push({ ...desc(el), title: t.slice(0, 60), why: 'its title holds words found nowhere else' });
    }
    for (const el of document.querySelectorAll('[role="toolbar"] [disabled]')) if (!picture(el)) out.disabled.push({ ...desc(el), why: 'disabled attribute in a toolbar' });   // G-4
    for (const el of document.querySelectorAll('[aria-disabled="true"]')) {
      if (picture(el)) continue;
      const ids = (el.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
      const why = ids.map((id) => document.getElementById(id)).filter((d) => d && seen(d));
      if (!why.length) out.disabled.push({ ...desc(el), why: 'no visible reason through aria-describedby' });
    }
    // C-5: an on item differs from an off peer by more than color, background and shadow.
    const STATE = '[aria-pressed="true"], [aria-selected="true"], [aria-checked="true"], [aria-current]:not([aria-current="false"])';
    const PROPS = ['fontWeight', 'fontStyle', 'textDecorationLine', 'textDecorationStyle', 'textDecorationThickness', 'borderTopStyle', 'borderBottomStyle', 'borderLeftStyle', 'borderRightStyle', 'borderTopWidth', 'borderBottomWidth', 'borderLeftWidth', 'borderRightWidth', 'outlineStyle', 'textTransform', 'fontSize'];
    const offState = (e) => !e.matches(STATE);
    for (const el of document.querySelectorAll(STATE)) {
      if (picture(el) || !el.matches(CONTROLS)) continue;
      const group = el.parentElement && el.parentElement.matches('li') ? el.parentElement.parentElement : el.parentElement;
      if (!group) continue;
      const peer = [...group.querySelectorAll(el.tagName)].find((e) => e !== el && e.className === el.className && offState(e) && e.closest(el.parentElement.matches('li') ? 'li' : '*').parentElement === (el.parentElement.matches('li') ? group : el.parentElement));
      if (!peer) continue;
      const a = getComputedStyle(el), b = getComputedStyle(peer);
      const diff = PROPS.filter((k) => a[k] !== b[k]);
      const glyph = el.querySelector('[data-icon]') && !peer.querySelector('[data-icon]');
      const pa = getComputedStyle(el, '::before').content + getComputedStyle(el, '::after').content, pb = getComputedStyle(peer, '::before').content + getComputedStyle(peer, '::after').content;
      if (!diff.length && !glyph && pa === pb) out.stateCues.push({ ...desc(el), state: ['aria-pressed', 'aria-selected', 'aria-checked', 'aria-current'].find((x) => el.hasAttribute(x) && el.getAttribute(x) !== 'false'), peer: (peer.textContent || '').trim().slice(0, 30) });
    }
    // E-1 and E-3: nothing moves on its own; a glyph's transition lasts 200 ms or less.
    const secs = (v) => Math.max(0, ...v.split(',').map((x) => (x.trim().endsWith('ms') ? parseFloat(x) / 1000 : parseFloat(x)) || 0));
    for (const el of document.querySelectorAll('animate, animateTransform, animateMotion, set')) out.motion.push({ ...desc(el), why: 'SMIL animation' });
    for (const el of document.querySelectorAll('video[autoplay], audio[autoplay]')) out.motion.push({ ...desc(el), why: 'autoplay' });
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      if (cs.animationName !== 'none' && /infinite/.test(cs.animationIterationCount)) out.motion.push({ ...desc(el), why: 'an animation that repeats forever' });
      if ((el.matches('[data-icon], [data-icon] *') || el.querySelector(':scope > [data-icon]')) && secs(cs.transitionDuration) > 0.2) out.motion.push({ ...desc(el), why: `a glyph transition of ${cs.transitionDuration}` });
    }
    // D2-402: every mark drawn from its token; every mark token read where chapter 11 is in the page.
    // A-5 (round 2): every step mark's state in words. Trackers carry no data-step: their words are in the stage's alt
    // text and status lines. In each stage that draws status marks, outside failure plates, each state's word appears
    // at least as often as its marks: done, now, not yet, never happened, stopped, and "you can take part now" beside
    // a take-part mark.
    const WORDS = { 'S-done': /\bdone\b/gi, 'S-now': /(?<!take part )\bnow\b/gi, 'S-take-part': /\byou can take part now\b/gi, 'S-not-yet': /\bnot yet\b/gi, 'S-never-happened': /\bnever happened\b/gi, 'S-stopped': /\bstopped\b/gi };
    for (const st of document.querySelectorAll('[data-specimen]')) {
      if (st.closest('.plate--failure')) continue;
      const marks = [...st.querySelectorAll('[data-icon-family="status"][data-icon]')].filter((m) => WORDS[m.getAttribute('data-icon')]);
      if (!marks.length) continue;
      out.stateStages++;
      const named = [st.getAttribute('aria-label') || '', ...(st.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean).map((id) => (document.getElementById(id) || {}).textContent || '')];
      const text = (named.join(' ') + ' ' + st.innerText + ' ' + [...st.querySelectorAll('[aria-label]')].map((e) => e.getAttribute('aria-label')).join(' ')).replace(/\s+/g, ' ');
      const count = {}; for (const m of marks) { const k = m.getAttribute('data-icon'); count[k] = (count[k] || 0) + 1; }
      const short = Object.entries(count).filter(([k, n]) => (text.match(WORDS[k]) || []).length < n).map(([k, n]) => `${k} ${(text.match(WORDS[k]) || []).length} of ${n}`);
      if (short.length) out.stateWords.push({ where: st.getAttribute('data-specimen'), short: short.join(', ') });
    }
    const probe = document.createElement('div'); probe.style.position = 'absolute'; probe.style.visibility = 'hidden'; document.body.append(probe);
    const val = (expr) => { probe.style.width = expr; return parseFloat(getComputedStyle(probe).width); };
    const got = (el, prop) => parseFloat(getComputedStyle(el).getPropertyValue(prop));
    out.marks.held = !!document.getElementById('icons');
    for (const m of MARKS) {
      const want = val(m.expr);
      const readers = [...document.querySelectorAll(`:is(svg.mk, svg.sx-mk) ${m.reader}`)];
      out.marks.readers[m.token] = readers.length;
      if (out.marks.held && !readers.length) out.marks.unread.push(m.token);
      const kinds = m.kind ? [...document.querySelectorAll(`:is(svg.mk, svg.sx-mk) ${m.kind}`)].filter((el) => !el.closest('.plate--failure')) : [];
      for (const el of new Set([...readers, ...kinds])) {
        if (el.closest('.plate--failure') && !readers.includes(el)) continue;
        const v = got(el, m.prop);
        if (!(Math.abs(v - want) < 0.01)) out.marks.off.push({ token: m.token, where: window.__sb.where(el), prop: m.prop, drawn: v, token_px: want });
      }
    }
    probe.remove();
    return out;
  }, { GLYPH_ONLY_OK, READS_AT_24, ICON_SIZES, MARKS });
}

// D-1 (UX-1): with forced colors on, in dark and light, every glyph part still differs from what lies behind it. A glyph
// part is any [data-icon] or a wordless element inside a control; a <use> counts as one part, with its symbol's paints. One drawn by a CSS background, shadow or image that
// forced colors erases fails, and so does an SVG part whose fill and stroke both match the ground.
async function sbForced(page) {
  await sbInstall(page);
  const mark = await page.evaluate(() => {
    const { rendered, picture, CONTROLS } = window.__sb;
    let n = 0;
    const tag = (el, kind) => { el.setAttribute('data-sb-glyph', kind + ':' + (n++)); };
    for (const el of document.querySelectorAll(`[data-icon], [data-icon] *, :is(${CONTROLS}) *`)) {
      if (picture(el) || !rendered(el)) continue;
      const t = el.tagName.toLowerCase();
      if (el.namespaceURI === 'http://www.w3.org/2000/svg') { if (['path', 'line', 'circle', 'rect', 'polyline', 'polygon', 'ellipse', 'use'].includes(t)) tag(el, 'svg'); continue; }
      if ((el.textContent || '').trim() || el.querySelector('svg, img')) continue;
      const cs = getComputedStyle(el); const c = window.__sb.parse(cs.backgroundColor);
      if ((c && c.a > 0) || cs.backgroundImage !== 'none' || cs.boxShadow !== 'none') tag(el, 'css');
    }
    // how far each part stands out from its ground with the page's own colors
    for (const el of document.querySelectorAll('[data-sb-glyph]')) el.setAttribute('data-sb-normal', String(window.__sbContrast(el)));
    return { n, uses: document.querySelectorAll('use[data-sb-glyph]').length };
  });
  const out = { glyphParts: mark.n, useParts: mark.uses, erased: [] };
  for (const scheme of ['dark', 'light']) {
    await page.emulateMedia({ forcedColors: 'active', colorScheme: scheme });
    await page.waitForTimeout(50);
    const r = await page.evaluate((scheme) => {
      const { desc } = window.__sb;
      const bad = [];
      for (const el of document.querySelectorAll('[data-sb-glyph]')) {
        const before = parseFloat(el.getAttribute('data-sb-normal')), now = window.__sbContrast(el);
        if (before >= 1.5 && now < 1.5) bad.push({ ...desc(el.closest('[data-icon]') || el), scheme, drawnBy: el.getAttribute('data-sb-glyph').startsWith('css') ? 'CSS background' : 'SVG fill or stroke', contrast: Math.round(before * 100) / 100 + ' to ' + Math.round(now * 100) / 100 });
      }
      return bad;
    }, scheme);
    out.erased.push(...r);
  }
  await page.emulateMedia({ forcedColors: 'none', colorScheme: 'light' });
  await page.evaluate(() => document.querySelectorAll('[data-sb-glyph]').forEach((el) => { el.removeAttribute('data-sb-glyph'); el.removeAttribute('data-sb-normal'); }));
  return out;
}

// E-2: under prefers-reduced-motion every animation and transition resolves to none or 0 s.
async function sbReduced(page) {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.waitForTimeout(50);
  await sbInstall(page);
  const r = await page.evaluate(() => {
    const secs = (v) => Math.max(0, ...v.split(',').map((x) => (x.trim().endsWith('ms') ? parseFloat(x) / 1000 : parseFloat(x)) || 0));
    const bad = [];
    for (const el of document.querySelectorAll('body *')) {
      const cs = getComputedStyle(el);
      if (cs.animationName !== 'none' && secs(cs.animationDuration) > 0) bad.push({ ...window.__sb.desc(el), why: `animation ${cs.animationName} ${cs.animationDuration}` });
      else if (secs(cs.transitionDuration) > 0 && cs.transitionProperty !== 'none') bad.push({ ...window.__sb.desc(el), why: `transition ${cs.transitionProperty} ${cs.transitionDuration}` });
    }
    return bad;
  });
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  return r;
}

// F-1 and F-3: with SC 1.4.12's text spacing, and then with text at 200 percent, no control clips its words, no glyph
// overlaps its word, and (with the spacing) the page does not scroll sideways.
async function sbSpacing(page) {
  await sbInstall(page);
  const pass = async (mode) => {
    await page.evaluate((mode) => {
      const st = document.createElement('style'); st.id = 'sb-spacing';
      st.textContent = mode === 'spacing'
        ? '* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important } p { margin-bottom: 2em !important }'
        : 'html { font-size: 200% !important }';
      document.head.append(st);
    }, mode);
    await page.waitForTimeout(150);
    const r = await page.evaluate((mode) => {
      const { rendered, picture, CONTROLS, desc } = window.__sb;
      const bad = [];
      for (const el of document.querySelectorAll(CONTROLS)) {
        if (picture(el) || !rendered(el) || el.matches('.skip') || el.closest('[aria-hidden="true"]')) continue;
        const cs = getComputedStyle(el);
        const clipsX = /hidden|clip/.test(cs.overflowX) && el.scrollWidth > el.clientWidth + 1;
        const clipsY = /hidden|clip/.test(cs.overflowY) && el.scrollHeight > el.clientHeight + 1;
        if (clipsX || clipsY) bad.push({ ...desc(el), mode, why: 'clips its words' });
        const g = el.querySelector('[data-icon]');
        if (g && rendered(g)) {
          const gb = g.getBoundingClientRect(); const range = document.createRange();
          for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) {
            range.selectNodeContents(n);
            for (const t of range.getClientRects()) if (t.left < gb.right - 0.5 && t.right > gb.left + 0.5 && t.top < gb.bottom - 0.5 && t.bottom > gb.top + 0.5) { bad.push({ ...desc(el), mode, why: 'its glyph overlaps its word' }); break; }
          }
        }
      }
      if (mode === 'spacing' && document.documentElement.scrollWidth > window.innerWidth + 1) bad.push({ where: 'page', mode, why: `scrolls sideways (${document.documentElement.scrollWidth} px)` });
      document.getElementById('sb-spacing').remove();
      return bad;
    }, mode);
    await page.waitForTimeout(150);
    return r;
  };
  return [...(await pass('spacing')), ...(await pass('zoom'))];
}

// G-3 and G-2 for the phone menu: Menu opens the dialog with focus inside it; Tab stays inside and in view; Escape and
// Close each shut it and return focus to Menu.
async function sbMenu(page) {
  const has = await page.evaluate(() => { const b = document.getElementById('menubtn'); return !!(b && b.getBoundingClientRect().width && getComputedStyle(b).display !== 'none'); });
  if (!has) return null;
  const out = { problems: [] };
  const state = () => page.evaluate(() => {
    const m = document.getElementById('menu'), b = document.getElementById('menubtn'), a = document.activeElement;
    const inside = !!(a && a.closest && a.closest('#menu'));
    let inView = true;
    if (inside && a !== m) { const r = a.getBoundingClientRect(), d = m.getBoundingClientRect(); inView = r.top >= d.top - 1 && r.bottom <= d.bottom + 1 && r.height > 0; }
    return { open: !!m.open, expanded: b.getAttribute('aria-expanded'), inside, onMenu: a === b, outside: a && a !== document.body && !inside ? (a.textContent || a.tagName).trim().slice(0, 30) : null, inView, at: a ? (a.textContent || a.tagName).trim().slice(0, 30) : null };
  });
  for (const via of ['Escape', 'Close']) {
    await page.evaluate(() => { window.scrollTo(0, 0); document.getElementById('menubtn').focus(); });
    await page.keyboard.press('Enter'); await page.waitForTimeout(150);
    let s = await state();
    if (!s.open || s.expanded !== 'true' || !s.inside) out.problems.push(`Menu did not open with focus inside (${JSON.stringify(s)})`);
    for (let i = 0; i < 40 && s.open; i++) {
      await page.keyboard.press('Tab'); s = await state();
      if (s.outside) { out.problems.push(`Tab left the open menu for "${s.outside}"`); break; }
      if (!s.inView) { out.problems.push(`focus sat out of view in the menu on "${s.at}"`); break; }
    }
    if (via === 'Escape') await page.keyboard.press('Escape');
    else { await page.evaluate(() => document.querySelector('#menu .menu-close').focus()); await page.keyboard.press('Enter'); }
    await page.waitForTimeout(150);
    s = await state();
    if (s.open || s.expanded !== 'false') out.problems.push(`${via} did not close the menu (${JSON.stringify(s)})`);
    else if (!s.onMenu) out.problems.push(`${via} closed the menu but focus went to "${s.at}", not Menu`);
  }
  await page.evaluate(() => { const m = document.getElementById('menu'); if (m.open) m.close(); document.activeElement && document.activeElement.blur && document.activeElement.blur(); window.scrollTo(0, 0); });
  return out;
}

function sbFailures(b, width) {
  const f = []; const add = (key, msg) => f.push({ key, msg: `${width}: ${msg}` });
  const first = (xs) => JSON.stringify(xs[0]);
  const a = b.audit;
  if (a.iconNames.length) add('iconNames', `${a.iconNames.length} glyph(s) beside their word but not hidden (A-1), first: ${first(a.iconNames)}`);
  if (a.iconTwice.length) add('iconNames', `${a.iconTwice.length} glyph(s) whose name repeats the words beside them (A-2), first: ${first(a.iconTwice)}`);
  if (a.switchHeights.length) add('iconTargets', `${a.switchHeights.length} Fit to window button(s) under 44 px tall (DR-153), first: ${first(a.switchHeights)}`);
  if (a.iconTargets.length) add('iconTargets', `${a.iconTargets.length} control(s) holding a glyph under 44 by 44 px (B-1), first: ${first(a.iconTargets)}`);
  const noFamily = a.missingFamily.filter((m) => REQUIRE_FAMILY === true || (Array.isArray(REQUIRE_FAMILY) && REQUIRE_FAMILY.includes(m.chapter)));
  if (noFamily.length) add('iconSizes', `${noFamily.length} glyph(s) without data-icon-family (D2-517) in ${[...new Set(noFamily.map((m) => '#' + m.chapter))].join(', ')}, first: ${first(noFamily)}`);
  if (a.iconSizes.length) add('iconSizes', `${a.iconSizes.length} glyph(s) at a size their family does not use (B-3), first: ${first(a.iconSizes)}`);
  if (a.labelInName.length) add('labelInName', `${a.labelInName.length} control(s) whose name does not start with their visible words (A-3), first: ${first(a.labelInName)}`);
  if (a.controlNames.length) add('controlNames', `${a.controlNames.length} control(s) with a glyph and no visible word, off the allowed list (A-4), first: ${first(a.controlNames)}`);
  if (a.titleOnly.length) add('titleOnly', `${a.titleOnly.length} title attribute(s) carrying a meaning nothing else carries (A-8), first: ${first(a.titleOnly)}`);
  if (a.disabled.length) add('disabledControls', `${a.disabled.length} unavailable control(s) without a focusable state and a visible reason (G-4), first: ${first(a.disabled)}`);
  if (a.stateCues.length) add('stateCues', `${a.stateCues.length} on state(s) told from off by color alone (C-5), first: ${first(a.stateCues)}`);
  if (a.stateWords.length) add('stateWords', `${a.stateWords.length} stage(s) whose step marks lack their state in words (A-5), first: ${first(a.stateWords)}`);
  if (a.motion.length) add('motion', `${a.motion.length} moving or slow glyph element(s) (E-1, E-3), first: ${first(a.motion)}`);
  if (a.marks.off.length) add('markTokens', `${a.marks.off.length} mark(s) drawn off their token (D2-402), first: ${first(a.marks.off)}`);
  if (a.marks.unread.length) add('markTokens', `mark token(s) with no reader on the page: ${a.marks.unread.join(', ')}`);
  if (b.forced && b.forced.erased.length) add('forcedGlyphs', `${b.forced.erased.length} glyph part(s) that forced colors erases (D-1, UX-1), first: ${first(b.forced.erased)}`);
  if (b.reduced && b.reduced.length) add('reducedMotion', `${b.reduced.length} element(s) still moving under reduced motion (E-2), first: ${first(b.reduced)}`);
  if (b.spacing && b.spacing.length) add('textSpacing', `${b.spacing.length} clip, overlap or sideways scroll with text spacing or 200 percent text (F-1, F-3), first: ${first(b.spacing)}`);
  if (b.menu && b.menu.problems.length) add('menuDialog', `the phone menu (G-2, G-3): ${b.menu.problems.join('; ')}`);
  return f;
}

async function runAxe(page) {
  if (!AXE) return null;
  await page.addScriptTag({ path: AXE });
  return page.evaluate(async () => {
    const tags = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
    const fmt = (r) => r.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes[0] && v.nodes[0].target.join(' ') }));
    const a = await window.axe.run(document, { runOnly: { type: 'tag', values: tags }, rules: { 'color-contrast': { enabled: false } } });
    const b = await window.axe.run({ include: [['body']], exclude: [['[data-check-exempt~="contrast"]']] }, { runOnly: { type: 'rule', values: ['color-contrast'] } });
    return fmt(a).concat(fmt(b));
  });
}

// G-1 (stage B, UX-5): a ring is an outline of 2 px or more at 3 to 1 against what lies behind it. A box-shadow does not
// count, since forced colors removes it.
async function focusAudit(page, stops) {
  const results = [];
  await sbInstall(page);
  await page.evaluate(() => { document.activeElement && document.activeElement.blur && document.activeElement.blur(); window.scrollTo(0, 0); });
  for (let i = 0; i < stops; i++) {
    await page.keyboard.press('Tab');
    const r = await page.evaluate(() => {
      const el = document.activeElement; if (!el || el === document.body) return null;
      const cs = getComputedStyle(el);
      const { parse, ratio, bgBehind } = window.__sb;
      const oc = parse(cs.outlineColor);
      // the ring reads against the ground beside it: outside the box, or the box's own fill where the box is opaque
      const own = parse(cs.backgroundColor);
      const grounds = [parseFloat(cs.outlineOffset) < 0 ? bgBehind(el) : bgBehind(el.parentElement || el)].concat(own && own.a > 0.5 ? [own] : []);
      const contrast = oc ? Math.round(Math.max(...grounds.map((g) => ratio(oc, g))) * 100) / 100 : 0;
      const ring = cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) >= 2 && contrast >= 3;
      const r = el.getBoundingClientRect(); const head = document.querySelector('.masthead');
      const hb = head ? head.getBoundingClientRect().bottom : 0;
      const obscured = !el.closest('.masthead') && !el.closest('dialog') && getComputedStyle(el).position !== 'fixed' && r.bottom <= hb + 1;
      return { tag: el.tagName, label: (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40), ring, outline: `${cs.outlineStyle} ${cs.outlineWidth}`, contrast, shadowOnly: cs.outlineStyle === 'none' && cs.boxShadow !== 'none', obscured };
    });
    if (!r) break;
    results.push(r);
  }
  return results;
}

async function checkPage(browser, file, widths, opts = {}) {
  const report = { file: path.relative(ROOT, file), checked: new Date().toISOString(), axe: AXE ? path.relative(ROOT, AXE) : null, runs: [], failures: [] };
  const dir = path.dirname(file); const stem = path.basename(file, '.html');
  const capDir = path.join(dir, 'captures');
  if (opts.captures) fs.mkdirSync(capDir, { recursive: true });
  for (const width of widths) {
    const height = { 1440: 900, 1024: 768, 390: 844, 360: 780 }[width] || 900;
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const outside = new Set(); const errors = [];
    page.on('request', (req) => { const u = req.url(); if (/^(file|data|blob|about):/.test(u)) return; const h = new URL(u).hostname; if (!ALLOWED_HOSTS.includes(h)) outside.add(h); });
    page.on('pageerror', (e) => errors.push(String(e.message || e).slice(0, 200)));
    await page.goto('file://' + file, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    if (opts.mutate) await page.evaluate(opts.mutate);
    const a = await audit(page);
    a.frames = await frameAudit(page);
    a.fit = await fitAudit(page);
    const fails = failuresFrom(a, width);
    const sb = { audit: await sbAudit(page) };
    if (!opts.skipStageB) {
      sb.forced = await sbForced(page);
      if (width === 1440 || opts.plant) sb.reduced = await sbReduced(page);
      if (width <= 390) sb.spacing = await sbSpacing(page);
      sb.menu = await sbMenu(page);
    }
    fails.push(...sbFailures(sb, width));
    a.stageB = { icons: sb.audit.icons, stateStages: sb.audit.stateStages, inlineTargets: sb.audit.inlineTargets || 0, missingFamily: sb.audit.missingFamily, markReaders: sb.audit.marks.readers, glyphParts: sb.forced ? sb.forced.glyphParts : null, useParts: sb.forced ? sb.forced.useParts : null,
      menu: sb.menu ? (sb.menu.problems.length ? sb.menu.problems : 'opens, holds focus, closes by Escape and Close, returns focus') : 'not shown at this width' };
    if (a.fit.under.length) fails.push({ key: 'fitFloor', msg: `${width}: ${a.fit.under.length} plate(s) whose Fit to window sets text under 13 px: ${a.fit.under.slice(0, 8).map((x) => `${x.specimen} (${x.smallest} px at ${Math.round(x.scale * 100)}%, "${x.sample}")`).join('; ')}` });
    let axe = null;
    if (!opts.skipAxe) {
      axe = await runAxe(page);
      if (axe && axe.length) fails.push({ key: 'axe', msg: `${width}: axe ${axe.map((v) => v.id + ' x' + v.nodes).join(', ')}` });
      if (!axe) fails.push({ key: 'axe', msg: `${width}: axe-core not found (set AXE_PATH; see the shell notes, section 6)` });
    }
    let focus = null;
    if ((width === 1440 || width === 390) && !opts.skipFocus) {
      focus = await focusAudit(page, 60);
      const noRing = focus.filter((x) => !x.ring); const hidden = focus.filter((x) => x.obscured);
      if (noRing.length) fails.push({ key: 'focus', msg: `${width}: ${noRing.length} focus stop(s) without a 2 px outline at 3 to 1 (G-1), first: ${JSON.stringify(noRing[0])}` });
      if (hidden.length) fails.push({ key: 'focus', msg: `${width}: ${hidden.length} focus stop(s) hidden under the masthead, first: ${JSON.stringify(hidden[0])}` });
    }
    if (outside.size) fails.push({ key: 'requests', msg: `${width}: outside requests to ${[...outside].join(', ')}` });
    if (errors.length) fails.push({ key: 'errors', msg: `${width}: script errors: ${errors.slice(0, 3).join(' | ')}` });
    report.runs.push({ width, ...a, axe, focusStops: focus ? focus.length : null, focusProblems: focus ? focus.filter((x) => !x.ring || x.obscured).slice(0, 10) : null });
    report.failures.push(...fails);
    if (opts.captures && (width === 1440 || width === 390)) {
      const secs = await page.evaluate(() => [...document.querySelectorAll('main > section[id]')].map((s) => s.id));
      // a capture of a section the page no longer holds (such as signal-grid after the lockmark rename) is removed, so
      // the folder shows this page and nothing older
      const mine = new RegExp(`^${stem.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}-${width}-(.+)\\.jpg$`);
      for (const f of fs.readdirSync(capDir)) { const m = f.match(mine); if (m && !secs.includes(m[1])) fs.rmSync(path.join(capDir, f)); }
      await page.evaluate(() => window.scrollTo(0, 0));
      for (const id of secs) {
        const loc = page.locator(`main > section[id="${id}"]`);
        const box = await loc.boundingBox();
        if (!box || box.height > 30000) continue;
        await loc.screenshot({ path: path.join(capDir, `${stem}-${width}-${id}.jpg`), type: 'jpeg', quality: width === 1440 ? 82 : 78 });
      }
    }
    await ctx.close();
  }
  report.pass = report.failures.length === 0;
  return report;
}

// ------------------------------------------------------------------------------------------------ self-test
// Each plant puts one fault into a fresh copy of the demo build and names the test that must catch it.
const PLANTS = [
  { key: 'h1', fault: 'a second h1', js: () => { const h = document.createElement('h1'); h.textContent = 'A second title'; document.querySelector('.chapter .ch-head').append(h); } },
  { key: 'headingOrder', fault: 'an h4 straight after a chapter h2', js: () => { const h = document.createElement('h4'); h.textContent = 'Skipped level'; document.querySelector('.chapter .ch-title').after(h); } },
  { key: 'specimenHeadings', fault: 'an h3 inside a specimen', js: () => { const h = document.createElement('h3'); h.textContent = 'Mockup headline'; document.querySelector('[data-specimen]:not([data-pending])').prepend(h); } },
  { key: 'ruleIds', fault: 'a rule h3 without its Rule ID', js: () => { document.querySelector('.rule .rid').remove(); } },
  { key: 'ruleIds', fault: "a rule h3 whose ID names another chapter", js: () => { document.querySelector('.rule .rid-n').textContent = '09.1'; } },
  { key: 'ruleAnchors', fault: 'a rule block whose id does not match its Rule ID', js: () => { document.querySelector('.rule').id = 'rule-xx'; } },
  { key: 'chapterH3', fault: 'a stray h3 in a chapter', js: () => { const h = document.createElement('h3'); h.textContent = 'Why it works'; document.querySelector('.rule .why').prepend(h); } },
  { key: 'duplicateIds', fault: 'two elements with one id', js: () => { const p = document.createElement('p'); p.id = 'contents'; p.textContent = 'Duplicate'; document.querySelector('.chapter .ch-head').append(p); } },
  { key: 'brokenLinks', fault: 'a same-page link to no id', js: () => { const a = document.createElement('a'); a.href = '#nowhere'; a.textContent = 'Nowhere'; document.querySelector('.rule .why').append(a); } },
  { key: 'relatedLinks', fault: 'a Related chapters link that lands on the contents', js: () => { document.querySelector('.rel-inline a').setAttribute('href', '#contents'); } },
  { key: 'aliases', fault: 'the #grid alias removed from 08 The lockmark', js: () => { document.getElementById('grid').remove(); } },
  { key: 'specimenAlt', fault: 'a specimen stage with no alt', js: () => { document.querySelector('[data-specimen][role="img"]').removeAttribute('aria-label'); } },
  { key: 'imgAlt', fault: 'an <img> with no alt', js: () => { const i = document.createElement('img'); i.src = 'data:image/gif;base64,R0lGODlhAQABAAAAACw='; i.width = 20; i.height = 20; document.querySelector('.rule .why').append(i); } },
  { key: 'svgNames', fault: 'an inline SVG neither named nor hidden', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<svg width="24" height="24" viewBox="0 0 24 24"><rect width="24" height="24" fill="currentColor"/></svg>'); } },
  { key: 'pendingSpecimens', fault: 'a specimen file missing', js: () => { document.querySelector('[data-specimen]').setAttribute('data-pending', 'true'); } },
  { key: 'under13', fault: '12 px text outside an exempt plate', js: () => { document.querySelector('.rule-text').style.fontSize = '12px'; } },
  { key: 'contrast', fault: 'Stone text tint on Newsprint', js: () => { document.querySelector('.rule-text').style.color = 'var(--oa-color-tint-stone-n55)'; } },
  { key: 'redUnmarked', fault: 'a Pillar Red rule with no data-red', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p style="border-top:4px solid var(--oa-color-palette-pillar-red)">Red bar</p>'); } },
  { key: 'redJobs', fault: 'two working-red jobs in the page', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p data-red="working" data-red-job="ask" style="color:var(--oa-color-palette-charcoal);border-left:4px solid var(--oa-color-palette-pillar-red)">A</p><p data-red="working" data-red-job="error" style="border-left:4px solid var(--oa-color-palette-pillar-red)">B</p>'); } },
  { key: 'redJobsSpecimen', fault: 'two working-red jobs inside one specimen', js: () => { document.querySelector('[data-specimen]:not([data-pending])').insertAdjacentHTML('beforeend', '<p data-red="working" data-red-job="ask" style="border-left:4px solid var(--oa-color-palette-pillar-red)">A</p><p data-red="working" data-red-job="point" style="border-left:4px solid var(--oa-color-palette-pillar-red)">B</p>'); } },
  { key: 'redOnPrussian', fault: 'red on a Prussian ground', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div style="background:var(--oa-color-palette-prussian);padding:16px"><span data-red="signature" style="display:inline-block;width:20px;height:20px;background:var(--oa-color-palette-pillar-red)"></span></div>'); } },
  { key: 'emDash', fault: 'an em dash in prose', js: () => { document.querySelector('.rule-text').append(' One clause — then another.'); } },
  { key: 'lockedLines', fault: 'a near miss of the tagline', js: () => { document.querySelector('.rule-text').append(' A nation that answers to its people.'); } },
  { key: 'pillarOrder', fault: 'the pillars out of order', js: () => { document.querySelector('.rule-text').append(' Explain → Connect → Track → Act.'); } },
  { key: 'overflow', fault: 'a wide element outside a scrolling frame', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div style="width:3000px;height:4px;background:var(--oa-color-palette-charcoal)"></div>'); } },
  { key: 'specimenLandmarks', fault: 'a <nav> inside a specimen', js: () => { document.querySelector('[data-specimen]:not([data-pending])').insertAdjacentHTML('beforeend', '<nav aria-label="Site"><span>Home</span></nav>'); } },
  { key: 'specimenLandmarks', fault: 'an <article> inside a specimen', js: () => { document.querySelector('[data-specimen]:not([data-pending])').insertAdjacentHTML('beforeend', '<article><span>A story</span></article>'); } },
  { key: 'nameEntities', fault: 'an alt that reads "Oath &amp; Action" (escaped twice)', js: () => { document.querySelector('[data-specimen][role="img"]').setAttribute('aria-label', 'Oath &amp; Action, the wordmark at 24 px on Newsprint'); } },
  { key: 'nameEntities', fault: 'visible text that shows "&amp;"', js: () => { document.querySelector('.rule-text').append(' Load Inter &amp;family=Lora.'); } },
  { key: 'typeScale', fault: '21 px text in a specimen, off the scale', js: () => { document.querySelector('[data-specimen]:not([data-pending]):not([data-check-exempt~="scale"])').insertAdjacentHTML('beforeend', '<p style="font:700 21px/1.2 Inter;margin:0">Off-scale deck</p>'); } },
  { key: 'codes', fault: 'a decision code and "Gate" in rule text', js: () => { document.querySelector('.rule-text').append(' Approved at Gate 1 (DR-55).'); } },
  { key: 'codes', fault: 'a decision code in an alt text', js: () => { document.querySelector('[data-specimen][role="img"]').setAttribute('aria-label', 'A notice card at true size, as decided in D2-30.'); } },
  { key: 'codes', fault: '"the studio" in a caption', js: () => { document.querySelector('.plate-cap').append(' The studio drew it.'); } },
  // apply pass, November 7, 2026
  { key: 'codes', fault: 'a lowercase "gate" in rule text', js: () => { document.querySelector('.rule-text').append(' Shown to the editor at the next gate.'); } },
  { key: 'codes', fault: 'a gate drawn in a symbol, in its meaning sentence (allowed: must not be flagged)', expect: false, js: () => { document.querySelector('.rule-text').append(' A parcel meets a gate with two bars across it.'); } },
  { key: 'codes', fault: '"Board 6" in a caption', js: () => { document.querySelector('.plate-cap').append(' As drawn on Board 6.'); } },
  { key: 'codes', fault: '"stage B" in a chapter intro', js: () => { document.querySelector('.chapter .ch-head .instr').append(' Status marks arrive in stage B.'); } },
  { key: 'retiredWords', fault: '"Signal Grid" in rule text', js: () => { document.querySelector('.rule-text').append(' The Signal Grid codes the tracker.'); } },
  { key: 'retiredWords', fault: '"Signal Grid" in a specimen alt', js: () => { document.querySelector('[data-specimen][role="img"]').setAttribute('aria-label', 'A notice card with a 24 px Signal Grid in its kicker, at true size.'); } },
  { key: 'retiredWords', fault: '"Stage 4 of 9" in a caption', js: () => { document.querySelector('.plate-cap').append(' Stage 4 of 9: Out of committee.'); } },
  { key: 'retiredWords', fault: '"nine stages" in a failure plate', js: () => { document.querySelector('.plate--failure .plate-cap').append(' A tracker reads its nine stages left to right.'); } },
  { key: 'retiredWords', fault: '"Condensed width, proposed" as a proof label', js: () => { document.querySelector('.plate-label').append(' Condensed width, proposed'); } },
  { key: 'retiredClasses', fault: 'a coded grid (class oai-grid) in a correct plate', js: () => { document.querySelector('.plate--correct [data-specimen]').insertAdjacentHTML('beforeend', '<svg class="oai-svg oai-grid" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>'); } },
  { key: 'retiredClasses', fault: 'the composer (class oai-comp) after a rule', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div class="oai-comp"><span>Composer</span></div>'); } },
  { key: 'retiredClasses', fault: 'a coded grid inside a labeled failure plate (allowed: must not be flagged)', expect: false, js: () => { document.querySelector('.plate--failure [data-specimen]').insertAdjacentHTML('beforeend', '<svg class="oai-svg oai-grid" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>'); } },
  { key: 'partOrder', fault: 'a chapter that names another part than its opener', js: () => { document.querySelector('section.chapter').setAttribute('data-part', 'symbols'); } },
  { key: 'partOrder', fault: 'a part opener that does not link to its chapter', js: () => { document.querySelector('section.part .part-list a').remove(); } },
  { key: 'ruleRefs', fault: 'a citation of Rule 01.9, which chapter 01 does not hold', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p>See Rule 01.9 for the sizes.</p>'); } },
  { key: 'ruleRefs', fault: 'a range, "Rules 01.1 to 01.4", past chapter 01\'s last rule', js: () => { document.querySelector('.plate-cap').append(' Rules 01.1 to 01.4 set the frame.'); } },
  { key: 'ruleRefs', fault: 'a citation in an alt text', js: () => { document.querySelector('[data-specimen][role="img"]').setAttribute('aria-label', 'A notice card drawn as Rule 01.7 sets it, at true size.'); } },
  // apply fix pass, November 7, 2026. The demo's 640 px sheet holds 13 to 17 px text.
  { key: 'fitFloor', fault: 'a 2,000 px plate whose switch is forced to show, so Fit to window sets its text near 6 px', js: () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const fig = st.closest('figure');
    st.style.setProperty('--w', '2000px'); fig.querySelector('.plate-scroll').style.setProperty('--w', '2000px');
    fig.querySelector('.fit-switch').hidden = false; } },
  { key: 'fitFloor', fault: 'the same 2,000 px plate after a resize: the shell hides the switch, since fitting would break the floor (allowed: must not be flagged)', expect: false, js: async () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const fig = st.closest('figure');
    st.style.setProperty('--w', '2000px'); fig.querySelector('.plate-scroll').style.setProperty('--w', '2000px');
    window.dispatchEvent(new Event('resize')); await new Promise((r) => setTimeout(r, 400)); },
    verify: (r) => r.runs[0].fit.offered.every((x) => x.specimen !== 's-demo-sheet') },
  { key: 'fitFloor', fault: 'a 1,200 px plate set only in 48 px type: the shell offers the switch, and fitting keeps it over 13 px (allowed: must not be flagged)', expect: false, js: async () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const fig = st.closest('figure');
    st.innerHTML = '<p style="font:700 48px/1.1 Inter;margin:0;padding:24px">Forty-eight pixel type only</p>';
    st.style.setProperty('--w', '1200px'); fig.querySelector('.plate-scroll').style.setProperty('--w', '1200px');
    window.dispatchEvent(new Event('resize')); await new Promise((r) => setTimeout(r, 400)); },
    verify: (r) => r.runs[0].fit.offered.some((x) => x.specimen === 's-demo-sheet' && x.smallest >= 13) },
  { key: 'illusOnce', fault: 'an Illustrative label in a piece whose caption carries one too', js: () => {
    const fig = document.querySelector('.plate-cap .illus').closest('figure');
    fig.querySelector('.plate-stage').insertAdjacentHTML('afterbegin', '<span class="illus">Illustrative</span>'); } },
  // Q1 to Q4 pass, November 8, 2026 (CD-S9). The demo's 640 px sheet fits its frame at 1440 px.
  { key: 'scrollHint', fault: 'a 640 px plate that fits its frame, with its "Wider than this column" hint shown', js: () => {
    document.querySelector('[data-specimen="s-demo-sheet"]').closest('figure').querySelector('.plate-hint').hidden = false; } },
  { key: 'scrollHint', fault: 'the same fitting plate with a tab stop and a "Scroll sideways" name on its frame', js: () => {
    const box = document.querySelector('[data-specimen="s-demo-sheet"]').closest('.plate-scroll');
    box.setAttribute('tabindex', '0'); box.setAttribute('role', 'group'); box.setAttribute('aria-label', 'Sheet, at true size. Scroll sideways to see all of it.'); } },
  { key: 'scrollHint', fault: 'a 2,000 px plate that scrolls with its hint, tab stop and name left off (no resize)', js: () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const box = st.closest('.plate-scroll');
    st.style.setProperty('--w', '2000px'); box.style.setProperty('--w', '2000px'); } },
  { key: 'frameFit', fault: 'a plate 16 px too wide for 48 px sides, held at 48 px sides, so it scrolls though 32 px sides would hold it (the CD-S9 fault)', js: async () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const box = st.closest('.plate-scroll');
    const w = (box.clientWidth - 96 + 16) + 'px';
    st.style.setProperty('--w', w); box.style.setProperty('--w', w); box.style.paddingInline = '48px';
    window.dispatchEvent(new Event('resize')); await new Promise((r) => setTimeout(r, 400)); } },
  { key: 'frameFit', fault: 'the same plate with the shell\'s own sides after a resize: it takes 32 px sides and sits whole and centered with no hint (allowed: must not be flagged)', expect: false, js: async () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const box = st.closest('.plate-scroll');
    const w = (box.clientWidth - 96 + 16) + 'px';
    st.style.setProperty('--w', w); box.style.setProperty('--w', w);
    window.dispatchEvent(new Event('resize')); await new Promise((r) => setTimeout(r, 400)); },
    verify: (r) => r.runs[0].frames.snug.some((x) => x.specimen === 's-demo-sheet' && x.sides === 32 && !x.hint && !x.scrolls)
      && !r.failures.some((f) => f.key === 'scrollHint') },
  { key: 'frameFit', fault: 'a fitting 640 px plate pushed off center by a 120 px left side', js: () => {
    document.querySelector('[data-specimen="s-demo-sheet"]').closest('.plate-scroll').style.paddingLeft = '120px'; } },
  // Stage B, November 9, 2026: the accessibility audit's checks that run today (section 2), DR-153 and the mark tokens (D2-402)
  { key: 'forcedGlyphs', fault: 'a menu glyph drawn as three CSS-background bars in a button, which forced colors erases (UX-1, D-1)', js: () => {
    const bar = '<i style="display:block;height:2px;background:currentColor"></i>';
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', `<button type="button" style="min-height:44px;display:inline-flex;align-items:center;gap:8px"><span aria-hidden="true" style="display:inline-grid;width:18px;height:12px;align-content:space-between">${bar}${bar}${bar}</span>Menu</button>`); } },
  { key: 'forcedGlyphs', fault: 'the same glyph drawn as an SVG stroke in currentColor (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<button type="button" style="min-height:44px;display:inline-flex;align-items:center;gap:8px"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="U-menu" data-icon-family="utility" style="fill:none;stroke:currentColor;stroke-width:2"><path d="M3 7h18M3 12h18M3 17h18"/></svg>Menu</button>'); } },
  // promotion, November 10, 2026: a glyph drawn from a sprite symbol through <use>, as the masthead's menu glyph is now
  { key: 'forcedGlyphs', fault: 'a menu glyph drawn through <use> from a symbol that keeps the file\'s literal ink, which forced colors on a dark ground erases (UX-1, D-1)', js: () => {
    document.body.insertAdjacentHTML('afterbegin', '<svg class="oa-sprite" aria-hidden="true" focusable="false" width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden"><symbol id="sb-sym-ink" viewBox="0 0 24 24"><g fill="none" stroke="#121212" stroke-width="2" stroke-linecap="round"><path d="M4 6H20 M4 12H20 M4 18H20"/></g></symbol></svg>');
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<button type="button" style="min-height:44px;display:inline-flex;align-items:center;gap:8px"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="U-menu" data-icon-family="utility"><use href="#sb-sym-ink"/></svg>Menu</button>'); } },
  { key: 'forcedGlyphs', fault: 'the same glyph through <use> from a symbol in currentColor, as the sprite writes it (allowed: must not be flagged)', expect: false, js: () => {
    document.body.insertAdjacentHTML('afterbegin', '<svg class="oa-sprite" aria-hidden="true" focusable="false" width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden"><symbol id="sb-sym-cur" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6H20 M4 12H20 M4 18H20"/></g></symbol></svg>');
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<button type="button" style="min-height:44px;display:inline-flex;align-items:center;gap:8px"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="U-menu" data-icon-family="utility"><use href="#sb-sym-cur"/></svg>Menu</button>'); },
    verify: (r) => r.runs[0].stageB.useParts >= 1 },
  { key: 'focus', fault: 'a button whose focus ring is a box-shadow, which forced colors removes (UX-5, G-1)', focus: true, js: () => {
    const st = document.createElement('style'); st.textContent = '.sb-ring:focus-visible{outline:none;box-shadow:0 0 0 2px #2E7D6B}'; document.head.append(st);
    document.querySelector('.mh-bar .home').insertAdjacentHTML('afterend', '<button type="button" class="sb-ring">Shadow ring</button>'); } },
  { key: 'focus', fault: 'the same button with the shell\'s 2 px outline (allowed: must not be flagged)', expect: false, focus: true, js: () => {
    document.querySelector('.mh-bar .home').insertAdjacentHTML('afterend', '<button type="button">Outline ring</button>'); } },
  { key: 'menuDialog', fault: 'the phone menu closes by Escape but sends focus to the home link, not back to Menu (G-3)', widths: [390], js: () => {
    document.getElementById('menu').addEventListener('close', () => setTimeout(() => document.querySelector('.mh-bar .home').focus(), 0)); } },
  { key: 'motion', fault: 'a glyph that spins forever (E-1)', js: () => {
    const st = document.createElement('style'); st.textContent = '@keyframes sb-spin{to{transform:rotate(360deg)}}'; document.head.append(st);
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p>Loading <span data-icon="U-loading" data-icon-family="utility" aria-hidden="true" style="display:inline-block;width:24px;height:24px;border-top:2px solid;animation:sb-spin 1s linear infinite"></span></p>'); } },
  { key: 'motion', fault: 'an SMIL animation in an SVG (E-1)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="5" fill="currentColor"><animate attributeName="r" values="5;8;5" dur="1s" repeatCount="indefinite"/></circle></svg>'); } },
  { key: 'reducedMotion', fault: 'a 300 ms transition that stays on under reduced motion (E-2)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p style="transition:opacity 300ms !important">Fades in</p>'); } },
  { key: 'labelInName', fault: 'a button that shows "Done" and is named "Close the dialog" (A-3)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<button type="button" aria-label="Close the dialog">Done</button>'); } },
  { key: 'controlNames', fault: 'a glyph-only button named "Settings" (A-4)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<button type="button" aria-label="Settings" style="min-width:44px;min-height:44px"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="6" fill="currentColor"/></svg></button>'); } },
  { key: 'controlNames', fault: 'the glyph-only clear control in a search field, named "Clear the search" (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<button type="button" aria-label="Clear the search" style="min-width:44px;min-height:44px"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2"/></svg></button>'); } },
  { key: 'titleOnly', fault: 'a button named only by its title, "Download" (A-8)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<button type="button" title="Download" style="min-width:44px;min-height:44px"><svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><path d="M12 4v12" stroke="currentColor" stroke-width="2"/></svg></button>'); } },
  { key: 'iconNames', fault: 'a named glyph beside its own word, read twice (A-1, A-2)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<ul><li>Download <svg data-icon="U-download" data-icon-family="utility" role="img" aria-label="Download" viewBox="0 0 24 24" width="24" height="24"><path d="M12 4v12" stroke="currentColor" stroke-width="2"/></svg></li></ul>'); } },
  { key: 'iconTargets', fault: 'a link with a utility glyph standing 30 px tall (B-1)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><a href="#top" style="display:inline-flex;align-items:center;height:30px;gap:8px"><svg data-icon="U-arrow-up" data-icon-family="utility" aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><path d="M12 19V5" stroke="currentColor" stroke-width="2"/></svg>Top</a></p>'); } },
  { key: 'iconTargets', fault: 'a link with its 16 px mark inline in a paragraph\'s running text, WCAG 2.5.8\'s inline exception (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p>Read the <a href="#top">full record <svg data-icon="U-another-site" data-icon-family="utility" aria-hidden="true" focusable="false" viewBox="0 0 16 16" width="16" height="16"><path d="M4 12 12 4" stroke="currentColor" stroke-width="1.5"/></svg></a> before you write to the office.</p>'); },
    verify: (r) => r.runs[0].stageB.inlineTargets >= 1 },
  { key: 'iconTargets', fault: 'the Fit to window switch back at 36 px (DR-153)', js: () => {
    const st = document.createElement('style'); st.textContent = '.fit-btn{min-height:36px !important}'; document.head.append(st); } },
  { key: 'iconSizes', fault: 'a topic symbol at 16 px (DR-136, B-3)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg data-icon="CL-001" data-icon-family="topic" aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="8" fill="currentColor"/></svg> Voting</p>'); } },
  // round 2, November 10, 2026: the list of 41 and the family required in chapter 10
  { key: 'iconSizes', fault: 'a topic symbol on the list of 41 at 24 px (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg data-icon="CL-032" data-icon-family="atlas" aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="8" fill="currentColor"/></svg> Local news supply</p>'); } },
  { key: 'iconSizes', fault: 'a topic symbol not on the list of 41 at 24 px (DR-136, B-3)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg data-icon="CL-055" data-icon-family="topic" aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="8" fill="currentColor"/></svg> Productivity</p>'); } },
  { key: 'iconSizes', fault: 'a glyph without data-icon-family in chapter 10, where the family is required (D2-517)', js: () => {
    document.querySelector('main').insertAdjacentHTML('beforeend', '<section class="chapter" id="symbols"><p><svg data-icon="CL-001" aria-hidden="true" focusable="false" viewBox="0 0 48 48" width="48" height="48"><circle cx="24" cy="24" r="16" fill="currentColor"/></svg> Voting</p></section>'); } },
  { key: 'iconSizes', fault: 'a glyph without data-icon-family in any other chapter, now that the family is required everywhere (D2-517)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg data-icon="CL-001" aria-hidden="true" focusable="false" viewBox="0 0 48 48" width="48" height="48"><circle cx="24" cy="24" r="16" fill="currentColor"/></svg> Voting</p>'); } },
  { key: 'stateWords', fault: 'a tracker of three steps whose alt text names no state (A-5)', js: () => {
    const st = document.querySelector('.plate--correct [data-specimen][role="img"]'); st.setAttribute('aria-label', 'A bill at true size, on a line of three steps.');
    st.insertAdjacentHTML('beforeend', '<svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="48" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g><g data-icon="S-not-yet" data-icon-family="status"><circle cx="83" cy="15" r="12" fill="none" stroke="currentColor" stroke-width="1.5"/></g></svg>'); } },
  { key: 'stateWords', fault: 'the same tracker with each step\'s name and state in its alt text (allowed: must not be flagged)', expect: false, js: () => {
    const st = document.querySelector('.plate--correct [data-specimen][role="img"]'); st.setAttribute('aria-label', 'A bill at true size. Steps: 1 Filed done; 2 Hearing now; 3 Committee vote not yet.');
    st.insertAdjacentHTML('beforeend', '<svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="48" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g><g data-icon="S-not-yet" data-icon-family="status"><circle cx="83" cy="15" r="12" fill="none" stroke="currentColor" stroke-width="1.5"/></g></svg>'); },
    verify: (r) => r.runs[0].stageB.stateStages >= 1 },
  { key: 'disabledControls', fault: 'a disabled attribute on a toolbar button (G-4)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div role="toolbar" aria-label="Report tools"><button type="button" disabled>Print</button></div>'); } },
  { key: 'stateCues', fault: 'a pressed button told from its peer by fill and color alone (C-5)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div><button type="button" class="sb-seg" aria-pressed="true" style="background:#121212;color:#DCD9D2">On</button><button type="button" class="sb-seg" aria-pressed="false">Off</button></div>'); } },
  { key: 'stateCues', fault: 'the same pressed button, underlined as well (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div><button type="button" class="sb-seg" aria-pressed="true" style="background:#121212;color:#DCD9D2;text-decoration:underline">On</button><button type="button" class="sb-seg" aria-pressed="false">Off</button></div>'); } },
  { key: 'textSpacing', fault: 'a link held to 20 px by 80 px with its overflow hidden, which clips with text spacing (F-1)', widths: [390], js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><a href="#top" style="display:inline-block;height:20px;width:80px;overflow:hidden">Back to the top</a></p>'); } },
  { key: 'markTokens', fault: 'a tracker\'s now ring drawn at 2.5 px in a correct plate, off its 3 px token (D2-402)', js: () => {
    document.querySelector('.plate--correct [data-specimen]').insertAdjacentHTML('beforeend', '<svg class="sx-mk" width="30" height="30" viewBox="0 0 30 30" aria-hidden="true" focusable="false"><circle cx="15" cy="15" r="13.75" class="sx-fb sx-si" stroke-width="2.5" fill="none" stroke="#121212"/></svg>'); } },
  { key: 'markTokens', fault: 'the same ring drawn at 3 px, which the shell sets from its token (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.plate--correct [data-specimen]').insertAdjacentHTML('beforeend', '<svg class="sx-mk" width="30" height="30" viewBox="0 0 30 30" aria-hidden="true" focusable="false"><circle cx="15" cy="15" r="13.5" class="sx-fb sx-si" stroke-width="3" fill="none" stroke="#121212"/></svg>'); },
    verify: (r) => r.runs[0].stageB.markReaders['ring-now'] >= 1 },
];

async function selfTest() {
  const outDir = fs.mkdtempSync(path.join(process.env.TMPDIR || os.tmpdir(), 'oa-guide-check-'));
  const page = path.join(outDir, 'Guide-Check-Demo.html');
  execFileSync('python3', ['-I', path.join(__dirname, 'guide_build.py'), '--demo', '--quiet', '--out', page,
    '--chapters', path.join(outDir, 'no-chapters'), '--specimens', path.join(outDir, 'no-specimens')]);
  const browser = await chromium.launch();
  const result = { checked: new Date().toISOString(), page: 'demo build (guide_build.py --demo), in a temporary folder', axe: AXE ? 'found' : 'not found', clean: null, plants: [] };
  // the clean demo: no structural, text, red or writing failure, and the exempt failure plate's 12 px gray text is skipped
  const clean = await checkPage(browser, page, [1440, 390], { skipFocus: false });
  result.clean = { pass: clean.pass, failures: clean.failures.map((f) => f.msg), exemptions: clean.runs[0].specimens.exemptions, skippedTexts: clean.runs[0].text.skipped };
  for (const p of PLANTS) {
    const r = await checkPage(browser, page, p.widths || [1440], { mutate: p.js, skipAxe: true, skipFocus: !p.focus, plant: true });
    const caught = r.failures.filter((f) => f.key === p.key);
    const others = r.failures.filter((f) => f.key !== p.key).map((f) => f.key);
    // a plant with expect: false proves an allowance: the test must stay quiet. verify, where given, reads the run
    // itself, for example that the shell offered or withheld a switch.
    const expect = p.expect !== false;
    const verified = p.verify ? !!p.verify(r) : true;
    result.plants.push({ test: p.key, fault: p.fault, expect: expect ? 'caught' : 'not flagged', caught: caught.length > 0, verified, ok: (caught.length > 0) === expect && verified,
      message: caught[0] ? caught[0].msg : null, alsoFlagged: [...new Set(others)] });
  }
  await browser.close();
  result.pass = result.clean.pass && result.plants.every((p) => p.ok);
  const ri = process.argv.indexOf('--results');
  const outPath = ri > 0 && process.argv[ri + 1] ? path.resolve(process.argv[ri + 1]) : path.join(ROOT, 'work/boards/phase-2/stage-a/20261106_Guide-Check-Plant-Results.json');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(result, null, 1));
  const faults = result.plants.filter((p) => p.expect === 'caught'), allow = result.plants.filter((p) => p.expect !== 'caught');
  console.log(`${result.pass ? 'PASS' : 'FAIL'} self-test: clean demo ${result.clean.pass ? 'passes' : 'FAILS'}; ${faults.filter((p) => p.ok).length} of ${faults.length} planted faults caught`
    + (allow.length ? `; ${allow.filter((p) => p.ok).length} of ${allow.length} allowed cases left alone` : ''));
  if (!result.clean.pass) result.clean.failures.forEach((f) => console.log('  clean: ' + f));
  for (const p of result.plants) console.log(`  ${p.ok ? (p.expect === 'caught' ? 'caught' : 'quiet ') : (p.expect === 'caught' ? 'MISSED' : 'FLAGGED')}  ${p.test.padEnd(17)} ${p.fault}${p.alsoFlagged.length ? '  (also: ' + p.alsoFlagged.join(', ') + ')' : ''}`);
  console.log('  results: ' + outPath);
  fs.rmSync(outDir, { recursive: true, force: true });
  process.exit(result.pass ? 0 : 1);
}

// ------------------------------------------------------------------------------------------------ main
(async () => {
  if (process.argv.includes('--self-test')) return selfTest();
  const arg = process.argv.slice(2).find((x, i, all) => !x.startsWith('--') && all[i - 1] !== '--results');
  const file = arg ? path.resolve(arg) : '';
  if (!file || !fs.existsSync(file)) { console.error('usage: node guide_check.js <page.html> [--quick] [--no-captures] | --self-test'); process.exit(2); }
  const widths = process.argv.includes('--quick') ? [1440, 390] : [1440, 1024, 390, 360];
  const browser = await chromium.launch();
  const report = await checkPage(browser, file, widths, { captures: !process.argv.includes('--no-captures') });
  await browser.close();
  const outPath = path.join(path.dirname(file), `${path.basename(file, '.html')}-Guide-Check-Results.json`);
  fs.writeFileSync(outPath, JSON.stringify(report, null, 1));
  const r0 = report.runs[0];
  console.log(`${report.pass ? 'PASS' : 'FAIL'} ${report.file}: ${widths.length} widths, ${r0.structure.rules} rules, ${r0.specimens.stages} specimens, ${r0.anchors.links} same-page links, ${report.failures.length} failures`);
  if (r0.specimens.exemptions.length) console.log(`  exemptions: ${r0.specimens.exemptions.map((x) => x.specimen + ' (' + x.skips + ')').join(', ')}`);
  for (const f of report.failures) console.log('  - ' + f.msg);
  console.log('  results: ' + path.relative(ROOT, outPath));
  process.exit(report.pass ? 0 : 1);
})();
