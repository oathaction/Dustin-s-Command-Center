/* Line with a data gap marked (coverage plan 3.3, core; S31). One series as a Charcoal line from a zero-based scale. A row
 * with no value is a gap: the line stops before it and starts again after it, never bridged, and a light column over the
 * missing period carries a label that names it (Rule 14.11). Consecutive empty rows make one gap.
 * encode: x (month, date or year), y (number; an empty cell is a gap). labels: gap (words for each gap, with {x} for its
 * first missing x, formatted by formats.x, and {x_last} for its last), gap_place ("left" or "right" of the column, at the
 * plot's top; "right" by default). formats: x (in the gap words, "month" by default), y (values in notes), y_tick (axis),
 * y_tick_top (the top tick). scale: {"y": [lo, hi]} as for every form. annotations: [{at: {x}, text, value, place, dx, dy,
 * max, dot, anchor, phone}]: "value": true prints the point's value before the text; a phone object overrides on a phone,
 * and "phone": {"hide": true} leaves the note out there. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'line-data-gap',
    name: 'Line With Data Gap',
    family: 'change-over-time',
    encode: { x: 'time', y: 'number' },
    labels: ['gap', 'gap_place'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, ex = c.field('x'), ey = c.field('y'), f = c.spec.formats || {}, W = c.width;
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var n = rows.length, ts = rows.map(function (r) { return K.time(r[ex]); });
      var have = rows.filter(function (r) { return r[ey] !== null && r[ey] !== undefined; });
      var vmax = Math.max.apply(null, have.map(function (r) { return r[ey]; }));
      var vs = P.value_scale(c, 0, vmax, 5), ticks = vs.ticks;
      var top = c.size('label') * 2 + c.size('tick') + 18, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.y_tick || 'number');
      var x0 = gut + 8, x1 = W - (c.phone ? 8 : 16);
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([ts[0], ts[n - 1]], [x0, x1]);
      var half = n > 1 ? (xs(ts[1]) - xs(ts[0])) / 2 : 4;
      // the gaps: runs of rows with no value
      var gaps = [], run = null;
      rows.forEach(function (r, i) {
        var miss = r[ey] === null || r[ey] === undefined;
        if (miss && !run) { run = { a: i, b: i }; gaps.push(run); } else if (miss) run.b = i; else run = null;
      });
      // each gap's column first, under the grid, so the gridlines read through it
      gaps.forEach(function (g) {
        var ga = Math.max(x0, xs(ts[g.a]) - half), gb = Math.min(x1, xs(ts[g.b]) + half);
        c.rect(ga, top, Math.max(2, gb - ga), bot - top, { fill: 'track', data: { key: rows[g.a][ex], field: ey, gap: 'yes' } });
      });
      P.value_grid(c, ys, ticks, f.y_tick || 'number', x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      // the line, in segments that stop at each gap
      var segs = [[]];
      rows.forEach(function (r, i) {
        if (r[ey] === null || r[ey] === undefined) { if (segs[segs.length - 1].length) segs.push([]); return; }
        segs[segs.length - 1].push([xs(ts[i]), ys(r[ey]), r]);
      });
      segs.filter(function (s) { return s.length; }).forEach(function (s) {
        var d = s.map(function (p, i) { return (i ? 'L' : 'M') + K.round(p[0]) + ',' + K.round(p[1]); }).join('');
        if (s.length === 1) d += 'L' + K.round(s[0][0] + 0.1) + ',' + K.round(s[0][1]);
        c.path(d, { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
        c.path(d, { stroke: 'subject', width: c.t('line-subject'), data: { field: ey } }, [x0, top, x1 - x0, plotH]);
        s.forEach(function (p) { c.datum(p[0], p[1], { data: { key: p[2][ex], field: ey, value: p[2][ey] } }); });
      });
      // the ends of the line at each gap get a small dot, so a reader sees the line stop on purpose
      gaps.forEach(function (g) {
        [g.a - 1, g.b + 1].forEach(function (k) {
          if (k < 0 || k >= n || rows[k][ey] === null) return;
          c.circle(xs(ts[k]), ys(rows[k][ey]), c.t('dot-small-vertex-radius'), { fill: 'subject', mark: false });
        });
      });
      // each gap's words, above the plot beside its column, with a leader down to the column's top
      if (c.labels.gap) {
        var side = c.labels.gap_place || 'right';
        gaps.forEach(function (g) {
          var words = String(c.labels.gap).replace('{x}', K.fmt(rows[g.a][ex], f.x || 'month')).replace('{x_last}', K.fmt(rows[g.b][ex], f.x || 'month'));
          var gx = xs(ts[g.a]) + (xs(ts[g.b]) - xs(ts[g.a])) / 2, ww = c.measure(words, 'label', 600);
          var anchor = side === 'left' ? 'end' : 'start', tx = side === 'left' ? gx + half : gx - half;
          if (anchor === 'start' && tx + ww > W && tx > W / 2) { anchor = 'end'; tx = gx + half; }
          if (anchor === 'end' && tx - ww < 0 && tx < W / 2) { anchor = 'start'; tx = gx - half; }
          // words wider than the room on their side wrap onto a second line above the first
          var room = anchor === 'end' ? tx : W - tx, lines = ww > room ? c.wrap(words, 'label', room, 600) : [words];
          var lh = Math.round(c.size('label') * 1.25), ty = top - 12 - lh * (lines.length - 1);
          c.text(tx, ty, words, { role: 'label', weight: 600, anchor: anchor, halo: true, max: lines.length > 1 ? room : undefined });
          ty += lh * (lines.length - 1);
          c.line(gx, ty + 5, gx, top, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
        });
      }
      // the time axis: a tick and the year at each January
      var ay = bot + c.size('tick') + 10;
      P.year_axis(c, xs, ts[0], ts[n - 1], ay, x1);
      // notes with leaders to their points
      c.annotations.forEach(function (a) {
        if (c.phone && a.phone && a.phone.hide) return;
        var k = rows.findIndex(function (r) { return String(r[ex]) === String(a.at.x); });
        if (k < 0 || rows[k][ey] === null) { c.warn('annotation at ' + JSON.stringify(a.at) + ' matches no row with a value'); return; }
        var o = Object.assign({}, a, c.phone && a.phone ? a.phone : {});
        var px = xs(ts[k]), py = ys(rows[k][ey]);
        if (o.dot) c.circle(px, py, c.t('dot-subject-radius'), { fill: 'subject', mark: false });
        var words = a.value ? K.fmt(rows[k][ey], f.y || 'number') + (a.text || '') : a.text;
        P.note(c, px, py, words, { place: o.place, dx: o.dx, dy: o.dy, max: o.max, weight: a.value ? 700 : 400, anchor: o.anchor, leader: o.leader });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
