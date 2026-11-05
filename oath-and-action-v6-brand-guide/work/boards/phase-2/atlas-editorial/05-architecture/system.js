/* System 5, Architecture: page glue around atlas-kit.js. Inlined by build_system.py after the kit.
   1. The panel lives in the current view's slot, so it stands beside the drawing it explains.
   2. The building's return line, outside-force stubs and ground line are drawn from the floors' measured boxes.
   3. The panel's kind line becomes a two-part ID chip (M3). The view tabs mark the current view. */
(function () {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const NS = 'http://www.w3.org/2000/svg';
  const RM = matchMedia('(prefers-reduced-motion: reduce)');
  const panel = $('[data-ak-panel]');

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
  function tabs() {
    const v = (window.AtlasKit && AtlasKit.state().view) || viewFromHash();
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

  // ------------------------------------------------------------------ the building's lines
  const el = (tag, attrs, parent) => { const x = document.createElementNS(NS, tag); for (const k in attrs) x.setAttribute(k, attrs[k]); if (parent) parent.append(x); return x; };
  function head(g, x, y, dir, len, base, cls) {
    const s = dir === 'right' ? 1 : -1;
    el('path', { class: cls, d: `M${x} ${y}L${x - s * len} ${y - base / 2}L${x - s * len} ${y + base / 2}Z` }, g);
  }
  function drawBuilding() {
    const b = $('.bldg'); if (!b || !b.getClientRects().length) return;
    const svg = $('svg.bl-lines', b); const R = b.getBoundingClientRect();
    if (!R.width) return;
    const box = (n) => { const r = n.getBoundingClientRect(); return { l: r.left - R.left, t: r.top - R.top, r: r.right - R.left, b: r.bottom - R.top, h: r.height }; };
    const F = {}; $$('.floor', b).forEach((f) => { F[f.dataset.floor] = box(f); F[f.dataset.floor].xin = +f.dataset.xin || 0; });
    svg.replaceChildren();
    svg.setAttribute('viewBox', `0 0 ${R.width} ${R.height}`);
    const E = F.E, A = F.A, EC = F.EC;
    const xr = Math.max(9, Math.round(E.l / 2) - 6) + 0.5;
    const yOf = (f) => Math.round(f.t + Math.min(44, f.h / 2)) + 0.5;
    const yE = yOf(E), yA = yOf(A), yEC = yOf(EC);
    // the return line: heavy from Policy down to Wealth (the main circuit), then on to Your household
    const g = el('g', { 'data-mirror': 'flow-return' }, svg);
    el('path', { class: 'rl', 'stroke-width': 3, d: `M${E.l} ${yE}H${xr + 12}Q${xr} ${yE} ${xr} ${yE + 12}V${yA - 12}Q${xr} ${yA} ${xr + 12} ${yA}H${A.l - 13}` }, g);
    head(g, A.l, yA, 'right', 13, 11, 'rl-hd');
    el('path', { class: 'rl', 'stroke-width': 2, d: `M${xr} ${yA}V${yEC - 8}Q${xr} ${yEC} ${xr + 8} ${yEC}H${EC.l - 10}` }, g);
    head(g, EC.l, yEC, 'right', 10, 8, 'rl-hd');
    const nA = +b.dataset.retA, nEC = +b.dataset.retEc;
    const mid = (xr + A.l) / 2 + 3;
    el('text', { class: 'rl-n', x: mid, y: yA - 8, 'text-anchor': 'middle' }, g).textContent = nA;
    el('text', { class: 'rl-n', x: mid, y: yEC - 8, 'text-anchor': 'middle' }, g).textContent = nEC;
    // a 1 px leader ties the roof note to the line it names
    const ret = $('.roof .ret', b); if (ret) {
      const T = box(ret);
      el('path', { class: 'leader', d: `M${xr} ${Math.round(T.b) + 6}V${yE - 16}` }, svg);
    }
    // the ground line, under the economy layer
    el('path', { class: 'grade', d: `M0 ${EC.t + 1.5}H${EC.r}` }, svg);
    // outside forces: one stub into each floor they push on, with its count
    const ox = $('.outside', b); if (ox && ox.getClientRects().length) {
      const O = box(ox);
      if (O.l > E.r) {
        const oh = $('.roof .ox-roof', b);
        if (oh && oh.getClientRects().length) {
          const H = box(oh), cx = Math.round(O.l + 20) + 0.5;
          el('path', { class: 'leader', d: `M${cx} ${Math.round(H.b) + 6}V${O.t - 4}` }, svg);
        }
        Object.keys(F).forEach((k) => {
          const f = F[k]; if (!f.xin || f.b > O.b + 1) return;
          const y = Math.round(f.t + Math.min(44, f.h / 2)) + 0.5;
          el('path', { class: 'stub', 'stroke-width': 2, d: `M${O.l} ${y}H${f.r + 10}` }, svg);
          head(svg, f.r, y, 'left', 10, 8, 'stub-hd');
          el('text', { class: 'stub-n', x: (O.l + f.r) / 2 + 3, y: y - 7, 'text-anchor': 'middle' }, svg).textContent = f.xin;
        });
      }
    }
    mirror();
  }
  // the return line copies its button's lit and selected states, so it lights and takes the red with it
  function mirror() {
    $$('svg.bl-lines [data-mirror]').forEach((g) => {
      const src = $(`[data-select="${g.dataset.mirror}"]`);
      g.classList.toggle('ak-rel', !!src && src.classList.contains('ak-rel'));
      ['data-red', 'data-red-job'].forEach((a) => { if (src && src.hasAttribute(a) && src.hasAttribute('data-ak-sel')) g.setAttribute(a, src.getAttribute(a)); else g.removeAttribute(a); });
    });
  }
  let raf = 0;
  const later = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(drawBuilding); };
  const bl = $('.bldg');
  if (bl && 'ResizeObserver' in window) new ResizeObserver(later).observe(bl);
  addEventListener('resize', later);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(later);
  const ov = $('[data-view-root="overview"]');
  if (ov) new MutationObserver(() => requestAnimationFrame(mirror)).observe(ov, { attributes: true, subtree: true, attributeFilter: ['class', 'data-ak-sel', 'data-red'] });

  // a question lights its tiles; bring the building into view so the reader sees them. While the page scrolls under a
  // still pointer, hover previews pause, so the question's lighting is what the reader lands on.
  let quiet = 0;
  window.addEventListener('pointerover', (ev) => { if (performance.now() < quiet) ev.stopPropagation(); }, true);
  document.addEventListener('click', (ev) => {
    const q = ev.target.closest('.qq'); if (!q) return;
    setTimeout(() => {
      if (!q.hasAttribute('data-ak-sel')) return;
      quiet = performance.now() + 1200;
      const lit = $$('.bldg .tile.ak-rel');
      const target = lit.length ? lit[0] : $('.bldg');
      const phone = matchMedia('(max-width: 899.98px)').matches;
      target.scrollIntoView({ block: lit.length && !phone ? 'center' : 'start', behavior: RM.matches ? 'auto' : 'smooth' });
    }, 30);
  });

  window.addEventListener('DOMContentLoaded', () => { tabs(); later(); });
  addEventListener('hashchange', () => setTimeout(() => { tabs(); later(); }, 0));
  window.AtlasSystem = { draw: drawBuilding };
  if (window.AtlasKit) { AtlasKit.init(); tabs(); later(); }
})();
