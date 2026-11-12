/* Area chart (coverage plan 3.3, extended; S29). One total over time, filled from zero in the band fill (as S13's panels draw it) with the series as
 * a Charcoal line on top, so the area reads as the amount itself. The scale always starts at zero (Rule 14.4).
 * encode: x (year, month or date), y (number). labels: area (words set inside the fill, naming what it counts), area_at
 * (the x value under which those words sit), x_ticks (the x values to label, in place of the kit's own thinning).
 * formats: y (values in notes), y_tick (axis). annotations: [{at: {x}, text, value, place, dx, dy, max, dot, anchor,
 * phone}]: "value": true prints the point's value before the text; a phone object overrides on a phone, and
 * "phone": {"hide": true} leaves the note out there. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'area',
    name: 'Area Chart',
    family: 'change-over-time',
    encode: { x: 'time', y: 'number' },
    labels: ['area', 'area_at', 'x_ticks'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, ex = c.field('x'), ey = c.field('y'), f = c.spec.formats || {}, W = c.width;
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var ts = rows.map(function (r) { return K.time(r[ex]); });
      var tlo = ts[0], thi = ts[ts.length - 1];
      var vmax = Math.max.apply(null, rows.map(function (r) { return r[ey]; }));
      var vs = P.value_scale(c, 0, vmax, 5), ticks = vs.ticks;
      var top = c.size('tick') + 6, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.y_tick || 'integer');
      var x0 = gut + 12, x1 = W - (c.phone ? 8 : 16);
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([tlo, thi], [x0, x1]);
      var pts = rows.map(function (r) { return [xs(K.time(r[ex])), ys(r[ey])]; });
      var line = pts.map(function (p, i) { return (i ? 'L' : 'M') + K.round(p[0]) + ',' + K.round(p[1]); }).join('');
      // the area under the line, from the zero line up, drawn before the grid so the gridlines read across it
      var yz = ys(0);
      c.path('M' + K.round(pts[0][0]) + ',' + K.round(yz) + line.replace(/^M/, 'L') + 'L' + K.round(pts[pts.length - 1][0]) + ',' + K.round(yz) + 'Z',
        { fill: 'band', data: { field: ey } }, [x0, top, x1 - x0, plotH]);
      P.value_grid(c, ys, ticks, f.y_tick || 'integer', x0, x1, gut);
      // the series line on a keyline of the ground, then the zero line over the fill's foot
      c.path(line, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
      c.path(line, { stroke: 'subject', width: c.t('line-subject'), data: { field: ey } }, [x0, top, x1 - x0, plotH]);
      rows.forEach(function (r, i) { c.datum(pts[i][0], pts[i][1], { data: { key: r[ex], field: ey, value: r[ey] } }); });
      P.zero_line(c, yz, x0, x1);
      // the words that name the fill, set inside it under the line
      if (c.labels.area) {
        var at = c.labels.area_at !== undefined ? rows.filter(function (r) { return String(r[ex]) === String(c.labels.area_at); })[0] : rows[Math.floor(rows.length / 2)];
        if (!at) c.warn('labels.area_at matches no row');
        else {
          var ax = xs(K.time(at[ex])), ay = ys(at[ey]), maxw = Math.max(80, (x1 - x0) * (c.phone ? 0.6 : 0.4));
          var lines = c.wrap(c.labels.area, 'label', maxw, 600);
          var lh = Math.round(c.size('label') * 1.25), hgt = c.size('label') + lh * (lines.length - 1);
          var by = Math.min(yz - 12 - lh * (lines.length - 1), ay + (yz - ay) / 2 + hgt / 2 - lh * (lines.length - 1));
          c.text(ax, by, c.labels.area, { role: 'label', weight: 600, anchor: 'middle', max: maxw + 1 });
        }
      }
      // the time axis: a tick and a label at each chosen x, thinned to fit and ending on the last value when it can
      var ay2 = bot + c.size('tick') + 10, picks = c.labels.x_ticks;
      if (!picks) {
        var span = Math.round(thi - tlo), wmax = c.measure('0000', 'tick') + 16, steps = [1, 2, 3, 4, 5, 10, 20, 25, 50], step = null;
        steps.forEach(function (s) { if (step === null && xs(tlo + s) - xs(tlo) >= wmax && span % s === 0) step = s; });
        if (step === null) steps.forEach(function (s) { if (step === null && xs(tlo + s) - xs(tlo) >= wmax) step = s; });
        picks = [];
        for (var yr = Math.ceil(tlo - 1e-9); yr <= thi + 1e-9; yr += step || 1) picks.push(yr);
      }
      picks.forEach(function (p) {
        var x = xs(K.time(p)), word = K.fmt(p, 'year'), yw = c.measure(word, 'tick');
        var anchor = x + yw / 2 > W ? 'end' : x - yw / 2 < 0 ? 'start' : 'middle';
        c.line(x, bot + 1, x, bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(anchor === 'end' ? W : anchor === 'start' ? 0 : x, ay2, word, { role: 'tick', anchor: anchor });
      });
      // notes inside the plot, each with a leader to its point
      c.annotations.forEach(function (a) {
        if (c.phone && a.phone && a.phone.hide) return;
        var hit = rows.filter(function (r) { return String(r[ex]) === String(a.at.x); })[0];
        if (!hit) { c.warn('annotation at ' + JSON.stringify(a.at) + ' matches no row'); return; }
        var px = xs(K.time(hit[ex])), py = ys(hit[ey]);
        var o = Object.assign({}, a, c.phone && a.phone ? a.phone : {});
        if (o.dot) c.circle(px, py, c.t('dot-subject-radius'), { fill: 'subject', mark: false });
        var words = a.value ? K.fmt(hit[ey], f.y || 'integer') + (a.text ? a.text : '') : a.text;
        P.note(c, px, py, words, { place: o.place, dx: o.dx, dy: o.dy, max: o.max, weight: a.value ? 700 : 400, anchor: o.anchor, leader: o.leader });
      });
      c.height(ay2 + 4);
    }
  });
})(globalThis.OAChart);
