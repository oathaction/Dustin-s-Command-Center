/* Fan chart (coverage plan 3.7, extended; S59). A projection's median as a line in the subject ink with a dot and its
 * value at each period, over two nested bands (K.parts.band): the outer in magnitude step 1 and the inner in step 2, so
 * the fan reads from its middle outward in grayscale too. A key over the plot names the two bands and the line. The
 * outer band's two ends are printed at the last period. A period drawn apart (labels.apart, such as the longer run) sits
 * to the right of a thin rule, its median a dot and its inner band a whisker, since it has no date.
 * encode: x (category: the periods, years in order, and the one drawn apart), y (number: the median), outer_low and
 * outer_high (numbers), inner_low and inner_high (numbers, optional).
 * labels: apart (the x value drawn apart), apart_label (its words under the axis), key_outer, key_inner, key_median (the
 * key's words; an entry is left out when its words are), y_axis (words over the value axis).
 * formats: y (values and ticks unless tick is set), tick. scale: y ([lo, hi]). On a phone the same arrangement draws
 * narrower, the key wrapping to more rows. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'fan-chart',
    name: 'Fan Chart',
    family: 'uncertainty-and-estimates',
    encode: { x: 'category', y: 'number', outer_low: 'number', outer_high: 'number', inner_low: 'number?', inner_high: 'number?' },
    labels: ['apart', 'apart_label', 'key_outer', 'key_inner', 'key_median', 'y_axis'],
    interval: 'level',
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ex = c.field('x'), ey = c.field('y'), eol = c.field('outer_low'), eoh = c.field('outer_high'), eil = c.field('inner_low', false), eih = c.field('inner_high', false);
      var tick = c.size('tick'), size = c.size('label'), fy = f.y || 'number:1', ft = f.tick || 'integer';
      var apart = L.apart === undefined || L.apart === null ? null : String(L.apart);
      var main = c.rows.filter(function (r) { return String(r[ex]) !== apart; }), ap = c.rows.filter(function (r) { return String(r[ex]) === apart; })[0] || null;
      var vals = [];
      c.rows.forEach(function (r) { [ey, eol, eoh, eil, eih].forEach(function (k) { if (k && typeof r[k] === 'number') vals.push(r[k]); }); });
      var vs = P.value_scale(c, Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), ph ? 4 : 5), ticks = vs.ticks;
      var y = 0;
      // the key over the plot
      var kents = [];
      if (L.key_outer) kents.push({ label: L.key_outer, fill: 'mag-1' });
      if (L.key_inner && eil) kents.push({ label: L.key_inner, fill: 'mag-2' });
      if (L.key_median) kents.push({ label: L.key_median, shape: 'line', stroke: 'subject', width: c.t('line-subject') });
      if (kents.length) y += P.key(c, kents, 0, size, W) + 6;
      if (L.y_axis) { c.text(0, y + tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y += tick + 8; }
      var top = y + tick, plotH = ph ? 240 : 300, bot = top + plotH;
      var gut = P.value_gutter(c, ticks, ft), x0 = gut + 8;
      var endw = Math.ceil(Math.max(c.measure(K.fmt(main[main.length - 1][eoh], fy), 'label', 600), c.measure(K.fmt(main[main.length - 1][eol], fy), 'label', 600)));
      var apw = ap ? Math.max(48, Math.ceil(c.measure(L.apart_label || apart, 'tick')) + 12) : 0;
      var x1 = W - (ap ? apw + 24 : 0) - endw - 10;
      var xs = K.scale.linear([0, Math.max(1, main.length - 1)], [x0 + 16, x1]), ys = K.scale.linear([vs.lo, vs.hi], [bot, top]);
      P.value_grid(c, ys, ticks, ft, x0, W, gut);
      P.zero_line(c, ys, x0, W);
      var px = function (i) { return xs(i); };
      // the two bands, the outer first
      var key = function (r) { return String(r[ex]); };
      P.band(c, main.map(function (r, i) { return { x: px(i), y0: ys(r[eol]), y1: ys(r[eoh]), key: key(r), low: r[eol], high: r[eoh] }; }), { fill: 'mag-1', field_low: eol, field_high: eoh });
      if (eil && eih) P.band(c, main.map(function (r, i) { return { x: px(i), y0: ys(r[eil]), y1: ys(r[eih]), key: key(r), low: r[eil], high: r[eih] }; }), { fill: 'mag-2', field_low: eil, field_high: eih });
      // the median: a line with a dot and its value at each period
      var d = main.map(function (r, i) { return (i ? 'L' : 'M') + K.round(px(i)) + ',' + K.round(ys(r[ey])); }).join('');
      c.path(d, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
      c.path(d, { stroke: 'subject', width: c.t('line-subject') }, [x0, top, x1 - x0, plotH]);
      main.forEach(function (r, i) {
        c.circle(px(i), ys(r[ey]), c.t('dot-vertex-radius') + 1, Object.assign({ fill: 'subject', data: { key: key(r), field: ey, value: r[ey] } }));
        c.text(px(i), ys(r[eih] !== undefined && eih ? Math.max(r[ey], r[eih]) : r[ey]) - 8, K.fmt(r[ey], fy), { role: 'tick', weight: 600, anchor: 'middle', fill: 'label', halo: true });
      });
      // the outer band's ends at the last period
      var lr = main[main.length - 1], lx = px(main.length - 1) + 8;
      c.text(lx, ys(lr[eoh]) + tick * 0.35, K.fmt(lr[eoh], fy), { role: 'label', weight: 600 });
      c.text(lx, ys(lr[eol]) + tick * 0.35, K.fmt(lr[eol], fy), { role: 'label', weight: 600 });
      // the period drawn apart, past a thin rule
      if (ap) {
        var rx = W - apw / 2, sep = W - apw - 12;
        c.line(sep, top - tick, sep, bot + 4, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
        if (eil && eih && typeof ap[eil] === 'number') P.whisker(c, ys(ap[eil]), ys(ap[eih]), rx, { dir: 'v', stroke: 'context', key: key(ap), low: ap[eil], high: ap[eih] });
        c.circle(rx, ys(ap[ey]), c.t('dot-vertex-radius') + 1, { fill: 'subject', data: { key: key(ap), field: ey, value: ap[ey] } });
        c.text(rx, ys(Math.max(ap[ey], eih && typeof ap[eih] === 'number' ? ap[eih] : ap[ey])) - 8, K.fmt(ap[ey], fy), { role: 'tick', weight: 600, anchor: 'middle', fill: 'label', halo: true });
      }
      // the periods along the bottom
      // the periods along the bottom: the last, and every k-th back from it that sits apart
      var ay = bot + tick + 10, n = main.length, pick = [];
      for (var k = 1; k <= n; k++) {
        pick = main.map(function (r, i) { return i; }).filter(function (i) { return (n - 1 - i) % k === 0; });
        if (pick.every(function (i, j) { return !j || px(pick[j - 1]) + c.measure(String(main[pick[j - 1]][ex]), 'tick') / 2 + 10 <= px(i) - c.measure(String(main[i][ex]), 'tick') / 2; })) break;
      }
      main.forEach(function (r, i) { c.line(px(i), bot, px(i), bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      pick.forEach(function (i) { c.text(px(i), ay, String(main[i][ex]), { role: 'tick', anchor: 'middle' }); });
      var end = ay + 4;
      if (ap) { var ab = c.text(W - apw / 2, ay, L.apart_label || apart, { role: 'tick', anchor: 'middle', max: apw + 10 }); end = Math.max(end, ab.bottom); }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
