/* Column (coverage plan 3.1, core; S17). One column per category or period from a zero line, in the data's order or
 * spec.sort, each value printed at the column's end and each category named under it. Columns the title names are set in
 * ink, the rest in the light fill on Newsprint and the context ink on Charcoal (palette rule R3). On a phone the columns turn into bars read from top to bottom, so every value keeps its label.
 * encode: x (the column's key: a category, year or number), y (number), sub (text, optional: a second line under each
 * name, such as the years a Congress sat; printed under every column where it fits, else under the first and last).
 * labels: categories ({x value: printed name}; the x value itself otherwise), named (an x value or a list of them, set in
 * ink; with none, every column is in ink), point (the one x value a title names in working red, with its keyline on
 * Newsprint; ED-E1). The fills come from K.parts.named_fill. formats: value (the printed values). A negative value draws below the zero line. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'column',
    name: 'Column',
    family: 'comparison',
    encode: { x: 'category', y: 'number', sub: 'text?' },
    labels: ['categories', 'named', 'point'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ex = c.field('x'), ey = c.field('y'), es = c.field('sub', false);
      var f = c.spec.formats || {}, W = c.width, L = c.labels, names = L.categories || {};
      // palette rule R3 and the red point by name (ED-E1), through the kit's shared part
      var fill = K.parts.named_fill(c, L.named, ex, null, L.point);
      var is_named = function (r) { return fill.is_named(r) || fill.is_point(r); };
      // the red point's keyline is its own outline over the fill: kit.css's keyline class sets fill none, so the two on
      // one element would leave the point hollow on Newsprint
      var keyline = function (r, x, y, w, h) { var k = fill.keyline(r); if (k.stroke) c.rect(x + 0.5, y + 0.5, Math.max(0, w - 1), Math.max(0, h - 1), { stroke: k.stroke, width: k.width, mark: false }); };
      var name = function (r) { return names[String(r[ex])] !== undefined ? names[String(r[ex])] : String(r[ex]); };
      var val = function (r) { return K.fmt(r[ey], f.value || 'integer'); };
      var vals = rows.map(function (r) { return r[ey]; });
      var max = Math.max(0, Math.max.apply(null, vals)), min = Math.min(0, Math.min.apply(null, vals));
      var size = c.size('label'), tick = c.size('tick'), n = rows.length;
      if (c.phone) {
        // bars, one per row from top to bottom: the name (and its second line) at the left, the value at the bar's end
        var lw = 0;
        rows.forEach(function (r) {
          lw = Math.max(lw, c.measure(name(r), 'label', 700));
          if (es && r[es] !== null && r[es] !== undefined) lw = Math.max(lw, c.measure(String(r[es]), 'tick'));
        });
        var vw = 0, vwn = 0;
        rows.forEach(function (r) { var w = c.measure(val(r), 'label', 700, true); if (r[ey] < 0) vwn = Math.max(vwn, w); else vw = Math.max(vw, w); });
        var left = Math.ceil(lw + 14) + (min < 0 ? vwn + 8 : 0);
        var xs = K.scale.linear([min, max], [left, Math.max(left + 40, W - vw - 8)]), zx = xs(0);
        var bh = c.t('bar-phone-height'), lh2 = Math.round(tick * 1.3);
        var pitch = Math.max(bh, size + (es ? lh2 : 0)) + 14, y = 2, top = y;
        rows.forEach(function (r, i) {
          var by = y + i * pitch, cy = by + bh / 2, two = es && r[es] !== null && r[es] !== undefined;
          var ny = two ? cy - lh2 / 2 + size * 0.35 : cy + size * 0.35;
          c.text(0, ny, name(r), { role: 'label', weight: is_named(r) ? 700 : 600 });
          if (two) c.text(0, ny + lh2, String(r[es]), { role: 'tick', fill: 'secondary' });
          var xe = xs(r[ey]);
          c.rect(Math.min(zx, xe), by, Math.abs(xe - zx), bh, { fill: fill(r), kind: 'bar', axis: 'x', zero: zx, data: { key: r[ex], field: ey, value: r[ey] } });
          keyline(r, Math.min(zx, xe), by, Math.abs(xe - zx), bh);
          var neg = r[ey] < 0;
          c.text(neg ? xe - 6 : xe + 6, cy + size * 0.35, val(r), { role: 'label', weight: is_named(r) ? 700 : 600, anchor: neg ? 'end' : 'start', tnum: true });
        });
        var bottom = top + (n - 1) * pitch + bh;
        c.line(zx, top - 4, zx, bottom + 4, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
        c.height(bottom + 6);
        return;
      }
      // columns: values above (below for a negative), names and second lines under the zero line
      var plotH = c.t('columns-height'), head = size + 10;
      var top2 = head, bot = top2 + plotH;
      var span = max - min || 1, zy;
      // the zero line sits where the share of negative values puts it
      zy = top2 + plotH * (max / span);
      var ys = K.scale.linear([min, max], [top2 + plotH, top2]);
      // a column fills its step as a ranked bar fills its pitch (bar height over pitch), so the two forms read alike
      var step = W / n, bw = Math.min(step * c.t('bar-height') / c.t('bar-pitch'), step - 8);
      var xc = function (i) { return step * i + step / 2; };
      rows.forEach(function (r, i) {
        var v = r[ey], yv = ys(v), x = xc(i);
        c.rect(x - bw / 2, Math.min(zy, yv), bw, Math.abs(yv - zy), { fill: fill(r), kind: 'bar', axis: 'y', zero: zy, data: { key: r[ex], field: ey, value: v } });
        keyline(r, x - bw / 2, Math.min(zy, yv), bw, Math.abs(yv - zy));
        var neg = v < 0;
        c.text(x, neg ? yv + size + 4 : yv - 7, val(r), { role: 'label', weight: is_named(r) ? 700 : 600, anchor: 'middle', tnum: true });
      });
      c.line(0, zy, W, zy, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      // the names under the zero line (under the lowest negative column when there is one)
      var ny = Math.max(zy, min < 0 ? ys(min) + size + 6 : zy) + tick + 10;
      rows.forEach(function (r, i) {
        c.text(xc(i), ny, name(r), { role: 'tick', weight: is_named(r) ? 700 : 600, anchor: 'middle', fill: 'label' });
      });
      var h = ny + 4;
      if (es) {
        // every second line where each fits its column's step; otherwise the first and last only, set outward
        var all = rows.every(function (r) { return c.measure(String(r[es] == null ? '' : r[es]), 'tick') + 10 <= step; });
        var sy = ny + Math.round(tick * 1.4);
        rows.forEach(function (r, i) {
          if (r[es] === null || r[es] === undefined) return;
          if (all) c.text(xc(i), sy, String(r[es]), { role: 'tick', anchor: 'middle' });
          else if (i === 0) c.text(xc(i) - bw / 2, sy, String(r[es]), { role: 'tick' });
          else if (i === n - 1) c.text(xc(i) + bw / 2, sy, String(r[es]), { role: 'tick', anchor: 'end' });
        });
        h = sy + 4;
      }
      c.height(Math.max(h, bot));
    }
  });
})(globalThis.OAChart);
