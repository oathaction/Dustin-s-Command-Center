/* Connected scatter (coverage plan 3.6, extended; S56). Two measures moving together over time: one dot a period at its
 * two values, joined in time order by a thin path in the subject ink, so the path's shape is the answer (the data lead's
 * rulings (a) and (e)). A period with either value missing breaks the path, which never bridges it, and the gap is named
 * by labels.gap at the middle of the break. Periods the spec names carry their words, placed by the kit's shared part
 * (K.parts.place_labels) clear of every dot, with a leader where they sit further out; a name with no clear place is
 * listed under the chart. The first and last periods take a larger dot, so the path's direction reads without arrows.
 * Gridlines both ways, the y values in a left gutter and the x values along the bottom.
 * encode: time (month or year: each period's first month for a quarter), x (number), y (number).
 * labels: named ({time: words}: periods named on the drawing; the latest claims room first, then the gap, then the rest
 * in the spec's order), gap (words naming a missing period, placed at the break), x_axis, y_axis (axis words).
 * formats: x, y (ticks). scale: x and y ([lo, hi]), x_step, y_step and x_step_phone (the ticks' steps). On a phone the
 * same arrangement draws narrower.
 * Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'connected-scatter',
    name: 'Connected Scatter',
    family: 'correlation',
    encode: { time: 'time', x: 'number?', y: 'number?' },
    labels: ['named', 'gap', 'x_axis', 'y_axis'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var et = c.field('time'), ex = c.field('x'), ey = c.field('y'), tick = c.size('tick');
      var fx = f.x || 'integer', fy = f.y || 'integer', named = L.named || {};
      var ok = function (r) { return typeof r[ex] === 'number' && typeof r[ey] === 'number'; };
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[et]) - K.time(b[et]); });
      var have = rows.filter(ok);
      var xv = have.map(function (r) { return r[ex]; }), yv = have.map(function (r) { return r[ey]; });
      var sc = c.spec.scale || {}, nx = W < 300 ? 3 : ph ? 4 : 6, ny = ph ? 4 : 5;
      var dx = sc.x || K.nice(Math.min.apply(null, xv), Math.max.apply(null, xv), nx), dy = sc.y || K.nice(Math.min.apply(null, yv), Math.max.apply(null, yv), ny);
      // the spec may set each axis's step (scale.x_step, scale.y_step), so whole-number ticks never fall on a half
      var tx = K.ticks(dx[0], dx[1], 0, (!ph && sc.x_step) || (ph && sc.x_step_phone) || K.nice(dx[0], dx[1], nx).step), ty = K.ticks(dy[0], dy[1], 0, sc.y_step || K.nice(dy[0], dy[1], ny).step);
      var y0 = 0;
      if (L.y_axis) { c.text(0, tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y0 = tick + 10; }
      var gut = P.value_gutter(c, ty, fy), x0 = gut + 8, x1 = W - 6;
      var top = y0 + tick * 0.5, plotH = ph ? Math.round((x1 - x0) * 1.0) : 440, bot = top + plotH, pad = 6;
      var xs = K.scale.linear([dx[0], dx[1]], [x0 + pad, x1 - pad]), ys = K.scale.linear([dy[0], dy[1]], [bot - pad, top + pad]);
      ty.forEach(function (v) { c.line(x0, ys(v), x1, ys(v), { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); c.text(gut, ys(v) + tick * 0.35, K.fmt(v, fy), { role: 'tick', anchor: 'end', tnum: true }); });
      tx.forEach(function (v) { c.line(xs(v), top, xs(v), bot, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      c.line(x0, bot, x1, bot, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      var ay = bot + tick + 8, tb = tx.map(function (v) { var w = K.fmt(v, fx), tw = c.measure(w, 'tick'), x = xs(v), an = x + tw / 2 > W ? 'end' : 'middle'; return { w: w, x: x, an: an, l: an === 'end' ? W - tw : x - tw / 2, r: an === 'end' ? W : x + tw / 2 }; });
      var keep = tb;
      for (var kk = 1; kk <= tb.length; kk++) { keep = tb.filter(function (b, i) { return i % kk === 0; }); if (keep.every(function (b, j) { return !j || keep[j - 1].r + 10 <= b.l; })) break; }
      tx.forEach(function (v) { c.line(xs(v), bot, xs(v), bot + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      keep.forEach(function (b) { c.text(b.an === 'end' ? W : b.x, ay, b.w, { role: 'tick', anchor: b.an }); });
      // the path, broken where a period lacks a value, then a small dot at every period
      var runs = [], cur = [];
      rows.forEach(function (r) { if (ok(r)) cur.push(r); else { if (cur.length) runs.push(cur); cur = []; } });
      if (cur.length) runs.push(cur);
      var pt = function (r) { return [xs(r[ex]), ys(r[ey])]; };
      runs.forEach(function (run) {
        if (run.length < 2) return;
        var d = run.map(function (r, i) { var p = pt(r); return (i ? 'L' : 'M') + K.round(p[0]) + ',' + K.round(p[1]); }).join('');
        c.path(d, { stroke: 'subject', width: c.t('spark-context') }, [x0, top, x1 - x0, plotH]);
      });
      var rs = c.t('dot-small-vertex-radius') * (ph ? 0.8 : 1), first = have[0], last = have[have.length - 1];
      have.forEach(function (r) {
        var p = pt(r), big = r === first || r === last;
        if (big) c.circle(p[0], p[1], c.t('dot-vertex-radius') + 1 + c.t('keyline'), { fill: 'surface', mark: false });
        c.circle(p[0], p[1], big ? c.t('dot-vertex-radius') + 1 : rs, { fill: 'subject', data: { key: r[et], field: ey, value: r[ey], x: r[ex] } });
        c.datum(p[0], p[1], { data: { key: r[et], field: ex, value: r[ex] } });
      });
      // the named periods and the gap's words, through the kit's shared placing (R2-C2), clear of every dot; a name with no
      // clear place is listed under the chart, and the table gives every period
      var items = [];
      Object.keys(named).forEach(function (k) {
        var r = rows.filter(function (q) { return String(q[et]) === k; })[0];
        if (!r || !ok(r)) { c.warn('labels.named names no period with both values: ' + k); return; }
        var p = pt(r), big = r === first || r === last;
        items.push({ x: p[0], y: p[1], r: big ? c.t('dot-vertex-radius') + 1 : rs, words: named[k], weight: 600, last: r === last });
      });
      if (L.gap) {
        rows.forEach(function (r, i) {
          if (ok(r) || !i || i === rows.length - 1) return;
          var a = rows[i - 1], b = rows[i + 1];
          if (!ok(a) || !ok(b)) return;
          var pa = pt(a), pb = pt(b);
          items.push({ x: (pa[0] + pb[0]) / 2, y: (pa[1] + pb[1]) / 2, r: 2, words: L.gap, weight: 400, gap: true });
        });
      }
      // the latest period and the gap claim room first, then the named periods in the spec's order
      items.sort(function (a, b) { return (a.last ? 0 : a.gap ? 1 : 2) - (b.last ? 0 : b.gap ? 1 : 2); });
      // every dot and the path itself, sampled every few pixels, are boxes no name may cover, so names sit in open space
      var avoid = have.map(function (r) { var p = pt(r); return { x: p[0] - rs, y: p[1] - rs, w: 2 * rs, h: 2 * rs }; });
      runs.forEach(function (run) {
        for (var i = 1; i < run.length; i++) {
          var a = pt(run[i - 1]), b = pt(run[i]), n = Math.ceil(Math.sqrt(Math.pow(b[0] - a[0], 2) + Math.pow(b[1] - a[1], 2)) / 5);
          for (var j = 1; j < n; j++) avoid.push({ x: a[0] + (b[0] - a[0]) * j / n - 1, y: a[1] + (b[1] - a[1]) * j / n - 1, w: 2, h: 2 });
        }
      });
      // each name in turn, reaching further out until a place is clear (the part tries one reach a call)
      var pl = { placed: [], unplaced: [] };
      items.forEach(function (it) {
        var got = null;
        [16, 30, 48, 70, 96, 130, 170, 220].some(function (reach) {
          var res = P.place_labels(c, [it], { top: top, bottom: bot, avoid: avoid, reach: reach });
          if (res.placed.length) { got = res.placed[0]; return true; }
          return false;
        });
        if (got) pl.placed.push(got); else pl.unplaced.push(it);
      });
      var end = ay + 4;
      if (L.x_axis) { var xb = c.text(W, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, anchor: 'end', max: W - x0 }); end = xb.bottom; }
      if (pl.unplaced.length) {
        var ub = c.text(0, end + c.size('note') + 8, K.word('unlabeled_marks').replace('{codes}', pl.unplaced.map(function (it) { return it.words; }).join('; ')), { role: 'note', max: W, fill: 'secondary' });
        end = ub.bottom;
      }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
