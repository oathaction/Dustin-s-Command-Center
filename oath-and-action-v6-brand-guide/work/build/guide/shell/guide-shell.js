// Oath & Action Brand Guide, Edition 06: the guide shell's script. guide_build.py inlines it at the end of the page.
// Built from the Gate 1 wireframe's interaction model (work/boards/phase-1/navigation/wireframe.js):
// marks the current part, chapter and rule; moves focus to the heading a link lands on (or to the target itself when it
// holds none); offers a way back after a cross-reference, right after the heading that took focus; runs the phone menu
// as a modal dialog; makes a specimen frame or code block a named, keyboard-scrollable group only while it overflows;
// switches wide comparison frames between true size and fit to window; hides the rail once the full-width appendix
// reaches it; and drives the Copy buttons with a status line. Fix pass, November 6, 2026: AX-S1, AX-S3, AX-S11, AX-S12, D2-251.
// Apply fix pass, November 7, 2026: Fit to window is offered only where it keeps every text at 13 px or more (CA-M1, CA-N9).
// Q1 to Q4 pass, November 8, 2026: a frame takes 32 px sides where that holds its stage whole at true size (CD-S9).
// Round 3 fix pass, November 10, 2026: the tokens.css button saves a zip through the host where one answers (DR-192,
// D2-964); from 80em a fixed plate wider than its column breaks out over the rail where the page holds it whole (CA-S13).
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var header = $('.masthead');
  var tracked = $$('[data-track]');
  var where = $('#where');
  var menuWhere = $('#menu-where-text');
  var rail = $('.rail');
  var menu = $('#menu');
  var menuBtn = $('#menubtn');
  var menuScroll = $('.menu-scroll');
  var appendix = $('#proofs');
  var current = null, currentRule = null;
  var pinnedUntil = 0;
  var pendingReturn = null;
  var navigatingFromMenu = false;

  function keepInView(el, box, foot) {
    if (!el || !box) return;
    var e = el.getBoundingClientRect(), b = box.getBoundingClientRect(), f = foot || 8;
    if (e.top < b.top + 8) box.scrollTop -= (b.top + 8 - e.top);
    else if (e.bottom > b.bottom - f) box.scrollTop += (e.bottom - b.bottom + f);
  }
  function sectionFor(el) { return el && el.closest ? el.closest('[data-track]') : null; }

  function setCurrent(sec) {
    if (sec === current) return;
    current = sec;
    $$('[data-loc][aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    $$('[data-part-link][aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    var label = sec ? sec.getAttribute('data-label') : 'Cover';
    if (where) where.textContent = label;
    if (menuWhere) menuWhere.textContent = label;
    if (!sec) return;
    var loc = sec.id === 'proofs' ? ['proofs', 'proofs-item'] : [sec.id];
    loc.forEach(function (id) { $$('[data-loc="' + id + '"]').forEach(function (a) { a.setAttribute('aria-current', 'location'); }); });
    var part = sec.getAttribute('data-part') || (sec.id === 'contents' ? 'contents' : null);
    if (part) $$('[data-part-link="' + part + '"]').forEach(function (a) { a.setAttribute('aria-current', 'location'); });
    keepInView($('.rail [data-loc="' + sec.id + '"]'), rail, 72);   // clear of the rail's "More below" cue (CA-S8)
    railMore();
  }

  // The current rule inside a chapter is marked in that chapter's "In this chapter" list.
  function setRule(chapter, line) {
    var rules = chapter ? $$('.rule, .closer', chapter) : [];
    var cur = null;
    for (var i = 0; i < rules.length; i++) { if (rules[i].getBoundingClientRect().top <= line) cur = rules[i]; else break; }
    if (cur === currentRule) return;
    if (currentRule) $$('.local-toc a[aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    currentRule = cur;
    if (cur && chapter) { var a = $('.local-toc a[href="#' + cur.id + '"]', chapter); if (a) a.setAttribute('aria-current', 'true'); }
  }

  // From 90em the appendix spans the whole page and slides over the rail; once it reaches the rail, the rail is hidden,
  // so no link under the appendix can take focus out of sight. A plate frame that breaks out over the rail (CA-S13)
  // hides it the same way while the two overlap.
  // CA-S8 (round 2): the rail says "More below" at its foot while it can scroll further down
  function railMore() {
    if (!rail) return;
    rail.classList.toggle('can-scroll', rail.scrollHeight - rail.scrollTop - rail.clientHeight > 4);
  }
  if (rail) { rail.addEventListener('scroll', railMore, { passive: true }); window.addEventListener('resize', railMore); window.addEventListener('load', railMore); railMore(); }

  function railCover() {
    if (!rail) return;
    var rr = rail.getBoundingClientRect();
    var covered = !!appendix && window.matchMedia('(min-width: 90em)').matches && appendix.getBoundingClientRect().top < rr.bottom;
    if (!covered) covered = $$('.plate.is-breakout > .plate-scroll').some(function (b) {
      var r = b.getBoundingClientRect(); return r.top < rr.bottom && r.bottom > rr.top && r.left < rr.right;
    });
    rail.classList.toggle('is-covered', covered);
  }

  // The current section is the last one whose top has passed a line a quarter of the way down the window.
  function compute() {
    var line = header.getBoundingClientRect().bottom + window.innerHeight * 0.25;
    var cur = null;
    for (var i = 0; i < tracked.length; i++) { if (tracked[i].getBoundingClientRect().top <= line) cur = tracked[i]; else break; }
    setRule(cur && cur.classList.contains('chapter') ? cur : null, line);
    return cur;
  }
  var ticking = false, pinTimer = null;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      railCover();
      var wait = pinnedUntil - Date.now();
      if (wait > 0) { clearTimeout(pinTimer); pinTimer = setTimeout(function () { setCurrent(compute()); }, wait + 20); return; }
      setCurrent(compute());
    });
  }, { passive: true });

  // Cross-references remember where the reader came from.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.xref');
    if (!a) return;
    var origin = a.closest('.rule[id], .closer[id], .rule-group[id], [data-track]');
    var sec = sectionFor(a);
    if (!origin || !sec) return;
    var what = '';
    if (!origin.matches('[data-track]')) {
      var h = origin.querySelector('h3, .rg-head');
      what = h ? h.textContent.replace(/\s+/g, ' ').trim().replace(/[.:]$/, '') : '';
    }
    pendingReturn = { id: origin.id, label: (what ? what + ', ' : '') + sec.getAttribute('data-label') };
  });

  function onHash() {
    var id = decodeURIComponent(location.hash.slice(1));
    $$('.return').forEach(function (p) { p.hidden = true; p.textContent = ''; });
    if (!id) { pendingReturn = null; return; }
    var target = document.getElementById(id);
    if (!target) { pendingReturn = null; return; }
    // a V5 alias such as #grid stands at the top of its new chapter
    var host = target.classList.contains('alias') ? target.parentElement : target;
    var sec = sectionFor(host);
    if (sec) { setCurrent(sec); pinnedUntil = Date.now() + 600; }
    // Focus moves to the heading the link points at, so the next Tab continues from there. A target with no heading
    // (a group block, a table row inside a specimen) takes focus itself (AX-S11).
    var h = host.matches('h1, h2, h3') ? host : host.querySelector('h1, h2, h3');
    if (host.id === 'main') h = host;
    if (!h && host !== document.body) h = host;
    if (h) { if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    if (pendingReturn && sec && pendingReturn.id !== id) {
      // the way back sits right after the heading that took focus, so the next Tab reaches it (AX-S1)
      var own = host.matches('.rule, .closer, .rule-group, .proof-group') ? host.querySelector(':scope > .return') : null;
      var slot = own || $('.return', sec);
      if (slot) {
        var back = document.createElement('a');
        back.href = '#' + pendingReturn.id;
        back.textContent = 'Return to ' + pendingReturn.label;
        slot.appendChild(back);
        slot.hidden = false;
      }
    }
    pendingReturn = null;
  }
  window.addEventListener('hashchange', onHash);

  // Phone menu: a modal dialog with one navigation block, every part and chapter in it.
  if (menu && menuBtn) {
    menuBtn.addEventListener('click', function () {
      menu.showModal();
      menuBtn.setAttribute('aria-expanded', 'true');
      var cur = $('a[aria-current]', menu);
      if (cur) { keepInView(cur, menuScroll); cur.focus(); } else { $('#menuclose').focus(); }
    });
    $('#menuclose').addEventListener('click', function () { menu.close(); });
    menu.addEventListener('close', function () {
      menuBtn.setAttribute('aria-expanded', 'false');
      if (!navigatingFromMenu) menuBtn.focus();
      navigatingFromMenu = false;
    });
    menu.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (a) {
        e.preventDefault();
        navigatingFromMenu = true;
        menu.close();
        var href = a.getAttribute('href');
        if (location.hash === href) onHash(); else location.hash = href;
        var t = document.getElementById(href.slice(1));
        if (t && location.hash === href) t.scrollIntoView();
      } else if (e.target === menu) {
        menu.close();
      }
    });
    window.addEventListener('resize', function () { if (menu.open && window.matchMedia('(min-width: 64em)').matches) menu.close(); });
  }

  // A flowing stage whose content cannot shrink to the column (a wide table on a 360 px phone) grows to hold it, so the
  // keyline always encloses the content and the frame scrolls in its place (B1).
  function hugFlowing() {
    $$('.plate-stage:not([data-width]):not([data-pending])').forEach(function (st) {
      st.style.minWidth = '';
      var over = st.scrollWidth - st.clientWidth;
      if (over > 1) st.style.minWidth = Math.ceil(st.offsetWidth + over + parseFloat(getComputedStyle(st).paddingRight)) + 'px';
    });
  }

  // CD-S9 (Q1 to Q4 pass): a frame whose stage would scroll inside its usual sides (48 px from 48em) tries the narrower
  // sides of .is-snug (32 px, set in the stylesheet) and keeps them only where the stage then fits whole, so it sits
  // centered at true size with no hint and no tab stop. A frame that fits today keeps its sides, and one that still
  // overflows at 32 px keeps them too and scrolls as before. The stage's need is its layout width at true size, which a
  // Fit to window scale does not change. Where .is-snug narrows nothing (phones, the appendix), the frame keeps its sides.
  function snug() {
    var boxes = $$('.plate-scroll');
    var sides = function (b) { var cs = getComputedStyle(b); return parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight); };
    var tries = [];
    boxes.forEach(function (b) {
      var st = $('.plate-stage', b); if (!st) return;
      var need = Math.max(st.offsetWidth, st.scrollWidth);
      if (need + sides(b) > b.clientWidth + 1) tries.push({ box: b, need: need });
    });
    tries.forEach(function (t) { t.box.classList.add('is-snug'); });
    tries.filter(function (t) { return t.need + sides(t.box) > t.box.clientWidth; })
      .forEach(function (t) { t.box.classList.remove('is-snug'); });
  }
  // CA-S13 (round 3): from 80em, a chapter plate whose fixed stage does not fit its column at true size, even inside
  // the narrow sides, takes the room to its left, over the rail, out to the page's own margin, where that holds the
  // stage whole. Its frame and stage move, centered in the wider frame; its head and caption stay on the text column.
  // The appendix spans the page already, and a stage too wide for the page keeps its frame and scrolls as before.
  function breakout() {
    var pageBox = $('.frame');
    var on = !!pageBox && window.matchMedia('(min-width: 80em)').matches;
    var edge = 0, side = 0;
    if (on) {
      edge = pageBox.getBoundingClientRect().left + parseFloat(getComputedStyle(pageBox).paddingLeft);
      var rs = getComputedStyle(document.documentElement), tok = rs.getPropertyValue('--oa-space-400').trim();
      side = /rem$/.test(tok) ? parseFloat(tok) * parseFloat(rs.fontSize) : (parseFloat(tok) || 32);
    }
    $$('.chapter .plate > .plate-scroll[data-width]').forEach(function (b) {
      var fig = b.parentElement, st = $('.plate-stage', b);
      fig.classList.toggle('is-breakout', false); fig.style.setProperty('--bo', '0px');
      if (!on || !st) return;
      var reach = Math.floor(fig.getBoundingClientRect().left - edge);
      var need = Math.max(st.offsetWidth, st.scrollWidth) + 2 * side;
      if (reach >= 1 && need > b.clientWidth + 1 && need <= b.clientWidth + reach) {
        fig.style.setProperty('--bo', reach + 'px');
        fig.classList.toggle('is-breakout', true);
      }
    });
    // round 2 (call 13): a flowing stage marked data-breakout, such as chapter 26's token table, whose columns need the
    // room, takes all of it from 80em, out to the page's own margin
    $$('.chapter .plate > .plate-scroll[data-breakout]').forEach(function (b) {
      var fig = b.parentElement;
      fig.classList.toggle('is-breakout', false); fig.style.setProperty('--bo', '0px');
      if (!on) return;
      var reach = Math.floor(fig.getBoundingClientRect().left - edge);
      if (reach >= 1) { fig.style.setProperty('--bo', reach + 'px'); fig.classList.toggle('is-breakout', true); }
    });
  }
  // Every frame returns to its usual sides first, so the flowing stages and the tests above all measure from there.
  function sizeFrames() {
    $$('.plate-scroll.is-snug').forEach(function (b) { b.classList.remove('is-snug'); });
    hugFlowing();
    breakout();
    snug();
  }

  // A frame or code block that overflows becomes a focusable group named for what it holds, so a keyboard can scroll
  // it; one that fits stays out of the Tab order (AX-S3). Groups stay out of the landmark list. A plate that scrolls
  // shows its hint in the plate head, before the specimen (AX-S12).
  function frames() {
    $$('[data-plate-scroll]').forEach(function (box) {
      var wide = box.scrollWidth > box.clientWidth + 1;
      var tall = box.matches('pre') && box.scrollHeight > box.clientHeight + 1;
      var fig = box.closest('.plate');
      if (fig) {
        fig.classList.toggle('is-wide', wide);
        var hint = $('.plate-hint', fig);
        if (hint) hint.hidden = !wide;
      }
      var name = box.getAttribute('data-frame-name') || 'Frame';
      if (wide || tall) {
        box.setAttribute('tabindex', '0');
        box.setAttribute('role', 'group');
        // round 2 (CA-S2): the name says which way the frame scrolls; a code panel holds code, not a piece at true size
        var way = wide && tall ? 'down and sideways' : wide ? 'sideways' : 'down';
        box.setAttribute('aria-label', fig && !box.matches('pre') ? name + ', at true size. Scroll ' + way + ' to see all of it.' : name + '. Scroll ' + way + ' to see all of it.');
      } else if (box.hasAttribute('tabindex')) {
        ['tabindex', 'role', 'aria-label'].forEach(function (k) { box.removeAttribute(k); });
      }
    });
  }

  // True size or fit to window, for the wide comparison frames (D2-251). True size is the default; fit scales the whole
  // stage to the frame's inner width and says by how much.
  function applyFit(fig) {
    var box = $('.plate-scroll', fig), wrap = $('.plate-fit', fig), stage = $('.plate-stage', fig), size = $('.plate-size', fig);
    if (!box || !wrap || !stage) return;
    var on = fig.getAttribute('data-fit') === 'fit';
    stage.style.transform = ''; stage.style.transformOrigin = ''; wrap.style.width = ''; wrap.style.height = '';
    var cs = getComputedStyle(box);
    var avail = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    var w = stage.offsetWidth, hgt = stage.offsetHeight;
    var s = on ? Math.min(1, avail / w) : 1;
    if (on && s < 1) {
      stage.style.transformOrigin = '0 0'; stage.style.transform = 'scale(' + s + ')';
      wrap.style.width = (w * s) + 'px'; wrap.style.height = (hgt * s) + 'px';
    }
    if (size) size.textContent = on ? (s < 1 ? 'Fit to window, ' + Math.round(s * 100) + ' percent of true size' : 'Fits at true size, ' + w.toLocaleString('en-US') + ' px wide') : size.getAttribute('data-true');
  }
  function setFit(fig, mode) {
    fig.setAttribute('data-fit', mode);
    $$('.fit-btn', fig).forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-fit') === mode)); });
    applyFit(fig);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.fit-btn');
    if (!b) return;
    setFit(b.closest('.plate'), b.getAttribute('data-fit'));
    frames();
    snapStages();
  });

  // Fix pass (CA-M1, CA-N9): every fixed-width plate carries the switch, hidden. It shows only where the stage is wider
  // than its frame and fitting it keeps the smallest text at 13 px or more, the guide's floor (Rule 06.1). Elsewhere
  // the frame scrolls at true size. The smallest text is measured at true size, SVG text at its drawn size.
  var FLOOR = 13;
  function smallestText(stage) {
    var keep = stage.style.transform; stage.style.transform = '';
    var min = Infinity;
    $$('*', stage).forEach(function (el) {
      if (/^(script|style|title|desc|defs)$/i.test(el.tagName) || el.closest('title, desc, defs, .vh')) return;
      var own = false;
      for (var n = el.firstChild; n; n = n.nextSibling) { if (n.nodeType === 3 && n.textContent.trim()) { own = true; break; } }
      if (!own) return;
      var r = el.getBoundingClientRect(); if (r.width === 0 && r.height === 0) return;
      var cs = getComputedStyle(el); if (cs.visibility === 'hidden') return;
      var size = parseFloat(cs.fontSize);
      if (el instanceof SVGElement) {
        var svg = el.closest('svg'), vb = svg && svg.viewBox && svg.viewBox.baseVal;
        if (vb && vb.width) size = size * svg.getBoundingClientRect().width / vb.width;
      }
      if (size < min) min = size;
    });
    stage.style.transform = keep;
    return min;
  }
  function offerFit() {
    $$('.plate--fit').forEach(function (fig) {
      var sw = $('.fit-switch', fig), box = $('.plate-scroll', fig), stage = $('.plate-stage', fig);
      if (!sw || !box || !stage) return;
      var cs = getComputedStyle(box);
      var avail = box.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
      var s = Math.min(1, avail / stage.offsetWidth);
      var ok = s < 0.999 && smallestText(stage) * s >= FLOOR - 0.05;
      sw.hidden = !ok;
      if (!ok && fig.getAttribute('data-fit') === 'fit') setFit(fig, 'true');
    });
  }

  // Stage C, round 1 (D2-1332): a fixed-width plate's stage lands on a whole device pixel, so a piece shown at true size
  // draws sharp at 1x. The text above a plate sets fractional line heights, so its top can fall between pixels. One pass
  // reads every stage's place, a second sets the CSS translate property by the fraction: it moves the drawing alone,
  // never what follows it. A plate set to Fit to window is scaled, so it is left as it is.
  function snapStages() {
    var st = $$('.plate-stage[data-width]');
    st.forEach(function (s) { s.style.translate = ''; });
    var d = window.devicePixelRatio || 1;
    var off = st.map(function (s) {
      if (s.closest('.plate--fit[data-fit="fit"]')) return null;
      var r = s.getBoundingClientRect(), x = (r.left + window.scrollX) * d, y = (r.top + window.scrollY) * d;
      return [(Math.round(x) - x) / d, (Math.round(y) - y) / d];
    });
    st.forEach(function (s, i) {
      var o = off[i];
      if (o && (Math.abs(o[0]) > 0.001 || Math.abs(o[1]) > 0.001)) s.style.translate = o[0].toFixed(3) + 'px ' + o[1].toFixed(3) + 'px';
    });
  }

  var rt = null;
  window.addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(function () { sizeFrames(); $$('.plate--fit[data-fit="fit"]').forEach(applyFit); offerFit(); frames(); railCover(); snapStages(); }, 120);
  });

  // The token downloads (round 2, November 10, 2026; DR-192 and D2-964 in round 3; tokens.json in stage C round 1,
  // DR-214). The page carries each file once, as a link marked data-oa-file: tokens.css in the colophon, tokens.json in
  // Rule 26.8. Every button marked data-oa-download="<that link's id>" starts that file's download where the reader is.
  // Published, the page sits in a host that saves a file only through its own call, which refuses a .css or .json name.
  // Where window.claude reaches the host's downloads capability, every button offers the zip the build packed beside
  // its link, holding the one file, and says so. The host asks the reader before it saves. Declined: nothing more. Any
  // other refusal: the buttons go back to the plain links, and the one clicked starts. With no host, the links work.
  var dlFiles = $$('a[data-oa-file][id]');
  var dlHost = null;   // the host's downloads namespace, once it resolves
  function dlPlain(l) { return l.getAttribute('data-oa-file-words') || l.getAttribute('data-oa-css-words') || l.textContent; }
  function dlWords(zip) {
    dlFiles.forEach(function (l) {
      var w = zip && l.getAttribute('data-oa-zip') ? (l.getAttribute('data-oa-zip-words') || dlPlain(l)) : dlPlain(l);
      $$('a[data-oa-download="' + l.id + '"]').concat([l]).forEach(function (a) { a.textContent = w; });
    });
  }
  if (dlFiles.some(function (l) { return l.getAttribute('data-oa-zip'); }) && window.claude && typeof window.claude.use === 'function') {
    try {
      Promise.resolve(window.claude.use('downloads')).then(function (ns) {
        if (ns && typeof ns.save === 'function') { dlHost = ns; dlWords(true); }
      }, function () { /* no host save: the plain links stay */ });
    } catch (err) { /* no host save: the plain links stay */ }
  }
  function zipBytes(l) {
    var s = atob(l.getAttribute('data-oa-zip')), u = new Uint8Array(s.length);
    for (var i = 0; i < s.length; i++) u[i] = s.charCodeAt(i);
    return u;
  }
  function hostSave(l) {
    var req;
    try { req = dlHost.save({ filename: l.getAttribute('data-oa-zip-name'), data: zipBytes(l) }); } catch (err) { req = Promise.reject(err); }
    Promise.resolve(req).then(function () { /* the host saved it */ }, function (err) {
      var code = err && err.code;
      // declined: the reader said no. rate_limited: a prompt is already open, so the reader is already deciding.
      if (code === 'declined' || code === 'rate_limited') return;
      dlHost = null;
      dlWords(false);
      l.click();
    });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-oa-download], a[data-oa-file]');
    if (!a) return;
    // round 2 (CA-M1): a live demo's link carries data-oa-file="<id>", the page's own copy of the file it names, since no
    // file sits beside the guide; a file's own link carries the attribute with no value
    var to = a.getAttribute('data-oa-file');
    var l = a.hasAttribute('data-oa-file') ? (to && to !== a.id ? document.getElementById(to) : a) : document.getElementById(a.getAttribute('data-oa-download'));
    if (!l || !l.hasAttribute('data-oa-file')) return;
    if (dlHost && l.getAttribute('data-oa-zip')) { e.preventDefault(); hostSave(l); return; }
    if (a === l) return;   // a file's own link downloads by itself
    e.preventDefault();
    l.click();
  });

  // Copy buttons write their result to the status line beside them (a polite live region).
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button.copy');
    if (!b) return;
    var src = document.getElementById(b.getAttribute('data-copy-from'));
    var value = src ? src.textContent : (b.getAttribute('data-copy') || '');
    // DR-203 (stage C): a code plate has one status line for its panels, and the line names what was copied
    var scope = b.closest('.plate--code, .closer, .rule, section');
    var st = scope ? $('.status[role="status"]', scope) : null;   // the shell's own line, never a live demo's
    var old = scope && $('.copy-fallback', scope);
    if (old) old.remove();
    // F-7 (stage C): the line shows the success or the error mark before its words, and an error starts "Error:"
    var say = function (t, err) {
      if (!st) return;
      var words = $('.st-t', st) || st;
      words.textContent = '';
      if (err) { var bold = document.createElement('b'); bold.textContent = 'Error:'; words.appendChild(bold); words.appendChild(document.createTextNode(' ' + t)); } else words.textContent = t;
      // an SVG has no hidden property, so the attribute itself is set
      $$('.st-ok', st).forEach(function (m) { m.toggleAttribute('hidden', !!err); });
      $$('.st-err', st).forEach(function (m) { m.toggleAttribute('hidden', !err); });
      st.classList.toggle('is-error', !!err); st.classList.toggle('is-ok', !err);
      if (err) { st.setAttribute('data-red', 'working'); st.setAttribute('data-red-job', 'error'); } else { st.removeAttribute('data-red'); st.removeAttribute('data-red-job'); }
    };
    var what = b.getAttribute('data-copy-what');
    var lines = value.replace(/\n$/, '').split('\n').length;
    var done = function () { say(what ? 'Copied ' + what + ', ' + lines + (lines === 1 ? ' line' : ' lines') + ', to the clipboard.' : 'Copied ' + value.split('\n').length + ' lines to the clipboard.'); };
    var fail = function () {
      say('The browser blocked copying. The text is selected below: press Control and C, or Command and C.', true);
      var ta = document.createElement('textarea');
      ta.className = 'copy-fallback'; ta.readOnly = true; ta.value = value; ta.rows = 6;
      ta.setAttribute('aria-label', 'Text to copy');
      st.insertAdjacentElement('afterend', ta);
      ta.focus(); ta.select();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(value).then(done, fail); else fail();
  });

  // D2-975 (round 3): the build writes every ID with an ASCII hyphen inside <span class="nw">, in place of U+2011, which
  // the page's fonts do not draw and a search for "CL-001" misses. A live specimen's script may still write U+2011 into
  // its text as it runs (a filtered list, a report page), so the same rule runs here on anything a script adds: in
  // text, each word that holds U+2011 goes in <span class="nw"> with an ASCII hyphen; in SVG, in a field and in a name
  // (aria-label, alt, title), U+2011 simply becomes an ASCII hyphen.
  var NBH = '\u2011', NBH_WORD = /[\w.]*\u2011[\w\u2011]*/g, NBH_ALL = /\u2011/g;
  function holdWhole(node) {
    var t = node.nodeValue, p = node.parentNode;
    if (!t || t.indexOf(NBH) < 0 || !p) return;
    if (p.namespaceURI === 'http://www.w3.org/2000/svg' || /^(SCRIPT|STYLE|TEXTAREA|OPTION|TITLE)$/.test(p.nodeName)) { node.nodeValue = t.replace(NBH_ALL, '-'); return; }
    var frag = document.createDocumentFragment(), last = 0, m;
    NBH_WORD.lastIndex = 0;
    while ((m = NBH_WORD.exec(t))) {
      if (m.index > last) frag.appendChild(document.createTextNode(t.slice(last, m.index)));
      var span = document.createElement('span'); span.className = 'nw'; span.textContent = m[0].replace(NBH_ALL, '-');
      frag.appendChild(span); last = m.index + m[0].length;
    }
    if (last < t.length) frag.appendChild(document.createTextNode(t.slice(last)));
    p.replaceChild(frag, node);
  }
  var NAMES = ['aria-label', 'alt', 'title'];
  function holdNames(el) {
    NAMES.forEach(function (k) { var v = el.getAttribute && el.getAttribute(k), nv = v && v.replace(NBH_ALL, '-'); if (v && nv !== v) el.setAttribute(k, nv); });
  }
  function sweep(root) {
    if (root.nodeType === 3) { holdWhole(root); return; }
    if (root.nodeType !== 1) return;
    holdNames(root);
    var found = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    for (var n = w.nextNode(); n; n = w.nextNode()) if (n.nodeValue.indexOf(NBH) >= 0) found.push(n);
    found.forEach(holdWhole);
    $$('[aria-label], [alt], [title]', root).forEach(holdNames);
  }
  sweep(document.body);
  if (window.MutationObserver) {
    new MutationObserver(function (recs) {
      recs.forEach(function (r) {
        if (r.type === 'characterData') holdWhole(r.target);
        else if (r.type === 'attributes') holdNames(r.target);
        else for (var i = 0; i < r.addedNodes.length; i++) sweep(r.addedNodes[i]);
      });
    }).observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: NAMES });
  }

  function start() {
    sizeFrames();
    offerFit();
    frames();
    railCover();
    if (location.hash) onHash(); else setCurrent(compute());
  }
  start();
  snapStages();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { current = null; start(); snapStages(); });
})();
