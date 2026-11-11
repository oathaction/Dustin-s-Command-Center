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
// Added in the round 3 fix pass (November 10, 2026):
//   frameFit           also: from 80em, a chapter plate whose fixed stage scrolls though breaking out over the rail to the
//                      page's margin would hold it whole (CA-S13); and a frame that breaks out hides the rail while it
//                      covers it, so no rail link sits out of sight
//   textSpacing        also: at 1024 px, with text at 200 percent, the page does not scroll sideways (CA-S17, SC 1.4.4)
//   forcedWordmark     with forced colors on, dark and light, the masthead wordmark draws in one color (CA-S16)
//   nbHyphen           no U+2011 (the non-breaking hyphen) in the page's text, SVG text included, or in an alt, title,
//                      aria-label or other name: the page's fonts do not draw it and a search for "CL-001" misses it
//                      (D2-975); the build writes IDs with an ASCII hyphen inside <span class="nw">
//   iconTargets        also: a control that shows only after a reader types, such as a search field's Clear, is typed
//                      into view and held to 44 by 44 px (CA-M2). Runs last, so no other check sees the typed state
// Added in stage C, round 0 (November 10, 2026):
//   textSpacing        also: at 390 and 360 px, with text at 200 percent, the page does not scroll sideways and no
//                      masthead control leaves the screen (D2-1103, SC 1.4.4 and 1.4.10)
//   codeMatch          every code plate's panels, pasted as a builder would into a page that holds tokens.css, the brand's
//                      fonts and body { margin: 0; font: var(--oa-type-body) } and nothing else, draw pixel for pixel
//                      what the guide's live stage draws, in the light and the dark theme, at the stage's own width (DR-203)
//   openerFit          a chapter's opener figure sits in the chapter head, before the first rule, whole in its frame at
//                      true size (D2-965, D2-1134)
//   lightOnDark        with the device set to dark, the guide stays light: the root keeps data-oa-theme="light" and
//                      color-scheme "only light", and every element's colors, fills, strokes, borders, outlines, shadows
//                      and color scheme compute exactly as they do with the device set to light (DR-204, D2-1133)
// Added in promotion C (November 11, 2026):
//   fitSwitch          DR-179 and DR-209 as drawn: every <svg> that draws one of the 41 at 24 px (its box measured, so a
//                      size CSS sets counts too) pairs <use class="oa-at-1x"> of the 24 px fit with <use class="oa-at-2x">
//                      of its own master, and only the 41 switch; at 1x the fit shows alone at every width, and on a
//                      high-density screen the master shows alone (1440 px at 2x and 390 px at 3x, in their own runs);
//                      data-oa-res="fixed" marks a plate that shows one drawing on every screen. The list of 41 is read
//                      from the construction file, as guide_build.py and chapter 10's generator read it (B-3 too)
// Added in stage C, round 1 (November 11, 2026), each described where it is defined below:
//   keyPath            every code set's keyboard path from its keys file, walked in both live stages at 1440 and 390 px
//   motionPlay         every moving specimen: still on load, Play, Pause and Reset, comes to rest, and under reduced motion
//                      the final frame at once
//   tokenTable         chapter 26's token table against tokens.json
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
    if (fr.couldBreakOut && fr.couldBreakOut.length) add('frameFit', `${fr.couldBreakOut.length} chapter frame(s) that scroll though breaking out over the rail would hold the stage whole (CA-S13): ${ids(fr.couldBreakOut)}; first: ${JSON.stringify(fr.couldBreakOut[0])}`);
    const hid = (fr.breakout || []).filter((x) => x.overlaps && x.railShown);
    if (hid.length) add('frameFit', `${hid.length} frame(s) that break out over the rail while the rail still shows, so its links sit under the frame (CA-S13): ${ids(hid)}`);
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
  return page.evaluate(async () => {
    const rootCs = getComputedStyle(document.documentElement);
    const tok = rootCs.getPropertyValue('--oa-space-400').trim();
    const snugPx = /rem$/.test(tok) ? parseFloat(tok) * parseFloat(rootCs.fontSize) : (parseFloat(tok) || 32);
    const out = { snugPx, frames: 0, scrolling: 0, snug: [], hintNoScroll: [], scrollNoHint: [], couldFit: [], offCenter: [], couldBreakOut: [], breakout: [] };
    // CA-S13 (round 3): from 80em a chapter plate may take the room to its left, over the rail, out to the page's margin
    const wideBreak = window.matchMedia('(min-width: 80em)').matches;
    const pageBox = document.querySelector('.frame');
    const edge = pageBox ? pageBox.getBoundingClientRect().left + parseFloat(getComputedStyle(pageBox).paddingLeft) : 0;
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
        const reach = Math.floor(fig.getBoundingClientRect().left - edge);
        if (wideBreak && pageBox && box.hasAttribute('data-width') && fig.closest('.chapter') && !fig.classList.contains('is-breakout') && reach >= 1
          && need + 2 * snugPx <= box.clientWidth + reach) out.couldBreakOut.push({ specimen: id, need, frame: box.clientWidth, reach });
      } else {
        if (hintOn || tabStop || named) out.hintNoScroll.push({ specimen: id, hint: hintOn, tabStop, named });
        const s = st.getBoundingClientRect();
        const gaps = [+(s.left - r.left).toFixed(2), +(r.right - s.right).toFixed(2)];
        const scaled = Math.abs(s.width - st.offsetWidth) > 1;
        if (Math.abs(gaps[0] - gaps[1]) > 1 || scaled) out.offCenter.push({ specimen: id, gaps, drawn: +s.width.toFixed(2), trueWidth: st.offsetWidth });
      }
    }
    // a frame that breaks out hides the rail while it covers it: each one is scrolled into view and the rail read
    const rail = document.querySelector('.rail');
    const keep = window.scrollY;
    for (const fig of document.querySelectorAll('figure.plate.is-breakout')) {
      const box = fig.querySelector(':scope > .plate-scroll');
      box.scrollIntoView({ block: 'center' });
      await new Promise((res) => requestAnimationFrame(() => requestAnimationFrame(res)));
      const b = box.getBoundingClientRect(), rr = rail ? rail.getBoundingClientRect() : null;
      const overlaps = !!rr && rr.width > 0 && b.left < rr.right && b.top < rr.bottom && b.bottom > rr.top;
      const railShown = !!rail && getComputedStyle(rail).visibility !== 'hidden' && getComputedStyle(rail).display !== 'none';
      out.breakout.push({ specimen: fig.querySelector('.plate-stage').getAttribute('data-specimen'), left: Math.round(b.left), width: Math.round(b.width), scrolls: box.scrollWidth > box.clientWidth + 1, overlaps, railShown });
    }
    window.scrollTo(0, keep);
    await new Promise((res) => requestAnimationFrame(() => requestAnimationFrame(res)));
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
// and atlas drawings and the four pillar icons. Promotion C: read from that file, the one source guide_build.py and
// chapter 10's generator read, so the three cannot drift apart. CL-075 Housing is not on it (DR-207).
const CONSTRUCTION = path.join(ROOT, 'work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md');
const READS_AT_24 = (() => {
  const m = fs.readFileSync(CONSTRUCTION, 'utf8').match(/\*\*The list, by ID\*\*[\s\S]*?\n\n(.*?)\n/);
  const ids = (m && m[1].match(/(?:CL|R)-\d+/g)) || [];
  if (ids.length !== 41 || new Set(ids).size !== 41 || !['CL-019', 'CL-020', 'CL-021', 'CL-022'].every((x) => ids.includes(x))) {
    console.error(`guide_check: ${path.relative(ROOT, CONSTRUCTION)} gives ${ids.length} IDs under "The list, by ID"; the list of 41 with the four pillar icons is needed`);
    process.exit(2);
  }
  return ids;
})();
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
// Promotion C (November 11, 2026): DR-179 and DR-209 as the browser draws them, at the page's own device scale. Each
// <svg> outside the sprites that draws one of the 41 at 24 px (its drawn box, whatever sets it) or carries the switch's
// classes: the switch pairs one 24 px fit of the 41 with its own master, the right one of the two shows alone at this
// scale, and a master of the 41 never stands alone at 24 px. A fit standing alone at 24 px draws on 2x screens too.
// data-oa-res="fixed" exempts a plate that shows one drawing on every screen on purpose.
async function fitSwitch(page, dpr) {
  return page.evaluate(({ READS_AT_24, dpr }) => {
    const out = { dpr, glyphs: 0, pairs: 0, fitShown: 0, masterShown: 0, fixed: 0, problems: [] };
    const where = (el) => { const st = el.closest('[data-specimen]'); const sec = el.closest('section[id]'); return st ? st.getAttribute('data-specimen') : sec ? '#' + sec.id : 'masthead and shell'; };
    const ref = (u) => (u.getAttribute('href') || u.getAttribute('xlink:href') || '').replace(/^#/, '');
    const kind = (sid) => {
      let m = sid.match(/^oa-sym-((?:cl|r)-\d+)-(16|24)px$/);
      if (m) return { fit: true, id: m[1].toUpperCase(), size: Number(m[2]) };
      m = sid.match(/^oa-sym-((?:cl|r)-\d+)$/);
      return m ? { fit: false, id: m[1].toUpperCase() } : null;
    };
    const shown = (el) => getComputedStyle(el).display !== 'none';
    const drawn = (el) => { const r = el.getBoundingClientRect(); if (!r.width && !r.height) return false; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; } return !el.closest('dialog:not([open])'); };
    const on41 = (k) => k && READS_AT_24.includes(k.id) && (!k.fit || k.size === 24);
    for (const svg of document.querySelectorAll('svg')) {
      if (svg.closest('.oa-sprite')) continue;
      const uses = [...svg.querySelectorAll('use')].filter((u) => u.closest('svg') === svg)
        .map((u) => ({ u, sid: ref(u), k: kind(ref(u)), one: u.classList.contains('oa-at-1x'), two: u.classList.contains('oa-at-2x') }));
      const ones = uses.filter((x) => x.one), twos = uses.filter((x) => x.two);
      if (!uses.some((x) => on41(x.k)) && !ones.length && !twos.length) continue;
      if (!drawn(svg)) continue;
      const w = Math.round(svg.getBoundingClientRect().width * 2) / 2;
      const at24 = Math.abs(w - 24) < 0.5;
      if (!at24 && !ones.length && !twos.length) continue;   // a master of the 41 at 48 px and up
      out.glyphs++;
      const loc = { where: where(svg), w, uses: uses.map((x) => x.sid + (x.one ? ' (1x)' : x.two ? ' (2x)' : '')).join(', ') };
      if (svg.getAttribute('data-oa-res') === 'fixed') { out.fixed++; continue; }
      if (ones.length || twos.length) {
        const fit = ones.length === 1 && ones[0].k && ones[0].k.fit && on41(ones[0].k) ? ones[0] : null;
        const master = fit && twos.length === 1 && twos[0].k && !twos[0].k.fit && twos[0].k.id === fit.k.id ? twos[0] : null;
        if (!fit || !master) { out.problems.push({ ...loc, why: 'the switch pairs one 24 px fit of the 41 with its own master, and nothing else switches (DR-179, DR-209)' }); continue; }
        if (!at24) { out.problems.push({ ...loc, why: `the switch drawn at ${w} px; a fit serves 24 px only` }); continue; }
        out.pairs++;
        const wantFit = dpr < 2;
        if (shown(fit.u) !== wantFit || shown(master.u) === wantFit) out.problems.push({ ...loc, why: `at ${dpr}x the ${wantFit ? 'fit' : 'master'} must show alone, and the fit is ${shown(fit.u) ? 'shown' : 'hidden'}, the master ${shown(master.u) ? 'shown' : 'hidden'}` });
        else if (wantFit) out.fitShown++; else out.masterShown++;
      } else {
        const m = uses.find((x) => x.k && !x.k.fit && on41(x.k));
        const f = uses.find((x) => x.k && x.k.fit && on41(x.k));
        if (m) out.problems.push({ ...loc, why: `${m.k.id} at 24 px draws its master on 1x screens; 1x screens take its fit (${['CL-019', 'CL-020', 'CL-021', 'CL-022'].includes(m.k.id) ? 'DR-179' : 'DR-209'})` });
        else if (f) out.problems.push({ ...loc, why: `${f.k.id}'s 24 px fit stands alone, so 2x screens draw it too; pair it with its master` });
      }
    }
    return out;
  }, { READS_AT_24, dpr });
}

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
    // A-5 (round 2): every step of a tracker says its state in words. A tracker is a drawing with three or more step
    // marks; trackers carry no data-step, so their words are read in the stage's alt text, its status lines and the
    // names inside it. Each state's word must appear as often as its marks (a range such as "steps 1 to 3 done" counts
    // for each step): done, now, not yet, never happened, stopped, and "you can take part now" beside a take-part
    // mark. A live tracker fails without them; a picture's alt describes the picture, so a shortfall there is listed
    // for its owner (as D2-586 phased in the family attribute). Failure plates are skipped.
    const WORDS = { 'S-done': /\bdone\b/gi, 'S-now': /(?<!take part )\bnow\b/gi, 'S-take-part': /\byou can take part now\b/gi, 'S-not-yet': /\bnot yet\b/gi, 'S-never-happened': /\bnever happened\b/gi, 'S-stopped': /\bstopped\b/gi };
    const said = (text, re) => {
      let n = 0;
      for (const m of text.matchAll(re)) {
        const before = text.slice(Math.max(0, m.index - 40), m.index);
        const r = before.match(/steps?\s+(\d+)\s+(?:to|through)\s+(\d+)\D{0,24}$/i);
        // round 1 (chapter 17's maker, item 3): "steps 1 and 2 done" and "steps 1, 3 and 5 done" count each step named
        const l = r ? null : before.match(/steps\s+((?:\d+\s*,\s*)*\d+)\s+and\s+\d+\D{0,24}$/i);
        n += r ? Math.max(1, +r[2] - +r[1] + 1) : l ? l[1].split(',').length + 1 : 1;
      }
      return n;
    };
    out.statePictures = [];
    for (const st of document.querySelectorAll('[data-specimen]')) {
      if (st.closest('.plate--failure')) continue;
      // a plate may draw one row twice, one copy for each screen width, and hide the other: only the copy on screen counts,
      // as only it reaches a reader (round 3, the editor's note on s-01-pieces)
      const onScreen = (s) => [...s.querySelectorAll('[data-icon-family="status"][data-icon]')].filter((m) => rendered(m));
      const trackers = [...st.querySelectorAll('svg')].filter((s) => onScreen(s).length >= 3);
      if (!trackers.length) continue;
      out.stateStages++;
      const marks = trackers.flatMap(onScreen).filter((m) => WORDS[m.getAttribute('data-icon')]);
      const named = [st.getAttribute('aria-label') || '', ...(st.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean).map((id) => (document.getElementById(id) || {}).textContent || '')];
      const text = (named.join(' ') + ' ' + st.innerText + ' ' + [...st.querySelectorAll('[aria-label]')].map((e) => e.getAttribute('aria-label')).join(' ')).replace(/\s+/g, ' ');
      const count = {}; for (const m of marks) { const k = m.getAttribute('data-icon'); count[k] = (count[k] || 0) + 1; }
      const short = Object.entries(count).filter(([k, n]) => said(text, WORDS[k]) < n).map(([k, n]) => `${k} ${said(text, WORDS[k])} of ${n}`);
      if (!short.length) continue;
      (st.getAttribute('role') === 'img' ? out.statePictures : out.stateWords).push({ where: st.getAttribute('data-specimen'), short: short.join(', ') });
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
  const out = { glyphParts: mark.n, useParts: mark.uses, erased: [], wordmark: [] };
  for (const scheme of ['dark', 'light']) {
    await page.emulateMedia({ forcedColors: 'active', colorScheme: scheme });
    await page.waitForTimeout(50);
    // CA-S16 (round 3): the masthead wordmark draws in one color under forced colors, ampersand included
    out.wordmark.push(...await page.evaluate((scheme) => {
      const bad = [];
      for (const svg of document.querySelectorAll('.masthead svg.wm')) {
        if (!window.__sb.rendered(svg)) continue;
        const inks = new Set();
        for (const el of svg.querySelectorAll('path, rect, circle, polygon, use')) {
          const cs = getComputedStyle(el);
          if (cs.fill !== 'none') inks.add(cs.fill);
          if (cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0) inks.add(cs.stroke);
        }
        if (inks.size > 1) bad.push({ where: 'masthead', scheme, wordmark: svg.getAttribute('class'), inks: [...inks] });
      }
      return bad;
    }, scheme));
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
async function sbSpacing(page, modes = ['spacing', 'zoom'], zoomScroll = false) {
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
    // the shell sizes its frames on resize; a reader who sets a larger text size reloads or resizes, so it runs here too
    if (mode === 'zoom' && zoomScroll) { await page.evaluate(() => window.dispatchEvent(new Event('resize'))); await page.waitForTimeout(400); }
    const r = await page.evaluate(({ mode, zoomScroll }) => {
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
      if ((mode === 'spacing' || zoomScroll) && document.documentElement.scrollWidth > window.innerWidth + 1) {
        // round 1 (the accessibility lead's item 1): name what pushes the page wide, innermost first: an element whose
        // right edge passes the screen, with no box around it that scrolls or clips, and no child that passes it further
        const W = window.innerWidth + 1;
        const free = (el) => { for (let e = el.parentElement; e && e !== document.body; e = e.parentElement) { const ox = getComputedStyle(e).overflowX; if (/auto|scroll|hidden|clip/.test(ox)) return false; } return true; };
        const past = [...document.querySelectorAll('body *')].filter((el) => { const r = el.getBoundingClientRect(); return r.width && r.right > W && free(el); });
        const inner = past.filter((el) => !past.some((o) => o !== el && el.contains(o)));
        const name = (el) => { const st = el.closest('[data-specimen]'); const sec = el.closest('section[id]'); return { where: st ? st.getAttribute('data-specimen') : sec ? '#' + sec.id : 'page', el: el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''), right: Math.round(el.getBoundingClientRect().right), text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40) }; };
        bad.push({ where: 'page', mode, why: `scrolls sideways (${document.documentElement.scrollWidth} px)`, culprits: inner.slice(0, 4).map(name) });
      }
      // a masthead control pushed past either edge cannot be reached: past the left edge no scroll brings it back
      if (zoomScroll) for (const el of document.querySelectorAll('.masthead a, .masthead button')) {
        if (!rendered(el)) continue; const r = el.getBoundingClientRect();
        if (r.left < -1 || r.right > window.innerWidth + 1) bad.push({ ...desc(el), mode, why: `a masthead control off the screen (${Math.round(r.left)} to ${Math.round(r.right)} px)` });
      }
      document.getElementById('sb-spacing').remove();
      return bad;
    }, { mode, zoomScroll });
    if (mode === 'zoom' && zoomScroll) { await page.evaluate(() => window.dispatchEvent(new Event('resize'))); await page.waitForTimeout(400); }
    await page.waitForTimeout(150);
    return r;
  };
  const out = [];
  for (const m of modes) out.push(...(await pass(m)));
  return out;
}

// CA-M2 (round 3): B-1 for a control that shows only after a reader types, such as a search field's Clear. Each text
// field in a live specimen takes one letter from the keyboard; every control holding a glyph that came into view is
// measured; the field then goes back to what it held. The check runs after every other one at its width.
async function sbTyped(page) {
  await sbInstall(page);
  const n = await page.evaluate(() => {
    const { picture, rendered } = window.__sb;
    const sel = ['input:not([type])', 'input[type="text"]', 'input[type="search"]', '[role="searchbox"]'].map((x) => '[data-specimen] ' + x).join(', ');
    const fields = [...document.querySelectorAll(sel)].filter((el) => !picture(el) && rendered(el) && !el.disabled && !el.readOnly);
    fields.forEach((el, i) => el.setAttribute('data-sb-type', String(i)));
    return fields.length;
  });
  const out = { fields: n, shown: [], small: [] };
  for (let i = 0; i < n; i++) {
    const was = await page.evaluate((i) => {
      const f = document.querySelector(`[data-sb-type="${i}"]`); const st = f.closest('[data-specimen]');
      st.querySelectorAll(window.__sb.CONTROLS).forEach((c) => c.setAttribute('data-sb-was', window.__sb.rendered(c) ? '1' : '0'));
      return f.value;
    }, i);
    const loc = page.locator(`[data-sb-type="${i}"]`);
    await loc.scrollIntoViewIfNeeded();
    await loc.focus();
    await page.keyboard.press('End');
    await page.keyboard.type('a');
    await page.waitForTimeout(150);
    const r = await page.evaluate((i) => {
      const { rendered, desc } = window.__sb;
      const st = document.querySelector(`[data-sb-type="${i}"]`).closest('[data-specimen]');
      const shown = [], small = [];
      for (const c of st.querySelectorAll('[data-sb-was="0"]')) {
        if (!rendered(c) || !c.querySelector('[data-icon]')) continue;
        const b = c.getBoundingClientRect(); const w = Math.round(b.width * 10) / 10, h = Math.round(b.height * 10) / 10;
        shown.push({ ...desc(c), w, h });
        if (b.width < 43.5 || b.height < 43.5) small.push({ ...desc(c), icon: c.querySelector('[data-icon]').getAttribute('data-icon'), w, h, after: 'typing one letter' });
      }
      st.querySelectorAll('[data-sb-was]').forEach((c) => c.removeAttribute('data-sb-was'));
      return { shown, small };
    }, i);
    out.shown.push(...r.shown); out.small.push(...r.small);
    await loc.fill(was);
    await page.waitForTimeout(100);
  }
  await page.evaluate(() => { document.querySelectorAll('[data-sb-type]').forEach((el) => el.removeAttribute('data-sb-type')); if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); window.scrollTo(0, 0); });
  return out;
}

// DR-203 (stage C): the code a builder copies draws what the guide shows. Each code plate's panels are read as Copy
// gives them, pasted into a page that holds the brand's fonts, tokens.css (as the page's own download carries it) and
// body { margin: 0; font: var(--oa-type-body) }, at the same place on the screen as the live stage, and both are
// captured. The masthead and rail are hidden while the guide is captured, so nothing overlaps a stage.
// Round 1 (D2-1470): codeMatch runs on a fresh page, so no earlier check's hover, focus or scroll leaves a trace. A stage
// taller than the window is captured whole: the window grows to hold it, its top is scrolled to a whole pixel, and the
// pasted page sets the same fractional offset on both axes, so both captures fall on the same sub-pixel phase (of five
// phases tried on the tall stages, the measured one matched best every time). What may still differ, measured on the 56
// live stages of the newest build at 1440 and 390 px:
//   antialiasing on curved and diagonal edges, up to 49 of 255: a pixel may differ by EDGE_TOL or less where the guide's
//     own capture has an edge there (in its 3 by 3 neighbourhood some channel spans EDGE_SPAN or more: a red edge against
//     a dark keyline can span 160 in red and under 48 in luminance);
//   the capture's outer ring of pixels, which a stage ending between two pixels blends with whatever lies outside it;
//   a straight edge rounded one device pixel the other way deep in a 9 MB page, where Chromium's positions lose sub-pixel
//     precision: up to EDGE_ROWS whole rows or columns whose pixels match the other capture one pixel up, down or across.
// Anything else is drift: a larger difference on a flat area, more shifted rows, or a different size.
const EDGE_TOL = 64;
const EDGE_SPAN = 48;
const EDGE_ROWS = 4;
async function codeMatch(page) {
  const plates = await page.evaluate(() => [...document.querySelectorAll('.plate--code[data-code-set]')].map((f) => {
    const text = (lang) => { const pre = f.querySelector(`.code-panel[data-code-lang="${lang}"] pre`); return pre ? pre.textContent : null; };
    return { set: f.getAttribute('data-code-set'), html: text('html'), css: text('css'), js: text('js'),
      themes: [...f.querySelectorAll('.code-stage .code-root')].map((r) => r.closest('.code-stage').getAttribute('data-code-theme')) };
  }));
  const out = { plates: plates.length, stages: 0, results: [], bad: [], tolerance: { edge: EDGE_TOL, span: EDGE_SPAN, rows: EDGE_ROWS } };
  if (!plates.length) return out;
  const env = await page.evaluate(() => {
    const a = document.getElementById('tokens-download'); const href = a ? a.getAttribute('href') : '';
    const b64 = href.split(',')[1] || '';
    const tokens = b64 ? new TextDecoder().decode(Uint8Array.from(atob(b64), (c) => c.charCodeAt(0))) : '';
    const fonts = [...document.querySelectorAll('link[rel="stylesheet"]')].map((l) => l.href).filter((h) => /fonts\.googleapis/.test(h));
    return { tokens, fonts };
  });
  if (!env.tokens) { out.bad.push({ set: '*', why: 'the page carries no tokens.css download to paste beside the code' }); return out; }
  const hide = await page.addStyleTag({ content: '.masthead, .rail { visibility: hidden !important } html { scroll-behavior: auto !important }' });
  await page.mouse.move(0, 0);
  await page.evaluate(() => { if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); });
  const vp = page.viewportSize();
  const harness = await page.context().newPage();
  for (const pl of plates) {
    for (const theme of pl.themes) {
      const sel = `.plate--code[data-code-set="${pl.set}"] .code-stage[data-code-theme="${theme}"] .code-root`;
      const h = await page.evaluate((sel) => Math.ceil(document.querySelector(sel).getBoundingClientRect().height), sel);
      const tall = h + 96 > vp.height;
      if (tall) { await page.setViewportSize({ width: vp.width, height: h + 96 }); await page.waitForTimeout(400); }
      const box = await page.evaluate((sel) => {
        const r = document.querySelector(sel);
        // the stage's top 48 px under the window's top, on a whole scroll position
        const top = r.getBoundingClientRect().top + window.scrollY;
        window.scrollTo(0, Math.max(0, Math.floor(top) - 48));
        const b = r.getBoundingClientRect();
        return { x: b.left, y: b.top, w: b.width, h: b.height };
      }, sel);
      await page.waitForTimeout(60);
      const a = await page.locator(sel).screenshot();
      const fx = ((box.x % 1) + 1) % 1, fy = ((box.y % 1) + 1) % 1;
      await harness.setViewportSize(tall ? { width: vp.width, height: h + 96 } : vp);
      const js = pl.js ? `<script>${pl.js}<\/script>` : '';
      await harness.setContent(`<!doctype html><html lang="en" data-oa-theme="${theme}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">`
        + env.fonts.map((u) => `<link rel="stylesheet" href="${u}">`).join('') + `<style>${env.tokens}</style><style>body { margin: 0; font: var(--oa-type-body) }</style>`
        + `<style>${pl.css || ''}</style></head><body><div id="oa-harness" style="display:flow-root;width:${box.w}px;margin:${48 + fy}px 0 0 ${Math.floor(box.x) + fx}px">${pl.html || ''}</div>${js}</body></html>`, { waitUntil: 'networkidle' });
      await harness.evaluate(() => document.fonts.ready);
      await harness.mouse.move(0, 0);
      const b = await harness.locator('#oa-harness').screenshot();
      if (tall) { await page.setViewportSize(vp); await page.waitForTimeout(150); }
      out.stages++;
      if (Buffer.compare(a, b) === 0) { out.results.push({ set: pl.set, theme, same: true, w: Math.round(box.w), h: Math.round(box.h), tall }); continue; }
      const d = await harness.evaluate(async ([x64, y64, tol, span]) => {
        const load = (s) => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = 'data:image/png;base64,' + s; });
        const [x, y] = await Promise.all([load(x64), load(y64)]);
        if (x.width !== y.width || x.height !== y.height) return { size: `${x.width} by ${x.height} in the guide, ${y.width} by ${y.height} pasted` };
        const W = x.width, H = x.height;
        const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d', { willReadFrequently: true });
        g.drawImage(x, 0, 0); const dx = g.getImageData(0, 0, W, H).data;
        g.clearRect(0, 0, W, H); g.drawImage(y, 0, 0); const dy = g.getImageData(0, 0, W, H).data;
        const near = (i, j) => Math.max(Math.abs(dx[i] - dy[j]), Math.abs(dx[i + 1] - dy[j + 1]), Math.abs(dx[i + 2] - dy[j + 2])) <= tol;
        let n = 0, max = 0, flat = 0, big = 0, ring = 0, firstOff = null;
        const rows = new Set(), cols = new Set();
        for (let py = 0; py < H; py++) for (let px = 0; px < W; px++) {
          const i = (py * W + px) * 4;
          const m = Math.max(Math.abs(dx[i] - dy[i]), Math.abs(dx[i + 1] - dy[i + 1]), Math.abs(dx[i + 2] - dy[i + 2]));
          if (!m) continue;
          n++; if (m > max) max = m;
          if (px === 0 || py === 0 || px === W - 1 || py === H - 1) { ring++; continue; }
          if (m > tol) {
            if (near(i, i - W * 4) || near(i, i + W * 4)) { rows.add(py); continue; }
            if (near(i, i - 4) || near(i, i + 4)) { cols.add(px); continue; }
          }
          // an edge is where any channel changes across the 3 by 3 neighbourhood: Pillar Red against its Charcoal keyline
          // spans 160 in red and only 43 in luminance (the tracker's take-part disc at 360 px, round 1 final check)
          const lo = [255, 255, 255], hi = [0, 0, 0];
          for (let oy = -1; oy <= 1; oy++) for (let ox = -1; ox <= 1; ox++) {
            const qx = px + ox, qy = py + oy; if (qx < 0 || qy < 0 || qx >= W || qy >= H) continue;
            const k = (qy * W + qx) * 4;
            for (let c = 0; c < 3; c++) { if (dx[k + c] < lo[c]) lo[c] = dx[k + c]; if (dx[k + c] > hi[c]) hi[c] = dx[k + c]; }
          }
          const edge = Math.max(hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]);
          if (m > tol) { big++; if (!firstOff) firstOff = { x: px, y: py, by: m }; }
          else if (edge < span) { flat++; if (!firstOff) firstOff = { x: px, y: py, by: m, flat: true }; }
        }
        return { pixels: n, max, total: W * H, flat, big, ring, shiftedRows: rows.size, shiftedCols: cols.size, firstOff };
      }, [a.toString('base64'), b.toString('base64'), EDGE_TOL, EDGE_SPAN]);
      const edgesOnly = !d.size && d.big === 0 && d.flat === 0 && d.shiftedRows <= EDGE_ROWS && d.shiftedCols <= EDGE_ROWS;
      out.results.push({ set: pl.set, theme, same: false, edgesOnly, tall, ...d });
      if (!edgesOnly) out.bad.push({ set: pl.set, theme, why: d.size ? `draws ${d.size}` : `${d.pixels} of ${d.total} pixels differ, by up to ${d.max} of 255; ${d.big} by more than ${EDGE_TOL} off an edge shift, ${d.flat} on a flat area, ${d.shiftedRows} row(s) and ${d.shiftedCols} column(s) a pixel apart; first at ${JSON.stringify(d.firstOff)}` });
    }
  }
  await harness.close();
  await hide.evaluate((el) => el.remove());
  return out;
}

// codeMatch on a page of its own, loaded fresh (D2-1470)
async function codeMatchFresh(ctx, file) {
  const page = await ctx.newPage();
  await page.goto('file://' + file, { waitUntil: 'load' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});   // the fonts' requests may linger; the page itself has loaded
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const r = await codeMatch(page);
  await page.close();
  return r;
}

// D2-1133 (stage C): the guide forces light under tokens.css's dark theme (DR-204). The page is read once with the
// device set to light, then again with it set to dark; every element must compute the same. The light reading stays in
// the page, so only the differences cross back.
const DARK_PROPS = ['color', 'background-color', 'background-image', 'border-top-color', 'border-right-color', 'border-bottom-color',
  'border-left-color', 'outline-color', 'text-decoration-color', 'fill', 'stroke', 'stop-color', 'box-shadow', 'color-scheme', 'caret-color', 'accent-color'];
async function lightOnDark(page) {
  const read = () => page.evaluate((props) => {
    const els = [document.documentElement, ...document.querySelectorAll('body, body *')];
    return els.map((el) => { const cs = getComputedStyle(el); return props.map((k) => cs.getPropertyValue(k)).join('|'); });
  }, DARK_PROPS);
  await page.emulateMedia({ colorScheme: 'light' });
  await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
  await page.evaluate((props) => {
    const els = [document.documentElement, ...document.querySelectorAll('body, body *')];
    window.__oaLight = els.map((el) => { const cs = getComputedStyle(el); return props.map((k) => cs.getPropertyValue(k)).join('|'); });
  }, DARK_PROPS);
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => r())));
  const r = await page.evaluate((props) => {
    const els = [document.documentElement, ...document.querySelectorAll('body, body *')];
    const light = window.__oaLight || [];
    const de = document.documentElement;
    const out = { elements: els.length, attribute: de.getAttribute('data-oa-theme'), scheme: getComputedStyle(de).colorScheme,
      dark: matchMedia('(prefers-color-scheme: dark)').matches, changed: [] };
    if (light.length !== els.length) { out.changed.push({ where: 'page', why: `element count ${light.length} with the device light, ${els.length} dark` }); return out; }
    const where = (el) => { const st = el.closest && el.closest('[data-specimen]'); const sec = el.closest && el.closest('section[id]'); return st ? st.getAttribute('data-specimen') : sec ? '#' + sec.id : el.tagName.toLowerCase(); };
    for (let i = 0; i < els.length; i++) {
      const cs = getComputedStyle(els[i]); const now = props.map((k) => cs.getPropertyValue(k));
      const was = light[i].split('|');
      const k = now.findIndex((v, j) => v !== was[j]);
      if (k >= 0) out.changed.push({ where: where(els[i]), el: els[i].tagName.toLowerCase() + (els[i].className && typeof els[i].className === 'string' ? '.' + els[i].className.split(' ')[0] : ''), prop: props[k], light: was[k].slice(0, 60), dark: now[k].slice(0, 60) });
    }
    delete window.__oaLight;
    return out;
  }, DARK_PROPS);
  await page.emulateMedia({ colorScheme: 'light' });
  return r;
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
  if (b.forced && b.forced.wordmark && b.forced.wordmark.length) add('forcedWordmark', `the masthead wordmark draws in more than one color under forced colors (CA-S16), first: ${first(b.forced.wordmark)}`);
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
  // Stage C: the walk starts from the top of the page whatever ran before it. A blur alone leaves Chromium's sequential
  // focus starting point where an earlier check left it (codeMatch's captures left it in a code stage), so a mark at the
  // start of the body takes focus first and goes once the first Tab has left it.
  await page.evaluate(() => {
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    const start = document.createElement('span'); start.id = 'oa-focus-start'; start.tabIndex = -1;
    document.body.prepend(start); start.focus({ preventScroll: true }); window.scrollTo(0, 0);
  });
  for (let i = 0; i < stops; i++) {
    await page.keyboard.press('Tab');
    if (i === 0) await page.evaluate(() => { const s = document.getElementById('oa-focus-start'); if (s) s.remove(); });
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

// ------------------------------------------------------------------------------------------------ stage C, round 1
// Three checks the round 0 notes planned (November 11, 2026, guide engineer).
//
// keyPath    Each code set's keyboard path, from <set>.keys.json (format oa-keys/1, the accessibility lead's chapter 18
//            notes), walked in each live stage at 1440 and 390 px: a fresh page per path, focus on a stand-in control
//            just before the stage, then each step's key or typed words, and after it the focus, states and status
//            words the step names. The first step that does not hold fails the path.
// motionPlay Every moving specimen, marked data-oa-motion (round 0's contract; chapter 17 builds to it), outside a
//            failure plate: nothing moves on load; it has Play, Pause and Reset (data-oa-play, data-oa-pause,
//            data-oa-reset, one button may carry two); after Play it comes to rest, so nothing loops; and with reduced
//            motion on, in a run of its own, Play shows the final frame at once and nothing after it moves, with every
//            animation at 0 ms.
// tokenTable Chapter 26's table (s-26-token-table) against tokens.json: one row per token, the file's count and version,
//            every CSS name defined on the page's root, and every swatch drawn in the hex its row prints.
const CODE_DIRS = [path.join(ROOT, 'work/build/guide/code'), path.join(ROOT, 'work/build/guide/shell/fixtures/code')];
const TOKENS_JSON = path.join(ROOT, 'work/build/tokens/tokens.json');
const KEY_WIDTHS = [1440, 390];

function keysFor(set) {
  for (const d of CODE_DIRS) {
    const f = path.join(d, `${set}.keys.json`);
    if (fs.existsSync(f)) {
      try { return { file: f, data: JSON.parse(fs.readFileSync(f, 'utf8')) }; } catch (e) { return { file: f, error: String(e.message || e) }; }
    }
  }
  return null;
}

function tokenFacts() {
  try {
    const t = JSON.parse(fs.readFileSync(TOKENS_JSON, 'utf8'));
    let n = 0;
    const walk = (o) => { if (o && typeof o === 'object') { if ('$value' in o) { n++; return; } for (const [k, v] of Object.entries(o)) if (!k.startsWith('$')) walk(v); } };
    walk(t);
    const x = (t.$extensions || {})['org.oathandaction'] || {};
    return { count: n, version: x.tokenSetVersion || x.version || null };
  } catch (e) { return null; }
}

// One step's checks, read inside the page: focus, states and the status line's words.
const KEY_STEP_READ = ({ stageSel, step }) => {
  const stage = document.querySelector(stageSel);
  const out = [];
  if (!stage) return ['the live stage is not on the page'];
  const words = (el) => (el ? el.textContent : '').replace(/\s+/g, ' ').trim();
  const pick = (sel) => (sel === '' || sel == null) ? stage : /^:root/.test(sel) ? document.querySelector(sel) : stage.querySelector(sel);
  const active = document.activeElement;
  const where = active ? (active.tagName.toLowerCase() + (active.className && typeof active.className === 'string' ? '.' + active.className.split(' ').join('.') : '') + (active.textContent ? ' "' + words(active).slice(0, 30) + '"' : '')) : 'nothing';
  if (step.focus === 'outside') { if (active && stage.contains(active)) out.push(`focus stayed inside the stage, on ${where}`); }
  else if (step.focus) {
    let hit = false;
    try { hit = [...stage.querySelectorAll(step.focus)].includes(active); } catch (e) { out.push(`the focus selector ${step.focus} does not parse`); }
    if (!hit) out.push(`focus is on ${where}, not ${step.focus}`);
  }
  for (const s of step.states || []) {
    if (s.storage) { let v = null; try { v = localStorage.getItem(s.storage); } catch (e) { v = null; } if (v !== s.is) out.push(`storage ${s.storage} holds ${JSON.stringify(v)}, not ${JSON.stringify(s.is)}`); continue; }
    let el = null;
    try { el = pick(s.el); } catch (e) { out.push(`the selector ${s.el} does not parse`); continue; }
    if (!el) { out.push(`no element ${s.el} in the stage`); continue; }
    // "present" asks only whether the attribute is there (a prefixed id differs by theme); "above" and "below" bound a
    // number (a scroll position has no fixed value). The accessibility lead's oa-keys/1 fields.
    if ('attr' in s) {
      const v = el.getAttribute(s.attr);
      if ('present' in s && (v !== null) !== !!s.present) out.push(`${s.el || 'the stage'} ${v !== null ? 'has' : 'lacks'} ${s.attr}${s.present ? '' : ', which it should lack'}`);
      if ('is' in s && v !== s.is) out.push(`${s.el || 'the stage'} has ${s.attr}=${JSON.stringify(v)}, not ${JSON.stringify(s.is)}`);
    }
    if ('prop' in s) {
      const v = el[s.prop];
      if ('is' in s && v !== s.is) out.push(`${s.el || 'the stage'}.${s.prop} is ${JSON.stringify(v)}, not ${JSON.stringify(s.is)}`);
      if ('above' in s && !(v > s.above)) out.push(`${s.el || 'the stage'}.${s.prop} is ${JSON.stringify(v)}, not above ${s.above}`);
      if ('below' in s && !(v < s.below)) out.push(`${s.el || 'the stage'}.${s.prop} is ${JSON.stringify(v)}, not below ${s.below}`);
    }
    if ('text' in s) { const v = words(el); if (v !== s.text) out.push(`${s.el || 'the stage'} says "${v.slice(0, 80)}", not "${s.text}"`); }
    if ('visible' in s) {
      const r = el.getBoundingClientRect(); let shown = r.width > 0 || r.height > 0;
      for (let e = el; e && e.nodeType === 1 && shown; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') shown = false; }
      if (shown !== s.visible) out.push(`${s.el} is ${shown ? 'shown' : 'hidden'}, not ${s.visible ? 'shown' : 'hidden'}`);
    }
  }
  if ('status' in step || 'status_has' in step) {
    let line = null;
    try { line = step.status_el ? stage.querySelector(step.status_el) : stage.querySelector('[role="status"]'); } catch (e) { line = null; }
    if (!line) out.push(`no status line ${step.status_el || '[role="status"]'} in the stage`);
    else {
      const v = words(line);
      if ('status' in step && v !== (step.status == null ? '' : step.status)) out.push(`the status line says "${v.slice(0, 90)}", not "${step.status == null ? '' : step.status}"`);
      if ('status_has' in step && !v.includes(step.status_has)) out.push(`the status line says "${v.slice(0, 90)}", without "${step.status_has}"`);
    }
  }
  return out;
};

async function keyPaths(browser, file, widths, opts = {}) {
  const probe = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const pg = await probe.newPage();
  await pg.goto('file://' + file, { waitUntil: 'load' });
  const sets = await pg.evaluate(() => [...document.querySelectorAll('.plate--code[data-code-set]')].map((f) => ({ set: f.getAttribute('data-code-set'), themes: [...f.querySelectorAll('.code-stage[data-code-theme]')].map((s) => s.getAttribute('data-code-theme')) })));
  await probe.close();
  const out = { sets: sets.length, withKeys: 0, paths: 0, walks: 0, steps: 0, missing: [], problems: [] };
  for (const { set, themes } of sets) {
    const k = keysFor(set);
    if (!k) { out.missing.push(set); continue; }
    if (k.error || !k.data || k.data.format !== 'oa-keys/1' || !Array.isArray(k.data.paths)) { out.problems.push({ set, why: `${path.relative(ROOT, k.file)} is not an oa-keys/1 file${k.error ? ': ' + k.error : ''}` }); continue; }
    out.withKeys++;
    for (const p of k.data.paths) {
      out.paths++;
      const setup = p.setup || {};
      for (const width of widths.filter((w) => !p.widths || p.widths.includes(w))) {
        const ctx = await browser.newContext({ viewport: { width, height: { 1440: 900, 390: 844 }[width] || 900 }, deviceScaleFactor: 1,
          reducedMotion: setup.reducedMotion ? 'reduce' : 'no-preference', colorScheme: setup.colorScheme === 'dark' ? 'dark' : 'light' });
        if (setup.clipboard === 'allow') await ctx.grantPermissions(['clipboard-read', 'clipboard-write']);
        const page = await ctx.newPage();
        if (setup.clipboard === 'deny') {
          await page.addInitScript(() => {
            const no = () => Promise.reject(Object.assign(new Error('Write permission denied.'), { name: 'NotAllowedError' }));
            try { Object.defineProperty(navigator, 'clipboard', { value: { writeText: no, write: no, readText: no }, configurable: true }); } catch (e) { /* the page keeps its own */ }
          });
        }
        await page.goto('file://' + file, { waitUntil: 'load' });
        await page.evaluate(() => document.fonts.ready);
        if (opts.mutate) await page.evaluate(opts.mutate);
        for (const theme of themes.filter((t) => !p.themes || p.themes.includes(t))) {
          const stageSel = `.plate--code[data-code-set="${set}"] .code-stage[data-code-theme="${theme}"]`;
          const ok = await page.evaluate((sel) => {
            const st = document.querySelector(sel); if (!st) return false;
            document.querySelectorAll('.oa-keys-start').forEach((b) => b.remove());
            const b = document.createElement('button'); b.type = 'button'; b.className = 'oa-keys-start'; b.textContent = 'Start of the keyboard path';
            st.parentNode.insertBefore(b, st); b.scrollIntoView({ block: 'center' }); b.focus();
            return document.activeElement === b;
          }, stageSel);
          out.walks++;
          if (!ok) { out.problems.push({ set, path: p.name, theme, width, step: 0, why: 'the stand-in control before the stage could not take focus' }); continue; }
          let i = 0;
          for (const step of p.steps || []) {
            i++; out.steps++;
            if (step.type != null) await page.keyboard.type(String(step.type), { delay: 20 });
            if (step.key) await page.keyboard.press(step.key === 'Space' ? ' ' : step.key);
            await page.waitForTimeout(typeof step.wait === 'number' ? step.wait : 150);
            const bad = await page.evaluate(KEY_STEP_READ, { stageSel, step });
            if (bad.length) { out.problems.push({ set, path: p.name, theme, width, step: i, key: step.key || `type "${step.type}"`, why: bad.join('; ') }); break; }
          }
        }
        await ctx.close();
      }
    }
  }
  return out;
}

// The drawn state of a moving specimen: each SVG shape outside its controls, as the browser draws it now.
const MOTION_STATE = (el) => [...el.querySelectorAll('svg *')].filter((x) => !x.closest('button, label, input, [data-oa-still]')).map((x) => {
  const cs = getComputedStyle(x);
  const at = ['transform', 'x', 'y', 'width', 'height', 'd', 'points', 'cx', 'cy', 'r', 'x1', 'y1', 'x2', 'y2', 'style'].map((a) => x.getAttribute(a) || '').join('|');
  return [cs.transform, cs.opacity, cs.strokeDashoffset, cs.visibility, cs.display, at].join('/');
}).join('\n');

async function motionAudit(browser, file, opts = {}) {
  const out = { players: 0, failurePlates: 0, problems: [], reduced: [] };
  const open = async (reduced) => {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, reducedMotion: reduced ? 'reduce' : 'no-preference' });
    const page = await ctx.newPage();
    await page.goto('file://' + file, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    if (opts.mutate) await page.evaluate(opts.mutate);
    return { ctx, page };
  };
  for (const reduced of [false, true]) {
    const { ctx, page } = await open(reduced);
    const list = await page.$$('[data-oa-motion]');
    const players = [];
    for (const h of list) {
      const info = await h.evaluate((el) => { const st = el.closest('[data-specimen]'); return { where: st ? st.getAttribute('data-specimen') : ((el.closest('section[id]') || {}).id || 'page'), failure: !!el.closest('.plate--failure'), nested: !!(el.parentElement && el.parentElement.closest('[data-oa-motion]')) }; });
      if (info.nested) continue;
      if (info.failure) { if (!reduced) out.failurePlates++; continue; }
      players.push({ h, where: info.where });
    }
    if (!reduced) out.players = players.length;
    for (const { h, where } of players) {
      await h.evaluate((el) => el.scrollIntoView({ block: 'center' }));
      const ctl = await h.evaluate((el) => {
        const scope = el.closest('[data-specimen]') || el;
        const q = (a) => el.querySelector(`[${a}]`) || scope.querySelector(`[${a}]`);
        return { play: !!q('data-oa-play'), pause: !!q('data-oa-pause'), reset: !!q('data-oa-reset') };
      });
      const s0 = await h.evaluate(MOTION_STATE);
      if (!reduced) {
        const missing = Object.entries(ctl).filter(([, v]) => !v).map(([k]) => k);
        if (missing.length) out.problems.push({ where, why: `no ${missing.join(', ')} control; a moving specimen has Play, Pause and Reset` });
        await page.waitForTimeout(400);
        const running = await h.evaluate((el) => el.getAnimations({ subtree: true }).filter((a) => a.playState === 'running').length);
        if (running || (await h.evaluate(MOTION_STATE)) !== s0) out.problems.push({ where, why: `it moves on load${running ? ` (${running} animation(s) running)` : ''}; motion plays only on request` });
        // chapter 17's players say where they stand in data-frame: "start" on load
        const f0 = await h.evaluate((el) => el.getAttribute('data-frame'));
        if (f0 !== null && f0 !== 'start') out.problems.push({ where, why: `data-frame is "${f0}" on load, not "start"` });
      }
      if (!ctl.play) continue;
      const play = await h.evaluateHandle((el) => el.querySelector('[data-oa-play]') || (el.closest('[data-specimen]') || el).querySelector('[data-oa-play]'));
      await play.asElement().click();
      if (reduced) {
        await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
        const s1 = await h.evaluate(MOTION_STATE);
        const long = await h.evaluate((el) => el.getAnimations({ subtree: true }).map((a) => a.effect && a.effect.getComputedTiming()).filter((t) => t && t.duration > 0 && t.duration !== Infinity).map((t) => Math.round(t.duration)));
        const after = await h.evaluate((el) => ({ frame: el.getAttribute('data-frame'), running: el.getAnimations({ subtree: true }).filter((a) => a.playState === 'running').length }));
        await page.waitForTimeout(1000);
        const s2 = await h.evaluate(MOTION_STATE);
        const why = [];
        if (s1 === s0) why.push('Play draws nothing new on the first frame');
        if (s2 !== s1) why.push('it keeps moving after the first frame');
        if (long.length) why.push(`animation(s) of ${[...new Set(long)].join(', ')} ms`);
        if (after.running) why.push(`${after.running} animation(s) still running`);
        if (after.frame !== null && after.frame !== 'end') why.push(`data-frame is "${after.frame}", not "end"`);
        out.reduced.push({ where, finalAtOnce: !why.length });
        if (why.length) out.problems.push({ where, why: `with reduced motion on: ${why.join('; ')}; Play shows the final frame at once` });
      } else {
        await page.waitForTimeout(2500);
        const a = await h.evaluate(MOTION_STATE);
        await page.waitForTimeout(600);
        const b = await h.evaluate(MOTION_STATE);
        const loops = await h.evaluate((el) => el.getAnimations({ subtree: true }).filter((x) => x.playState === 'running' && x.effect && x.effect.getComputedTiming().iterations === Infinity).length);
        if (a !== b || loops) out.problems.push({ where, why: `it still moves 2.5 s after Play${loops ? ` (${loops} endless animation(s))` : ''}; nothing loops` });
      }
    }
    await ctx.close();
  }
  return out;
}

// Chapter 26's table against tokens.json, read once at the first width.
async function tokenTable(page) {
  const facts = tokenFacts();
  const r = await page.evaluate(() => {
    const st = document.querySelector('[data-specimen="s-26-token-table"]');
    if (!st) return null;
    const tt = st.querySelector('.tt');
    const rows = [...st.querySelectorAll('tbody tr')].filter((tr) => !tr.classList.contains('tt-g'));
    const root = getComputedStyle(document.documentElement);
    const undef = [], off = [];
    const probe = document.createElement('span'); document.body.append(probe);
    let swatches = 0;
    for (const tr of rows) {
      const name = (tr.querySelector('code.tt-c') || {}).textContent || '';
      if (!root.getPropertyValue(name).trim()) undef.push(name);
      const sw = tr.querySelector('.tt-sw'); const v = tr.querySelector('.tt-v');
      if (sw && v) {
        swatches++;
        const hex = (v.textContent.match(/#[0-9A-Fa-f]{6}/) || [''])[0];
        probe.style.color = hex; const want = getComputedStyle(probe).color; const got = getComputedStyle(sw).backgroundColor;
        if (!hex || want !== got) off.push({ name, printed: hex, drawn: got });
      }
    }
    probe.remove();
    return { rows: rows.length, count: tt ? Number(tt.getAttribute('data-token-count')) : null, version: tt ? tt.getAttribute('data-token-version') : null, swatches, undef: undef.slice(0, 10), undefCount: undef.length, off: off.slice(0, 10), offCount: off.length };
  });
  if (!r) return null;
  r.file = facts;
  r.problems = [];
  if (!facts) r.problems.push('tokens.json could not be read');
  else {
    if (r.rows !== facts.count || r.count !== facts.count) r.problems.push(`${r.rows} rows (data-token-count ${r.count}) where tokens.json holds ${facts.count} tokens`);
    if (r.version !== facts.version) r.problems.push(`the table says version ${r.version}, tokens.json ${facts.version}`);
  }
  if (r.undefCount) r.problems.push(`${r.undefCount} CSS name(s) the page's root does not define, first: ${r.undef.join(', ')}`);
  if (r.offCount) r.problems.push(`${r.offCount} swatch(es) drawn in another color than their printed hex, first: ${JSON.stringify(r.off[0])}`);
  return r;
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
    // Round 1: the page's own load event first. At 9 MB the parser outlasts the network's 500 ms of quiet, so networkidle
    // alone hands the checks a page whose last chapters are not yet in the DOM; then the fonts and other requests settle.
    await page.goto('file://' + file, { waitUntil: 'load' });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});   // the fonts' requests may linger; the page itself has loaded
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);
    if (opts.mutate) await page.evaluate(opts.mutate);
    const a = await audit(page);
    // D2-975: no U+2011 in the page's text or names
    a.nbHyphen = await page.evaluate(() => {
      const hits = []; const where = (el) => { const st = el && el.closest && el.closest('[data-specimen]'); const sec = el && el.closest && el.closest('section[id]'); return st ? st.getAttribute('data-specimen') : sec ? '#' + sec.id : (el && el.tagName || '').toLowerCase(); };
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n = w.nextNode(); n; n = w.nextNode()) {
        if (!n.textContent.includes('\u2011')) continue;
        const el = n.parentElement; if (el && el.closest('script, style')) continue;
        hits.push({ where: where(el), in: 'text', text: n.textContent.trim().slice(0, 50) });
      }
      for (const el of document.querySelectorAll('[alt], [title], [aria-label], [aria-description], [placeholder], [data-frame-name], [aria-roledescription]')) {
        for (const k of ['alt', 'title', 'aria-label', 'aria-description', 'placeholder', 'data-frame-name', 'aria-roledescription']) {
          const v = el.getAttribute(k); if (v && v.includes('\u2011')) hits.push({ where: where(el), in: k, text: v.slice(0, 50) });
        }
      }
      if (document.title.includes('\u2011')) hits.push({ where: 'title', in: 'title', text: document.title.slice(0, 50) });
      return hits;
    });
    a.idsHeld = await page.evaluate(() => [...document.querySelectorAll('span.nw')].filter((x) => /^(?:CL|R|U|S|E)-\w/.test(x.textContent)).length);
    // D2-965, D2-1134: an opener sits in the chapter head, before the first rule, whole in its frame
    a.openers = await page.evaluate(() => [...document.querySelectorAll('.plate--opener')].map((f) => {
      const box = f.querySelector('.plate-scroll'); const st = f.querySelector('.plate-stage');
      const ch = f.closest('.chapter'); const rule = ch && ch.querySelector('.rule');
      const inHead = !!f.closest('.ch-head') && (!rule || (f.compareDocumentPosition(rule) & Node.DOCUMENT_POSITION_FOLLOWING) > 0);
      return { specimen: st ? st.getAttribute('data-specimen') : null, chapter: ch ? ch.id : null, inHead, scrolls: box ? box.scrollWidth > box.clientWidth + 1 : null };
    }));
    // DR-203: the code a builder copies draws what the guide shows
    a.code = opts.mutate ? await codeMatch(page) : await codeMatchFresh(ctx, file);   // a plant changes this page, so it runs here
    // D2-1133: the guide stays light with the device set to dark
    const dk = await lightOnDark(page);
    a.lightOnDark = { elements: dk.elements, attribute: dk.attribute, scheme: dk.scheme, deviceDark: dk.dark, changed: dk.changed.length, first: dk.changed.slice(0, 5) };
    // DR-179, DR-209: the 41 switch at 24 px; at this run's scale, 1x, the fit shows
    const failsSwitch = [];
    a.fitSwitch = await fitSwitch(page, 1);
    if (a.fitSwitch.problems.length) failsSwitch.push({ key: 'fitSwitch', msg: `${width}: ${a.fitSwitch.problems.length} glyph(s) of the 41 at 24 px off the 1x and 2x switch (DR-179, DR-209), first: ${JSON.stringify(a.fitSwitch.problems[0])}` });
    // round 1: chapter 26's table against tokens.json, once
    if (width === widths[0]) {
      a.tokenTable = await tokenTable(page);
      if (a.tokenTable) for (const pr of a.tokenTable.problems) failsSwitch.push({ key: 'tokenTable', msg: `${width}: the token table: ${pr}` });
    }
    a.frames = await frameAudit(page);
    a.fit = await fitAudit(page);
    const fails = failuresFrom(a, width);
    fails.push(...failsSwitch);
    const sb = { audit: await sbAudit(page) };
    if (!opts.skipStageB) {
      sb.forced = await sbForced(page);
      if (width === 1440 || opts.plant) sb.reduced = await sbReduced(page);
      // D2-1103 (stage C): phones take the sideways test with text at 200 percent, as 1024 px has since round 3
      if (width <= 390) sb.spacing = await sbSpacing(page, ['spacing', 'zoom'], true);
      else if (width === 1024 || opts.zoomScroll) sb.spacing = await sbSpacing(page, ['zoom'], true);
      sb.menu = await sbMenu(page);
    }
    fails.push(...sbFailures(sb, width));
    a.stageB = { icons: sb.audit.icons, stateStages: sb.audit.stateStages, statePictures: sb.audit.statePictures, inlineTargets: sb.audit.inlineTargets || 0, missingFamily: sb.audit.missingFamily, markReaders: sb.audit.marks.readers, glyphParts: sb.forced ? sb.forced.glyphParts : null, useParts: sb.forced ? sb.forced.useParts : null,
      menu: sb.menu ? (sb.menu.problems.length ? sb.menu.problems : 'opens, holds focus, closes by Escape and Close, returns focus') : 'not shown at this width',
      forcedWordmark: sb.forced ? (sb.forced.wordmark.length ? sb.forced.wordmark : 'one color in dark and light') : null };
    for (const o of a.openers) {
      if (!o.inHead) fails.push({ key: 'openerFit', msg: `${width}: the opener ${o.specimen} in #${o.chapter} sits outside the chapter head or after a rule (D2-1134)` });
      if (o.scrolls) fails.push({ key: 'openerFit', msg: `${width}: the opener ${o.specimen} in #${o.chapter} scrolls in its frame; an opener fits the column at true size (D2-965)` });
    }
    if (a.code.bad.length) fails.push({ key: 'codeMatch', msg: `${width}: ${a.code.bad.length} live code stage(s) draw differently from the code a builder copies (DR-203), first: ${JSON.stringify(a.code.bad[0])}` });
    if (!dk.dark) fails.push({ key: 'lightOnDark', msg: `${width}: the browser did not take the dark device setting, so the test could not run` });
    if (dk.attribute !== 'light' || !/only/.test(dk.scheme) || !/light/.test(dk.scheme)) fails.push({ key: 'lightOnDark', msg: `${width}: the root reads data-oa-theme=${JSON.stringify(dk.attribute)} and color-scheme "${dk.scheme}"; the guide forces "light" and "only light" (D2-1133)` });
    if (dk.changed.length) fails.push({ key: 'lightOnDark', msg: `${width}: ${dk.changed.length} element(s) change color with the device set to dark; the guide stays light (DR-204, D2-1133), first: ${JSON.stringify(dk.changed[0])}` });
    if (a.nbHyphen.length) fails.push({ key: 'nbHyphen', msg: `${width}: ${a.nbHyphen.length} U+2011 non-breaking hyphen(s) in text or names, which the page's fonts do not draw and a search for the ID misses (D2-975); first: ${JSON.stringify(a.nbHyphen[0])}` });
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
    // CA-M2: last, since it types into live specimens
    if (!opts.skipStageB) {
      const typed = await sbTyped(page);
      if (typed.small.length) report.failures.push({ key: 'iconTargets', msg: `${width}: ${typed.small.length} control(s) that show after typing, holding a glyph under 44 by 44 px (B-1, CA-M2), first: ${JSON.stringify(typed.small[0])}` });
      report.runs[report.runs.length - 1].typed = { fields: typed.fields, shown: typed.shown };
    }
    await ctx.close();
  }
  // DR-179, DR-209 on high-density screens: the master shows alone wherever the switch stands, in a run of its own
  report.hiDpi = [];
  for (const [width, dpr] of (opts.hiDpi || [])) {
    const ctx = await browser.newContext({ viewport: { width, height: { 1440: 900, 390: 844 }[width] || 900 }, deviceScaleFactor: dpr });
    const page = await ctx.newPage();
    await page.goto('file://' + file, { waitUntil: 'load' });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});   // the fonts' requests may linger; the page itself has loaded
    await page.evaluate(() => document.fonts.ready);
    if (opts.mutate) await page.evaluate(opts.mutate);
    const r = await fitSwitch(page, dpr);
    report.hiDpi.push({ width, dpr, glyphs: r.glyphs, pairs: r.pairs, masterShown: r.masterShown, fixed: r.fixed, problems: r.problems.slice(0, 10) });
    if (r.problems.length) report.failures.push({ key: 'fitSwitch', msg: `${width} at ${dpr}x: ${r.problems.length} glyph(s) of the 41 at 24 px off the 1x and 2x switch (DR-179, DR-209), first: ${JSON.stringify(r.problems[0])}` });
    await ctx.close();
  }
  // round 1: each code set's keyboard path, and every moving specimen
  if (opts.keys !== false) {
    const kw = KEY_WIDTHS.filter((w) => widths.includes(w));
    const k = await keyPaths(browser, file, kw.length ? kw : [widths[0]], opts);
    report.keys = { widths: kw, sets: k.sets, withKeys: k.withKeys, paths: k.paths, walks: k.walks, steps: k.steps, missing: k.missing, problems: k.problems.slice(0, 20) };
    const need = k.missing.filter((x) => /^c-18-/.test(x));
    if (need.length) report.failures.push({ key: 'keyPath', msg: `${need.length} chapter 18 code set(s) with no keys file: ${need.join(', ')}` });
    for (const pr of k.problems) report.failures.push({ key: 'keyPath', msg: `${pr.width || ''}${pr.width ? ' ' : ''}${pr.set}${pr.theme ? ' (' + pr.theme + ')' : ''}${pr.path ? ', "' + pr.path + '"' : ''}${pr.step ? ', step ' + pr.step + (pr.key ? ' (' + pr.key + ')' : '') : ''}: ${pr.why}` });
  }
  if (opts.motion !== false) {
    const m = await motionAudit(browser, file, opts);
    report.motion = { players: m.players, failurePlates: m.failurePlates, reduced: m.reduced, problems: m.problems };
    for (const pr of m.problems) report.failures.push({ key: 'motionPlay', msg: `${pr.where}: ${pr.why}` });
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
  { key: 'stateWords', fault: 'a live tracker of three steps whose words name no state (A-5)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-demo-live" role="group" aria-label="A bill"><p>A bill at step 2.</p><svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="48" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g><g data-icon="S-not-yet" data-icon-family="status"><circle cx="83" cy="15" r="12" fill="none" stroke="currentColor" stroke-width="1.5"/></g></svg></div>'); } },
  { key: 'stateWords', fault: 'a live tracker whose words give each step its state, two of them as a range (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-demo-live" role="group" aria-label="A bill"><p>Step 3 of 3: Committee vote. <span class="vh">Steps 1 to 2, Filed and Hearing, done. Step 3 Committee vote now.</span></p><svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-done" data-icon-family="status"><circle cx="48" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="83" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g></svg></div>'); },
    verify: (r) => r.runs[0].stageB.stateStages >= 1 },
  { key: 'stateWords', fault: 'a live tracker whose words give each step its state, two of them as "steps 1 and 2" (round 1; allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-demo-live" role="group" aria-label="A bill"><p>Step 3 of 3: Committee vote. <span class="vh">Steps 1 and 2, Filed and Hearing, done. Step 3 Committee vote now.</span></p><svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-done" data-icon-family="status"><circle cx="48" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="83" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g></svg></div>'); },
    verify: (r) => r.runs[0].stageB.stateStages >= 1 },
  { key: 'stateWords', fault: 'a live tracker whose words give each step its state, three done marks said as "steps 1 and 2 done", one short (A-5)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-demo-live" role="group" aria-label="A bill"><p>Step 4 of 4: Floor vote. <span class="vh">Steps 1 and 2, Filed and Hearing, done. Step 4 Floor vote now.</span></p><svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-done" data-icon-family="status"><circle cx="48" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-done" data-icon-family="status"><circle cx="70" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="83" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g></svg></div>'); }, },
  { key: 'stateWords', fault: 'a live tracker drawn twice, one copy for each screen width with the other hidden, its words giving each state once (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-demo-live" role="group" aria-label="A bill"><p>Step 3 of 3: Committee vote. <span class="vh">Steps 1 to 2, Filed and Hearing, done. Step 3 Committee vote now.</span></p><svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-done" data-icon-family="status"><circle cx="48" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="83" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g></svg><svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false" style="display:none"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-done" data-icon-family="status"><circle cx="48" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="83" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g></svg></div>'); },
    verify: (r) => r.runs[0].stageB.stateStages >= 1 },
  { key: 'stateWords', fault: 'a picture of a tracker whose alt describes shapes only: listed for its owner, not failed (allowed: must not be flagged)', expect: false, js: () => {
    const st = document.querySelector('.plate--correct [data-specimen][role="img"]'); st.setAttribute('aria-label', 'A bill at true size, on a line of three steps: a filled circle, a heavy ring and a fine ring.');
    st.insertAdjacentHTML('beforeend', '<svg class="sx-mk" width="96" height="30" viewBox="0 0 96 30" aria-hidden="true" focusable="false"><g data-icon="S-done" data-icon-family="status"><circle cx="13" cy="15" r="13" fill="currentColor"/></g><g data-icon="S-now" data-icon-family="status"><circle cx="48" cy="15" r="11.5" fill="none" stroke="currentColor" stroke-width="3"/></g><g data-icon="S-not-yet" data-icon-family="status"><circle cx="83" cy="15" r="12" fill="none" stroke="currentColor" stroke-width="1.5"/></g></svg>'); },
    verify: (r) => r.runs[0].stageB.statePictures.length >= 1 },
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
  // round 3 fix pass, November 10, 2026
  { key: 'frameFit', fault: 'a chapter plate 60 px wider than its column at 1440 px, left scrolling though breaking out over the rail would hold it (no resize, CA-S13)', js: () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const box = st.closest('.plate-scroll');
    const w = (box.clientWidth + 60) + 'px'; st.style.setProperty('--w', w); box.style.setProperty('--w', w); } },
  { key: 'frameFit', fault: 'the same plate after a resize: the shell breaks it out over the rail, whole and centered, and hides the rail while it covers it (allowed: must not be flagged)', expect: false, js: async () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const box = st.closest('.plate-scroll');
    const w = (box.clientWidth + 60) + 'px'; st.style.setProperty('--w', w); box.style.setProperty('--w', w);
    window.dispatchEvent(new Event('resize')); await new Promise((r) => setTimeout(r, 400)); },
    verify: (r) => r.runs[0].frames.breakout.some((x) => x.specimen === 's-demo-sheet' && !x.scrolls && x.overlaps && !x.railShown) },
  { key: 'frameFit', fault: 'a frame that breaks out over the rail while the rail stays shown (CA-S13)', js: async () => {
    const st = document.querySelector('[data-specimen="s-demo-sheet"]'); const box = st.closest('.plate-scroll');
    const w = (box.clientWidth + 60) + 'px'; st.style.setProperty('--w', w); box.style.setProperty('--w', w);
    window.dispatchEvent(new Event('resize')); await new Promise((r) => setTimeout(r, 400));
    const css = document.createElement('style'); css.textContent = '.rail.is-covered { visibility: visible !important }'; document.head.append(css); } },
  { key: 'textSpacing', fault: 'part links held on one line at 1024 px, which push the page sideways with text at 200 percent (CA-S17)', widths: [1024], js: () => {
    const css = document.createElement('style'); css.textContent = '.mh-bar, .partnav ul { flex-wrap: nowrap !important } .partnav a { white-space: nowrap }'; document.head.append(css);
    document.querySelector('.partnav ul').insertAdjacentHTML('beforeend', '<li><a href="#top">Symbols and graphics</a></li><li><a href="#top">Applications</a></li><li><a href="#top">Appendix</a></li>'); } },
  { key: 'textSpacing', fault: 'the shell\'s own masthead at 1024 px with text at 200 percent, its part links free to wrap (allowed: must not be flagged)', expect: false, widths: [1024], js: () => {
    document.querySelector('.partnav ul').insertAdjacentHTML('beforeend', '<li><a href="#top">Symbols and graphics</a></li><li><a href="#top">Applications</a></li><li><a href="#top">Appendix</a></li>'); } },
  { key: 'forcedWordmark', fault: 'the masthead wordmark\'s ampersand kept red under forced colors while its letters take a system color (CA-S16)', js: () => {
    const css = document.createElement('style'); css.textContent = '@media (forced-colors: active) { .home .wm { --amp: #E63946 !important } }'; document.head.append(css); } },
  { key: 'iconTargets', fault: 'a search field whose Clear button shows only after typing, at 40 by 40 px (B-1, CA-M2)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-demo-live" role="group" aria-label="A search"><label for="sb-q">Search the symbols</label><span style="display:inline-flex;align-items:center"><input id="sb-q" type="text"><button type="button" id="sb-clr" aria-label="Clear the search" hidden style="display:inline-flex;width:40px;height:40px;align-items:center;justify-content:center"><svg data-icon="U-close" data-icon-family="utility" aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2"/></svg></button></span></div>');
    const q = document.getElementById('sb-q'), c = document.getElementById('sb-clr'); q.addEventListener('input', () => { c.hidden = !q.value; }); } },
  { key: 'iconTargets', fault: 'the same field with its Clear button at 44 by 44 px (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-demo-live" role="group" aria-label="A search"><label for="sb-q">Search the symbols</label><span style="display:inline-flex;align-items:center"><input id="sb-q" type="text"><button type="button" id="sb-clr" aria-label="Clear the search" hidden style="display:inline-flex;width:44px;height:44px;align-items:center;justify-content:center"><svg data-icon="U-close" data-icon-family="utility" aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="24" height="24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2"/></svg></button></span></div>');
    const q = document.getElementById('sb-q'), c = document.getElementById('sb-clr'); q.addEventListener('input', () => { c.hidden = !q.value; }); },
    verify: (r) => r.runs[0].typed && r.runs[0].typed.shown.some((x) => x.label === 'Clear the search' && x.w >= 44) },
  { key: 'nbHyphen', fault: 'an ID written with U+2011 in the page title, which the shell does not rewrite (D2-975)', js: () => { document.title += ' CL\u2011001'; } },
  { key: 'nbHyphen', fault: 'an ID written with U+2011 in a frame\'s name (D2-975)', js: () => { document.querySelector('.plate-scroll').setAttribute('data-frame-name', 'Reforms R\u201101 to R\u201125'); } },
  { key: 'nbHyphen', fault: 'a script that writes an ID with U+2011 into rule text and an alt after load: the shell holds the ID whole in Inter\'s hyphen (allowed: must not be flagged)', expect: false, js: async () => {
    document.querySelector('.rule-text').append(' See CL\u2011001.'); document.querySelector('[data-specimen][role="img"]').setAttribute('aria-label', 'A list of reforms, R\u201101 to R\u201125, at true size.');
    await new Promise((r) => setTimeout(r, 50)); },
    verify: (r) => r.runs[0].idsHeld >= 1 },
  { key: 'nbHyphen', fault: 'an ID written by the build: an ASCII hyphen held whole in span.nw (allowed: must not be flagged)', expect: false, js: () => { document.querySelector('.rule-text').insertAdjacentHTML('beforeend', ' See <span class="nw">CL-001</span>.'); } },
  // stage C, round 0 (November 10, 2026)
  { key: 'codeMatch', fault: 'the shell reaching into a live code stage and narrowing its button, which a copy would not do (DR-203)', js: () => {
    const css = document.createElement('style'); css.textContent = '.code-stage .oa-save-btn { padding-inline: 4px !important }'; document.head.append(css); } },
  { key: 'codeMatch', fault: 'a CSS panel whose copy no longer matches the live stage: the button\'s side padding changed in the copy alone (DR-203)', js: () => {
    const pre = document.querySelector('.code-panel[data-code-lang="css"] pre code'); pre.textContent = pre.textContent.replace('padding: 0 var(--oa-space-300)', 'padding: 0 var(--oa-space-100)'); } },
  { key: 'codeMatch', fault: 'the demo\'s code set as built: the copy draws what the live stages draw in both themes (allowed: must not be flagged)', expect: false, js: () => {},
    verify: (r) => r.runs[0].code && r.runs[0].code.stages === 2 && r.runs[0].code.results.every((x) => x.same) },
  { key: 'openerFit', fault: 'an opener figure 900 px wide, which scrolls in its frame at 1440 px (D2-965)', js: () => {
    const h = document.querySelector('.chapter .ch-head'); h.insertAdjacentHTML('beforeend', '<figure class="plate plate--opener"><div class="plate-head"></div><div class="plate-scroll" data-plate-scroll data-frame-name="Opener" data-width="1400" style="--w:1400px"><div class="plate-stage oa-surface-newsprint" data-specimen="s-demo-opener" data-red="specimen" role="img" aria-label="A wide opening figure, a fixture at true size." style="--w:1400px" data-width="1400"><p>Wide</p></div></div></figure>'); } },
  { key: 'openerFit', fault: 'an opener that flows with the column, in the chapter head (allowed: must not be flagged)', expect: false, js: () => {
    const h = document.querySelector('.chapter .ch-head'); h.insertAdjacentHTML('beforeend', '<figure class="plate plate--opener"><div class="plate-head"></div><div class="plate-scroll" data-plate-scroll data-frame-name="Opener"><div class="plate-stage oa-surface-newsprint" data-specimen="s-demo-opener" data-red="specimen" role="img" aria-label="An opening figure that flows, a fixture."><p>Flows with the column</p></div></div></figure>'); },
    verify: (r) => r.runs[0].openers.length === 1 && r.runs[0].openers[0].inHead },
  { key: 'textSpacing', fault: 'a cover folio held on one line at 390 px, which pushes the page sideways with text at 200 percent (D2-1103)', widths: [390], js: () => {
    const css = document.createElement('style'); css.textContent = '.cover-folio span { white-space: nowrap !important }'; document.head.append(css);
    document.querySelector('.cover-folio span:last-child').textContent = 'Draft of November 7, 2026, for review'; } },
  { key: 'textSpacing', fault: 'a source line holding a long web address at 360 px, with no way to wrap it (D2-1103)', widths: [360], js: () => {
    const css = document.createElement('style'); css.textContent = '.sb-src li { overflow-wrap: normal !important; word-break: normal !important }'; document.head.append(css);
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<ol class="src-list sb-src"><li>Source: https://www.example.org/a-very-long-path/with-no-breaks/at-all-in-it/lawmaking-in-the-state-legislature.html</li></ol>'); } },
  { key: 'textSpacing', fault: 'the same source line in the shell\'s own list, free to wrap (allowed: must not be flagged)', expect: false, widths: [360], js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<ol class="src-list"><li>Source: https://www.example.org/a-very-long-path/with-no-breaks/at-all-in-it/lawmaking-in-the-state-legislature.html</li></ol>'); } },
  { key: 'lightOnDark', fault: 'the root without data-oa-theme="light", so tokens.css follows the device into Charcoal (D2-1133)', js: () => {
    document.documentElement.removeAttribute('data-oa-theme'); } },
  { key: 'lightOnDark', fault: 'a specimen whose own style turns its text pale when the device is dark (DR-204)', js: () => {
    const st = document.querySelector('[data-specimen]:not([data-pending])');
    st.insertAdjacentHTML('beforeend', '<style>@media (prefers-color-scheme: dark) { .sb-dark { color: var(--oa-color-palette-newsprint) } }</style><p class="sb-dark">Pale in the dark</p>'); } },
  { key: 'lightOnDark', fault: 'a block that shows the dark theme on purpose with data-oa-theme="dark", the same with the device light or dark (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-oa-theme="dark" style="padding:16px"><p style="color:var(--oa-color-text-secondary)">Secondary text on Charcoal, set by the theme.</p></div>'); } },
  // promotion C (November 11, 2026): the switch for all 41 (DR-179, DR-209) and CL-075 Housing at 48 px and up (DR-207)
  { key: 'fitSwitch', fault: 'a master of the 41 at 24 px, sized by CSS where the build cannot see it, drawn alone on 1x screens (DR-209)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg viewBox="0 0 128 128" style="width:24px;height:24px" aria-hidden="true" focusable="false" data-icon="CL-048" data-icon-family="topic"><use href="#oa-sym-cl-048"/></svg> Public records</p>'); } },
  { key: 'fitSwitch', fault: 'the switch as specimens write it, the fit at 1x and the master at 2x (allowed: must not be flagged)', expect: false, hiDpi: [[1440, 2]], js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-048" data-icon-family="topic"><use class="oa-at-1x" href="#oa-sym-cl-048-24px"/><use class="oa-at-2x" href="#oa-sym-cl-048"/></svg> Public records</p>'); },
    verify: (r) => r.runs[0].fitSwitch.fitShown === 1 && r.hiDpi[0].masterShown === 1 },
  { key: 'fitSwitch', fault: 'a specimen style that shows both drawings of the switch on 1x screens', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<style>.sb-both use { display: inline !important }</style><p class="sb-both"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-048" data-icon-family="topic"><use class="oa-at-1x" href="#oa-sym-cl-048-24px"/><use class="oa-at-2x" href="#oa-sym-cl-048"/></svg> Public records</p>'); } },
  { key: 'fitSwitch', fault: 'a specimen style that keeps the fit on 2x screens, which only the high-density run sees', hiDpi: [[1440, 2]], js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<style>@media (min-resolution: 2dppx) { .sb-keep .oa-at-1x { display: inline !important } .sb-keep .oa-at-2x { display: none !important } }</style><p class="sb-keep"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-048" data-icon-family="topic"><use class="oa-at-1x" href="#oa-sym-cl-048-24px"/><use class="oa-at-2x" href="#oa-sym-cl-048"/></svg> Public records</p>'); },
    verify: (r) => r.runs[0].fitSwitch.problems.length === 0 && r.hiDpi[0].problems.length === 1 },
  { key: 'fitSwitch', fault: 'the switch on CL-075 Housing, which is off the list of 41 (DR-207)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-075" data-icon-family="topic" style="display:none"></svg><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><use class="oa-at-1x" href="#oa-sym-cl-075-24px"/><use class="oa-at-2x" href="#oa-sym-cl-075"/></svg> Housing</p>'); } },
  { key: 'fitSwitch', fault: 'a 24 px fit of the 41 standing alone, so 2x screens draw it too', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-048" data-icon-family="topic"><use href="#oa-sym-cl-048-24px"/></svg> Public records</p>'); } },
  { key: 'fitSwitch', fault: 'a master of the 41 at 24 px on a plate marked data-oa-res="fixed" (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg viewBox="0 0 128 128" width="24" height="24" data-oa-res="fixed" aria-hidden="true" focusable="false" data-icon="CL-048" data-icon-family="topic"><use href="#oa-sym-cl-048"/></svg> Public records, the master at 24 px</p>'); },
    verify: (r) => r.runs[0].fitSwitch.fixed === 1 },
  { key: 'iconSizes', fault: 'CL-075 Housing at 24 px, off the list of 41 (DR-136, DR-207, B-3)', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg viewBox="0 0 128 128" width="24" height="24" aria-hidden="true" focusable="false" data-icon="CL-075" data-icon-family="topic"><use href="#oa-sym-cl-075"/></svg> Housing</p>'); } },
  { key: 'iconSizes', fault: 'CL-075 Housing at 48 px (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<p><svg viewBox="0 0 128 128" width="48" height="48" aria-hidden="true" focusable="false" data-icon="CL-075" data-icon-family="topic"><use href="#oa-sym-cl-075"/></svg> Housing</p>'); } },
  // stage C, round 1 (November 11, 2026): keyboard paths, moving specimens and the token table
  { key: 'keyPath', fault: 'the demo set\'s keyboard path as built: Tab, Enter, Space and Tab hold in both live stages (allowed: must not be flagged)', expect: false, js: () => {},
    verify: (r) => r.keys && r.keys.withKeys === 1 && r.keys.walks === 2 && r.keys.steps === 8 },
  { key: 'keyPath', fault: 'the Save button taken out of the Tab order, so the path\'s first Tab never reaches it', js: () => {
    document.querySelectorAll('.code-stage .oa-save-btn').forEach((b) => b.setAttribute('tabindex', '-1')); } },
  { key: 'keyPath', fault: 'a status line whose words differ from what the keys file says Enter announces', js: () => {
    document.querySelectorAll('.code-stage .oa-save-btn').forEach((b) => b.addEventListener('click', () => setTimeout(() => { b.parentElement.querySelector('.oa-save-note').textContent = 'Done.'; }, 0))); } },
  { key: 'motionPlay', fault: 'a player that plays on request, comes to rest, and shows its last frame at once under reduced motion (allowed: must not be flagged)', expect: false, js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div class="sb-mv" data-oa-motion><svg width="80" height="20" viewBox="0 0 80 20" aria-hidden="true" focusable="false"><rect class="sb-mv-r" width="10" height="10" fill="currentColor"/></svg><button type="button" data-oa-play data-oa-pause>Play</button><button type="button" data-oa-reset>Reset</button></div>'); const box = document.querySelectorAll('.sb-mv')[document.querySelectorAll('.sb-mv').length - 1]; const r = box.querySelector('rect'); box.querySelector('[data-oa-play]').addEventListener('click', () => { r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: (matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 400), fill: 'forwards' }); }); const rs = box.querySelector('[data-oa-reset]'); if (rs) rs.addEventListener('click', () => r.getAnimations().forEach((a) => a.cancel())); },
    verify: (r) => r.motion && r.motion.players === 1 && r.motion.reduced.length === 1 && r.motion.reduced[0].finalAtOnce },
  { key: 'motionPlay', fault: 'a moving specimen that starts on load and loops', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div class="sb-mv" data-oa-motion><svg width="80" height="20" viewBox="0 0 80 20" aria-hidden="true" focusable="false"><rect class="sb-mv-r" width="10" height="10" fill="currentColor"/></svg><button type="button" data-oa-play data-oa-pause>Play</button><button type="button" data-oa-reset>Reset</button></div>'); const box = document.querySelectorAll('.sb-mv')[document.querySelectorAll('.sb-mv').length - 1]; const r = box.querySelector('rect'); r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: 800, iterations: Infinity }); box.querySelector('[data-oa-play]').addEventListener('click', () => { r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: (matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 400), fill: 'forwards' }); }); const rs = box.querySelector('[data-oa-reset]'); if (rs) rs.addEventListener('click', () => r.getAnimations().forEach((a) => a.cancel())); } },
  { key: 'motionPlay', fault: 'a moving specimen with Play and Pause and no Reset', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div class="sb-mv" data-oa-motion><svg width="80" height="20" viewBox="0 0 80 20" aria-hidden="true" focusable="false"><rect class="sb-mv-r" width="10" height="10" fill="currentColor"/></svg><button type="button" data-oa-play data-oa-pause>Play</button></div>'); const box = document.querySelectorAll('.sb-mv')[document.querySelectorAll('.sb-mv').length - 1]; const r = box.querySelector('rect'); box.querySelector('[data-oa-play]').addEventListener('click', () => { r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: (matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 400), fill: 'forwards' }); }); const rs = box.querySelector('[data-oa-reset]'); if (rs) rs.addEventListener('click', () => r.getAnimations().forEach((a) => a.cancel())); } },
  { key: 'motionPlay', fault: 'a player that keeps its 400 ms under reduced motion', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div class="sb-mv" data-oa-motion><svg width="80" height="20" viewBox="0 0 80 20" aria-hidden="true" focusable="false"><rect class="sb-mv-r" width="10" height="10" fill="currentColor"/></svg><button type="button" data-oa-play data-oa-pause>Play</button><button type="button" data-oa-reset>Reset</button></div>'); const box = document.querySelectorAll('.sb-mv')[document.querySelectorAll('.sb-mv').length - 1]; const r = box.querySelector('rect'); box.querySelector('[data-oa-play]').addEventListener('click', () => { r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: 400, fill: 'forwards' }); }); const rs = box.querySelector('[data-oa-reset]'); if (rs) rs.addEventListener('click', () => r.getAnimations().forEach((a) => a.cancel())); } },
  { key: 'motionPlay', fault: 'a player whose motion loops after Play', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div class="sb-mv" data-oa-motion><svg width="80" height="20" viewBox="0 0 80 20" aria-hidden="true" focusable="false"><rect class="sb-mv-r" width="10" height="10" fill="currentColor"/></svg><button type="button" data-oa-play data-oa-pause>Play</button><button type="button" data-oa-reset>Reset</button></div>'); const box = document.querySelectorAll('.sb-mv')[document.querySelectorAll('.sb-mv').length - 1]; const r = box.querySelector('rect'); box.querySelector('[data-oa-play]').addEventListener('click', () => { r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: (matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 400), fill: 'forwards', iterations: Infinity }); }); const rs = box.querySelector('[data-oa-reset]'); if (rs) rs.addEventListener('click', () => r.getAnimations().forEach((a) => a.cancel())); } },
  { key: 'motionPlay', fault: 'a player that draws its last frame under reduced motion and leaves data-frame at "start" (chapter 17\'s contract)', js: () => { document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div class="sb-mv" data-oa-motion data-frame="start"><svg width="80" height="20" viewBox="0 0 80 20" aria-hidden="true" focusable="false"><rect class="sb-mv-r" width="10" height="10" fill="currentColor"/></svg><button type="button" data-oa-play data-oa-pause>Play</button><button type="button" data-oa-reset>Reset</button></div>'); const box = document.querySelectorAll('.sb-mv')[document.querySelectorAll('.sb-mv').length - 1]; const r = box.querySelector('rect'); box.querySelector('[data-oa-play]').addEventListener('click', () => { r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: (matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 400), fill: 'forwards' }); }); const rs = box.querySelector('[data-oa-reset]'); if (rs) rs.addEventListener('click', () => r.getAnimations().forEach((a) => a.cancel())); } },
  { key: 'motionPlay', fault: 'the same looping player on a failure plate, shown as a fault on purpose (allowed: must not be flagged)', expect: false, js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<figure class="plate plate--failure"><div class="sb-fail"></div></figure>'); document.querySelector('.sb-fail').insertAdjacentHTML('beforeend', '<div class="sb-mv" data-oa-motion><svg width="80" height="20" viewBox="0 0 80 20" aria-hidden="true" focusable="false"><rect class="sb-mv-r" width="10" height="10" fill="currentColor"/></svg><button type="button" data-oa-play data-oa-pause>Play</button><button type="button" data-oa-reset>Reset</button></div>'); const box = document.querySelectorAll('.sb-mv')[document.querySelectorAll('.sb-mv').length - 1]; const r = box.querySelector('rect'); box.querySelector('[data-oa-play]').addEventListener('click', () => { r.animate([{ transform: 'translateX(0px)' }, { transform: 'translateX(50px)' }], { duration: (matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 400), fill: 'forwards', iterations: Infinity }); }); const rs = box.querySelector('[data-oa-reset]'); if (rs) rs.addEventListener('click', () => r.getAnimations().forEach((a) => a.cancel())); },
    verify: (r) => r.motion && r.motion.failurePlates === 1 && r.motion.players === 0 },
  { key: 'tokenTable', fault: 'a token table of three rows where tokens.json holds hundreds', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-26-token-table"><div class="tt" data-token-count="3" data-token-version="0"><table><tbody>' + '<tr><th><code class="tt-c">--oa-color-palette-charcoal</code></th><td><span class="tt-sw" style="background:var(--oa-color-palette-charcoal)"></span><span class="tt-v">&#35;121212</span></td></tr>' + '<tr><th><code class="tt-c">--oa-color-palette-newsprint</code></th><td><span class="tt-sw" style="background:var(--oa-color-palette-newsprint)"></span><span class="tt-v">&#35;DCD9D2</span></td></tr>' + '<tr><th><code class="tt-c">--oa-color-palette-white</code></th><td><span class="tt-sw" style="background:var(--oa-color-palette-white)"></span><span class="tt-v">&#35;FFFFFF</span></td></tr>' + '</tbody></table></div></div>'); } },
  { key: 'tokenTable', fault: 'a token table with a name the page does not define and a swatch whose printed hex is not what it draws', js: () => {
    document.querySelector('.rule .why').insertAdjacentHTML('beforeend', '<div data-specimen="s-26-token-table"><div class="tt" data-token-count="3" data-token-version="0"><table><tbody>' + '<tr><th><code class="tt-c">--oa-color-palette-charcoal</code></th><td><span class="tt-sw" style="background:var(--oa-color-palette-charcoal)"></span><span class="tt-v">&#35;121212</span></td></tr>' + '<tr><th><code class="tt-c">--oa-no-such-token</code></th><td><span class="tt-sw" style="background:var(--oa-no-such-token)"></span><span class="tt-v">&#35;121212</span></td></tr>' + '<tr><th><code class="tt-c">--oa-color-palette-white</code></th><td><span class="tt-sw" style="background:var(--oa-color-palette-white)"></span><span class="tt-v">&#35;121212</span></td></tr>' + '</tbody></table></div></div>'); },
    verify: (r) => r.runs[0].tokenTable && r.runs[0].tokenTable.undefCount === 1 && r.runs[0].tokenTable.offCount === 2 },   // the undefined name's swatch draws nothing, so it is off too
];

async function selfTest() {
  const outDir = fs.mkdtempSync(path.join(process.env.TMPDIR || os.tmpdir(), 'oa-guide-check-'));
  const page = path.join(outDir, 'Guide-Check-Demo.html');
  execFileSync('python3', ['-I', path.join(__dirname, 'guide_build.py'), '--demo', '--quiet', '--out', page,
    '--chapters', path.join(outDir, 'no-chapters'), '--specimens', path.join(outDir, 'no-specimens')]);
  const browser = await chromium.launch();
  const result = { checked: new Date().toISOString(), page: 'demo build (guide_build.py --demo), in a temporary folder', axe: AXE ? 'found' : 'not found', clean: null, plants: [] };
  // the clean demo: no structural, text, red or writing failure, and the exempt failure plate's 12 px gray text is skipped
  const clean = await checkPage(browser, page, [1440, 390], { skipFocus: false, hiDpi: [[1440, 2], [390, 3]] });
  result.clean_keys = clean.keys; result.clean_motion = clean.motion;
  result.clean = { pass: clean.pass, failures: clean.failures.map((f) => f.msg), exemptions: clean.runs[0].specimens.exemptions, skippedTexts: clean.runs[0].text.skipped };
  for (const p of PLANTS) {
    const r = await checkPage(browser, page, p.widths || [1440], { mutate: p.js, skipAxe: true, skipFocus: !p.focus, plant: true, hiDpi: p.hiDpi || [],
      keys: p.key === 'keyPath', motion: p.key === 'motionPlay' });
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
  const report = await checkPage(browser, file, widths, { captures: !process.argv.includes('--no-captures'), hiDpi: [[1440, 2], [390, 3]] });
  await browser.close();
  const outPath = path.join(path.dirname(file), `${path.basename(file, '.html')}-Guide-Check-Results.json`);
  fs.writeFileSync(outPath, JSON.stringify(report, null, 1));
  const r0 = report.runs[0];
  console.log(`${report.pass ? 'PASS' : 'FAIL'} ${report.file}: ${widths.length} widths, ${r0.structure.rules} rules, ${r0.specimens.stages} specimens, ${r0.anchors.links} same-page links, ${report.failures.length} failures`);
  if (r0.specimens.exemptions.length) console.log(`  exemptions: ${r0.specimens.exemptions.map((x) => x.specimen + ' (' + x.skips + ')').join(', ')}`);
  console.log(`  fitSwitch: ${report.runs.map((r) => `${r.width} at 1x ${r.fitSwitch.pairs} switches, fit shown in ${r.fitSwitch.fitShown}`).join('; ')}; `
    + `${report.hiDpi.map((h) => `${h.width} at ${h.dpr}x ${h.pairs} switches, master shown in ${h.masterShown}`).join('; ')}`);
  if (report.keys) console.log(`  keyPath: ${report.keys.withKeys} of ${report.keys.sets} code sets with keys files, ${report.keys.paths} paths, ${report.keys.walks} walks and ${report.keys.steps} steps at ${report.keys.widths.join(' and ')} px`
    + (report.keys.missing.length ? `; no keys file: ${report.keys.missing.join(', ')}` : ''));
  if (report.motion) console.log(`  motion: ${report.motion.players} moving specimen(s), ${report.motion.reduced.filter((x) => x.finalAtOnce).length} showing the final frame at once under reduced motion; ${report.motion.failurePlates} on failure plates left alone`);
  const tt = report.runs[0].tokenTable;
  if (tt) console.log(`  tokenTable: ${tt.rows} rows, ${tt.swatches} swatches, version ${tt.version}; tokens.json ${tt.file ? tt.file.count + ', ' + tt.file.version : 'unread'}`);
  for (const f of report.failures) console.log('  - ' + f.msg);
  console.log('  results: ' + path.relative(ROOT, outPath));
  process.exit(report.pass ? 0 : 1);
})();
