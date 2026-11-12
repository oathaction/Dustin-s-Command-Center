/* Filterable lookup table (coverage plan 3.15, extended and interactive; S38). On the atlas site and in the guide a reader
 * searches and filters the whole register in its live table (spec.lookup, Rules 18.10, 18.15 and 18.16). The drawing is
 * the still image a post or an email carries (DR-49): the register filtered to one value of one facet, under the count
 * line the live table would show with that filter on, each record's title with its typed ID and its second column.
 * encode: key (id: the record's ID), title (text), facet (category: the column the still filters on), second (category,
 * optional: a short word printed at the right, such as a grade). labels: still (the facet value the still shows), count
 * ("{n} of {total} issue records: {facet}"), facet_words ({value: printed words}), second_words ({value: words}),
 * id_type (the type word before each ID, such as "Issue"). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'filterable-lookup-table',
    name: 'Filterable Lookup Table',
    family: 'tables-and-plain-words',
    encode: { key: 'id', title: 'text', facet: 'category', second: 'category?' },
    labels: ['still', 'count', 'facet_words', 'second_words', 'id_type'],
    phone: 'same',
    draw: function (c) {
      var ek = c.field('key'), et = c.field('title'), ef = c.field('facet'), es = c.field('second', false);
      var W = c.width, L = c.labels, FW = L.facet_words || {}, SW = L.second_words || {};
      var rows = c.rows.filter(function (r) { return String(r[ef]) === String(L.still); });
      if (!rows.length) c.warn('labels.still matches no row');
      var size = c.size('label'), tick = c.size('tick');
      var fw = FW[String(L.still)] !== undefined ? FW[String(L.still)] : String(L.still);
      var count = String(L.count || '{n} of {total}').replace('{n}', rows.length).replace('{total}', c.rows.length).replace('{facet}', fw);
      var y = size;
      var hb = c.text(0, y, count, { role: 'label', weight: 700, max: W });
      y = hb.bottom + 8;
      c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      var sw = 0;
      if (es) rows.forEach(function (r) { var w = SW[String(r[es])] !== undefined ? SW[String(r[es])] : String(r[es]); sw = Math.max(sw, c.measure(w, 'tick', 600)); });
      var tw = W - (es ? sw + 16 : 0);
      rows.forEach(function (r, i) {
        var top = y + 8;
        var idw = (L.id_type ? L.id_type + ' ' : '') + String(r[ek]);
        c.text(0, top + tick, idw, { role: 'tick', fill: 'secondary' });
        var tb = c.text(0, top + tick + 4 + size, String(r[et]), { role: 'label', weight: 600, max: tw });
        if (es) c.text(W, top + tick + 4 + size, SW[String(r[es])] !== undefined ? SW[String(r[es])] : String(r[es]), { role: 'tick', weight: 600, anchor: 'end', fill: 'label' });
        c.datum(0, top, { data: { key: r[ek], field: et } });
        y = tb.bottom + 8;
        c.line(0, y, W, y, { stroke: i === rows.length - 1 ? 'baseline' : 'gridline', width: c.t(i === rows.length - 1 ? 'line-baseline' : 'line-hairline'), mark: false });
      });
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
