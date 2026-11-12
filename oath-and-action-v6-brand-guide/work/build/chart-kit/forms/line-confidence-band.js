/* Confidence band on a line (coverage plan 3.7, core; S58). A series of survey estimates as a 2 px line in the subject
 * ink over a band across each one's interval (K.parts.band, in Stone magnitude step 1, the data lead's RB-D2, with its two
 * edges as 1 px lines in the context ink, RF-2), the line thin enough that the band shows. Where the publisher changed its method, the line and the band
 * both break and the year draws both estimates, each a small dot (Rule 14.11): a row whose break value is in
 * labels.break_end ends a run, and one in labels.break_start begins the next; at one x an ending row sorts first and a
 * starting row last, as line-event-notes reads the same lists. Notes at a break come from spec.annotations
 * ({at: {x, break}, text, place, dx, dy}). The last estimate is named at the line's end with its interval.
 * encode: x (year), y (number), low and high (numbers), or margin (number), break (category, optional).
 * labels: break_end, break_start (a value or a list), end (words at the line's end, with {y}, {low}, {high}, {margin}),
 * y_axis (words over the value axis).
 * formats: y (the end words and the ticks unless tick is set), tick. scale: y ([lo, hi]). On a phone the same arrangement
 * draws narrower, with fewer year labels. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'line-confidence-band',
    name: 'Line Confidence Band',
    family: 'uncertainty-and-estimates',
    encode: { x: 'time', y: 'number', low: 'number?', high: 'number?', margin: 'number?', break: 'category?' },
    labels: ['break_end', 'break_start', 'end', 'y_axis'],
    interval: true,
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ex = c.field('x'), ey = c.field('y'), eb = c.field('break', false), iv = P.interval_of(c);
      var tick = c.size('tick'), size = c.size('label'), fy = f.y || 'integer', ft = f.tick || fy;
      var ends = [].concat(L.break_end === undefined ? [] : L.break_end).map(String), starts = [].concat(L.break_start === undefined ? [] : L.break_start).map(String);
      var bv = function (r) { return eb && r[eb] !== null && r[eb] !== undefined ? String(r[eb]) : ''; };
      var rank = function (r) { return ends.indexOf(bv(r)) >= 0 ? 0 : starts.indexOf(bv(r)) >= 0 ? 2 : 1; };
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]) || rank(a) - rank(b); });
      // the runs: a starting row opens a new one, an ending row closes the one it is in
      var runs = [], cur = [];
      rows.forEach(function (r) {
        if (starts.indexOf(bv(r)) >= 0 && cur.length) { runs.push(cur); cur = []; }
        cur.push(r);
        if (ends.indexOf(bv(r)) >= 0) { runs.push(cur); cur = []; }
      });
      if (cur.length) runs.push(cur);
      var ts = rows.map(function (r) { return K.time(r[ex]); }), tlo = Math.min.apply(null, ts), thi = Math.max.apply(null, ts);
      var los = rows.map(function (r) { return iv(r).lo; }), his = rows.map(function (r) { return iv(r).hi; });
      var vs = P.value_scale(c, Math.min.apply(null, los), Math.max.apply(null, his), ph ? 4 : 5), ticks = vs.ticks;
      var y = 0;
      if (L.y_axis) { c.text(0, tick, L.y_axis, { role: 'tick', weight: 600, max: W }); y = tick + 8; }
      var last = rows[rows.length - 1], endw = L.end ? String(L.end).replace('{y}', K.fmt(last[ey], fy)).replace('{low}', K.fmt(iv(last).lo, fy)).replace('{high}', K.fmt(iv(last).hi, fy)).replace('{margin}', K.fmt(iv(last).m, fy)) : '';
      var endl = endw ? c.wrap(endw, 'label', ph ? 92 : 120, 700) : [], ew = 0;
      endl.forEach(function (l) { ew = Math.max(ew, c.measure(l, 'label', 700)); });
      var top = y + tick, plotH = c.t(ph ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, ft), x0 = gut + 8, x1 = W - (endw ? Math.ceil(ew) + 12 : 6);
      var xs = K.scale.linear([tlo, thi], [x0, x1]), ys = K.scale.linear([vs.lo, vs.hi], [bot, top]);
      P.value_grid(c, ys, ticks, ft, x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      // the band under the line, one run a part, never bridging a break
      var pts = [];
      runs.forEach(function (run) {
        run.forEach(function (r, i) {
          var t = iv(r);
          pts.push({ x: xs(K.time(r[ex])), y0: ys(t.lo), y1: ys(t.hi), key: r[ex] + (bv(r) ? '|' + bv(r) : ''), low: t.lo, high: t.hi, break: i === 0 });
        });
      });
      // RF-2 (round 2 fix pass, D3-903): the fill sits under 3 to 1 on both grounds, so the band carries its meaning by its
      // two edges, 1 px lines in the context ink (4.29 to 1 on Newsprint, 5.41 on Charcoal)
      P.band(c, pts, { fill: 'mag-1', edge: 'context', field_low: iv.fields.low || 'low', field_high: iv.fields.high || 'high' });
      // the line, one path a run
      var path = function (run) { return run.map(function (r, i) { return (i ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''); };
      // no keyline of the ground under the line: it would read as the band's edge
      runs.forEach(function (run) {
        if (run.length > 1) c.path(path(run), { stroke: 'subject', width: c.t('line-context') }, [x0, top, x1 - x0, plotH]);
        run.forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: r[ex] + (bv(r) ? '|' + bv(r) : ''), field: ey, value: r[ey] } }); });
      });
      // both estimates at a break, each a small dot on the ground's keyline
      runs.forEach(function (run, j) {
        [j > 0 ? run[0] : null, j < runs.length - 1 ? run[run.length - 1] : null].forEach(function (r) {
          if (!r) return;
          var px = xs(K.time(r[ex])), py = ys(r[ey]);
          c.circle(px, py, c.t('dot-vertex-radius') + c.t('keyline'), { fill: 'surface', mark: false });
          c.circle(px, py, c.t('dot-vertex-radius'), { fill: 'subject', mark: false });
        });
      });
      // the notes at the breaks
      (c.annotations || []).forEach(function (a) {
        var at = a.at || {}, r = rows.filter(function (q) { return String(q[ex]) === String(at.x) && (at.break === undefined || bv(q) === String(at.break)); })[0];
        if (!r) { c.warn('an annotation names no row: ' + JSON.stringify(at)); return; }
        var o = { place: (ph && a.phone && a.phone.place) || a.place || 'above', dx: (ph && a.phone && a.phone.dx !== undefined) ? a.phone.dx : a.dx, dy: a.dy, max: ph ? 120 : 180 };
        if (!(ph && a.phone && a.phone.hide)) P.note(c, xs(K.time(r[ex])), ys(r[ey]) - (o.place === 'above' ? 6 : 0), a.text, o);
      });
      // the last estimate named at the line's end
      if (endw) {
        var lx = x1 + 10, lh = Math.round(size * 1.2), ly = ys(last[ey]) - (endl.length - 1) * lh / 2 + size * 0.35;
        c.circle(xs(K.time(last[ex])), ys(last[ey]), c.t('dot-vertex-radius'), { fill: 'subject', mark: false });
        endl.forEach(function (l, i) { c.text(lx, ly + i * lh, l, { role: 'label', weight: 700 }); });
      }
      // the years along the bottom: the last, and every k-th back from it that sits apart
      var ay = bot + tick + 10, years = [];
      rows.forEach(function (r) { var t = Math.floor(K.time(r[ex])); if (years.indexOf(t) < 0) years.push(t); });
      var box = function (t) { var w = c.measure(String(t), 'tick'), x = xs(t), an = x + w / 2 > W ? 'end' : x - w / 2 < 0 ? 'start' : 'middle'; return { t: t, x: x, an: an, l: an === 'end' ? x - w : an === 'start' ? x : x - w / 2, r: an === 'end' ? x : an === 'start' ? x + w : x + w / 2 }; };
      var keep = [], nice = [1, 2, 5, 10, 20, 25, 50];
      for (var k = 0; k < nice.length; k++) {
        var st = nice[k], pick = years.filter(function (t) { return (thi - t) % st === 0; }).map(box);
        if (pick.every(function (b, j) { return !j || pick[j - 1].r + 10 <= b.l; })) { keep = pick; break; }
      }
      keep.forEach(function (b) { c.line(b.x, bot + 1, b.x, bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); c.text(b.x, ay, String(b.t), { role: 'tick', anchor: b.an }); });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
