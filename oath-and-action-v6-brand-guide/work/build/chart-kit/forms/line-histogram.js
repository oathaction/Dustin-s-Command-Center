/* Line histogram (coverage plan 3.5, extended; S52). Two or three distributions of one measure on the same bins, drawn
 * as stepped outlines over one baseline so each shape shows through the other (R2-2's summary: one row a bin and series).
 * The series the title follows is drawn in the subject ink at the subject line's weight, the others thinner in the context
 * ink (the data lead's ruling (e)); each is named where its outline peaks. A value axis at the left; the bins' edges along the bottom, thinned.
 * encode: start (number, the bin's lower edge), end (number, its upper edge), value (number: a count or share), series
 * (category), label (text, optional: the bin's words for an open last bin).
 * labels: lit (the series in ink), series ({value: printed name}), open_end (true: the last bin is open, labeled by its
 * own words), x_axis, y_axis (words over the value axis), medians ({series: value}: a short tick under the baseline in the
 * series' ink at each median, round 2 fix pass, CD B-S2), median_words (a second line under each name, with {median}).
 * formats: value, edge (the bin edges), tick. scale: y ([lo, hi]). On a phone the same arrangement draws narrower.
 * Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'line-histogram',
    name: 'Line Histogram',
    family: 'distribution-and-density',
    encode: { start: 'number', end: 'number', value: 'number', series: 'category', label: 'text?' },
    labels: ['lit', 'series', 'open_end', 'x_axis', 'y_axis', 'medians', 'median_words'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var es = c.field('start'), ee = c.field('end'), ev = c.field('value'), er = c.field('series'), el = c.field('label', false);
      var tick = c.size('tick'), size = c.size('label'), fe = f.edge || 'integer', ft = f.tick || f.value || 'integer';
      var by = {}, order = [];
      c.rows.forEach(function (r) { var k = String(r[er]); if (!by[k]) { by[k] = []; order.push(k); } by[k].push(r); });
      order.forEach(function (k) { by[k].sort(function (a, b) { return a[es] - b[es]; }); });
      var lit = L.lit === undefined || L.lit === null ? order[order.length - 1] : String(L.lit);
      if (!by[lit]) c.warn('labels.lit names no series: ' + lit);
      var sname = function (k) { return (L.series || {})[k] !== undefined ? L.series[k] : k; };
      var lo = Math.min.apply(null, c.rows.map(function (r) { return r[es]; })), hi = Math.max.apply(null, c.rows.map(function (r) { return r[ee]; }));
      var vmax = Math.max.apply(null, c.rows.map(function (r) { return r[ev]; }));
      var vs = P.value_scale(c, 0, vmax, ph ? 4 : 5), ticks = vs.ticks;
      var y = 0;
      if (L.y_axis) { c.text(0, tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y = tick + 8; }
      var top = y + tick, plotH = ph ? 240 : 300, bot = top + plotH;
      var gut = P.value_gutter(c, ticks, ft), x0 = gut + 8, x1 = W - 4;
      var xs = K.scale.linear([lo, hi], [x0, x1]), ys = K.scale.linear([vs.lo, vs.hi], [bot, top]);
      P.value_grid(c, ys, ticks, ft, x0, x1, gut);
      // each series' stepped outline: up the first edge, across each bin's top, down the last edge
      var step = function (k) {
        var rs = by[k], d = 'M' + K.round(xs(rs[0][es])) + ',' + K.round(bot);
        rs.forEach(function (r) { d += 'L' + K.round(xs(r[es])) + ',' + K.round(ys(r[ev])) + 'L' + K.round(xs(r[ee])) + ',' + K.round(ys(r[ev])); });
        return d + 'L' + K.round(xs(rs[rs.length - 1][ee])) + ',' + K.round(bot);
      };
      var others = order.filter(function (k) { return k !== lit; });
      others.forEach(function (k) {
        c.path(step(k), { stroke: 'context', width: c.t('line-context'), data: { series: k } }, [x0, top, x1 - x0, plotH]);
      });
      if (by[lit]) {
        c.path(step(lit), { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
        c.path(step(lit), { stroke: 'subject', width: c.t('line-subject'), data: { series: lit } }, [x0, top, x1 - x0, plotH]);
      }
      order.forEach(function (k) { by[k].forEach(function (r) { c.datum((xs(r[es]) + xs(r[ee])) / 2, ys(r[ev]), { data: { key: k + '|' + r[es], field: ev, value: r[ev] } }); }); });
      P.zero_line(c, ys, x0, x1);
      // each series' median: a 2 px tick under the baseline in the series' ink, longer than the bins' edge ticks
      var meds = L.medians || {}, fm = f.median || 'number:1';
      order.forEach(function (k) {
        if (typeof meds[k] !== 'number') return;
        c.line(xs(meds[k]), bot + 1, xs(meds[k]), bot + 9, { stroke: k === lit ? 'subject' : 'context', width: c.t('line-context'), mark: false });
      });
      // each series named over its peak, kept apart from the other's name and inside the plot
      var placed = [];
      order.slice().sort(function (a, b) { return a === lit ? -1 : b === lit ? 1 : 0; }).forEach(function (k) {
        var pk = by[k].reduce(function (m, r) { return r[ev] > m[ev] ? r : m; }, by[k][0]);
        var words = sname(k), w = c.measure(words, 'label', k === lit ? 700 : 600);
        var mw = L.median_words && typeof meds[k] === 'number' ? String(L.median_words).replace('{median}', K.fmt(meds[k], fm)) : '';
        if (mw) w = Math.max(w, c.measure(mw, 'tick', k === lit ? 600 : 400));
        var px = (xs(pk[es]) + xs(pk[ee])) / 2, py = ys(pk[ev]) - 8 - (mw ? tick + 3 : 0);
        // the other series' name moves to the side of the peak where the lit outline sits lowest
        if (placed.length) {
          var p0 = placed[0];
          if (Math.abs(px - p0.x) < (w + p0.w) / 2 + 12 && Math.abs(py - p0.y) < size + 4 + (mw ? tick + 3 : 0)) {
            var right = px >= p0.x;
            px = right ? p0.x + p0.w / 2 + w / 2 + 16 : p0.x - p0.w / 2 - w / 2 - 16;
          }
        }
        px = Math.min(Math.max(px, x0 + w / 2), x1 - w / 2);
        py = Math.max(py, top + size * 0.2);
        c.text(px, py, words, { role: 'label', weight: k === lit ? 700 : 600, anchor: 'middle', fill: k === lit ? 'label' : 'secondary', halo: true });
        if (mw) c.text(px, py + tick + 3, mw, { role: 'tick', weight: k === lit ? 600 : 400, anchor: 'middle', fill: k === lit ? 'label' : 'secondary', halo: true });
        placed.push({ x: px, y: py, w: w });
      });
      // the bins' edges along the bottom, thinned to fit; an open last bin takes its own words
      var ay = bot + tick + 10, ref = by[lit] || by[order[0]], edges = ref.map(function (r) { return r[es]; });
      var last = ref[ref.length - 1];
      if (!L.open_end) edges.push(hi);
      var boxes = edges.map(function (v) { var word = K.fmt(v, fe); return { word: word, x: xs(v), w: c.measure(word, 'tick') }; });
      if (L.open_end && el) { var ow = String(last[el]), w2 = c.measure(ow, 'tick'); boxes.push({ word: ow, x: Math.min((xs(last[es]) + xs(last[ee])) / 2, x1 - w2 / 2), w: w2, open: true }); }
      var pick = [];
      for (var kk = 1; kk <= boxes.length; kk++) {
        pick = boxes.filter(function (b, i) { return b.open || i % kk === 0; });
        if (pick.every(function (b, j) { return !j || pick[j - 1].x + pick[j - 1].w / 2 + 10 <= b.x - b.w / 2; })) break;
      }
      edges.forEach(function (v) { c.line(xs(v), bot, xs(v), bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      pick.forEach(function (b) { var anchor = b.x + b.w / 2 > W ? 'end' : 'middle'; c.text(anchor === 'end' ? W : b.x, ay, b.word, { role: 'tick', anchor: anchor }); });
      var end = ay + 4;
      if (L.x_axis) { var xb = c.text(x0, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, max: W - x0 }); end = xb.bottom; }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
