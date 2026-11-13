/* Comparison grid (coverage plan 3.11, extended; S71). Options against criteria: one row an option, named in bold, one
 * column a criterion, every cell in words in the text's ink on the ground, with a rule in the gridline ink between rows.
 * A cell may carry a second line in the tick size under its words, such as the text and date behind it. One column may
 * be a count, drawn as a bar of one series in the subject ink with its value printed. Desk: the columns side by side
 * at their shares of the width; where a column of words would fall under 96 px (a count's under 64), each option runs as a block down the page, its
 * name and count on one line, then each criterion's name over its words.
 * encode: name (text: the option), count (integer, optional: the bar).
 * labels: columns ([{field, label, share, under (a field printed under the cell's words, {field} in words: pattern),
 * under_words (words with {field} slots)}]), name_label, count_label, name_share, count_share. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'comparison-grid', name: 'Comparison Grid', family: 'structure',
    encode: { name: 'text', count: 'integer?' },
    labels: ['columns', 'name_label', 'count_label', 'name_share', 'count_share'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, en = c.field('name'), ek = c.field('count', false), cols = L.columns || [], g = 12, pad = 9;
      var tick = c.size('tick'), size = c.size('label'), lh = Math.round(tick * 1.3), llh = Math.round(size * 1.25);
      var ty = function (s) { s = String(s === null || s === undefined ? '' : s).replace(/[ \t\n]+/g, ' '); return c.spec.typography ? K.typeset(c.spec, s) : s; };
      var under = function (cl, r) { return cl.under_words ? ty(String(cl.under_words).replace(/\{(\w+)\}/g, function (_, f) { return r[f] === null || r[f] === undefined ? '' : r[f]; })) : ''; };
      var max = 0; c.rows.forEach(function (r) { if (ek) max = Math.max(max, +r[ek] || 0); });
      var vw = 0; if (ek) c.rows.forEach(function (r) { vw = Math.max(vw, c.measure(K.fmt(r[ek], 'integer'), 'tick', 600, true)); });
      var shares = [L.name_share || 1].concat(cols.map(function (cl) { return cl.share || 1; })).concat(ek ? [L.count_share || 0.6] : []);
      var tot = shares.reduce(function (s, v) { return s + v; }, 0), avail = W - g * (shares.length - 1), ws = shares.map(function (s) { return avail * s / tot; });
      var wide = ws.every(function (w, i) { return w >= (ek && i === ws.length - 1 ? 64 : 96); });
      var bar = function (x, yb, w, r) {
        var v = +r[ek] || 0, bw = Math.max(1, (w - vw - 6) * v / (max || 1));
        c.rect(x, yb - tick * 0.75, bw, tick * 0.8, { fill: 'subject', data: { key: String(r[en]), field: 'count', value: v } });
        c.text(x + bw + 5, yb, K.fmt(v, 'integer'), { role: 'tick', weight: 600, tnum: true, fill: 'label' });
      };
      var y = 0;
      if (wide) {
        var xs = [0]; ws.forEach(function (w, i) { if (i) xs.push(xs[i - 1] + ws[i - 1] + g); });
        var heads = [L.name_label || ''].concat(cols.map(function (cl) { return cl.label; })).concat(ek ? [L.count_label || ''] : []);
        var hb = 0;
        heads.forEach(function (h, i) { hb = Math.max(hb, c.text(xs[i], tick * 0.95, h, { role: 'tick', weight: 600, fill: 'secondary', max: ws[i] }).bottom); });
        y = hb + 6;
        c.line(0, y, W, y, { stroke: 'label', width: 1, mark: false });
        c.rows.forEach(function (r) {
          var top = y + pad, bot = top;
          bot = Math.max(bot, c.text(xs[0], top + size * 0.93, ty(r[en]), { role: 'label', weight: 700, max: ws[0], leading: llh }).bottom);
          cols.forEach(function (cl, i) {
            var tb = c.text(xs[i + 1], top + tick * 0.93, ty(r[cl.field]), { role: 'tick', fill: 'label', max: ws[i + 1], leading: lh });
            var u = under(cl, r);
            if (u) tb = c.text(xs[i + 1], tb.bottom + 4 + tick * 0.93, u, { role: 'tick', fill: 'secondary', max: ws[i + 1], leading: lh });
            bot = Math.max(bot, tb.bottom);
          });
          if (ek) bar(xs[xs.length - 1], top + tick * 0.93, ws[ws.length - 1], r);
          y = Math.ceil(bot + pad);
          c.line(0, y, W, y, { stroke: 'gridline', width: 1, mark: false });
        });
      } else {
        c.arrange('phone');
        c.line(0, 0.5, W, 0.5, { stroke: 'label', width: 1, mark: false });
        c.rows.forEach(function (r) {
          var top = y + pad;
          var nb = c.text(0, top + size * 0.93, ty(r[en]), { role: 'label', weight: 700, max: W, leading: llh });
          var yy = nb.bottom + 6;
          if (ek) {
            // the count first, its name over a bar as wide as the drawing allows
            var lb = c.text(0, yy + tick * 0.93, L.count_label || '', { role: 'tick', weight: 600, fill: 'secondary', max: W });
            bar(0, lb.bottom + 3 + tick * 0.93, Math.min(W, 260), r);
            yy = lb.bottom + 3 + tick * 1.2 + 7;
          }
          cols.forEach(function (cl) {
            var hb2 = c.text(0, yy + tick * 0.93, cl.label, { role: 'tick', weight: 600, fill: 'secondary', max: W });
            var tb = c.text(0, hb2.bottom + 1 + tick * 0.93, ty(r[cl.field]), { role: 'tick', fill: 'label', max: W, leading: lh });
            var u = under(cl, r);
            if (u) tb = c.text(0, tb.bottom + 3 + tick * 0.93, u, { role: 'tick', fill: 'secondary', max: W, leading: lh });
            yy = tb.bottom + 7;
          });
          y = Math.ceil(yy - 7 + pad);
          c.line(0, y, W, y, { stroke: 'gridline', width: 1, mark: false });
        });
      }
      c.height(y + 1);
    }
  });
})(globalThis.OAChart);
