// Oath & Action Brand Guide, Edition 06: the guide shell's script. guide_build.py inlines it at the end of the page.
// Built from the Gate 1 wireframe's interaction model (work/boards/phase-1/navigation/wireframe.js):
// marks the current part, chapter and rule; moves focus to the heading a link lands on (or to the target itself when it
// holds none); offers a way back after a cross-reference, right after the heading that took focus; runs the phone menu
// as a modal dialog; makes a specimen frame or code block a named, keyboard-scrollable group only while it overflows;
// switches wide comparison frames between true size and fit to window; hides the rail once the full-width appendix
// reaches it; and drives the Copy buttons with a status line. Fix pass, November 6, 2026: AX-S1, AX-S3, AX-S11, AX-S12, D2-251.
// Apply fix pass, November 7, 2026: Fit to window is offered only where it keeps every text at 13 px or more (CA-M1, CA-N9).
// Q1 to Q4 pass, November 8, 2026: a frame takes 32 px sides where that holds its stage whole at true size (CD-S9).
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

  function keepInView(el, box) {
    if (!el || !box) return;
    var e = el.getBoundingClientRect(), b = box.getBoundingClientRect();
    if (e.top < b.top + 8) box.scrollTop -= (b.top + 8 - e.top);
    else if (e.bottom > b.bottom - 8) box.scrollTop += (e.bottom - b.bottom + 8);
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
    keepInView($('.rail [data-loc="' + sec.id + '"]'), rail);
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
  // so no link under the appendix can take focus out of sight.
  function railCover() {
    if (!rail || !appendix) return;
    var wide = window.matchMedia('(min-width: 90em)').matches;
    var covered = wide && appendix.getBoundingClientRect().top < rail.getBoundingClientRect().bottom;
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
  // Every frame returns to its usual sides first, so the flowing stages and the test above both measure from there.
  function sizeFrames() {
    $$('.plate-scroll.is-snug').forEach(function (b) { b.classList.remove('is-snug'); });
    hugFlowing();
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
        box.setAttribute('aria-label', fig ? name + ', at true size. Scroll sideways to see all of it.' : name + '. Scroll to see all of it.');
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

  var rt = null;
  window.addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(function () { sizeFrames(); $$('.plate--fit[data-fit="fit"]').forEach(applyFit); offerFit(); frames(); railCover(); }, 120);
  });

  // A chapter's "Download tokens.css" links to the page's one download in the colophon, and a click starts that
  // download where the reader is, so the file sits in the page once (round 2, November 10, 2026).
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-oa-download]');
    if (!a) return;
    var target = document.getElementById(a.getAttribute('data-oa-download'));
    if (!target) return;
    e.preventDefault();
    target.click();
  });

  // Copy buttons write their result to the status line beside them (a polite live region).
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button.copy');
    if (!b) return;
    var src = document.getElementById(b.getAttribute('data-copy-from'));
    var value = src ? src.textContent : (b.getAttribute('data-copy') || '');
    var scope = b.closest('.closer, .rule, section');
    var st = scope ? $('[role="status"]', scope) : null;
    var old = scope && $('.copy-fallback', scope);
    if (old) old.remove();
    var say = function (t, err) { if (!st) return; st.textContent = t; st.classList.toggle('is-error', !!err); };
    var done = function () { say('Copied ' + value.split('\n').length + ' lines to the clipboard.'); };
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

  function start() {
    sizeFrames();
    offerFit();
    frames();
    railCover();
    if (location.hash) onHash(); else setCurrent(compute());
  }
  start();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { current = null; start(); });
})();
