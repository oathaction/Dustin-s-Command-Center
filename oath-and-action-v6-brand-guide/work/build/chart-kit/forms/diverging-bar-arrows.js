/* Diverging bar with arrows over time (coverage plan 3.2, extended; S26). One row per election or term, in time order down
 * the page; an arrow runs from a center line toward the side that holds the advantage, as long as the advantage. Every
 * arrow takes the one neutral ink, and each side's name is printed over its half and on the rows where the advantage
 * changes sides, so position and words carry the side (DR-48, DR-58).
 * encode: key (id), x (year or label for the row), left (number), right (number): the two sides' counts; the advantage is
 * right minus left. labels: left_title, right_title (words over each half), left_name, right_name (the side's name, set
 * before the figure on the first row and on each row where the advantage changes sides), value (words at each
 * arrow's tip, with {value}). formats: x (the row's
 * label, "year" by default), value, tick. Draws through K.parts.arrow, the shared arrow. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'diverging-bar-arrows',
    name: 'Diverging Bar With Arrows',
    family: 'shift-and-swing',
    encode: { key: 'id', x: 'time', left: 'number', right: 'number' },
    labels: ['left_title', 'right_title', 'left_name', 'right_name', 'value'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, f = c.spec.formats || {}, W = c.width, ek = c.field('key'), ex = c.field('x'), elf = c.field('left'), erg = c.field('right');
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var adv = function (r) { return r[erg] - r[elf]; };
      var size = c.size('label'), pitch = Math.max(c.t('shift-axis-pitch'), Math.round(size * 1.45));
      var mx = Math.max.apply(null, rows.map(function (r) { return Math.abs(adv(r)); }));
      // the scale reaches the longest arrow, with ticks only inside it
      var nk = K.nice(0, mx, c.phone ? 2 : 3), ticks = K.ticks(0, mx, 0, nk.step);
      nk = [0, Math.max(mx, ticks[ticks.length - 1])];
      var flips = rows.map(function (r, i) { return i === 0 || (adv(r) > 0) !== (adv(rows[i - 1]) > 0); });
      // the figure at each tip; on the first row and each row where the majority changed sides, the party's name before it
      var named = true;
      var words = function (r, i) {
        var v = String(L.value || '{value}').replace('{value}', K.fmt(Math.abs(adv(r)), f.value || 'integer')), pn = adv(r) > 0 ? L.right_name : L.left_name;
        return named && flips[i] && pn ? pn + ' ' + v : v;
      };
      var lw = 0;
      rows.forEach(function (r) { lw = Math.max(lw, c.measure(K.fmt(r[ex], f.x || 'year'), 'tick', 400, true)); });
      var x0 = Math.ceil(lw + 14);
      // the arrows grow as long as every row's tip and its words still fit; the center line sits where the two sides'
      // longest reaches meet, so a side whose arrows run shorter gives its room to the other
      var reach = function (ln, sg) {
        var m = 0;
        rows.forEach(function (r, i) { var a = adv(r); if (a * sg > 0) m = Math.max(m, Math.abs(a) / nk[1] * ln + 8 + c.measure(words(r, i), 'label', 700, true)); });
        return m;
      };
      var len = W - x0;
      while (len > 20 && reach(len, -1) + reach(len, 1) > W - x0) len -= 1;
      // in a column too narrow for the names beside short arrows, the rows carry figures and the titles name the halves
      if (len < (W - x0) * 0.3) { named = false; len = W - x0; while (len > 20 && reach(len, -1) + reach(len, 1) > W - x0) len -= 1; }
      var slack = Math.max(0, W - x0 - reach(len, -1) - reach(len, 1));
      var xc = x0 + reach(len, -1) + slack / 2;
      var xs = function (v) { return xc + v / nk[1] * len; };
      // the halves' names, then the scale both ways from the center
      var y = size;
      // each half's name over it; a name with a word wider than its side takes its own line, set to the drawing's edge
      var widest = function (t) { return Math.max.apply(null, String(t).split(' ').map(function (w) { return c.measure(w, 'label', 700); })); };
      if (L.left_title) {
        if (widest(L.left_title) <= xc - 10) c.text(xc - 10, y, L.left_title, { role: 'label', weight: 700, anchor: 'end', max: xc - 10 });
        else { var lt = c.text(0, y, L.left_title, { role: 'label', weight: 700, max: W }); y = lt.bottom + size; }
      }
      if (L.right_title) {
        if (widest(L.right_title) <= W - xc - 10) c.text(xc + 10, y, L.right_title, { role: 'label', weight: 700, anchor: 'start', max: W - xc - 10 });
        else { if (L.left_title && widest(L.left_title) <= xc - 10) y += Math.round(size * 1.3); c.text(W, y, L.right_title, { role: 'label', weight: 700, anchor: 'end', max: W }); }
      }
      var tb = c.texts.length ? Math.max.apply(null, c.texts.map(function (t) { return t.bottom; })) : 0;
      var ty = tb + 8 + c.size('tick');
      // a figure at each step out from the center, skipping any that would touch the one inside it
      var placed = [];
      ticks.forEach(function (t) {
        [1, -1].forEach(function (sg) {
          if (!t && sg < 0) return;
          var s2 = K.fmt(t, f.tick || 'integer'), hw = c.measure(s2, 'tick') / 2, x = xs(sg * t);
          if (x - hw < x0 || x + hw > W) return;
          if (placed.some(function (p) { return x - hw < p[1] + 6 && p[0] < x + hw + 6; })) return;
          placed.push([x - hw, x + hw]);
          c.text(x, ty, s2, { role: 'tick', anchor: 'middle' });
        });
      });
      var top = ty + 10, end = top + pitch * rows.length;
      ticks.forEach(function (t) {
        if (!t) return;
        [-1, 1].forEach(function (sg) { if (xs(sg * t) >= x0 && xs(sg * t) <= W) c.line(xs(sg * t), top, xs(sg * t), end, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      });
      c.line(xc, top - 4, xc, end, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      rows.forEach(function (r, i) {
        var ry = top + i * pitch + pitch / 2, a = adv(r), xe = xs(a);
        c.text(0, ry + size * 0.35, K.fmt(r[ex], f.x || 'year'), { role: 'tick', tnum: true });
        if (a) K.parts.arrow(c, xc, xe, ry, { data: { key: r[ek], field: 'advantage', value: a, party: a > 0 ? 'right' : 'left' } });
        c.text(a >= 0 ? xe + 7 : xe - 7, ry + size * 0.35, words(r, i), { role: 'label', weight: flips[i] ? 700 : 400, anchor: a >= 0 ? 'start' : 'end', tnum: true, halo: true });
      });
      c.height(end + 4);
    }
  });
})(globalThis.OAChart);
