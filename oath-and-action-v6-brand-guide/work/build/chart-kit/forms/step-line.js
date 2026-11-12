/* Step line (coverage plan 3.3, extended; S30). A rate or a rule that changes on dates: each row's value holds flat from
 * its x until the next row's x, and the line rises or falls straight up or down at the change, never on a slope. The scale
 * starts at zero. Each level carries its value; a run of rows with one value prints it once.
 * encode: x (year or date the value takes effect; a year spans to the next year), y (number), y2 (number, optional: a
 * second amount drawn thin in the context ink only where it differs from y, such as a higher amount for one group).
 * labels: value (words for each level, with {y} and any encode name, such as "${y}"), y2 (words for the y2 level, with
 * {y2}), x_end (the x where the last level ends; for years, the year after the last row by default).
 * formats: y, y2 (in the words), y_tick (axis). annotations: [{at: {x}, text, place, dx, dy, max, anchor, phone}]: a
 * note with a leader to the corner where that row's level begins; on a phone a note longer than 60 characters, or one
 * with "phone": {"below": true}, moves under the axis, and "phone": {"hide": true} leaves it out. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'step-line',
    name: 'Step Line',
    family: 'change-over-time',
    encode: { x: 'time', y: 'number', y2: 'number?' },
    labels: ['value', 'y2', 'x_end'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, ex = c.field('x'), ey = c.field('y'), e2 = c.field('y2', false), f = c.spec.formats || {}, W = c.width;
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var n = rows.length;
      var yearly = /^\d{4}$/.test(String(rows[0][ex]));
      var t0 = rows.map(function (r) { return K.time(r[ex]); });
      var tend = c.labels.x_end !== undefined ? K.time(c.labels.x_end) : yearly ? t0[n - 1] + 1 : t0[n - 1] + (t0[n - 1] - t0[n - 2]);
      var t1 = t0.slice(1).concat([tend]);
      var vals = [];
      rows.forEach(function (r) { vals.push(r[ey]); if (e2 && r[e2] !== null) vals.push(r[e2]); });
      var vs = P.value_scale(c, 0, Math.max.apply(null, vals), c.phone ? 4 : 5), ticks = vs.ticks;
      var top = c.size('label') + c.size('tick') + 14, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.y_tick || 'integer');
      var x0 = gut + 8, x1 = W - (c.phone ? 4 : 8);
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([t0[0], tend], [x0, x1]);
      P.value_grid(c, ys, ticks, f.y_tick || 'integer', x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      // the second amount, thin and in the context ink, only where it differs from the main one
      if (e2) {
        rows.forEach(function (r, i) {
          if (r[e2] === null || r[e2] === r[ey]) return;
          var xa = xs(t0[i]), xb = xs(t1[i]), yb = ys(r[e2]);
          c.line(xa, ys(r[ey]), xa, yb, { stroke: 'context', width: c.t('line-context'), mark: false });
          c.line(xa, yb, xb, yb, { stroke: 'context', width: c.t('line-context'), data: { key: r[ex] + '|' + e2, field: e2, value: r[e2] } });
          c.line(xb, yb, xb, ys(r[ey]), { stroke: 'context', width: c.t('line-context'), mark: false });
          if (c.labels.y2) {
            var w2 = P.fill(c, c.labels.y2, r), ww2 = c.measure(w2, 'label');
            c.text(Math.max(x0, Math.min(xa + 4, x1 - ww2)), yb - 8, w2, { role: 'label', weight: 400, fill: 'secondary', halo: true });
          }
        });
      }
      // the steps: flat through each span, straight up or down at each change
      var d = '';
      rows.forEach(function (r, i) {
        var xa = xs(t0[i]), xb = xs(t1[i]), y = ys(r[ey]);
        d += (i ? 'L' : 'M') + K.round(xa) + ',' + K.round(y) + 'L' + K.round(xb) + ',' + K.round(y);
      });
      c.path(d, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
      c.path(d, { stroke: 'subject', width: c.t('line-subject'), data: { field: ey } }, [x0, top, x1 - x0, plotH]);
      rows.forEach(function (r, i) { c.datum((xs(t0[i]) + xs(t1[i])) / 2, ys(r[ey]), { data: { key: r[ex], field: ey, value: r[ey] } }); });
      // each level's value once, over its run; where the words are wider than the run and a riser would cross them, under
      // the run, then beside it on the side where the line falls away
      var segs = [];
      rows.forEach(function (r, i) {
        if (i) segs.push([xs(t0[i]), ys(rows[i - 1][ey]), xs(t0[i]), ys(r[ey]), -1]);
        segs.push([xs(t0[i]), ys(r[ey]), xs(t1[i]), ys(r[ey]), i]);
        if (e2 && r[e2] !== null && r[e2] !== r[ey]) { segs.push([xs(t0[i]), ys(r[ey]), xs(t0[i]), ys(r[e2]), -1]); segs.push([xs(t1[i]), ys(r[ey]), xs(t1[i]), ys(r[e2]), -1]); }
      });
      var clear = function (bx, by, bw, bh, i0, i1) {
        if (bx < 0 || bx + bw > W) return false;
        if (segs.some(function (sg) { return (sg[4] < i0 || sg[4] > i1 || sg[4] < 0) && K.seg_hits_box(sg[0], sg[1], sg[2], sg[3], bx - 2, by - 2, bx + bw + 2, by + bh + 2); })) return false;
        return !c.texts.some(function (t) { return bx < t.x + t.w + 2 && t.x < bx + bw + 2 && by < t.y + t.h + 2 && t.y < by + bh + 2; });
      };
      if (c.labels.value) {
        var i = 0, sz = c.size('label'), asc = sz * 0.75;
        while (i < n) {
          var j = i;
          while (j + 1 < n && rows[j + 1][ey] === rows[i][ey]) j++;
          var xa = xs(t0[i]), xb = xs(t1[j]), ly = ys(rows[i][ey]), words = P.fill(c, c.labels.value, rows[i]), ww = c.measure(words, 'label', 700);
          var cx = Math.max(x0 + ww / 2, Math.min(x1 - ww / 2, (xa + xb) / 2));
          var nxt = j + 1 < n ? rows[j + 1][ey] : null, prv = i ? rows[i - 1][ey] : null;
          var cand = [[cx, ly - 9, 'middle'], [cx, ly + 9 + asc, 'middle']];
          if (nxt === null || nxt < rows[i][ey]) cand.push([xb + 6, ly + asc / 2, 'start']);
          if (prv === null || prv < rows[i][ey]) cand.push([xa - 6, ly + asc / 2, 'end']);
          var pick = cand.filter(function (p) { var bx = p[2] === 'middle' ? p[0] - ww / 2 : p[2] === 'end' ? p[0] - ww : p[0]; return clear(bx, p[1] - asc, ww, sz, i, j); })[0] || cand[0];
          c.text(pick[0], pick[1], words, { role: 'label', weight: 700, anchor: pick[2], halo: true, tnum: true });
          i = j + 1;
        }
      }
      // the time axis: each year's label centered in its span, with a tick at every boundary; on a narrow plot only the years
      // where the value changes keep their labels
      var ay = bot + c.size('tick') + 10, span_w = (x1 - x0) / Math.max(1, (tend - t0[0]));
      var fit = span_w >= c.measure('0000', 'tick') + 8, placed = [];
      var order = rows.map(function (r, k) { return k; });
      // where every year cannot carry its label, the years the value changes go first, then the first year
      if (!fit) order = order.filter(function (k) { return k > 0 && (rows[k][ey] !== rows[k - 1][ey] || (e2 && rows[k][e2] !== rows[k - 1][e2])); }).concat([0]);
      rows.forEach(function (r, k) { c.line(xs(t0[k]), bot + 1, xs(t0[k]), bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      if (yearly) order.forEach(function (k) {
        var r = rows[k], mx = (xs(t0[k]) + xs(t1[k])) / 2, word = K.fmt(r[ex], 'year'), hw = c.measure(word, 'tick') / 2;
        if (placed.some(function (p) { return mx - hw < p[1] + 6 && p[0] < mx + hw + 6; })) return;
        placed.push([mx - hw, mx + hw]);
        c.text(mx, ay, word, { role: 'tick', anchor: 'middle' });
      });
      c.line(xs(tend), bot + 1, xs(tend), bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      if (!yearly) {
        var px = K.ticks(t0[0], tend, c.phone ? 3 : 6);
        px.forEach(function (t) { if (Math.abs(t - Math.round(t)) < 1e-9) c.text(xs(t), ay, String(Math.round(t)), { role: 'tick', anchor: 'middle' }); });
      }
      // notes with leaders to the corner where a row's level begins; long ones go under the axis on a phone
      var below = [];
      c.annotations.forEach(function (a) {
        if (c.phone && a.phone && a.phone.hide) return;
        if (c.phone && ((a.phone && a.phone.below) || (!(a.phone && a.phone.below === false) && String(a.text).length > 60))) { below.push(a.text); return; }
        var k = rows.findIndex(function (r) { return String(r[ex]) === String(a.at.x); });
        if (k < 0) { c.warn('annotation at ' + JSON.stringify(a.at) + ' matches no row'); return; }
        var o = Object.assign({}, a, c.phone && a.phone ? a.phone : {});
        P.note(c, xs(t0[k]), ys(rows[k][ey]), a.text, { place: o.place, dx: o.dx, dy: o.dy, max: o.max, anchor: o.anchor, leader: o.leader });
      });
      var by = ay + 14;
      below.forEach(function (t) {
        var b = c.text(0, by + c.size('note'), t, { role: 'note', max: W });
        by = b.y + b.h + 10;
      });
      c.height(below.length ? by : ay + 4);
    }
  });
})(globalThis.OAChart);
