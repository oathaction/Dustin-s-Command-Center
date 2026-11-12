/* Stacked share bar with a midline (coverage plan 3.4, core; S43). One bar per row split in two parts that make the
 * whole, the first part from the left and the second in the track; a line at the midpoint shows which part is larger.
 * Rows read in the data's order or spec.sort, each name flush left and the first part's share in a column at the right.
 * encode: category (text), left (number: the first part, 0 to 100), right (number: the second part), code (text,
 * optional: a short name printed where the full name would leave the bar under 60 percent of the row, as on a phone).
 * labels: left, right (the two parts' names, set over the first bar), midline (words over the midline), value_head
 * (the share column's head), named and point (the rows the title names: their first part in ink or working red, every
 * other in the light fill; K.parts.named_fill), reference ({key, label}: a row drawn as a dashed line across every bar,
 * such as a national share, in place of a bar). formats: value (the printed share). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'stacked-share-bar', name: 'Stacked Share Bar', family: 'composition',
    encode: { category: 'text', left: 'number', right: 'number', code: 'text?' },
    labels: ['left', 'right', 'midline', 'value_head', 'named', 'point', 'reference'],
    phone: 'same',
    draw: function (c) {
      var ek = c.field('category'), el = c.field('left'), er = c.field('right'), ec = c.field('code', false);
      var L = c.labels, f = c.spec.formats || {}, W = c.width, ref = L.reference || null;
      var fill = K.parts.named_fill(c, L.named, ek, null, L.point);
      var refrow = ref ? c.rows.filter(function (r) { return String(r[ek]) === String(ref.key); })[0] : null;
      if (ref && !refrow) c.warn('labels.reference.key matches no row');
      var rows = c.rows.filter(function (r) { return r !== refrow; });
      var size = c.size('label'), tick = c.size('tick');
      var val = function (r) { return K.fmt(r[el], f.value || 'percent:0'); };
      var nw = 0, cw = 0, vw = c.measure(L.value_head || '', 'tick', 600);
      rows.forEach(function (r) {
        nw = Math.max(nw, c.measure(String(r[ek]), 'label', 600));
        if (ec) cw = Math.max(cw, c.measure(String(r[ec]), 'label', 600));
        vw = Math.max(vw, c.measure(val(r), 'label', 700, true));
      });
      // the full name where it leaves the bar at least 60 percent of the row; the short name otherwise
      var short = ec && W - nw - vw - 30 < 0.6 * W, lw = short ? cw : nw;
      var x0 = Math.ceil(lw + 14), x1 = Math.floor(W - vw - 14), xs = K.scale.linear([0, 100], [x0, x1]);
      var bh = c.t('bar-dense-height') - 2, pitch = bh + (c.phone ? 8 : 7);
      // the heads: part names over the first bar's two ends, the midline's and the reference's words over their lines,
      // each moved up a line where it would touch another
      var heads = [], put = function (x, words, anchor, weight) {
        if (!words) return;
        var w = c.measure(words, 'tick', weight), a = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
        if (a < 0) { x -= a; a = 0; }
        if (a + w > W) { x -= a + w - W; a = W - w; }
        var line = 0;
        while (heads.some(function (h) { return h.line === line && a < h.b + 10 && h.a < a + w + 10; })) line++;
        heads.push({ x: x, a: a, b: a + w, line: line, words: words, anchor: anchor === 'middle' ? 'middle' : (anchor || 'start'), weight: weight });
      };
      put(x0, L.left, 'start', 600);
      put(x1, L.right, 'end', 600);
      put(xs(50), L.midline, 'middle', 400);
      if (refrow) put(xs(refrow[el]), ref.label, 'middle', 400);
      put(W, L.value_head, 'end', 600);
      var nl = 1 + Math.max.apply(null, heads.map(function (h) { return h.line; })), lh = Math.round(tick * 1.35);
      var top = nl * lh + 6;
      heads.forEach(function (h) {
        c.text(h.x, top - 6 - h.line * lh - tick * 0.3, h.words, { role: 'tick', anchor: h.anchor, weight: h.weight, fill: h.weight === 600 ? 'label' : 'secondary' });
      });
      var bottom = top + rows.length * pitch - (pitch - bh);
      rows.forEach(function (r, i) {
        var by = top + i * pitch, cy = by + bh / 2 + size * 0.35, xm = xs(r[el]);
        var nm = fill.is_named(r) && fill.named || fill.is_point(r);
        c.text(0, cy, String(short ? r[ec] : r[ek]), { role: 'label', weight: nm ? 700 : 600 });
        c.rect(x0, by, xm - x0, bh, Object.assign({ fill: fill(r), kind: 'bar', axis: 'x', zero: x0, data: { key: r[ek], field: el, value: r[el] } }, fill.keyline(r)));
        c.rect(xm, by, x1 - xm, bh, { fill: 'track', kind: 'segment', data: { key: r[ek], field: er, value: r[er] } });
        c.text(W, cy, val(r), { role: 'label', weight: nm ? 700 : 400, anchor: 'end', tnum: true });
      });
      // the midline in ink through every bar, and the reference as a dashed line in the context ink
      c.line(xs(50), top - 4, xs(50), bottom + 4, { stroke: 'baseline', width: c.t('line-baseline'), mark: false });
      if (refrow) c.line(xs(refrow[el]), top - 4, xs(refrow[el]), bottom + 4, { stroke: 'context', width: c.t('line-baseline'), dash: '4 3', data: { key: refrow[ek], field: el, value: refrow[el] } });
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
