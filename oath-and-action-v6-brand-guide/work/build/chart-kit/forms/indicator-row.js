/* Indicator row (coverage plan 3.9, core; S60). A set of headline figures side by side, each under a hairline: its
 * kind in small words, the figure in the display face in the text's ink, and its caption under it. Figures are printed
 * as the data stores them, never retyped. The row wraps to as many columns as hold the widest figure at a readable size,
 * so a phone reads them one under another; no fill and no red (an indicator row reports a set).
 * Where captions run long (labels.beside), each figure sits beside its caption, one to a row, wherever the caption's
 * column holds 240 px, so a caption of two hundred characters takes three or four lines (CD A-S3); narrower, the figures
 * run one under another with their captions under them. A figure that holds words sets them in open tracking (BC S12).
 * encode: figure (text), caption (text), kind (text, optional), key (id, optional: the row's key for the checks).
 * labels: kinds ({stored kind: printed words}), columns (the most columns, default 4), beside (true: figures beside their
 * captions, one to a row). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'indicator-row', name: 'Indicator Row', family: 'gauges-and-indicators',
    encode: { figure: 'text', caption: 'text', kind: 'text?', key: 'id?' },
    labels: ['kinds', 'columns', 'beside'],
    phone: 'same',
    draw: function (c) {
      var rows = c.rows, efig = c.field('figure'), ecap = c.field('caption'), ekd = c.field('kind', false), ekey = c.field('key', false);
      var L = c.labels, W = c.width, kinds = L.kinds || {}, gap = c.phone ? 16 : 28;
      var base = Math.round(c.t(c.phone ? 'type-big-phone' : 'type-big') / 3), floor = c.t('type-title-phone-size');
      var widest = 0, open = function (r) { return /\s/.test(String(r[efig])); };
      rows.forEach(function (r) { widest = Math.max(widest, c.measure(String(r[efig]), base, 800, false, open(r))); });
      var tick = c.size('tick'), note = c.size('note'), nlh = c.t('type-note-leading');
      var kw = function (r) { return ekd && r[ekd] ? (kinds[r[ekd]] !== undefined ? kinds[r[ekd]] : String(r[ekd])) : ''; };
      // the caption as printed (the spec's typography first, which the page has already applied to the rows it reads back
      // from the table), its last two words then held together, so no word or figure ends it alone on a line
      var capw_of = function (r) { return String(K.typeset(c.spec, String(r[ecap]))).replace(/ (\S+)$/, '\u00a0$1'); };
      // figures beside their captions, one to a row, where the caption's column holds 240 px
      if (L.beside) {
        var leftw = widest;
        rows.forEach(function (r) { if (kw(r)) leftw = Math.max(leftw, Math.min(widest, c.measure(kw(r), 'tick', 600))); });
        var capx = Math.ceil(leftw + gap), capw = W - capx;
        if (capw >= 240) {
          var yb = 0;
          rows.forEach(function (r, i) {
            c.line(0, yb, W, yb, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
            var kb = kw(r) ? c.text(0, yb + 8 + tick, kw(r), { role: 'tick', weight: 600, fill: 'secondary', max: leftw }) : { bottom: yb + 4 };
            var fb = c.text(0, kb.bottom + 4 + base * 0.97, String(r[efig]), { role: 'big', size: base, weight: 800, fill: 'label', open: open(r),
              data: { key: ekey ? r[ekey] : i, field: efig, value: r[efig] } });
            var cb = c.text(capx, yb + 8 + note * 0.95, capw_of(r), { role: 'note', max: capw, leading: nlh });
            yb = Math.max(fb.bottom, cb.bottom) + 14;
          });
          c.height(yb - 14 + 4);
          return;
        }
      }
      // the most columns whose width holds the widest figure at no less than the phone title's size
      var cols = L.beside ? 1 : Math.min(L.columns || 4, rows.length), colw, fs;
      for (; cols >= 1; cols--) {
        colw = (W - (cols - 1) * gap) / cols;
        fs = Math.min(base, Math.floor(base * (colw - 2) / widest));
        if (fs >= floor || cols === 1) break;
      }
      var y = 0;
      for (var i = 0; i < rows.length; i += cols) {
        var line = rows.slice(i, i + cols), bottom = y;
        // every figure in a row on one baseline, under the tallest kind words in that row
        var kl = Math.max.apply(null, line.map(function (r) { return kw(r) ? c.wrap(kw(r), 'tick', colw, 600).length : 0; }));
        var fy = y + 8 + (kl ? kl * Math.round(tick * 1.25) + 2 : 0) + fs * 0.97 + 4;
        line.forEach(function (r, k) {
          var x = k * (colw + gap);
          c.line(x, y, x + colw, y, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
          if (kw(r)) c.text(x, y + 8 + tick, kw(r), { role: 'tick', weight: 600, fill: 'secondary', max: colw });
          var fb = c.text(x, fy, String(r[efig]), { role: 'big', size: fs, weight: 800, fill: 'label', open: open(r),
            data: { key: ekey ? r[ekey] : i + k, field: efig, value: r[efig] } });
          var cb = c.text(x, fb.bottom + 6 + note * 0.95, capw_of(r), { role: 'note', max: colw, leading: nlh });
          bottom = Math.max(bottom, cb.bottom);
        });
        y = bottom + (c.phone ? 18 : 26);
      }
      c.height(y - (c.phone ? 18 : 26) + 4);
    }
  });
})(globalThis.OAChart);
