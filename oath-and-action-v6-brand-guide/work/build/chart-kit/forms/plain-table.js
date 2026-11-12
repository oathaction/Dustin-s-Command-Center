/* Plain table (coverage plan 3.15, core; S41). A handful of numbers set as a quiet table: a row of column heads over a
 * hairline, one row per data row with its name at the left and each value right-aligned under its head, a rule under the
 * last row. The table is only as wide as its columns need, so the eye never crosses empty space to reach a value.
 * encode: row (text: the column that names each row), columns (list of value columns, in order).
 * labels: heads ({field: words}, the row column's head included), rows ({row value: printed name}), named (row values
 * printed bold). formats: by field name (such as {"value": "percent:0"}); integer otherwise. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'plain-table',
    name: 'Plain Table',
    family: 'tables-and-plain-words',
    encode: { row: 'text', columns: 'list' },
    labels: ['heads', 'rows', 'named'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, er = c.field('row'), cols = [].concat(c.field('columns'));
      var f = c.spec.formats || {}, W = c.width, L = c.labels, heads = L.heads || {}, rnames = L.rows || {};
      var named = [].concat(L.named || []).map(String);
      var bold = function (r) { return named.indexOf(String(r[er])) >= 0; };
      var rname = function (r) { return rnames[String(r[er])] !== undefined ? rnames[String(r[er])] : String(r[er]); };
      var cell = function (r, k) { return K.fmt(r[k], f[k] || 'integer'); };
      var size = c.size('label'), tick = c.size('tick'), gap = c.phone ? 20 : 32;
      // column widths: each value column as wide as its head or its widest value
      var cw = cols.map(function (k) {
        var w = c.measure(heads[k] || k, 'tick', 600);
        rows.forEach(function (r) { w = Math.max(w, c.measure(cell(r, k), 'label', 600, true)); });
        return Math.ceil(w);
      });
      var valw = cw.reduce(function (a, b) { return a + b + gap; }, 0);
      var lw = c.measure(heads[er] || '', 'tick', 600);
      rows.forEach(function (r) { lw = Math.max(lw, c.measure(rname(r), 'label', bold(r) ? 700 : 400)); });
      var lmax = Math.max(80, Math.min(Math.ceil(lw), W - valw));
      var tw = Math.min(W, lmax + valw);
      // the heads
      var y = tick + 2;
      if (heads[er]) c.text(0, y, heads[er], { role: 'tick', weight: 600, fill: 'label' });
      var right = [];
      var x = lmax;
      cols.forEach(function (k, i) { x += gap + cw[i]; right.push(x); c.text(x, y, heads[k] || k, { role: 'tick', weight: 600, anchor: 'end', fill: 'label' }); });
      y += 8;
      c.line(0, y, tw, y, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      // the rows
      var lh = Math.round(size * 1.25), pad = 10;
      rows.forEach(function (r, i) {
        var lines = c.wrap(rname(r), 'label', lmax, bold(r) ? 700 : 400).length;
        var top = y, base = top + pad + size;
        c.text(0, base, rname(r), { role: 'label', weight: bold(r) ? 700 : 400, max: lmax });
        cols.forEach(function (k, j) {
          c.text(right[j], base, cell(r, k), { role: 'label', weight: bold(r) ? 700 : 600, anchor: 'end', tnum: true });
          c.datum(right[j], base, { data: { key: r[er], field: k, value: r[k] } });
        });
        y = base + (lines - 1) * lh + pad;
        c.line(0, y, tw, y, { stroke: i === rows.length - 1 ? 'baseline' : 'gridline', width: c.t(i === rows.length - 1 ? 'line-baseline' : 'line-hairline'), mark: false });
      });
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
