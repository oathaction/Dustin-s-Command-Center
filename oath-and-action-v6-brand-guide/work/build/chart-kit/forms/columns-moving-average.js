/* Columns with a moving average (coverage plan 3.3, core; S14). Monthly values as columns from zero in Stone, the average
 * as a Charcoal line, preliminary months hatched and the average dashed where it includes one, the latest month labeled.
 * encode: x (month), y (number), average (number, optional), status (category, optional; spec.labels.preliminary_value
 * names the value that marks a preliminary month). labels: key_columns, key_preliminary, key_average, latest (one or two
 * lines with {x} and {y}), preliminary_value. formats: x, y (labels), y_tick (axis). annotations: [{at: {x}, text, target:
 * 'average' | 'y' | 'low', place, dx, dy}]. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'columns-moving-average',
    name: 'Columns With Moving Average',
    family: 'change-over-time',
    encode: { x: 'month', y: 'number', average: 'number?', status: 'category?' },
    labels: ['key_columns', 'key_preliminary', 'key_average', 'latest', 'preliminary_value'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ex = c.field('x'), ey = c.field('y'), ea = c.field('average', false), es = c.field('status', false);
      var f = c.spec.formats || {};
      var prelim_value = c.label('preliminary_value', 'preliminary');
      var is_pre = function (r) { return es && r[es] === prelim_value; };
      var W = c.width, y = 0;
      // the key
      var keys = [{ label: c.label('key_columns'), fill: 'context' }];
      if (es && rows.some(is_pre) && c.labels.key_preliminary) keys.push({ label: c.labels.key_preliminary, pattern: 'pre', stroke: 'context', direct: true });
      if (ea && c.labels.key_average) keys.push({ label: c.labels.key_average, shape: 'line', stroke: 'subject', direct: true });
      y += c.size('label') + 2;
      y += P.key(c, keys, 0, y, W) + 14;
      // the scale
      var vals = [];
      rows.forEach(function (r) { vals.push(r[ey]); if (ea && r[ea] !== null) vals.push(r[ea]); });
      var lo = Math.min(0, Math.min.apply(null, vals)), hi = Math.max(0, Math.max.apply(null, vals));
      var vs = P.value_scale(c, lo, hi, c.phone ? 4 : 5), ticks = vs.ticks;
      var gut = P.value_gutter(c, ticks, f.y_tick || 'signed');
      var top = y + 30, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]);
      var x0 = gut + 4, x1 = W;
      var n = rows.length, step = (x1 - x0) / n, bw = step * c.t('columns-fill-share');
      var xc = function (i) { return x0 + step * i + step / 2; };
      P.value_grid(c, ys, ticks, f.y_tick || 'signed', x0, x1, gut);
      // the columns
      c.pattern('pre', 'context');
      rows.forEach(function (r, i) {
        var v = r[ey], yz = ys(0), yv = ys(v);
        var o = { kind: 'bar', axis: 'y', zero: yz, data: { key: r[ex], field: ey, value: v } };
        if (is_pre(r)) {
          c.rect(xc(i) - bw / 2, Math.min(yz, yv), bw, Math.abs(yv - yz), Object.assign({ pattern: 'pre' }, o));
          c.rect(xc(i) - bw / 2 + 0.5, Math.min(yz, yv) + 0.5, Math.max(0, bw - 1), Math.max(0, Math.abs(yv - yz) - 1), { stroke: 'context', mark: false });
        } else c.rect(xc(i) - bw / 2, Math.min(yz, yv), bw, Math.abs(yv - yz), Object.assign({ fill: 'context' }, o));
      });
      P.zero_line(c, ys(0), x0, x1);
      // the average: solid through final months, dashed from the first segment that reaches a preliminary month
      if (ea) {
        var pts = rows.map(function (r, i) { return r[ea] === null ? null : [xc(i), ys(r[ea]), is_pre(r)]; });
        var solid = '', dash = '', prev = null;
        pts.forEach(function (p) {
          if (!p) { prev = null; return; }
          if (prev) {
            var seg = 'M' + K.round(prev[0]) + ',' + K.round(prev[1]) + 'L' + K.round(p[0]) + ',' + K.round(p[1]);
            if (p[2]) dash += seg; else solid += seg;
          }
          prev = p;
        });
        var lw = c.t('columns-average-line');
        if (solid) c.path(solid, { stroke: 'surface', width: lw + 2 * c.t('keyline'), mark: false });
        if (solid) c.path(solid, { stroke: 'subject', width: lw, data: { field: ea } }, [x0, top, x1 - x0, plotH]);
        if (dash) c.path(dash, { stroke: 'subject', width: lw, dash: '4 3', data: { field: ea, status: prelim_value } }, [x0, top, x1 - x0, plotH]);
      }
      // the time axis
      var tlo = K.time(rows[0][ex]), thi = K.time(rows[n - 1][ex]);
      var xt = function (t) { return x0 + (t - tlo) * 12 * step + (step - bw) / 2; };
      var ay = bot + c.size('tick') + 10;
      if (vs.lo < 0) ay = Math.max(ay, ys(vs.lo) + c.size('tick') + 10);
      P.year_axis(c, xt, tlo, thi, ay, x1);
      var h = ay + 6;
      // the latest month, labeled at the right edge
      var last = rows[n - 1];
      if (c.labels.latest) {
        var lines = [].concat(c.labels.latest).map(function (t) { return P.fill(c, t, last); });
        var lx = xc(n - 1), ly = Math.min(ys(last[ey]), ys(0)) - 8;
        var lt = top - 4 + c.size('label');
        var hi_y = Math.min(ly - 12 - (lines.length - 1) * 19, lt);
        c.text(W, hi_y, lines[0], { role: 'label', weight: 700, anchor: 'end', halo: true });
        for (var li = 1; li < lines.length; li++) c.text(W, hi_y + li * 19, lines[li], { role: 'label', weight: 400, anchor: 'end', fill: 'secondary', halo: true, size: c.size('tick') + 1 });
        c.line(lx, hi_y + (lines.length - 1) * 19 + 6, lx, ly, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      }
      // notes inside the plot
      c.annotations.forEach(function (a) {
        if (c.phone && a.phone && a.phone.hide) return;
        a = Object.assign({}, a, c.phone && a.phone ? a.phone : {});
        var i = rows.findIndex(function (r) { return String(r[ex]) === String(a.at.x); });
        if (i < 0) { c.warn('annotation at ' + a.at.x + ' matches no row'); return; }
        var r = rows[i], py;
        if (a.target === 'average' && ea) py = ys(r[ea]);
        else if (a.target === 'low') py = ys(Math.min(0, r[ey]));
        else py = ys(r[ey]);
        P.note(c, xc(i), py, a.text, { place: a.place, dx: a.dx, dy: a.dy, max: a.max });
      });
      c.height(h);
    }
  });
})(globalThis.OAChart);
