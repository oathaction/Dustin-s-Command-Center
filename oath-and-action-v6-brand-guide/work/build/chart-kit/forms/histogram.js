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
      });
      P.zero_line(c, ys, x0, x1);
      // the marker: a line dashed in the text's ink across the columns, its words above the plot (the data lead's ruling (b))
      if (mk) {
        var mx = xs(mk.value), mw = c.measure(mk.words || '', 'label');
        P.total_line(c, mx, mky + 6, mx, bot);
        if (mk.words) c.text(Math.min(Math.max(mx, x0 + mw / 2), x1 - mw / 2), mky, mk.words, { role: 'label', anchor: 'middle' });
      }
      // the counts over their columns, after the marker, on a halo of the ground where the marker crosses them
      if (fits) rows.forEach(function (r) {
        c.text((xs(r[es]) + xs(r[ee])) / 2, ys(r[en]) - 5, vw(r), { role: 'tick', weight: ink.named && ink.is_named(r) || ink.is_point(r) ? 700 : 400, anchor: 'middle', tnum: true, fill: 'label', halo: true });
      });
      // the bins' edges along the bottom, thinned so the labels sit apart; an open last bin takes its own words
      var ay = bot + tick + 8, edges = rows.map(function (r) { return r[es]; });
      var last = rows[rows.length - 1];
      if (!L.open_end) edges.push(hi);
      var place = function (b) { b.an = b.x - b.w / 2 < 0 ? 'start' : b.x + b.w / 2 > W ? 'end' : 'middle'; b.l = b.an === 'start' ? Math.max(0, b.x) : b.an === 'end' ? W - b.w : b.x - b.w / 2; b.r = b.l + b.w; return b; };
      var boxes = edges.map(function (v) { var word = K.fmt(v, fe); return place({ v: v, word: word, x: xs(v), w: c.measure(word, 'tick') }); });
      if (L.open_end) {
        var ow = el ? String(last[el]) : '', w2 = c.measure(ow, 'tick');
        boxes.push(place({ v: null, word: ow, x: Math.min((xs(last[es]) + xs(last[ee])) / 2, x1 - w2 / 2), w: w2, open: true }));
      }
      // every k-th edge from the first, the smallest k whose labels sit apart (an open last bin keeps its words)
      var pick = boxes;
      for (var k = 1; k <= boxes.length; k++) {
        pick = boxes.filter(function (b, i) { return b.open || i % k === 0; });
        if (pick.every(function (b, j) { return !j || pick[j - 1].r + 10 <= b.l; })) break;
      }
      edges.forEach(function (v) { c.line(xs(v), bot, xs(v), bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      pick.forEach(function (b) { c.text(b.an === 'start' ? b.l : b.an === 'end' ? W : b.x, ay, b.word, { role: 'tick', anchor: b.an }); });
      var bottom = ay + 4;
      if (L.x_axis) { var xb = c.text(x0, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, max: W - x0 }); bottom = xb.bottom; }
      c.height(bottom + 2);
    }
  });
})(globalThis.OAChart);
