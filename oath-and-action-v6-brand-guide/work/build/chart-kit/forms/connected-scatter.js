/* Connected scatter (coverage plan 3.6, extended; S56). Two measures moving together over time: one dot a period at its
 * two values, joined in time order by a thin path in the subject ink, so the path's shape is the answer (the data lead's
 * rulings (a) and (e)). A period with either value missing breaks the path, which never bridges it, and the gap is named
 * by labels.gap at the middle of the break. Periods the spec names carry their words on a leader (K.parts.note); the
 * first and last periods take a larger dot, so the path's direction reads without arrows. Gridlines both ways, the y
 * values in a left gutter and the x values along the bottom.
 * encode: time (month or year), x (number), y (number).
 * labels: named ({time: words}: periods named on the drawing), place ({time: "above", "below", "left" or "right"}),
 * dx ({time: px}), gap (words naming a missing period, placed at the break), gap_place ("above", "below", "left",
 * "right"), x_axis, y_axis (axis words).
 * formats: x, y (ticks). scale: x and y ([lo, hi]). On a phone the same arrangement draws narrower; a named period may
 * take its own place there (labels.place_phone).
 * Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'connected-scatter',
    name: 'Connected Scatter',
    family: 'correlation',
    encode: { time: 'time', x: 'number?', y: 'number?' },
    labels: ['named', 'place', 'place_phone', 'dx', 'gap', 'gap_place', 'x_axis', 'y_axis'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var et = c.field('time'), ex = c.field('x'), ey = c.field('y'), tick = c.size('tick');
      var fx = f.x || 'integer', fy = f.y || 'integer', named = L.named || {}, place = (ph && L.place_phone) || L.place || {}, dxs = L.dx || {};
      var ok = function (r) { return typeof r[ex] === 'number' && typeof r[ey] === 'number'; };
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[et]) - K.time(b[et]); });
      var have = rows.filter(ok);
      var xv = have.map(function (r) { return r[ex]; }), yv = have.map(function (r) { return r[ey]; });
      var sc = c.spec.scale || {}, nx = W < 300 ? 3 : ph ? 4 : 6, ny = ph ? 4 : 5;
      var dx = sc.x || K.nice(Math.min.apply(null, xv), Math.max.apply(null, xv), nx), dy = sc.y || K.nice(Math.min.apply(null, yv), Math.max.apply(null, yv), ny);
      var tx = K.ticks(dx[0], dx[1], 0, K.nice(dx[0], dx[1], nx).step), ty = K.ticks(dy[0], dy[1], 0, K.nice(dy[0], dy[1], ny).step);
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
      // the named periods, then the gap's words at the middle of the break
      Object.keys(named).forEach(function (k) {
        var r = rows.filter(function (q) { return String(q[et]) === k; })[0];
        if (!r || !ok(r)) { c.warn('labels.named names no period with both values: ' + k); return; }
        var p = pt(r);
        P.note(c, p[0], p[1], named[k], { place: place[k] || 'above', dx: dxs[k], max: ph ? 130 : 200 });
      });
      if (L.gap) {
        rows.forEach(function (r, i) {
          if (ok(r) || !i || i === rows.length - 1) return;
          var a = rows[i - 1], b = rows[i + 1];
          if (!ok(a) || !ok(b)) return;
          var pa = pt(a), pb = pt(b);
          P.note(c, (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2, L.gap, { place: L.gap_place || 'below', max: ph ? 130 : 180 });
        });
      }
      var end = ay + 4;
      if (L.x_axis) { var xb = c.text(W, ay + tick + 10, L.x_axis, { role: 'tick', weight: 600, anchor: 'end', max: W - x0 }); end = xb.bottom; }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
