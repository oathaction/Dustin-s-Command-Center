/* Histogram (coverage plan 3.5, core; S49). The spread of one measure across many units, drawn from a summary of bins
 * (R2-2): one column per bin, the columns side by side with a hairline gap, every count printed over its column where the
 * counts fit, or a value axis at the left where they do not. The bins' edges are labeled along the bottom, thinned to fit,
 * and an open last bin takes its own words. A marker, such as the median, may be drawn as a line across the columns with
 * its words above the plot.
 * encode: start (number, the bin's lower edge), end (number, its upper edge), count (number), label (text, optional: the
 * bin's words, used for an open last bin), key (code, optional: the bin's key for labels; start otherwise).
 * labels: named (keys of bins in the subject ink, the rest in the light fill), point (the one bin in the red point),
 * x_axis (words under the axis, such as "Years as a federal judge"), y_axis (words over the counts, such as "Judges"),
 * marker ({value, words}: a line at a value with its words above the plot), open_end (true: the last bin is open, labeled
 * by its own words), value (the words over each column, with {count}; default {count}).
 * formats: count, edge (the bin edges' format), tick. On a phone the same arrangement draws narrower; counts that do not
 * fit over their columns move to a value axis. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'histogram',
    name: 'Histogram',
    family: 'distribution-and-density',
    encode: { start: 'number', end: 'number', count: 'number', label: 'text?', key: 'code?' },
    labels: ['named', 'point', 'x_axis', 'y_axis', 'marker', 'open_end', 'value'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var es = c.field('start'), ee = c.field('end'), en = c.field('count'), el = c.field('label', false), ek = c.field('key', false) || es;
      var rows = c.rows.slice().sort(function (a, b) { return a[es] - b[es]; });
      var ink = P.named_fill(c, L.named, ek, 'subject', L.point);
      var fc = f.count || 'integer', fe = f.edge || 'integer', tick = c.size('tick'), size = c.size('label');
      var vw = function (r) { return String(L.value || '{count}').replace('{count}', K.fmt(r[en], fc)); };
      var lo = rows[0][es], hi = rows[rows.length - 1][ee], nmax = Math.max.apply(null, rows.map(function (r) { return r[en]; }));
      var y = 0;
      if (L.y_axis) { c.text(0, tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y = tick + 8; }
      // the marker's words sit over the plot, so they never touch a count
      var mk = L.marker && typeof L.marker.value === 'number' ? L.marker : null;
      var mky = 0;
      if (mk) { y += size; mky = y; y += 8; }
      // counts over the columns when every one fits its column's width; a value axis otherwise
      var gut0 = 0, x0 = 0, x1 = W, xs = K.scale.linear([lo, hi], [x0, x1]);
      var fits = rows.every(function (r) { return c.measure(vw(r), 'tick', 600, true) <= xs(r[ee]) - xs(r[es]) + 2; });
      var vs = P.value_scale(c, 0, nmax, ph ? 4 : 5), ticks = vs.ticks;
      if (!fits) { gut0 = P.value_gutter(c, ticks, f.tick || 'integer'); x0 = gut0 + 8; xs = K.scale.linear([lo, hi], [x0, x1]); }
      var top = y + (fits ? tick + 6 : 6), plotH = ph ? 220 : 280, bot = top + plotH;
      var ys = K.scale.linear([0, fits ? nmax : vs.hi], [bot, top]);
      if (!fits) P.value_grid(c, ys, ticks, f.tick || 'integer', x0, x1, gut0);
      // the columns, a hairline apart
      rows.forEach(function (r) {
        var a = xs(r[es]), b = xs(r[ee]), role = ink(r), h = bot - ys(r[en]);
        c.rect(a + 0.5, ys(r[en]), Math.max(1, b - a - 1), h, Object.assign({ fill: role, kind: 'bar', axis: 'y', zero: bot, data: { key: r[ek], field: en, value: r[en] } }, ink.keyline(r)));
        if (fits) c.text((a + b) / 2, ys(r[en]) - 5, vw(r), { role: 'tick', weight: ink.named && ink.is_named(r) || ink.is_point(r) ? 700 : 400, anchor: 'middle', tnum: true, fill: 'label' });
      });
      P.zero_line(c, ys, x0, x1);
      // the marker: a line in the text's ink across the columns, its words above the plot
      if (mk) {
        var mx = xs(mk.value), mw = c.measure(mk.words || '', 'label', 600);
        c.line(mx, mky + 6, mx, bot, { stroke: 'label', width: c.t('line-baseline'), dash: '4 3', mark: false });
        if (mk.words) c.text(Math.min(Math.max(mx, x0 + mw / 2), x1 - mw / 2), mky, mk.words, { role: 'label', weight: 600, anchor: 'middle' });
      }
      // the bins' edges along the bottom, thinned so the labels sit apart; an open last bin takes its own words
      var ay = bot + tick + 8, edges = rows.map(function (r) { return r[es]; });
      var last = rows[rows.length - 1];
      if (!L.open_end) edges.push(hi);
      var boxes = edges.map(function (v) { var word = K.fmt(v, fe), w = c.measure(word, 'tick'); return { v: v, word: word, x: xs(v), w: w }; });
      if (L.open_end) {
        var ow = el ? String(last[el]) : '', w2 = c.measure(ow, 'tick');
        boxes.push({ v: null, word: ow, x: Math.min((xs(last[es]) + xs(last[ee])) / 2, x1 - w2 / 2), w: w2, open: true });
      }
      var pick = [];
      for (var k = 1; k <= boxes.length; k++) {
        pick = boxes.filter(function (b, i) { return b.open || i % k === 0; });
        var ok = pick.every(function (b, j) { return !j || pick[j - 1].x + pick[j - 1].w / 2 + 10 <= b.x - b.w / 2; });
        if (ok && pick[0].x - pick[0].w / 2 >= -0.5) break;
      }
      edges.forEach(function (v) { c.line(xs(v), bot, xs(v), bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      pick.forEach(function (b) {
        var anchor = b.x - b.w / 2 < 0 ? 'start' : b.x + b.w / 2 > W ? 'end' : 'middle';
        c.text(anchor === 'start' ? Math.max(0, b.x) : anchor === 'end' ? W : b.x, ay, b.word, { role: 'tick', anchor: anchor });
      });
      var bottom = ay + 4;
      if (L.x_axis) { var xb = c.text(x0, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, max: W - x0 }); bottom = xb.bottom; }
      c.height(bottom + 2);
    }
  });
})(globalThis.OAChart);
