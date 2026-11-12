/* Bullet graph (coverage plan 3.9, extended; S64). A measure against its target and the ranges behind it, one row a
 * reading: the ranges as bands in the magnitude steps from zero, the measure as a narrow bar in the subject ink from
 * zero, the target as a tick in the text's ink across the bands. Every band edge and the target are named once over
 * the rows; each row prints its measure and its distance to the target in a column at the right (under the bar on a
 * phone). Bars start at zero (Rule 14.4).
 * encode: category (the row's name: a date, month or text), value (number), target (number, optional).
 * labels: bands ([{to, step, label}]: each band runs from the last one's end to `to`, in magnitude step 1 to 4, named
 * at its far edge), target_words ('{v}' words over the target's tick), value_words ('{v}'), rest_words ('{v}' words for
 * the distance to the target), category_format (a table format for the row names, such as month), per (a divisor for
 * the printed figures, such as 1000 to print millions as billions), tick_words ('{v}' words for the scale under the last
 * bar). formats: value (the figures in the words), tick (the scale's figures). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'bullet-graph', name: 'Bullet Graph', family: 'gauges-and-indicators',
    encode: { category: 'category', value: 'number', target: 'number?' },
    labels: ['bands', 'target_words', 'value_words', 'rest_words', 'category_format', 'per', 'tick_words'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, ek = c.field('category'), ev = c.field('value'), et = c.field('target', false), L = c.labels, W = c.width;
      var f = c.spec.formats || {}, bands = L.bands || [], size = c.size('label'), tick = c.size('tick');
      var fv = function (t, v, fm) { return String(t || '{v}').split('{v}').join(K.fmt(v / (L.per || 1), fm || f.value || 'integer')); };
      var name = function (r) { return K.fmt(r[ek], L.category_format || 'text'); };
      var hi = 0; rows.forEach(function (r) { hi = Math.max(hi, r[ev], et ? r[et] || 0 : 0); }); bands.forEach(function (b) { hi = Math.max(hi, b.to); });
      var nw = 0, vw = 0;
      rows.forEach(function (r) {
        nw = Math.max(nw, c.measure(name(r), 'label', 600));
        vw = Math.max(vw, c.measure(fv(L.value_words, r[ev]), 'label', 700, true));
        if (et && r[et]) vw = Math.max(vw, c.measure(fv(L.rest_words, r[et] - r[ev]), 'tick'));
      });
      var x0 = c.phone ? 0 : Math.ceil(nw + 16), x1 = c.phone ? W - 2 : Math.floor(W - vw - 14);
      var xs = K.scale.linear([0, hi], [x0, x1]);
      // the names of the band edges and the target over the rows, each moved up a line where it would touch another
      var heads = [], put = function (x, words, weight) {
        var w = c.measure(words, 'tick', weight), a = Math.max(0, Math.min(W - w, x - w - 4)), line = 0;
        while (heads.some(function (h) { return h.line === line && a < h.b + 12 && h.a < a + w + 12; })) line++;
        heads.push({ x: x, a: a, b: a + w, line: line, words: words, weight: weight });
      };
      // placed from the left, so a name further right sits higher and its hairline passes clear of the names under it
      var tgt = et ? rows[rows.length - 1][et] : null, todo = [];
      if (tgt && L.target_words) todo.push([xs(tgt), fv(L.target_words, tgt), 600]);
      bands.forEach(function (b) { if (b.label && (!tgt || Math.abs(b.to - tgt) > 1e-6)) todo.push([xs(b.to), b.label, 400]); });
      todo.sort(function (p, q) { return p[0] - q[0]; }).forEach(function (t) { put(t[0], t[1], t[2]); });
      var lh = Math.round(tick * 1.35), nl = heads.length ? 1 + Math.max.apply(null, heads.map(function (h) { return h.line; })) : 0, top = nl * lh + 8;
      heads.forEach(function (h) {
        var yy = top - 8 - h.line * lh - tick * 0.3;
        c.text(h.a, yy, h.words, { role: 'tick', weight: h.weight, fill: h.weight === 600 ? 'label' : 'secondary' });
        c.line(Math.min(h.x, W - 1), yy + 4, Math.min(h.x, W - 1), top - 2, { stroke: h.weight === 600 ? 'label' : 'secondary', width: c.t('line-hairline'), mark: false });
      });
      var bh = c.t('bar-height') + 4, mh = Math.round(bh / 3), y = top;
      rows.forEach(function (r, i) {
        // on a phone the row's name and figures sit under its bar, so the heads' hairlines reach the bands clear of words
        var by = y, cy = by + bh / 2;
        if (!c.phone) c.text(0, cy + size * 0.35, name(r), { role: 'label', weight: 600 });
        var from = 0;
        bands.forEach(function (b) { c.rect(xs(from), by, xs(b.to) - xs(from), bh, { fill: 'mag-' + (b.step || 1), kind: 'band', data: { key: r[ek], field: 'band', value: b.to } }); from = b.to; });
        c.rect(x0, cy - mh / 2, xs(r[ev]) - x0, mh, { fill: 'subject', kind: 'bar', axis: 'x', zero: x0, data: { key: r[ek], field: ev, value: r[ev] } });
        if (et && r[et]) c.line(xs(r[et]), by - 3, xs(r[et]), by + bh + 3, { stroke: 'label', width: 2, data: { key: r[ek], field: et, value: r[et] } });
        var rest = et && r[et] ? fv(L.rest_words, r[et] - r[ev]) : '';
        // under the last bar, the scale from zero, so the reader sees the bar start there (Rule 14.4, MA-6)
        var sb = by + bh;
        if (i === rows.length - 1) {
          var st = K.nice(0, hi, c.phone ? 3 : 4).step, ty = by + bh + 6 + tick, lastx = -1e9;
          c.line(x0, by + bh + 1, x0, by + bh + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
          for (var tv = 0; tv <= hi + 1e-9; tv += st) {
            var tw = fv(L.tick_words || '{v}', tv, f.tick || 'integer'), ww = c.measure(tw, 'tick'), tx = Math.max(ww / 2, Math.min(x1 - ww / 2, xs(tv)));
            if (tx - ww / 2 < lastx + 10) continue;
            c.line(xs(tv), by + bh + 1, xs(tv), by + bh + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
            c.text(tx, ty, tw, { role: 'tick', anchor: 'middle', tnum: true });
            lastx = tx + ww / 2;
          }
          sb = ty + 4;
        }
        if (!c.phone) {
          c.text(W, cy + (rest ? -2 : size * 0.35), fv(L.value_words, r[ev]), { role: 'label', weight: 700, anchor: 'end', tnum: true });
          if (rest) c.text(W, cy + tick + 1, rest, { role: 'tick', anchor: 'end' });
          y = sb + 16;
        } else {
          var ny = sb + 8 + size;
          c.text(0, ny, name(r), { role: 'label', weight: 600 });
          c.text(W, ny, fv(L.value_words, r[ev]), { role: 'label', weight: 700, anchor: 'end', tnum: true });
          if (rest) { c.text(W, ny + 4 + tick, rest, { role: 'tick', anchor: 'end' }); ny += 4 + tick; }
          y = ny + 18;
        }
      });
      c.height(y - (c.phone ? 14 : 12));
    }
  });
})(globalThis.OAChart);
