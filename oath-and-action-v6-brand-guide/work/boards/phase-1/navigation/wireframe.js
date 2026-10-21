// Guide shell wireframe for Gate 1. A proposal, not V6 code.
// Marks the current chapter in the rail, the part navigation, the header and the phone menu;
// moves focus to the heading a link lands on; offers a way back after a cross-reference;
// runs the phone menu as a modal dialog; and drives the copy and download controls.
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
  var current = null;
  var pinnedUntil = 0;
  var pendingReturn = null;
  var navigatingFromMenu = false;

  // Scroll a link into view inside its own scroll box only, never the page.
  function keepInView(el, box) {
    if (!el || !box) return;
    var e = el.getBoundingClientRect(), b = box.getBoundingClientRect();
    if (e.top < b.top + 8) box.scrollTop -= (b.top + 8 - e.top);
    else if (e.bottom > b.bottom - 8) box.scrollTop += (e.bottom - b.bottom + 8);
  }

  function sectionFor(el) {
    if (!el) return null;
    if (el.hasAttribute && el.hasAttribute('data-track')) return el;
    return el.closest ? el.closest('[data-track]') : null;
  }

  function setCurrent(sec) {
    if (sec === current) return;
    current = sec;
    $$('[data-loc][aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    $$('[data-part-link][aria-current]').forEach(function (a) { a.removeAttribute('aria-current'); });
    var label = sec ? sec.getAttribute('data-label') : 'Front matter';
    if (where) where.textContent = label;
    if (menuWhere) menuWhere.textContent = label;
    if (!sec) return;
    $$('[data-loc="' + sec.id + '"]').forEach(function (a) { a.setAttribute('aria-current', 'location'); });
    var part = sec.getAttribute('data-part');
    if (part) $$('[data-part-link="' + part + '"]').forEach(function (a) { a.setAttribute('aria-current', 'location'); });
    keepInView($('.rail [data-loc="' + sec.id + '"]'), rail);
  }

  // The current section is the last one whose top has passed a line a quarter of the way down the visible page.
  function compute() {
    var line = header.getBoundingClientRect().bottom + window.innerHeight * 0.25;
    var cur = null;
    for (var i = 0; i < tracked.length; i++) {
      if (tracked[i].getBoundingClientRect().top <= line) cur = tracked[i]; else break;
    }
    return cur;
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      if (Date.now() < pinnedUntil) return;
      setCurrent(compute());
    });
  }, { passive: true });

  // Cross-references remember where the reader came from.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.xref');
    if (!a) return;
    var origin = a.closest('[id^="rule-"], .closer[id], [data-track]');
    var sec = sectionFor(a);
    if (!origin || !sec) return;
    var what = origin.matches('[data-track]') ? '' : (origin.querySelector('h3') ? origin.querySelector('h3').textContent.replace(/\s+/g, ' ').trim() : '');
    pendingReturn = { id: origin.id, label: (what ? what + ', ' : '') + sec.getAttribute('data-label') };
  });

  function onHash() {
    var id = decodeURIComponent(location.hash.slice(1));
    $$('.return').forEach(function (p) { p.hidden = true; p.textContent = ''; });
    if (!id) { pendingReturn = null; return; }
    var target = document.getElementById(id);
    if (!target) { pendingReturn = null; return; }
    var sec = sectionFor(target);
    if (target === document.getElementById('main')) sec = null;
    if (sec) { setCurrent(sec); pinnedUntil = Date.now() + 900; }
    // Move focus to the heading the link points at, so the next Tab continues from there.
    var h = target.matches('h1, h2, h3') ? target : target.querySelector('h1, h2, h3');
    if (target.id === 'main') h = target;
    if (h) {
      if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1');
      h.focus({ preventScroll: true });
    }
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

  // Phone menu: a modal dialog listing every part and chapter.
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
    window.addEventListener('resize', function () {
      if (menu.open && window.matchMedia('(min-width: 64em)').matches) menu.close();
    });
  }

  // Copy controls with a status line.
  function statusFor(el) {
    var scope = el.closest('.rule, .downloads, .closer, section');
    return scope ? $('[role="status"]', scope) : null;
  }
  function say(st, text, isError) {
    if (!st) return;
    st.textContent = text;
    st.classList.toggle('is-error', !!isError);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button.copy');
    if (!b) return;
    var value = b.getAttribute('data-copy');
    var st = statusFor(b);
    var old = st && st.parentNode.querySelector('.copy-fallback');
    if (old) old.remove();
    var done = function () { say(st, 'Copied ' + value + ' to the clipboard.'); };
    var fail = function () {
      say(st, 'The browser blocked copying. The value is selected below: press Control and C, or Command and C.', true);
      var input = document.createElement('input');
      input.className = 'copy-fallback'; input.readOnly = true; input.value = value;
      input.setAttribute('aria-label', 'Value to copy');
      st.insertAdjacentElement('afterend', input);
      input.focus(); input.select();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(value).then(done, fail); else fail();
  });

  // Download controls with a status line. Disabled ones stay focusable and say why.
  var palette = [
    ['newsprint', '#DCD9D2'], ['charcoal', '#121212'], ['pillar-red', '#E63946'], ['prussian', '#1F2D5A'],
    ['stone', '#5D636D'], ['verdigris', '#4A7C74'], ['white', '#FFFFFF']
  ];
  function fileBody(kind) {
    if (kind === 'css') {
      return '/* Oath & Action locked palette. Draft from the Gate 1 wireframe, October 21, 2026. Not the V6 token file. */\n:root {\n' +
        palette.map(function (p) { return '  --oa-color-' + p[0] + ': ' + p[1] + ';'; }).join('\n') + '\n}\n';
    }
    var o = {}; palette.forEach(function (p) { o[p[0]] = { $value: p[1], $type: 'color' }; });
    return JSON.stringify({ $description: 'Oath & Action locked palette. Draft from the Gate 1 wireframe, October 21, 2026. Not the V6 token file.', oa: { color: o } }, null, 2) + '\n';
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button.dl');
    if (!b) return;
    var st = statusFor(b);
    if (b.getAttribute('aria-disabled') === 'true') { say(st, 'Unavailable. ' + b.getAttribute('data-reason')); return; }
    var name = b.getAttribute('data-file'), kind = b.getAttribute('data-kind');
    try {
      var body = fileBody(kind);
      var blob = new Blob([body], { type: kind === 'css' ? 'text/css' : 'application/json' });
      var url = URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      say(st, 'Download started: ' + name + ', ' + blob.size + ' bytes. Check your downloads folder.');
    } catch (err) {
      say(st, 'Error: the file did not download. Try again.', true);
    }
  });

  // Start position: the board's frames open the shell at a chapter with ?at=<id>, scrolling only this window.
  var at = new URLSearchParams(location.search).get('at');
  if (at && document.getElementById(at)) {
    var t = document.getElementById(at);
    var y = t.getBoundingClientRect().top + window.pageYOffset - header.getBoundingClientRect().height - 20;
    window.scrollTo(0, y);
  }
  if (location.hash) onHash(); else setCurrent(compute());
})();
