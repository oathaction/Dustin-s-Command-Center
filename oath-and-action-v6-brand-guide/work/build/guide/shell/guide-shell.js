// Oath & Action Brand Guide, Edition 06: the guide shell's script. guide_build.py inlines it at the end of the page.
// Built from the Gate 1 wireframe's interaction model (work/boards/phase-1/navigation/wireframe.js):
// marks the current part, chapter and rule; moves focus to the heading a link lands on; offers a way back after a
// cross-reference; runs the phone menu as a modal dialog; makes a specimen frame a keyboard-scrollable region only when
// its true-size specimen is wider than the screen; and drives the Copy buttons with a status line.
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
      var wait = pinnedUntil - Date.now();
      if (wait > 0) { clearTimeout(pinTimer); pinTimer = setTimeout(function () { setCurrent(compute()); }, wait + 20); return; }
      setCurrent(compute());
    });
  }, { passive: true });

  // Cross-references remember where the reader came from.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.xref');
    if (!a) return;
    var origin = a.closest('.rule[id], .closer[id], [data-track]');
    var sec = sectionFor(a);
    if (!origin || !sec) return;
    var what = '';
    if (!origin.matches('[data-track]')) {
      var h = origin.querySelector('h3');
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
    // Focus moves to the heading the link points at, so the next Tab continues from there.
    var h = host.matches('h1, h2, h3') ? host : host.querySelector('h1, h2, h3');
    if (host.id === 'main') h = host;
    if (h) { if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    if (pendingReturn && sec && pendingReturn.id !== id) {
      var slot = $('.return', sec);
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

  // A frame whose true-size specimen or table is wider than the screen becomes a named, focusable region, so a
  // keyboard can scroll it; a frame that fits stays out of the Tab order.
  function frames() {
    $$('[data-plate-scroll]').forEach(function (box) {
      var wide = box.scrollWidth > box.clientWidth + 1;
      var fig = box.closest('.plate');
      if (fig) fig.classList.toggle('is-wide', wide);
      if (wide) {
        if (!box.hasAttribute('tabindex')) {
          var stage = box.querySelector('[data-specimen]');
          var cap = box.querySelector('caption');
          var name = stage ? 'Specimen at true size, wider than the screen. Scroll sideways.' : (cap ? cap.textContent + '. Scroll sideways.' : 'Wide table. Scroll sideways.');
          box.setAttribute('tabindex', '0');
          box.setAttribute('role', 'region');
          box.setAttribute('aria-label', name);
        }
        if (fig && !fig.querySelector('.plate-hint')) {
          var hint = document.createElement('p');
          hint.className = 'plate-hint';
          hint.textContent = 'Shown at true size, wider than this screen. Scroll the frame sideways to see all of it.';
          box.insertAdjacentElement('afterend', hint);
        }
      } else if (box.getAttribute('role') === 'region') {
        box.removeAttribute('tabindex'); box.removeAttribute('role'); box.removeAttribute('aria-label');
      }
    });
  }
  var rt = null;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(frames, 120); });

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
    frames();
    if (location.hash) onHash(); else setCurrent(compute());
  }
  start();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { current = null; start(); });
})();
