/* System 5, Architecture: page glue around atlas-kit.js. Inlined by build_system.py after the kit.
   1. The panel lives in the current view's slot, so it stands beside the drawing it explains.
   2. Both buildings (the glance and the full one) draw their return line and outside-force stubs from measured boxes.
   3. The panel's kind line becomes a two-part ID chip (M3). The view tabs mark the current view.
   4. Fix pass: floors in the glance jump to the full building; the skip link lands on the view's heading and keeps the
      hash; a drawing that takes focus says how the arrow keys work; on a phone the tapped item moves above the sheet. */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const NS = 'http://www.w3.org/2000/svg';
  const RM = matchMedia('(prefers-reduced-motion: reduce)');
  const PHONE = matchMedia('(max-width: 899.98px)');
  const panel = $('[data-ak-panel]');
  const smooth = () => (RM.matches ? 'auto' : 'smooth');

  function viewFromHash() {
    const h = decodeURIComponent(location.hash.slice(1)).toLowerCase().split('/')[0];
    if (h && $(`[data-view-root="${h}"]`)) return h;
    const host = h && $(`[data-view-root] [data-select="${h}"]`);
    if (host) return host.closest('[data-view-root]').dataset.viewRoot;
    if (h && document.getElementById(h)) return null;
    return 'overview';
  }
  function placePanel() {
    const v = viewFromHash(); if (!v || !panel) return;
    const slot = $(`[data-view-root="${v}"] [data-panel-slot]`);
    if (slot && panel.parentNode !== slot) slot.append(panel);
  }
  function view() { return (window.AtlasKit && AtlasKit.state().view) || viewFromHash() || 'overview'; }
  function tabs() {
    const v = view();
    $$('[data-tab]').forEach((a) => { if (a.dataset.tab === v) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
  }
  placePanel();
  addEventListener('hashchange', placePanel);          // registered before the kit, so the panel moves first

  // the kind line: "Variable C3" becomes a chip with the full type word
  const kind = panel && $('[data-ak-panel-kind]', panel);
  if (kind) {
    new MutationObserver(() => {
      const t = kind.textContent;
      if (kind.dataset.done === t) return;
      const m = t.match(/^(Variable|Connection|Loop|Reform|Area|Question) (\S+)$/);
      if (m) kind.innerHTML = `<span class="chip"><span class="k">${m[1]}</span><span class="c">${m[2]}</span></span>`;
      kind.dataset.done = kind.textContent;
    }).observe(kind, { childList: true, characterData: true, subtree: true });
  }

  // ------------------------------------------------------------------ the buildings' lines
  const el = (tag, attrs, parent) => { const x = document.createElementNS(NS, tag); for (const k in attrs) x.setAttribute(k, attrs[k]); if (parent) parent.append(x); return x; };
  function head(g, x, y, dir, len, base, cls) {
    const s = dir === 'right' ? 1 : -1;
    el('path', { class: cls, d: `M${x} ${y}L${x - s * len} ${y - base / 2}L${x - s * len} ${y + base / 2}Z` }, g);
  }
  // One drawing routine for both buildings. The return line carries the same weight as the joints' arrows (3 px):
  // the building is a circuit, and nothing on it reads as a one-way ladder.
  function drawLines(b, o) {
    if (!b || !b.getClientRects().length) return;
    const svg = $('svg.bl-lines', b); const R = b.getBoundingClientRect();
    if (!R.width) return;
    const box = (n) => { const r = n.getBoundingClientRect(); return { l: r.left - R.left, t: r.top - R.top, r: r.right - R.left, b: r.bottom - R.top, h: r.height }; };
    const F = {}; $$(o.floors, b).forEach((f) => { F[f.dataset.floor] = box(f); F[f.dataset.floor].xin = +f.dataset.xin || 0; });
    svg.replaceChildren();
    svg.setAttribute('viewBox', `0 0 ${R.width} ${R.height}`);
    const E = F.E, A = F.A, EC = F.EC; if (!E || !A || !EC) return;
    const xr = Math.max(9, Math.round(E.l / 2) - 4) + 0.5;
    const yOf = (f) => Math.round(f.t + Math.min(o.anchor, f.h / 2)) + 0.5;
    const yE = yOf(E), yA = yOf(A), yEC = yOf(EC);
    const g = el('g', { 'data-mirror': 'flow-return' }, svg);
    const r = o.bend;
    el('path', { class: 'rl', 'stroke-width': 3, d: `M${E.l} ${yE}H${xr + r}Q${xr} ${yE} ${xr} ${yE + r}V${yA - r}Q${xr} ${yA} ${xr + r} ${yA}H${A.l - 13}` }, g);
    head(g, A.l, yA, 'right', 13, 11, 'rl-hd');
    el('path', { class: 'rl', 'stroke-width': 3, d: `M${xr} ${yA}V${yEC - r}Q${xr} ${yEC} ${xr + r} ${yEC}H${EC.l - 13}` }, g);
    head(g, EC.l, yEC, 'right', 13, 11, 'rl-hd');
    const mid = (xr + A.l) / 2 + 4;
    if (A.l - xr > 22) {
      el('text', { class: 'rl-n', x: mid, y: yA - 8, 'text-anchor': 'middle' }, g).textContent = b.dataset.retA;
      el('text', { class: 'rl-n', x: mid, y: yEC - 8, 'text-anchor': 'middle' }, g).textContent = b.dataset.retEc;
    }
    if (o.leader) {
      const ret = $(o.leader, b); if (ret && ret.getClientRects().length) {
        const T = box(ret);
        el('path', { class: 'leader', d: `M${xr} ${Math.round(T.b) + 6}V${yE - 16}` }, svg);
      }
    }
    if (o.ground) el('path', { class: 'grade', d: `M0 ${EC.t + 1.5}H${EC.r}` }, svg);
    const ox = $(o.out, b); if (ox && ox.getClientRects().length) {
      const O = box(ox);
      if (O.l > E.r) {
        if (o.outLeader) {
          const oh = $(o.outLeader, b);
          if (oh && oh.getClientRects().length) {
            const H = box(oh), cx = Math.round(O.l + 20) + 0.5;
            el('path', { class: 'leader', d: `M${cx} ${Math.round(H.b) + 6}V${O.t - 4}` }, svg);
          }
        }
        Object.keys(F).forEach((k) => {
          const f = F[k]; if (!f.xin || f.b > O.b + 1) return;
          const y = yOf(f);
          el('path', { class: 'stub', 'stroke-width': 2, d: `M${O.l} ${y}H${f.r + 10}` }, svg);
          head(svg, f.r, y, 'left', 10, 8, 'stub-hd');
          if (O.l - f.r > 20) el('text', { class: 'stub-n', x: (O.l + f.r) / 2 + 3, y: y - 7, 'text-anchor': 'middle' }, svg).textContent = f.xin;
        });
      }
    }
  }
  function drawAll() {
    drawLines($('.bldg'), { floors: '.floor', out: '.outside', anchor: 44, bend: 12, leader: '.roof .ret', outLeader: '.roof .ox-roof', ground: true });
    drawLines($('.gl'), { floors: '.gl-row', out: '.gl-out', anchor: 99, bend: 8 });
    mirror();
  }
  // the return line copies its button's lit and selected states, so it lights and takes the red with it
  function mirror() {
    $$('.bldg svg.bl-lines [data-mirror]').forEach((g) => {
      const src = $(`.bldg [data-select="${g.dataset.mirror}"]`);
      g.classList.toggle('ak-rel', !!src && src.classList.contains('ak-rel'));
      ['data-red', 'data-red-job'].forEach((a) => { if (src && src.hasAttribute(a) && src.hasAttribute('data-ak-sel')) g.setAttribute(a, src.getAttribute(a)); else g.removeAttribute(a); });
    });
  }
  let raf = 0;
  const later = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(drawAll); };
  ['.bldg', '.gl'].forEach((s) => { const n = $(s); if (n && 'ResizeObserver' in window) new ResizeObserver(later).observe(n); });
  addEventListener('resize', later);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(later);
  const ov = $('[data-view-root="overview"]');
  if (ov) new MutationObserver(() => requestAnimationFrame(mirror)).observe(ov, { attributes: true, subtree: true, attributeFilter: ['class', 'data-ak-sel', 'data-red'] });

  // hover previews pause while the page scrolls under a still pointer, so the reader lands on what they picked
  let quiet = 0;
  window.addEventListener('pointerover', (ev) => { if (performance.now() < quiet) ev.stopPropagation(); }, true);

  // a floor in the glance jumps to that floor in the full building and opens it in the panel
  document.addEventListener('click', (ev) => {
    const go = ev.target.closest('[data-floor-go]'); if (!go || !window.AtlasKit) return;
    const key = go.dataset.floorGo;
    AtlasKit.select(key);
    quiet = performance.now() + 1200;
    const pid = key.replace('area-', '').toUpperCase();
    const target = $(`.bldg .floor[data-floor="${pid}"]`) || $('.bldg .outside');
    if (target) target.scrollIntoView({ block: 'start', behavior: smooth() });
  });

  // a question lights its tiles; bring the first lit tile into view
  document.addEventListener('click', (ev) => {
    const q = ev.target.closest('.qq'); if (!q) return;
    setTimeout(() => {
      if (!q.hasAttribute('data-ak-sel')) return;
      quiet = performance.now() + 1200;
      const lit = $$('.bldg .tile.ak-rel');
      const target = lit.length ? lit[0] : $('.bldg');
      target.scrollIntoView({ block: lit.length && !PHONE.matches ? 'center' : 'start', behavior: smooth() });
    }, 30);
  });

  // on a phone, the item the reader picked moves into the band above the sheet before the sheet covers it
  function aboveSheet(item) {
    if (!PHONE.matches || !item || !item.getClientRects().length || (panel && panel.hidden)) return;
    const r = item.getBoundingClientRect(), band = innerHeight * 0.52 - 12;
    if (r.top >= 8 && r.bottom <= band) return;
    const want = Math.max(8, (band - r.height) / 2);
    quiet = performance.now() + 900;
    window.scrollBy({ top: r.top - want, behavior: 'auto' });
  }
  document.addEventListener('click', (ev) => {
    const it = ev.target.closest('[data-select]'); if (!it || it.closest('.qcards')) return;
    setTimeout(() => aboveSheet($$(`[data-select="${it.dataset.select}"]`).find((x) => x.getClientRects().length && x.hasAttribute('data-ak-sel'))), 0);
  });

  // skip link: land on the view's heading and keep the view's address
  const skip = $('.skip');
  if (skip) skip.addEventListener('click', (ev) => {
    ev.preventDefault();
    const h = $(`[data-view-root="${view()}"] [data-ak-heading]`);
    if (h) { h.setAttribute('tabindex', '-1'); h.focus(); h.scrollIntoView({ block: 'start' }); }
  });

  // a drawing that takes focus says how its arrow keys work, in its readout line
  const HINT = 'Arrow keys move between items. Enter opens one.';
  document.addEventListener('focusin', (ev) => {
    const d = ev.target.closest && ev.target.closest('[data-ak-roving]'); if (!d) return;
    if (ev.relatedTarget && d.contains(ev.relatedTarget)) return;
    const scope = d.closest('.blk, .vmain, .lsec, .qsec, [data-view-root]');
    const ro = scope && $('[data-ak-readout]', scope);
    if (ro) setTimeout(() => { if (!ro.textContent.startsWith(HINT)) ro.textContent = `${HINT} ${ro.textContent}`; }, 0);
  });

  window.addEventListener('DOMContentLoaded', () => { tabs(); later(); });
  addEventListener('hashchange', () => setTimeout(() => { tabs(); later(); }, 0));
  window.AtlasSystem = { draw: drawAll };
  if (window.AtlasKit) { AtlasKit.init(); tabs(); later(); }
})();
