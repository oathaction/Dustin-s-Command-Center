/* Line field with highlight (coverage plan 3.3, extended; S27). Every series as a thin gray line on one scale, so the
 * reader sees the spread, and one series lit in ink with its name and latest value. A few other series may be named in
 * gray at their ends, to mark the field's edges. The scale starts at zero; a line at the index base, where the data has
 * one, is drawn heavier.
 * encode: x (year, month or date), y (number), series (category), label (text, optional: the series' name). labels: lit
 * (the series in ink), named (a list of series named in gray), end (words at a named line's end, with {name} and {y}),
 * base (a y value drawn as a heavier line, such as 100 for an index), base_label (words over the value axis).
 * formats: y (in the words), tick. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'line-field',
    name: 'Line Field',
    family: 'change-over-time',
    encode: { x: 'time', y: 'number', series: 'category', label: 'text?' },
    labels: ['lit', 'named', 'end', 'base', 'base_label'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ex = c.field('x'), ey = c.field('y'), es = c.field('series'), el = c.field('label', false);
      var by = {}, order = [];
      c.rows.forEach(function (r) { var k = String(r[es]); if (!by[k]) { by[k] = []; order.push(k); } by[k].push(r); });
      order.forEach(function (k) { by[k].sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); }); });
      var ts = c.rows.map(function (r) { return K.time(r[ex]); }), tlo = Math.min.apply(null, ts), thi = Math.max.apply(null, ts);
      var vmax = Math.max.apply(null, c.rows.map(function (r) { return r[ey]; }));
      var vs = P.value_scale(c, 0, vmax, 5), ticks = vs.ticks;
      var named = [String(L.lit)].concat((L.named || []).map(String)).filter(function (k) { return by[k]; });
      var endw = function (k) { var l = by[k][by[k].length - 1]; return String(L.end || '{name}').replace('{name}', el ? l[el] : k).replace('{y}', K.fmt(l[ey], f.y || 'number:0')); };
      var maxw = Math.round(W * (c.phone ? 0.3 : 0.25)), lw = 0, lines = {};
      named.forEach(function (k) { var wt = k === String(L.lit) ? 700 : 400; lines[k] = c.wrap(endw(k), 'label', maxw, wt); lines[k].forEach(function (l) { lw = Math.max(lw, c.measure(l, 'label', wt)); }); });
      var head = L.base_label ? c.size('tick') + 10 : 0;
      if (L.base_label) c.text(0, c.size('tick'), L.base_label, { role: 'tick', weight: 600, max: W });
      var top = head + c.size('tick') + 6, plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, ticks, f.tick || 'integer');
      var x0 = gut + 8, x1 = W - Math.ceil(lw) - 16;
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), xs = K.scale.linear([tlo, thi], [x0, x1]);
      P.value_grid(c, ys, ticks, f.tick || 'integer', x0, x1, gut);
      P.zero_line(c, ys, x0, x1);
      if (L.base !== undefined) c.line(x0, ys(L.base), x1, ys(L.base), { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      var path = function (k) { return by[k].map(function (r, i) { return (i ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[ey])); }).join(''); };
      // the field in gray, the named gray lines a step darker, then the lit line on its keyline
      order.forEach(function (k) {
        if (k === String(L.lit)) return;
        var nm = named.indexOf(k) >= 0;
        c.path(path(k), { stroke: nm ? 'context' : 'ghost', width: nm ? c.t('spark-context') : c.t('line-hairline'), data: { series: k } }, [x0, top, x1 - x0, plotH]);
        by[k].forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: k + '|' + r[ex], field: ey, value: r[ey] } }); });
      });
      if (by[String(L.lit)]) {
        var k0 = String(L.lit);
        c.path(path(k0), { stroke: 'surface', width: c.t('line-subject') + 2 * c.t('keyline'), mark: false });
        c.path(path(k0), { stroke: 'subject', width: c.t('line-subject'), data: { series: k0 } }, [x0, top, x1 - x0, plotH]);
        by[k0].forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[ey]), { data: { key: k0 + '|' + r[ex], field: ey, value: r[ey] } }); });
      } else c.warn('labels.lit names no series');
      // the names at the ends, spread apart where they would touch
      var lh = Math.round(c.size('label') * 1.2), gap = 4;
      var labs = named.map(function (k) { var l = by[k][by[k].length - 1]; return { k: k, want: ys(l[ey]), h: lh * lines[k].length, last: l }; }).sort(function (a, b) { return a.want - b.want; });
      labs.forEach(function (l) { l.y = l.want - l.h / 2; });
      for (var pass = 0; pass < 30; pass++) {
        var moved = false;
        for (var i = 1; i < labs.length; i++) { var o = labs[i - 1].y + labs[i - 1].h + gap - labs[i].y; if (o > 0.1) { labs[i - 1].y -= o / 2; labs[i].y += o / 2; moved = true; } }
        if (labs.length && labs[0].y < top - 6) { labs[0].y = top - 6; moved = true; }
        if (!moved) break;
      }
      labs.forEach(function (l) {
        var lit = l.k === String(L.lit), lx = x1 + 10, ly = l.y + c.size('label') * 0.85;
        c.circle(xs(K.time(l.last[ex])), ys(l.last[ey]), c.t(lit ? 'dot-vertex-radius' : 'dot-small-vertex-radius'), { fill: lit ? 'subject' : 'context', mark: false });
        lines[l.k].forEach(function (ln, j) { c.text(lx, ly + j * lh, ln, { role: 'label', weight: lit ? 700 : 400, fill: lit ? 'label' : 'secondary' }); });
      });
      // the time axis: a tick and a centered label at each x the rows hold, thinned to fit
      var ay = bot + c.size('tick') + 10, xsv = [];
      c.rows.forEach(function (r) { var t = K.time(r[ex]); if (xsv.indexOf(t) < 0) xsv.push(t); });
      xsv.sort(function (a, b) { return a - b; });
      // the first and last x keep their labels; those between take theirs where they touch neither neighbor
      var box = function (t) { var word = String(Math.floor(t)), w = c.measure(word, 'tick'), x = xs(t), anchor = x + w / 2 > W ? 'end' : 'middle'; return { t: t, word: word, x: x, anchor: anchor, l: anchor === 'end' ? x - w : x - w / 2, r: anchor === 'end' ? x : x + w / 2 }; };
      var keep = [box(xsv[0])];
      if (xsv.length > 1) keep.push(box(xsv[xsv.length - 1]));
      xsv.slice(1, -1).forEach(function (t) { var b = box(t); if (!keep.some(function (k) { return b.l < k.r + 8 && k.l < b.r + 8; })) keep.push(b); });
      xsv.forEach(function (t) { c.line(xs(t), bot + 1, xs(t), bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false }); });
      keep.forEach(function (b) { c.text(b.x, ay, b.word, { role: 'tick', anchor: b.anchor }); });
      c.height(Math.max(ay + 4, labs.length ? labs[labs.length - 1].y + labs[labs.length - 1].h : 0));
    }
  });
})(globalThis.OAChart);
