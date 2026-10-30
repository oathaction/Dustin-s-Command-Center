/* atlas-kit.js: shared interaction kit for the twelve atlas concepts. Oath & Action Edition 06, Phase 2, October 30, 2026.
   Spec: work/handoffs/phase-2/20261030_Atlas-Interaction-Memo.md. Framework-free; inline it at the end of <body> with
   atlas-kit.css, then call AtlasKit.init(). The concept draws; the kit only reads these hooks:
     [data-view-root="area-c"] data-crumb="Area C, Electoral competition" data-parent="overview"   one per level
       (optional data-ak-reform="reform-r-01": a reform the view shows by default, whose targets take the red)
     [data-ak-heading]  heading focused after a move down      a[href="#area-c"]  a move between levels (pushes history)
     [data-select="var-c3"] data-rel="link-l25 var-c2" data-say="..."   a selectable item, what it lights, its readout
     [data-ak-roving] data-ak-nav="spatial|sequence" [data-ak-wrap]     one tab stop per drawing; arrow keys inside
     template[data-detail="var-c3"] data-kind="Variable C3" data-title="Electoral pressure"   the panel content
     [data-ak-panel] > [data-ak-panel-kind] [data-ak-panel-title] [data-ak-panel-body] [data-ak-close] [data-ak-sheet-toggle]
     [data-ak-pick="var-c2"]  a button in a panel body that selects another item in the same view
     [data-ak-crumbs] [data-ak-status] [data-ak-readout] [data-locate="area-c"] [data-ak-full="region-id"] [data-ak-stepper]
   Hash grammar: #<view>[/<selection>], e.g. #overview, #area-c/var-c3, #loop-r10/reform-r-01. A level change pushes
   a history entry; a selection replaces the current one, so Back always moves by level. */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const RM = matchMedia('(prefers-reduced-motion: reduce)'), ITEM = '[data-select], a[href^="#"]';
  const vis = (el) => !!el && el.isConnected && el.getClientRects().length > 0;
  const rootOf = (v) => v && $(`[data-view-root="${v}"]`);
  const S = { view: null, sel: null, origin: {}, invoker: null, base: document.title, opts: {}, stops: [] };

  // 1. Where am I: the chain of views from the overview down feeds the breadcrumb, the locator and the title.
  function chain(v) { const out = []; for (let r = rootOf(v); r; r = rootOf(r.dataset.parent)) out.unshift(r); return out; }
  function crumbs(list) {
    $$('[data-ak-crumbs]').forEach((nav) => {
      const ol = document.createElement('ol');
      list.forEach((r, k) => {
        const li = document.createElement('li'), last = k === list.length - 1, x = document.createElement(last ? 'span' : 'a');
        x.textContent = r.dataset.crumb || r.dataset.viewRoot;
        if (last) x.setAttribute('aria-current', 'page'); else x.href = '#' + r.dataset.viewRoot;
        li.append(x); ol.append(li);
      });
      nav.replaceChildren(ol);
    });
  }
  function say(msg) { const st = $('[data-ak-status]'); if (st) st.textContent = msg; }
  function heading(r) { const h = $('[data-ak-heading]', r) || $('h1, h2', r); if (h && !h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1'); return h; }
  // 2. The router. An unknown view falls back to the first view with a message. A key with no view of its own
  //    (an area this concept does not draw up close) opens in the panel of the view that holds it.
  function parse() {
    const [v, s] = decodeURIComponent(location.hash.slice(1)).toLowerCase().split('/');
    if (rootOf(v)) return { view: v, sel: s || null };
    const host = v && $(`[data-view-root] [data-select="${v}"]`);
    if (host) return { view: host.closest('[data-view-root]').dataset.viewRoot, sel: v };
    if (v) say(`This page has no view called ${v}. Showing the overview.`);
    return { view: $('[data-view-root]').dataset.viewRoot, sel: null };
  }
  function route(how) {
    const h = decodeURIComponent(location.hash.slice(1));
    if (how !== 'load' && h && !rootOf(h.toLowerCase().split('/')[0]) && document.getElementById(h)) return;   // a plain in-page anchor
    say('');
    const prev = S.view, { view, sel } = parse(), moved = view !== prev;
    const up = moved && !!prev && chain(prev).some((r) => r.dataset.viewRoot === view);
    const from = moved && !up && vis(S.origin[prev]) ? S.origin[prev].getBoundingClientRect() : null;
    const root = rootOf(view), list = chain(view);
    if (moved) {
      $$('[data-view-root]').forEach((r) => { r.hidden = r !== root; });
      S.view = view; S.sel = null; crumbs(list);
      $$('[data-locate]').forEach((x) => x.classList.toggle('ak-here', list.some((r) => r.dataset.viewRoot === x.dataset.locate)));
      document.title = (root.dataset.crumb || view) + ' | ' + S.base;
    }
    select(sel, {});
    if (!moved || how === 'load') return;
    // Focus: going up returns to the item the reader left from; going down lands on the selection or the heading.
    const back = S.origin[view];
    if (!up) scrollTo(0, 0);
    focusItem(up && root.contains(back) && vis(back) ? back : $('[data-ak-sel]', root) || heading(root));
    // Motion: the view lands from the point that opened it, or settles back onto it. CSS drops it under reduced motion.
    const at = from || (up && vis(back) ? back.getBoundingClientRect() : null), rr = root.getBoundingClientRect();
    root.style.transformOrigin = at ? `${at.left + at.width / 2 - rr.left}px ${at.top + at.height / 2 - rr.top}px` : '50% 0';
    root.classList.remove('ak-in', 'ak-out'); void root.offsetWidth; root.classList.add(up ? 'ak-out' : 'ak-in');
  }
  // 3. Selection, with the red rule as DR-18 reads it.
  function select(key, o) {
    const root = rootOf(S.view), item = key && $(`[data-select="${key}"]`, root);
    $$('[data-ak-sel]').forEach((x) => { x.removeAttribute('data-ak-sel'); if (x.hasAttribute('aria-pressed')) x.setAttribute('aria-pressed', 'false'); });
    S.sel = item ? key : null;
    if (item) { item.setAttribute('data-ak-sel', ''); if (item.hasAttribute('aria-pressed')) item.setAttribute('aria-pressed', 'true'); }
    paint(root); light(item); panel(item, o);
    history.replaceState(history.state, '', '#' + S.view + (S.sel ? '/' + S.sel : ''));
  }
  // One working red per view. A reform in view (selected, or named by data-ak-reform) gives it to the reform's targets
  // and sends selection to ink; with no reform in view the selected item may take it. Never on a Prussian surface.
  function paint(root) {
    $$('[data-ak-red]').forEach((x) => { x.classList.remove('ak-target'); ['data-red', 'data-red-job', 'data-ak-red'].forEach((a) => x.removeAttribute(a)); });
    if (!root || (root.closest('[data-surface]') || { dataset: {} }).dataset.surface === 'prussian') return;
    const mark = (x, job) => { x.setAttribute('data-red', 'working'); x.setAttribute('data-red-job', job); x.setAttribute('data-ak-red', ''); };
    const reform = S.sel && S.sel.startsWith('reform-') ? S.sel : root.dataset.akReform;
    const r = reform && ($(`[data-select="${reform}"]`, root) || $(`[data-select="${reform}"]`));
    if (r) (r.dataset.targets || '').split(/\s+/).filter(Boolean).forEach((t) =>
      $$(`[data-select][data-node="${t}"], [data-select][data-link="${t}"]`, root).forEach((x) => { x.classList.add('ak-target'); mark(x, (r.dataset.reform || reform) + ' targets'); }));
    const sel = $('[data-ak-sel]', root), busy = $$('[data-red="working"]', root).some((x) => vis(x) && !x.hasAttribute('data-ak-sel'));
    if (sel && !reform && !busy) mark(sel, 'selected item');
  }
  // Related marks: the item and everything in its data-rel stay in ink; the rest of the view steps to muted.
  function light(item) {
    const root = rootOf(S.view); if (!root) return;
    $$('.ak-rel').forEach((x) => x.classList.remove('ak-rel'));
    const keys = item ? [item.dataset.select, ...(item.dataset.rel || '').split(/\s+/)].filter(Boolean) : [];
    keys.forEach((k) => $$(`[data-select="${k}"]`, root).forEach((x) => x.classList.add('ak-rel')));
    if (item) item.classList.add('ak-rel');
    root.classList.toggle('ak-dim', keys.length > 1);
    $$('[data-ak-readout]', root).forEach((ro) => {
      if (ro.dataset.idle === undefined) ro.dataset.idle = ro.textContent;
      ro.textContent = item ? item.dataset.say || item.getAttribute('aria-label') || item.textContent.trim() : ro.dataset.idle;
    });
  }
  const selected = () => S.sel && $(`[data-select="${S.sel}"]`, rootOf(S.view));
  // 4. The panel: a column beside the drawing, or a bottom sheet under 900 px. It takes focus when the reader asked
  //    for it (click, Enter); closing returns focus to the item that opened it.
  function panel(item, o) {
    const p = $('[data-ak-panel]'); if (!p) return;
    if (!item) {
      const was = !p.hidden; p.hidden = true; document.documentElement.classList.remove('ak-sheet');
      if (was && o.focus && vis(S.invoker)) focusItem(S.invoker);
      return;
    }
    const key = item.dataset.select, t = (S.opts.detail && S.opts.detail(key, item)) || $(`template[data-detail="${key}"]`);
    $('[data-ak-panel-kind]', p).textContent = t ? t.dataset.kind || '' : '';
    $('[data-ak-panel-title]', p).textContent = t ? t.dataset.title : item.getAttribute('aria-label') || key;
    const body = $('[data-ak-panel-body]', p), tg = $('[data-ak-sheet-toggle]', p);
    body.replaceChildren(t ? t.content.cloneNode(true) : document.createTextNode(item.dataset.say || ''));
    $$('[data-ak-pick]', body).forEach((b) => { if (!$(`[data-select="${b.dataset.akPick}"]`, rootOf(S.view))) b.replaceWith(b.textContent); });
    if (tg) { tg.setAttribute('aria-expanded', 'false'); tg.textContent = 'More'; }
    p.classList.remove('ak-tall'); p.hidden = false; document.documentElement.classList.add('ak-sheet');
    if (o.focus) { p.scrollTop = 0; $('[data-ak-panel-title]', p).focus(); }
  }
  function close() { S.invoker = selected() || S.invoker; select(null, { focus: true }); }
  // 5. Drawings: one tab stop each (roving tabindex). Arrow keys move by position ("spatial") or along a fixed order
  //    such as a loop's links ("sequence"); Home and End jump; Enter or Space selects; Escape closes the panel.
  function setTab(d, el) { $$(ITEM, d).forEach((x) => x.setAttribute('tabindex', x === el ? '0' : '-1')); }
  function focusItem(el) { if (!el) return; const d = el.closest('[data-ak-roving]'); if (d) setTab(d, el); el.focus(); }
  function nearest(from, list, dx, dy) {
    const c = (el) => { const b = el.getBoundingClientRect(); return [b.left + b.width / 2, b.top + b.height / 2]; };
    const [x0, y0] = c(from); let best = null, score = Infinity;
    list.forEach((el) => {
      const [x, y] = c(el), along = (x - x0) * dx + (y - y0) * dy, across = Math.abs((x - x0) * dy + (y - y0) * dx);
      const s = along + 2 * across + (across > along ? 1e4 : 0);   // prefer the 45-degree cone in the pressed direction
      if (el !== from && along > 1 && s < score) { score = s; best = el; }
    });
    return best;
  }
  const KEYS = { ArrowRight: [1, 0], ArrowLeft: [-1, 0], ArrowDown: [0, 1], ArrowUp: [0, -1] };
  function onKey(e) {
    const p = $('[data-ak-panel]');
    if (e.key === 'Escape' && p && !p.hidden && !$('dialog[open]')) { e.preventDefault(); close(); return; }
    const d = e.target.closest && e.target.closest('[data-ak-roving]'), it = d && e.target.closest(ITEM);
    if (!it || !d.contains(it)) return;
    if ((e.key === 'Enter' || e.key === ' ') && !it.matches('a')) { e.preventDefault(); it.dispatchEvent(new MouseEvent('click', { bubbles: true })); return; }
    if (!KEYS[e.key] && e.key !== 'Home' && e.key !== 'End') return;
    e.preventDefault();
    const list = $$(ITEM, d).filter(vis), i = list.indexOf(it), step = KEYS[e.key] ? KEYS[e.key][0] + KEYS[e.key][1] : 0;
    const wrap = (j) => (d.hasAttribute('data-ak-wrap') ? list[(j + list.length) % list.length] : list[j]);
    focusItem(e.key === 'Home' ? list[0] : e.key === 'End' ? list[list.length - 1]
      : d.dataset.akNav === 'sequence' ? wrap(i + step) : nearest(it, list, ...KEYS[e.key]));
  }
  // 6. Pointer, focus and touch. Hover only previews what focus and a tap also give: the lit marks and the readout.
  function onClick(e) {
    const dlg = e.target.closest('dialog.ak-full'), q = (s) => e.target.closest(s);
    if (dlg && q(ITEM)) dlg.akShut(false);                       // in full size, a click returns to the page first
    const a = q('a[href^="#"]'), pick = q('[data-ak-pick]'), it = q('[data-select]'), tg = q('[data-ak-sheet-toggle]');
    if (a) { const r = rootOf(S.view); S.origin[S.view] = r && r.contains(a) ? a : selected(); }
    else if (pick) { const x = $(`[data-select="${pick.dataset.akPick}"]`, rootOf(S.view)); if (x) { S.invoker = x; select(pick.dataset.akPick, { focus: true }); } }
    else if (it) { S.invoker = it; select(it.dataset.select === S.sel ? null : it.dataset.select, { focus: true }); }
    else if (q('[data-ak-close]')) close();
    else if (tg) { const tall = $('[data-ak-panel]').classList.toggle('ak-tall'); tg.setAttribute('aria-expanded', String(tall)); tg.textContent = tall ? 'Less' : 'More'; }
    else if (q('[data-ak-full]')) full(q('[data-ak-full]'));
    else if (q('[data-ak-roving]') && S.sel) select(null, {});       // a click on empty map space clears the selection
  }
  function hoverItem(e) { const it = e.target.closest && e.target.closest(ITEM); return it && it.closest('[data-ak-roving]') && rootOf(S.view).contains(it) ? it : null; }

  // Full size: moves a scroll region's drawing into a modal <dialog>. Escape or "Close full size" puts it back at once,
  // so a click on an item inside can select it or move a level.
  function full(btn) {
    const reg = document.getElementById(btn.dataset.akFull); if (!reg) return;
    const dlg = document.createElement('dialog'), x = document.createElement('button'), kids = [...reg.childNodes];
    dlg.className = 'ak-full'; dlg.setAttribute('aria-label', (reg.getAttribute('aria-label') || 'Drawing') + ', full size');
    x.type = 'button'; x.className = 'ak-btn'; x.textContent = 'Close full size';
    dlg.akShut = (refocus) => { if (!dlg.isConnected) return; dlg.close(); reg.append(...kids); dlg.remove(); if (refocus) btn.focus(); };
    x.addEventListener('click', () => dlg.akShut(true));
    dlg.addEventListener('cancel', (ev) => { ev.preventDefault(); dlg.akShut(true); });
    dlg.append(x, ...kids); reg.after(dlg); dlg.showModal(); x.focus();
  }
  // A scroll region is a tab stop only while it scrolls, so a wide screen keeps one stop per drawing.
  function fit() { $$('.ak-scroll[role="region"]').forEach((r) => { r.tabIndex = r.scrollWidth > r.clientWidth + 1 ? 0 : -1; }); }

  // 7. Loop step-through. [data-ak-stepper] holds buttons [data-ak-step="play|prev|next|reset"], a [data-ak-step-status]
  //    line (aria-live="polite") and a list whose items carry data-ak-step-keys="link-l08 var-c2", one per numbered link.
  //    The list is the still sequence. Marks with data-ak-at="n" show from step n. Play advances every data-ak-hold ms
  //    and stops after the closing link (nothing loops). A runner travels each link unless reduced motion is set.
  function stepper(box) {
    const view = box.closest('[data-view-root]'), steps = $$('[data-ak-step-keys]', box), n = steps.length;
    const btn = (k) => $(`[data-ak-step="${k}"]`, box), status = $('[data-ak-step-status]', box);
    const hold = +box.dataset.akHold || 3200, keysOf = (k) => steps[k].dataset.akStepKeys.split(/\s+/);
    let i = 0, timer = null;
    if (status) status.dataset.idle = status.textContent;
    function go(j) {
      const fwd = j > i; i = Math.max(0, Math.min(n, j));
      $$('.ak-now, .ak-done', view).forEach((x) => x.classList.remove('ak-now', 'ak-done'));
      steps.forEach((li, k) => (k === i - 1 ? li.setAttribute('aria-current', 'step') : li.removeAttribute('aria-current')));
      for (let k = 0; k < i; k++) keysOf(k).forEach((key) => $$(`[data-select="${key}"]`, view).forEach((x) => x.classList.add(k === i - 1 ? 'ak-now' : 'ak-done')));
      $$('.ak-now', view).forEach((x) => x.classList.remove('ak-done'));
      $$('[data-ak-at]', view).forEach((m) => m.toggleAttribute('hidden', +m.dataset.akAt > i));   // SVG has no .hidden
      view.classList.toggle('ak-stepping', i > 0);
      const end = i === n && box.dataset.akEnd ? ' ' + box.dataset.akEnd : '';
      if (status) status.textContent = i ? `Step ${i} of ${n}. ${steps[i - 1].textContent.trim()}${end}` : status.dataset.idle;
      if (fwd && i) run(i - 1);
    }
    function run(k) {
      const path = keysOf(k).map((key) => $(`[data-select="${key}"] path.ak-mark`, view)).find(Boolean);
      if (RM.matches || !path) return;
      const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle'), L = path.getTotalLength(), t0 = performance.now();
      dot.setAttribute('r', '5'); dot.setAttribute('class', 'ak-runner'); dot.setAttribute('aria-hidden', 'true'); path.parentNode.append(dot);
      (function f(t) {   // 560 ms, easing out, the token "draw" duration
        const u = Math.min(1, (t - t0) / 560), pt = path.getPointAtLength(L * (1 - Math.pow(1 - u, 3)));
        dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y);
        if (u < 1) requestAnimationFrame(f); else dot.remove();
      })(t0);
    }
    const label = () => { if (btn('play')) btn('play').textContent = timer ? 'Pause' : i >= n ? 'Play again' : 'Play'; };
    const stop = () => { clearTimeout(timer); timer = null; label(); };
    const tick = () => { go(i + 1); timer = i < n ? setTimeout(tick, hold) : null; label(); };
    box.addEventListener('click', (e) => {
      const a = e.target.closest('[data-ak-step]') && e.target.closest('[data-ak-step]').dataset.akStep; if (!a) return;
      if (a === 'play') { if (timer) stop(); else { if (i >= n) go(0); tick(); } return; }
      go(a === 'next' ? i + 1 : a === 'prev' ? i - 1 : 0); stop();
    });
    go(0); S.stops.push(stop);
  }
  // 8. Start once, after the page markup. opts.detail(key, item) may return a <template> for the panel.
  function init(opts) {
    S.opts = opts || {};
    $$('[data-ak-roving]').forEach((d) => $$(ITEM, d).forEach((x, k) => x.setAttribute('tabindex', k ? '-1' : '0')));
    $$('[data-select]').forEach((x) => { if (x.matches('button, [role="button"]') && !x.hasAttribute('aria-pressed')) x.setAttribute('aria-pressed', 'false'); });
    $$('[data-ak-stepper]').forEach(stepper);
    document.addEventListener('keydown', onKey);
    document.addEventListener('click', onClick);
    document.addEventListener('pointerover', (e) => { const it = e.pointerType === 'mouse' && hoverItem(e); if (it) light(it); });
    document.addEventListener('pointerout', (e) => { const it = e.pointerType === 'mouse' && hoverItem(e); if (it && !it.contains(e.relatedTarget)) light(selected()); });
    document.addEventListener('focusin', (e) => { const it = hoverItem(e); if (it) { setTab(it.closest('[data-ak-roving]'), it); light(it); } });
    document.addEventListener('focusout', (e) => { if (hoverItem(e)) light(selected()); });
    addEventListener('hashchange', () => { S.stops.forEach((f) => f()); route('nav'); fit(); });
    addEventListener('resize', fit);
    route('load'); fit();
  }
  window.AtlasKit = { init, select: (k) => select(k, { focus: true }), refresh: () => paint(rootOf(S.view)), state: () => ({ view: S.view, sel: S.sel }) };
})();
