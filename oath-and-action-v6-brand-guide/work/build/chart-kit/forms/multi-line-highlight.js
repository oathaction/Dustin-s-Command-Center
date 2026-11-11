/* Multi-line with one highlighted, as small multiples (coverage plan 3.3, core; S05). One panel per series on one shared
 * scale; each panel draws its own series in Charcoal over the others in thin Stone, so a reader compares shape and level.
 * A change in the break column between two points starts a new segment, never bridged (R16).
 * encode: x (year or month), y (number), series (category), break (category, optional).
 * labels: panels ([{value, label}] in order), panel_value (words under each panel title with {x} and {y} of its last point),
 * domain ([lo, hi]), columns (panels per row at desktop; 2 on a phone). formats: x, y, tick. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'multi-line-highlight', name: 'Small Multiple Lines', family: 'change-over-time',
    encode: { x: 'time', y: 'number', series: 'category', break: 'category?' },
    labels: ['panels', 'panel_value', 'domain', 'columns'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, rows = c.rows, ex = c.field('x'), ey = c.field('y'), es = c.field('series'), eb = c.field('break', false);
      var f = c.spec.formats || {}, W = c.width, L = c.labels;
      var panels = L.panels || [];
      var by = {};
      rows.forEach(function (r) { (by[String(r[es])] = by[String(r[es])] || []).push(r); });
      Object.keys(by).forEach(function (k) { by[k].sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); }); });
      var ts = rows.map(function (r) { return K.time(r[ex]); }), tlo = Math.min.apply(null, ts), thi = Math.max.apply(null, ts);
      var vals = rows.map(function (r) { return r[ey]; });
      var dom = L.domain || K.nice(Math.min.apply(null, vals), Math.max.apply(null, vals), 4);
      var cols = c.phone ? 2 : (L.columns || panels.length), gapx = c.phone ? 18 : 26;
      var tk = K.ticks(dom[0], dom[1], 4), gut = 0;
      tk.forEach(function (t, i) { gut = Math.max(gut, c.measure(K.fmt(t, (i === tk.length - 1 && f.tick_last) || f.tick || 'integer'), 'tick') + 12); });
      gut = Math.ceil(gut);
      var pw = Math.floor((W - gut - gapx * (cols - 1)) / cols), ph = c.phone ? 110 : 130, head = 46;
      function segs(list) {
        var out = [[]];
        list.forEach(function (r, i) {
          if (i && eb && r[eb] !== list[i - 1][eb] && out[out.length - 1].length) out.push([]);
          if (i && K.time(r[ex]) === K.time(list[i - 1][ex]) && out[out.length - 1].length) out.push([]);
          out[out.length - 1].push(r);
        });
        return out.filter(function (s) { return s.length > 1; });
      }
      var y0 = 0, ticks = K.ticks(dom[0], dom[1], 4);
      panels.forEach(function (pnl, i) {
        var col = i % cols, row = Math.floor(i / cols);
        var px = gut + col * (pw + gapx), py = y0 + row * (ph + head + 34);
        var ys = K.scale.linear(dom, [py + head + ph, py + head]), xs = K.scale.linear([tlo, thi], [px, px + pw]);
        var mine = by[String(pnl.value)] || [];
        var lb = c.text(px, py + c.size('label'), pnl.label, { role: 'label', weight: 600, max: pw });
        if (L.panel_value && mine.length) c.text(px, lb.y + lb.h + c.size('tick') + 2, P.fill(c, L.panel_value, mine[mine.length - 1]), { role: 'tick' });
        ticks.forEach(function (t) {
          c.line(px, ys(t), px + pw, ys(t), { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
          if (col === 0) c.text(gut - 8, ys(t) + c.size('tick') * 0.35, K.fmt(t, (t === ticks[ticks.length - 1] && f.tick_last) || f.tick || 'integer'), { role: 'tick', anchor: 'end' });
        });
        panels.forEach(function (o) {
          if (o.value === pnl.value) return;
          segs(by[String(o.value)] || []).forEach(function (s) {
            c.path(s.map(function (r, j) { return (j ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''), { stroke: 'context', width: c.t('line-hairline'), mark: false });
          });
        });
        segs(mine).forEach(function (s) {
          c.path(s.map(function (r, j) { return (j ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''), { stroke: 'subject', width: c.t('line-context'), data: { series: pnl.value } }, [px, py + head, pw, ph]);
        });
        mine.forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: pnl.value + '|' + r[ex] + (eb ? '|' + r[eb] : ''), field: ey, value: r[ey] } }); });
        var ay = py + head + ph + c.size('tick') + 6;
        c.text(px, ay, K.fmt(tlo, 'year'), { role: 'tick' });
        c.text(px + pw, ay, K.fmt(Math.round(thi), 'year'), { role: 'tick', anchor: 'end' });
      });
      var nrows = Math.ceil(panels.length / cols);
      c.height(y0 + nrows * (ph + head + 34) - 10);
    }
  });
})(globalThis.OAChart);
