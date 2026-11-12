/* Status chips (coverage plan 3.9, core; S63). A list of records, each with its status in a chip, as chapter 18 draws a
 * chip: the word in the label style on a hairline edge in the text's ink, one style for every status, so the words carry
 * the status and no color codes it (no red). Each record leads with its typed ID in its own chip (Rule 13.9, H11) and its
 * title, then the words that give the status its case and date, then the check the record carries. On a phone, and
 * where the row is narrow, the status chip sits over the record's words.
 * encode: key (id), title (text), date (date: when the record was checked), result (text, optional: the check's word).
 * labels: id_type (the type word in each ID chip, such as Issue), status ({key: {chip, words}}), check_words ('{result},
 * {date}' words for the check line). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'status-chips', name: 'Status Chips', family: 'gauges-and-indicators',
    encode: { key: 'id', title: 'text', date: 'date?', result: 'text?' },
    labels: ['id_type', 'status', 'check_words'],
    phone: 'same',
    draw: function (c) {
      var ek = c.field('key'), et = c.field('title'), ed = c.field('date', false), er = c.field('result', false), L = c.labels, W = c.width;
      var st = L.status || {}, size = c.size('label'), tick = c.size('tick'), note = c.size('note'), nlh = c.t('type-note-leading');
      var th = c.t('tag-height') + 4, px = c.t('tag-pad-x') + 2;
      var chip = function (x, y, words, weight) {
        var w = c.measure(words, 'tick', weight) + 2 * px;
        c.rect(x + 0.5, y + 0.5, w - 1, th - 1, { stroke: 'label', width: c.t('line-hairline'), mark: false });
        c.text(x + px, y + th / 2 + tick * 0.35, words, { role: 'tick', weight: weight, fill: 'label' });
        return w;
      };
      var cw = 0;
      c.rows.forEach(function (r) { var s = st[r[ek]] || {}; if (s.chip) cw = Math.max(cw, c.measure(s.chip, 'tick', 700) + 2 * px); if (!s.chip) c.warn('labels.status names no chip for ' + r[ek]); });
      var side = W >= 520, x0 = side ? Math.ceil(cw + 20) : 0, mw = W - x0, y = 0;
      c.line(0, 0.5, W, 0.5, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      c.rows.forEach(function (r) {
        var s = st[r[ek]] || {}, top = y + 12, yy = top;
        // the status chip, at the left of the row or over its words
        if (s.chip) chip(0, top, s.chip, 700);
        c.datum(cw / 2, top + th / 2, { data: { key: r[ek], field: 'status', value: s.chip || '' } });
        if (!side) yy += th + 8;
        // the typed ID in its chip, then the title beside it where it fits, else under it
        var idw = chip(x0, yy, (L.id_type ? L.id_type + ' ' : '') + r[ek], 400), tx = x0 + idw + 8;
        var tl = c.wrap(String(r[et]), 'label', mw - idw - 8, 700);
        var tb;
        if (tl.length <= 2) tb = c.text(tx, yy + th / 2 + size * 0.35, String(r[et]), { role: 'label', weight: 700, max: mw - idw - 8 + 1 });
        else tb = c.text(x0, yy + th + 6 + size * 0.95, String(r[et]), { role: 'label', weight: 700, max: mw });
        var b = Math.max(yy + th, tb.bottom);
        if (s.words) b = c.text(x0, b + 6 + note * 0.95, s.words, { role: 'note', max: mw, leading: nlh, fill: 'label' }).bottom;
        if (L.check_words && (er || ed)) {
          var cwds = String(L.check_words).split('{result}').join(er ? String(r[er] || '') : '').split('{date}').join(ed ? K.fmt(r[ed], 'date') : '');
          b = c.text(x0, b + 4 + tick * 0.95, cwds, { role: 'tick', max: mw }).bottom;
        }
        y = Math.max(b, top + th) + 12;
        c.line(0, y + 0.5, W, y + 0.5, { stroke: 'gridline', width: c.t('line-hairline'), mark: false });
      });
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
