// Rendered checks for an Oath & Action guide page built by guide_build.py (November 6, 2026, guide engineer).
// The chart checks stay in dataviz_check.js; this script holds the tests guide pages need, and ports the text, red,
// overflow, axe and focus checks so one run covers a guide page.
//
// Usage:
//   node work/build/scripts/phase-2/guide_check.js <page.html> [--quick] [--no-captures]
//   node work/build/scripts/phase-2/guide_check.js --self-test      plants each fault in a demo build and proves the test catches it
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
//                      "Phase", "Gate" or "gate" in any case, "Board 5" or any "Board N" or "board A", "stage A" to
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
  ['\\bgates?\\b', 'gi', 'studio word'],
  ['\\b[Bb]oards?[\\s\\u00a0]+(?:\\d+|[A-Z])\\b', 'g', 'studio word'],
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

async function focusAudit(page, stops) {
  const results = [];
  await page.evaluate(() => { document.activeElement && document.activeElement.blur && document.activeElement.blur(); window.scrollTo(0, 0); });
  for (let i = 0; i < stops; i++) {
    await page.keyboard.press('Tab');
    const r = await page.evaluate(() => {
      const el = document.activeElement; if (!el || el === document.body) return null;
      const cs = getComputedStyle(el);
      const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow && cs.boxShadow !== 'none');
      const r = el.getBoundingClientRect(); const head = document.querySelector('.masthead');
      const hb = head ? head.getBoundingClientRect().bottom : 0;
      const obscured = !el.closest('.masthead') && !el.closest('dialog') && getComputedStyle(el).position !== 'fixed' && r.bottom <= hb + 1;
      return { tag: el.tagName, label: (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40), ring, obscured };
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
    const fails = failuresFrom(a, width);
    let axe = null;
    if (!opts.skipAxe) {
      axe = await runAxe(page);
      if (axe && axe.length) fails.push({ key: 'axe', msg: `${width}: axe ${axe.map((v) => v.id + ' x' + v.nodes).join(', ')}` });
      if (!axe) fails.push({ key: 'axe', msg: `${width}: axe-core not found (set AXE_PATH; see the shell notes, section 6)` });
    }
    let focus = null;
    if (width === 1440 && !opts.skipFocus) {
      focus = await focusAudit(page, 60);
      const noRing = focus.filter((x) => !x.ring); const hidden = focus.filter((x) => x.obscured);
      if (noRing.length) fails.push({ key: 'focus', msg: `${width}: ${noRing.length} focus stop(s) without a visible ring, first: ${JSON.stringify(noRing[0])}` });
      if (hidden.length) fails.push({ key: 'focus', msg: `${width}: ${hidden.length} focus stop(s) hidden under the masthead, first: ${JSON.stringify(hidden[0])}` });
    }
    if (outside.size) fails.push({ key: 'requests', msg: `${width}: outside requests to ${[...outside].join(', ')}` });
    if (errors.length) fails.push({ key: 'errors', msg: `${width}: script errors: ${errors.slice(0, 3).join(' | ')}` });
    report.runs.push({ width, ...a, axe, focusStops: focus ? focus.length : null, focusProblems: focus ? focus.filter((x) => !x.ring || x.obscured).slice(0, 10) : null });
    report.failures.push(...fails);
    if (opts.captures && (width === 1440 || width === 390)) {
      const secs = await page.evaluate(() => [...document.querySelectorAll('main > section[id]')].map((s) => s.id));
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
    const r = await checkPage(browser, page, [1440], { mutate: p.js, skipAxe: true, skipFocus: true });
    const caught = r.failures.filter((f) => f.key === p.key);
    const others = r.failures.filter((f) => f.key !== p.key).map((f) => f.key);
    // a plant with expect: false proves an allowance: the test must stay quiet
    const expect = p.expect !== false;
    result.plants.push({ test: p.key, fault: p.fault, expect: expect ? 'caught' : 'not flagged', caught: caught.length > 0, ok: (caught.length > 0) === expect,
      message: caught[0] ? caught[0].msg : null, alsoFlagged: [...new Set(others)] });
  }
  await browser.close();
  result.pass = result.clean.pass && result.plants.every((p) => p.ok);
  const outPath = path.join(ROOT, 'work/boards/phase-2/stage-a/20261106_Guide-Check-Plant-Results.json');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(result, null, 1));
  const faults = result.plants.filter((p) => p.expect === 'caught'), allow = result.plants.filter((p) => p.expect !== 'caught');
  console.log(`${result.pass ? 'PASS' : 'FAIL'} self-test: clean demo ${result.clean.pass ? 'passes' : 'FAILS'}; ${faults.filter((p) => p.ok).length} of ${faults.length} planted faults caught`
    + (allow.length ? `; ${allow.filter((p) => p.ok).length} of ${allow.length} allowed cases left alone` : ''));
  if (!result.clean.pass) result.clean.failures.forEach((f) => console.log('  clean: ' + f));
  for (const p of result.plants) console.log(`  ${p.ok ? (p.expect === 'caught' ? 'caught' : 'quiet ') : (p.expect === 'caught' ? 'MISSED' : 'FLAGGED')}  ${p.test.padEnd(17)} ${p.fault}${p.alsoFlagged.length ? '  (also: ' + p.alsoFlagged.join(', ') + ')' : ''}`);
  console.log('  results: ' + path.relative(ROOT, outPath));
  fs.rmSync(outDir, { recursive: true, force: true });
  process.exit(result.pass ? 0 : 1);
}

// ------------------------------------------------------------------------------------------------ main
(async () => {
  if (process.argv.includes('--self-test')) return selfTest();
  const arg = process.argv.slice(2).find((x) => !x.startsWith('--'));
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
