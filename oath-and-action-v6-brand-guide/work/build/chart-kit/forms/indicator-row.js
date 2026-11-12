/* Indicator row (coverage plan 3.9, core; S60). A set of headline figures side by side, each under a hairline: its
 * kind in small words, the figure in the display face in the text's ink, and its caption under it. Figures are printed
 * as the data stores them, never retyped. The row wraps to as many columns as hold the widest figure at a readable size,
 * so a phone reads them one under another; no fill and no red (an indicator row reports a set).
 * encode: figure (text), caption (text), kind (text, optional), key (id, optional: the row's key for the checks).
 * labels: kinds ({stored kind: printed words}), columns (the most columns, default 4). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'indicator-row', name: 'Indicator Row', family: 'gauges-and-indicators',
    encode: { figure: 'text', caption: 'text', kind: 'text?', key: 'id?' },
    labels: ['kinds', 'columns'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, efig = c.field('figure'), ecap = c.field('caption'), ekd = c.field('kind', false), ekey = c.field('key', false);
      var L = c.labels, W = c.width, kinds = L.kinds || {}, gap = c.phone ? 16 : 28;
      var base = Math.round(c.t(c.phone ? 'type-big-phone' : 'type-big') / 3), floor = c.t('type-title-phone-size');
      var widest = 0;
      rows.forEach(function (r) { widest = Math.max(widest, K.measure(String(r[efig]), base, 800, 'display')); });
      // the most columns whose width holds the widest figure at no less than the phone title's size
      var cols = Math.min(L.columns || 4, rows.length), colw, fs;
      for (; cols >= 1; cols--) {
        colw = (W - (cols - 1) * gap) / cols;
        fs = Math.min(base, Math.floor(base * (colw - 2) / widest));
        if (fs >= floor || cols === 1) break;
      }
      var tick = c.size('tick'), note = c.size('note'), nlh = c.t('type-note-leading'), y = 0;
      for (var i = 0; i < rows.length; i += cols) {
        var line = rows.slice(i, i + cols), bottom = y, kw = function (r) { return ekd && r[ekd] ? (kinds[r[ekd]] !== undefined ? kinds[r[ekd]] : String(r[ekd])) : ''; };
        // every figure in a row on one baseline, under the tallest kind words in that row
        var kl = Math.max.apply(null, line.map(function (r) { return kw(r) ? c.wrap(kw(r), 'tick', colw, 600).length : 0; }));
        var fy = y + 8 + (kl ? kl * Math.round(tick * 1.25) + 2 : 0) + fs * 0.97 + 4;
        line.forEach(function (r, k) {
          var x = k * (colw + gap);
          c.line(x, y, x + colw, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
          if (kw(r)) c.text(x, y + 8 + tick, kw(r), { role: 'tick', weight: 600, fill: 'secondary', max: colw });
          var fb = c.text(x, fy, String(r[efig]), { role: 'big', size: fs, weight: 800, fill: 'label',
            data: { key: ekey ? r[ekey] : i + k, field: efig, value: r[efig] } });
          // the caption's last two words held together, so no word or figure ends it alone on a line
          var cap = String(r[ecap]).replace(/ (\S+)$/, '\u00a0$1');
          var cb = c.text(x, fb.bottom + 6 + note * 0.95, cap, { role: 'note', max: colw, leading: nlh });
          bottom = Math.max(bottom, cb.bottom);
        });
        y = bottom + (c.phone ? 18 : 26);
      }
      c.height(y - (c.phone ? 18 : 26) + 4);
    }
  });
})(globalThis.OAChart);
