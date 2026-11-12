/* Connected scatter (coverage plan 3.6, extended; S56). Two measures moving together over time: one dot a period at its
 * two values, joined in time order by a thin path in the subject ink, so the path's shape is the answer (the data lead's
 * rulings (a) and (e)). A period with either value missing breaks the path, which never bridges it, and the gap is named
 * at the middle of the break by a small open ring, which a one-line key over the plot names with labels.gap's words
 * (MB-19: marked and named at every width). Periods the
 * spec names carry their words beside their dot, or further out on a hairline leader that crosses no stretch of the path
 * and passes no other dot (the data lead's MB-12); the latest period takes a place clear of the path first, then a
 * leader that crosses it, and only then a place beside its dot on a halo over the path; a name with no place is listed under the chart. The first and last periods take a larger dot, so the path's direction reads without arrows.
 * Gridlines both ways, the y values in a left gutter and the x values along the bottom.
 * encode: time (month or year: each period's first month for a quarter), x (number), y (number).
 * labels: named ({time: words}: periods named on the drawing; the latest claims room first, then the rest in the spec's
 * order), short ({time: words} for a column under 330 px), gap (words naming a missing period, in the key over the
 * plot), x_axis, y_axis (axis words).
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
    labels: ['named', 'short', 'gap', 'x_axis', 'y_axis'],
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
      // the gap's key over the plot: an open ring and labels.gap's words, so the break is marked and named at every width
      // (the data lead's MB-19), since in a dense path no place beside the break stays clear at every width
      var gapped = !!L.gap && rows.some(function (r, i) { return !ok(r) && i > 0 && i < rows.length - 1 && ok(rows[i - 1]) && ok(rows[i + 1]); });
      if (gapped) {
        var gsz = c.size('label'), gb = c.text(20, gsz, L.gap, { role: 'label', max: W - 20 });
        c.circle(7, gsz * 0.62, 3.5, { fill: 'surface', mark: false });
        c.circle(7, gsz * 0.62, 3.5, { stroke: 'subject', width: c.t('line-context') - 0.5, mark: false });
        c.key([{ fill: 'surface', pattern: true }]);
        y0 = gb.bottom + 12;
      }
      if (L.y_axis) { c.text(0, y0 + tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y0 += tick + 10; }
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
      // the named periods, placed clear of every dot (below), and the gap's ring at the middle of its break; a name with no
      // clear place is listed under the chart, and the table gives every period
      var items = [];
      Object.keys(named).forEach(function (k) {
        var r = rows.filter(function (q) { return String(q[et]) === k; })[0];
        if (!r || !ok(r)) { c.warn('labels.named names no period with both values: ' + k); return; }
        var p = pt(r), big = r === first || r === last;
        var words = W < 330 && L.short && L.short[k] !== undefined ? L.short[k] : named[k];   // a narrow column takes the short words
        items.push({ x: p[0], y: p[1], r: big ? c.t('dot-vertex-radius') + 1 : rs, words: words, short: L.short && L.short[k] !== undefined ? L.short[k] : null, weight: 600, last: r === last });
      });
      if (L.gap) {
        rows.forEach(function (r, i) {
          if (ok(r) || !i || i === rows.length - 1) return;
          var a = rows[i - 1], b = rows[i + 1];
          if (!ok(a) || !ok(b)) return;
          var pa = pt(a), pb = pt(b);
          items.push({ x: (pa[0] + pb[0]) / 2, y: (pa[1] + pb[1]) / 2, r: 3.5, words: L.gap, weight: 400, gap: true });
        });
      }
      // the latest period and the gap claim room first, then the named periods in the spec's order
      items.sort(function (a, b) { return (a.last ? 0 : a.gap ? 1 : 2) - (b.last ? 0 : b.gap ? 1 : 2); });
      // every dot and the path itself, sampled every few pixels, are boxes no name may cover, so names sit in open space
      var dotbox = have.map(function (r) { var p = pt(r); return { x: p[0] - rs, y: p[1] - rs, w: 2 * rs, h: 2 * rs }; });
      var pathbox = [], segs = [];
      runs.forEach(function (run) {
        for (var i = 1; i < run.length; i++) {
          var a = pt(run[i - 1]), b = pt(run[i]), n = Math.ceil(Math.sqrt(Math.pow(b[0] - a[0], 2) + Math.pow(b[1] - a[1], 2)) / 5);
          segs.push([a, b]);
          for (var j = 1; j < n; j++) pathbox.push({ x: a[0] + (b[0] - a[0]) * j / n - 1, y: a[1] + (b[1] - a[1]) * j / n - 1, w: 2, h: 2 });
        }
      });
      var avoid = dotbox.concat(pathbox);
      // a leader may cross no stretch of the path and pass no other dot (the data lead's MB-12)
      var cross = function (p1, p2, p3, p4) {
        var d = function (a, b, q) { return (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0]); };
        return d(p1, p2, p3) * d(p1, p2, p4) < 0 && d(p3, p4, p1) * d(p3, p4, p2) < 0;
      };
      var leader_clear_dots = function (it, l0, l1) {
        return have.every(function (r) {
          var q = pt(r); if (Math.abs(q[0] - it.x) < 0.5 && Math.abs(q[1] - it.y) < 0.5) return true;
          var vx = l1[0] - l0[0], vy = l1[1] - l0[1], t = Math.max(0, Math.min(1, ((q[0] - l0[0]) * vx + (q[1] - l0[1]) * vy) / (vx * vx + vy * vy || 1)));
          return Math.pow(l0[0] + t * vx - q[0], 2) + Math.pow(l0[1] + t * vy - q[1], 2) > Math.pow(rs + 2, 2);
        });
      };
      var leader_clear = function (it, l0, l1) {
        if (segs.some(function (sg) { return cross(l0, l1, sg[0], sg[1]); })) return false;
        return have.every(function (r) {
          var q = pt(r); if (Math.abs(q[0] - it.x) < 0.5 && Math.abs(q[1] - it.y) < 0.5) return true;
          var vx = l1[0] - l0[0], vy = l1[1] - l0[1], t = Math.max(0, Math.min(1, ((q[0] - l0[0]) * vx + (q[1] - l0[1]) * vy) / (vx * vx + vy * vy || 1)));
          return Math.pow(l0[0] + t * vx - q[0], 2) + Math.pow(l0[1] + t * vy - q[1], 2) > Math.pow(rs + 2, 2);
        });
      };
      var size = c.size('label'), A = 0.864, B = 0.136;
      var places = [[1, 0], [-1, 0], [0, -1], [0, 1], [0.75, -0.75], [0.75, 0.75], [-0.75, -0.75], [-0.75, 0.75]];
      var hit = function (b, boxes) { return boxes.some(function (t) { return b.x < t.x + t.w + 2 && t.x < b.x + b.w + 2 && b.y < t.y + t.h + 2 && t.y < b.y + b.h + 2; }); };
      // a name beside its dot (up to 8 px further, with no leader), or further out on a hairline leader that keeps clear of
      // the path and the other dots
      var place = function (it, blocks, reaches, o) {
        o = o || {};
        // words may wrap to o.max px; a leader may cross the path where o.loose is set, never another dot
        var lines = o.max ? c.wrap(it.words, 'label', o.max, it.weight) : [String(it.words)], lh = Math.round(size * 1.2);
        var w = 0; lines.forEach(function (ln) { w = Math.max(w, c.measure(ln, 'label', it.weight)); });
        var h = size + (lines.length - 1) * lh;
        for (var ri = 0; ri < reaches.length; ri++) {
          var dd = it.r + 4 + reaches[ri];
          for (var k = 0; k < places.length; k++) {
            var ax = places[k][0], ay2 = places[k][1], anchor = ax > 0 ? 'start' : ax < 0 ? 'end' : 'middle';
            var x = it.x + ax * dd, top0 = ay2 < 0 ? it.y + ay2 * dd - h : ay2 > 0 ? it.y + ay2 * dd : it.y - h / 2;
            var bx = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x, box = { x: bx, y: top0, w: w, h: h };
            if (box.x < 0 || box.x + box.w > W || box.y < top || box.y + box.h > bot) continue;
            if (hit(box, c.texts) || hit(box, blocks)) continue;
            var lx = Math.max(box.x, Math.min(it.x, box.x + box.w)), ly = Math.max(box.y, Math.min(it.y, box.y + box.h));
            var vx = lx - it.x, vy = ly - it.y, len = Math.sqrt(vx * vx + vy * vy) || 1;
            var l0 = [it.x + vx / len * (it.r + 1), it.y + vy / len * (it.r + 1)], l1 = [lx - vx / len * 2, ly - vy / len * 2];
            if (reaches[ri] > 8 && !(o.loose ? leader_clear_dots(it, l0, l1) : leader_clear(it, l0, l1))) continue;
            if (reaches[ri] > 8 && c.texts.some(function (t) { return K.seg_hits_box(l0[0], l0[1], l1[0], l1[1], t.x - 1, t.y - 1, t.x + t.w + 1, t.y + t.h + 1); })) continue;
            var xt = anchor === 'middle' ? bx + w / 2 : anchor === 'end' ? bx + w : bx;
            c.text(xt, top0 + A * size, lines.join(' '), { role: 'label', weight: it.weight, anchor: anchor, halo: true, max: o.max ? o.max + 1 : undefined, leading: lh });
            if (reaches[ri] > 8) c.line(l0[0], l0[1], l1[0], l1[1], { stroke: 'leader', width: c.t('line-hairline'), mark: false });
            return true;
          }
        }
        return false;
      };
      var unplaced = [];
      items.forEach(function (it) {
        var mine = function (b) { return !(Math.abs(b.x + b.w / 2 - it.x) < 0.5 && Math.abs(b.y + b.h / 2 - it.y) < 0.5); };
        // the latest period sits beside its dot, over the path on a halo if it must; the others reach out on leaders that
        // cross no path
        // where a narrow column leaves no such place, a leader may cross the path, and last a name may lie on a halo over
        // the path, never over a dot or a name
        var far = [12, 26, 44, 66, 92, 124, 160];
        var dots_only = dotbox.filter(mine);
        // round 2 fix pass (BC S1): the latest period first takes a place clear of the path, beside its dot or on a leader that
        // crosses no path, then a leader that may cross it; only then does it sit over the path on a halo, which would cut a
        // gap out of the path's line
        // where its full words find no such place, it takes its short words (labels.short) clear of the path first
        var sh = it.short && it.short !== it.words ? Object.assign({}, it, { words: it.short }) : null;
        if (it.last) { if (!place(it, avoid.filter(mine), [0, 4, 8].concat(far)) && !(sh && place(sh, avoid.filter(mine), [0, 4, 8].concat(far))) && !place(it, avoid.filter(mine), far, { loose: true }) && !place(it, dots_only, [0, 4, 8]) && !place(it, dots_only, far, { loose: true })) unplaced.push(it); return; }
        // the gap: a small open ring at the middle of the break, which the key over the plot names (MB-19)
        if (it.gap) {
          c.circle(it.x, it.y, 3.5, { fill: 'surface', mark: false });
          c.circle(it.x, it.y, 3.5, { stroke: 'subject', width: c.t('line-context') - 0.5, mark: false });
          return;
        }
        if (!place(it, avoid.filter(mine), [0].concat(far)) && !place(it, avoid.filter(mine), far, { loose: true }) && !place(it, dots_only, [0].concat(far), { loose: true })) unplaced.push(it);
      });
      var pl = { unplaced: unplaced };
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
