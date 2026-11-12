/* Sparkline (coverage plan 3.3, core; S28). A word-sized line set inside a sentence, as a reader meets it in prose: the
 * line runs as wide as a short word group and as tall as the type, scaled to its own lowest and highest values, with a dot
 * on its last value and a smaller one on its first. The words around it come from the spec, and the figures in them from
 * the data, so the sentence and the line always agree.
 * encode: x (year, month or date), values (list of number columns, one per sentence that names it). labels: sentences
 * ([{field, text}]: text holds {spark} once where the line sits, and may hold {first}, {last}, {min}, {max} (values of
 * field, formatted by formats[field]), {first_x}, {last_x}, {min_x}, {max_x} (formatted by formats.x, "year" by default)
 * and {change_pct} (the change from first to last in percent, formatted by formats.change_pct), and low (true: a ring on
 * the lowest value, for a sentence that names it)), spark_em (the line's width in ems, 6 by default). Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'sparkline',
    name: 'Sparkline',
    family: 'change-over-time',
    encode: { x: 'time', values: 'list' },
    labels: ['sentences', 'spark_em'],
    phone: 'same',
    draw: function (c) {
      var ex = c.field('x'), f = c.spec.formats || {}, W = c.width;
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var size = c.t(c.phone ? 'type-label' : 'type-measure-size'), lead = c.phone ? Math.round(size * 1.5) : c.t('type-measure-leading');
      var sw = Math.round(size * (c.labels.spark_em || 6)), sh = Math.round(size * 1.0), space = K.measure(' ', size, 400, 'reading', true);
      var y = size;
      (c.labels.sentences || []).forEach(function (sn, si) {
        var col = sn.field, list = rows.filter(function (r) { return r[col] !== null && r[col] !== undefined; });
        if (!list.length) { c.warn('no values for ' + col); return; }
        var lo = list[0], hi = list[0];
        list.forEach(function (r) { if (r[col] < lo[col]) lo = r; if (r[col] > hi[col]) hi = r; });
        var first = list[0], last = list[list.length - 1], fx = f.x || 'year', fv = f[col] || 'integer';
        var fill = { first: K.fmt(first[col], fv), last: K.fmt(last[col], fv), min: K.fmt(lo[col], fv), max: K.fmt(hi[col], fv),
          first_x: K.fmt(first[ex], fx), last_x: K.fmt(last[ex], fx), min_x: K.fmt(lo[ex], fx), max_x: K.fmt(hi[ex], fx),
          change_pct: K.fmt((last[col] - first[col]) / first[col] * 100, f.change_pct || 'number:0') };
        var text = String(sn.text).replace(/\{(first|last|min|max|first_x|last_x|min_x|max_x|change_pct)\}/g, function (_, k) { return fill[k]; });
        // lay the sentence out word by word, the line taking one word's place
        var parts = text.split('{spark}'), items = [];
        parts.forEach(function (p, i) {
          p.split(/ +/).filter(function (w) { return w.length; }).forEach(function (w) { items.push({ w: w }); });
          if (i < parts.length - 1) items.push({ spark: true });
        });
        var lines = [[]], lw = 0;
        items.forEach(function (it) {
          var w = it.spark ? sw : K.measure(it.w, size, 400, 'reading', true);
          if (lines[lines.length - 1].length && lw + space + w > W) { lines.push([]); lw = 0; }
          lw += (lines[lines.length - 1].length ? space : 0) + w;
          lines[lines.length - 1].push(it);
        });
        lines.forEach(function (ln, li) {
          var x = 0, run = [], by = y + li * lead;
          var flush = function () { if (run.length) { var b = c.text(x, by, run.join(' '), { role: 'label', size: size, weight: 400, tnum: true }); x = b.x + b.w; run = []; } };
          ln.forEach(function (it, k) {
            if (!it.spark) { if (!run.length && k) x += space; run.push(it.w); return; }
            flush();
            var sx = x + (k ? space : 0), top = by - size * 0.86, bot = top + sh;
            var xs = K.scale.linear([K.time(list[0][ex]), K.time(last[ex])], [sx + 2, sx + sw - 3]);
            var ys = K.scale.linear([lo[col], hi[col] === lo[col] ? lo[col] + 1 : hi[col]], [bot, top]);
            var d = list.map(function (r, i) { return (i ? 'L' : 'M') + K.round(xs(K.time(r[ex]))) + ',' + K.round(ys(r[col])); }).join('');
            c.path(d, { stroke: 'subject', width: c.t('spark-line'), data: { series: col } }, [sx, top, sw, sh]);
            list.forEach(function (r) { c.datum(xs(K.time(r[ex])), ys(r[col]), { data: { key: col + '|' + r[ex], field: col, value: r[col] } }); });
            c.circle(xs(K.time(first[ex])), ys(first[col]), c.t('spark-end-radius') * 0.7, { fill: 'subject', mark: false });
            c.circle(xs(K.time(last[ex])), ys(last[col]), c.t('spark-end-radius'), { fill: 'subject', mark: false });
            if (sn.low && lo !== first && lo !== last) c.circle(xs(K.time(lo[ex])), ys(lo[col]), c.t('spark-end-radius'), { fill: 'surface', mark: false }), c.circle(xs(K.time(lo[ex])), ys(lo[col]), c.t('spark-end-radius'), { stroke: 'subject', width: 1.5, mark: false });
            x = sx + sw;
          });
          flush();
        });
        y += lines.length * lead + (si < c.labels.sentences.length - 1 ? Math.round(lead * 0.5) : 0);
      });
      c.height(y - lead + size * 0.3 + 4);
    }
  });
})(globalThis.OAChart);
