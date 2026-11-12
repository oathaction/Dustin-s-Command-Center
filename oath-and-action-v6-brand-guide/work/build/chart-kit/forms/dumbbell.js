/* Dumbbell (coverage plan 3.1, core; S04). Two values per row on one scale: the earlier as an open dot, the later filled,
 * each value printed beside its dot, the row's words at the right edge.
 * encode: category (category), value (number), series (category: the column naming which of the two a row is).
 * labels: from, to (the series values), from_label, to_label (printed once over the first row), categories ({value: label}),
 * row_words ({category value: words}), domain ([lo, hi], in the value column's own unit as the data file holds it, before
 * any format: dollars for a column of dollars printed as billions). formats: value, tick.
 * The scale keeps room for the value printed at each end of every row, at every width (access S2, round 1 fix pass), and
 * the check fails a row whose two dots sit closer than a dot's radius, where the drawing shows no change. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'dumbbell', name: 'Dumbbell', family: 'comparison',
    encode: { category: 'category', value: 'number', series: 'category' },
    labels: ['from', 'to', 'from_label', 'to_label', 'categories', 'row_words', 'domain'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ek = c.field('category'), ev = c.field('value'), es = c.field('series');
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.categories || {}, words = L.row_words || {};
      var cats = [], pair = {};
      rows.forEach(function (r) {
        var k = String(r[ek]);
        if (!pair[k]) { pair[k] = {}; cats.push(k); }
        if (String(r[es]) === String(L.from)) pair[k].from = r;
        else if (String(r[es]) === String(L.to)) pair[k].to = r;
      });
      var vals = rows.map(function (r) { return r[ev]; });
      var dom = L.domain || K.nice(Math.min.apply(null, vals), Math.max.apply(null, vals), 4);
      var lw = 0, ww = 0;
      cats.forEach(function (k) { lw = Math.max(lw, c.measure(names[k] || k, 'label', 600)); ww = Math.max(ww, words[k] ? c.measure(words[k], 'label', 600) : 0); });
      var x0 = c.phone ? 28 : Math.ceil(lw + 40), x1 = c.phone ? W - 28 : W - ww - 48;
      // each row prints its lower value left of its left dot and its higher value right of its right dot, 12 px out; move
      // the scale's ends in until the widest of those fits between the names (or the left edge) and the row words (or the
      // right edge). A layout where every value fits keeps the ends above.
      var fv = f.value || 'number:1', lim0 = c.phone ? 0 : Math.ceil(lw + 8), lim1 = c.phone ? W : W - (ww ? ww + 8 : 0);
      var ends = cats.filter(function (k) { return pair[k].from && pair[k].to; }).map(function (k) {
        var u = pair[k].from[ev], v = pair[k].to[ev], lo = Math.min(u, v), hi = Math.max(u, v);
        return { lo: lo, hi: hi, wl: c.measure(K.fmt(lo, fv), 'label', lo === v ? 700 : 400), wr: c.measure(K.fmt(hi, fv), 'label', hi === v ? 700 : 400) };
      });
      for (var it = 0; it < 6; it++) {
        var sc = K.scale.linear(dom, [x0, x1]), need0 = 0, need1 = 0;
        ends.forEach(function (e) {
          need0 = Math.max(need0, lim0 - (sc(e.lo) - 12 - e.wl));
          need1 = Math.max(need1, (sc(e.hi) + 12 + e.wr) - lim1);
        });
        if (need0 <= 0.5 && need1 <= 0.5) break;
        if (need0 > 0.5) x0 += Math.ceil(need0);
        if (need1 > 0.5) x1 -= Math.ceil(need1);
        if (x1 - x0 < 40) { c.warn('the values at the scale\'s ends leave the plot under 40 px; shorten the names or set labels.domain'); break; }
      }
      var xs = K.scale.linear(dom, [x0, x1]), pitch = c.phone ? 62 : 46, y = c.size('tick') + 4;
      var ticks = K.ticks(dom[0], dom[1], c.phone ? 4 : 5);
      ticks.forEach(function (t, i) { c.text(xs(t), y, K.fmt(t, i === ticks.length - 1 ? (f.tick_last || f.tick || 'integer') : (f.tick || 'integer')), { role: 'tick', anchor: 'middle' }); });
      y += 30;
      var r_open = c.t('dot-open-radius'), r_fill = c.t('dot-subject-radius');
      cats.forEach(function (k, i) {
        var p = pair[k];
        if (!p.from || !p.to) { c.warn('row ' + k + ' lacks one of its two values'); return; }
        var ry = y + i * pitch + (c.phone ? 22 : 0);
        if (c.phone) c.text(0, ry - 18, names[k] || k, { role: 'label', weight: 600 });
        else c.text(0, ry + c.size('label') * 0.35, names[k] || k, { role: 'label', weight: 600 });
        if (words[k]) c.text(W, (c.phone ? ry - 18 : ry + c.size('label') * 0.35), words[k], { role: 'label', weight: 600, anchor: 'end' });
        c.line(xs(dom[0]), ry, xs(dom[1]), ry, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        var a = xs(p.from[ev]), b = xs(p.to[ev]);
        c.line(a, ry, b, ry, { stroke: 'subject', width: c.t('line-context'), mark: false });
        c.circle(a, ry, r_open, { fill: 'surface', row: k, data: { key: k + '|' + L.from, field: ev, value: p.from[ev] } });
        c.circle(a, ry, r_open, { stroke: 'subject', width: c.t('line-context'), mark: false });
        c.circle(b, ry, r_fill, { fill: 'subject', row: k, data: { key: k + '|' + L.to, field: ev, value: p.to[ev] } });
        var left = a < b ? p.from : p.to, right = a < b ? p.to : p.from;
        var lx = Math.min(a, b) - 12, rx = Math.max(a, b) + 12, ty = ry + c.size('label') * 0.35;
        c.text(lx, ty, K.fmt(left[ev], f.value || 'number:1'), { role: 'label', weight: left === p.to ? 700 : 400, anchor: 'end', fill: left === p.to ? 'label' : 'secondary' });
        c.text(rx, ty, K.fmt(right[ev], f.value || 'number:1'), { role: 'label', weight: right === p.to ? 700 : 400, fill: right === p.to ? 'label' : 'secondary' });
        if (i === 0 && L.from_label && L.to_label) {
          var wa = c.measure(L.from_label, 'tick', 600), wb = c.measure(L.to_label, 'tick', 600);
          var apart = Math.abs(a - b) > (wa + wb) / 2 + 6;
          var yy = c.phone ? ry + 22 : ry - 14;
          c.text(a, yy, L.from_label, { role: 'tick', anchor: apart ? 'middle' : (a < b ? 'end' : 'start'), weight: 600 });
          c.text(b, yy, L.to_label, { role: 'tick', anchor: apart ? 'middle' : (a < b ? 'start' : 'end'), weight: 600 });
        }
      });
      c.key([{ fill: 'subject', direct: true }, { fill: 'surface', pattern: true }]);   // the open circle reads by its outline
      c.height(y + (cats.length - 1) * pitch + (c.phone ? 40 : 16));
    }
  });
})(globalThis.OAChart);
