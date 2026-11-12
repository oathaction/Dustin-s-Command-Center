/* Grouped bar (coverage plan 3.1, extended; S22). Two to four series side by side within each category: one horizontal
 * bar per series from a zero line, in the four-ink order (cat-1 to cat-4, the fourth hatched), each value printed at its
 * bar's end. The first group names each series after its value, so the chart needs no key.
 * Category names sit at the left, or above each group on a phone.
 * encode: category (category), series (category), value (number).
 * labels: series ({series value: printed name}, in the order the bars draw), categories ({category: printed name}).
 * formats: value. scale: x ([lo, hi]). */
(function (K) {
  'use strict';
  var INK = ['cat-1', 'cat-2', 'cat-3', 'cat-4'];
  K.register_chart({
    form: 'grouped-bar',
    name: 'Grouped Bar',
    family: 'comparison',
    encode: { category: 'category', series: 'category', value: 'number' },
    labels: ['series', 'categories'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ek = c.field('category'), es = c.field('series'), ev = c.field('value');
      var f = c.spec.formats || {}, W = c.width, L = c.labels, cnames = L.categories || {}, snames = L.series || {};
      var cats = [], series = Object.keys(snames), at = {};
      rows.forEach(function (r) {
        var k = String(r[ek]), s = String(r[es]);
        if (cats.indexOf(k) < 0) cats.push(k);
        if (series.indexOf(s) < 0) series.push(s);
        at[k + '\u0000' + s] = r;
      });
      if (series.length > 4) c.warn('more than four series: split into small multiples (Rule 14.8)');
      var cname = function (k) { return cnames[k] !== undefined ? cnames[k] : k; };
      var sname = function (s) { return snames[s] !== undefined ? snames[s] : s; };
      var val = function (r) { return K.fmt(r[ev], f.value || 'number:1'); };
      var size = c.size('label'), y = 0;
      if (series.length > 3) c.pattern('g4', 'cat-4');
      // the measures
      var bh = c.t('bar-dense-height'), inner = 2, ggap = c.phone ? 14 : 16, lh = Math.round(size * 1.25);
      var lmax = c.phone ? W : Math.floor(W * 0.3), lw = 0, vw = 0;
      cats.forEach(function (k) { c.wrap(cname(k), 'label', lmax, 600).forEach(function (l) { lw = Math.max(lw, c.measure(l, 'label', 600)); }); });
      rows.forEach(function (r) { vw = Math.max(vw, c.measure(val(r), 'label', 600, true)); });
      var x0 = c.phone ? 0 : Math.ceil(lw + 20);
      var vals = rows.map(function (r) { return r[ev]; });
      var dom = (c.spec.scale || {}).x || [Math.min(0, Math.min.apply(null, vals)), Math.max(0, Math.max.apply(null, vals))];
      var xs = K.scale.linear(dom, [x0, Math.max(x0 + 60, W - vw - 10)]), zx = xs(0);
      var gh = series.length * bh + (series.length - 1) * inner;
      var gy = y + (c.phone ? size + 6 : 4), top = gy, bottom = gy;
      cats.forEach(function (k, gi) {
        var lines = c.wrap(cname(k), 'label', lmax, 600).length;
        if (gi) gy += gh + ggap + (c.phone ? lines * lh + 4 : 0);
        if (c.phone) c.text(0, gy - 7 - (lines - 1) * lh, cname(k), { role: 'label', weight: 600, max: lmax });
        else c.text(0, gy + gh / 2 + size * 0.35 - (lines - 1) * lh / 2, cname(k), { role: 'label', weight: 600, max: lmax });
        series.forEach(function (s, si) {
          var r = at[k + '\u0000' + s];
          if (!r) return;
          var by = gy + si * (bh + inner), xe = xs(r[ev]), cy = by + bh / 2;
          var o = { kind: 'bar', axis: 'x', zero: zx, data: { key: k + '|' + s, field: ev, value: r[ev] } };
          if (si === 3) {
            c.rect(Math.min(zx, xe), by, Math.abs(xe - zx), bh, Object.assign({ pattern: 'g4' }, o));
            c.rect(Math.min(zx, xe) + 0.5, by + 0.5, Math.max(0, Math.abs(xe - zx) - 1), bh - 1, { stroke: 'cat-4', mark: false });
          } else c.rect(Math.min(zx, xe), by, Math.abs(xe - zx), bh, Object.assign({ fill: INK[si] }, o));
          var neg = r[ev] < 0;
          var vb = c.text(neg ? xe - 6 : xe + 6, cy + size * 0.35, val(r), { role: 'label', weight: 600, tnum: true, anchor: neg ? 'end' : 'start' });
          // the first group names each series after its value, so no key is needed (Rule 14.3)
          if (gi === 0) c.text(neg ? vb.x - 8 : vb.x + vb.w + 8, cy + size * 0.35, sname(s), { role: 'label', weight: 400, anchor: neg ? 'end' : 'start' });
          bottom = by + bh;
        });
        if (c.phone) c.line(zx, gy - 3, zx, gy + gh + 3, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      });
      if (!c.phone) c.line(zx, top - 4, zx, bottom + 4, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
