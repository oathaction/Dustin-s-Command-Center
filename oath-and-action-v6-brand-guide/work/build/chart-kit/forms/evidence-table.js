/* Evidence table (coverage plan 3.15, core; S39). Claims side by side with what a reader needs to weigh each one: at the
 * left, its grade in words and its period, with its typed ID above them where the spec names the ID's type; at the right, the claim, who it covers, its source where
 * the data names one, and its limits, each after a short head. On a phone the ID, grade and period run on one line above
 * the claim. Hairlines part the rows.
 * encode: key (id: the claim's ID), claim (text), grade (category), period (text), covers (text, optional), limits (text),
 * source (text, optional). labels: grades ({grade value: printed word}), id_type (optional: the type word set before each ID,
 * for an ID the atlas types, such as "Reform"; with none, no ID prints), heads ({covers, limits, source, period}: the short heads before those lines; period's on a phone). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'evidence-table',
    name: 'Evidence Table',
    family: 'tables-and-plain-words',
    encode: { key: 'id', claim: 'text', grade: 'category', period: 'text', covers: 'text?', limits: 'text', source: 'text?' },
    labels: ['grades', 'id_type', 'heads'],
    phone: 'differs',
    draw: function (c) {
      var rows = c.rows, ek = c.field('key'), ec = c.field('claim'), eg = c.field('grade'), ep = c.field('period');
      var ecv = c.field('covers', false), el = c.field('limits'), es = c.field('source', false);
      var W = c.width, L = c.labels, G = L.grades || {}, H = L.heads || {};
      var grade = function (r) { return G[String(r[eg])] !== undefined ? G[String(r[eg])] : String(r[eg]); };
      var idw = function (r) { return L.id_type ? L.id_type + ' ' + String(r[ek]) : ''; };
      var size = c.size('label'), tick = c.size('tick'), lh = Math.round(size * 1.3), tlh = Math.round(tick * 1.4);
      var lw = 0;
      rows.forEach(function (r) { lw = Math.max(lw, idw(r) ? c.measure(idw(r), 'tick') : 0, c.measure(grade(r), 'label', 700)); });
      var mw = c.phone ? 0 : Math.min(Math.ceil(lw) + 8, Math.floor(W * 0.22));
      var xr = c.phone ? 0 : mw + 24, rw = W - xr;
      var y = 0;
      c.line(0, y, W, y, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      rows.forEach(function (r, i) {
        var top = y + 12, ly, my;
        // the ID, grade and period
        if (c.phone) {
          var g1 = c.text(0, top + size, grade(r), { role: 'label', weight: 700 });
          if (idw(r)) c.text(g1.x + g1.w + 10, top + size, idw(r), { role: 'tick', fill: 'secondary' });
          my = top + size;
          ly = my + 8;
        } else {
          var gy = top + size;
          if (idw(r)) { c.text(0, top + tick, idw(r), { role: 'tick', fill: 'secondary' }); gy = top + tick + 6 + size; }
          var gb = c.text(0, gy, grade(r), { role: 'label', weight: 700, max: mw });
          var pb = c.text(0, gb.bottom - size * 0.241 + tlh, String(r[ep]), { role: 'tick', fill: 'secondary', max: mw });
          my = pb.bottom;
          ly = top - 2;
        }
        c.datum(0, top, { data: { key: r[ek], field: eg, value: r[eg] } });
        // the claim, then its covers, source and limits lines
        var cb = c.text(xr, ly + size, String(r[ec]), { role: 'label', weight: 600, max: rw });
        var yy = cb.bottom - size * 0.241;
        var line = function (head, words) {
          if (words === null || words === undefined || words === '') return;
          var tb = c.text(xr, yy + tlh + 2, (head ? head + ' ' : '') + String(words), { role: 'tick', max: rw, fill: 'secondary' });
          yy = tb.bottom - tick * 0.241;
        };
        if (c.phone) line(H.period, r[ep]);
        if (ecv) line(H.covers, r[ecv]);
        if (es) line(H.source, r[es]);
        line(H.limits, r[el]);
        y = Math.max(yy, c.phone ? 0 : my) + 14;
        c.line(0, y, W, y, { stroke: i === rows.length - 1 ? 'baseline' : 'gridline', width: c.t(i === rows.length - 1 ? 'line-baseline' : 'line-hairline'), mark: false });
      });
      c.height(y + 2);
    }
  });
})(globalThis.OAChart);
