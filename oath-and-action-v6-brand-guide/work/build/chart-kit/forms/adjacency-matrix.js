/* Adjacency matrix (coverage plan 3.12, extended; S74). Every link between a set of parts as a grid: one row a part the
 * links start from, one column a part they end at, each filled cell stepped by its count with the count printed in it,
 * empty cells the ground inside a gridline. Cells whose links all fall in a class of their own (encode.special: links
 * that carry no sign) take no fill and a 1.5 px edge in the text's ink, with the class's own key entry (the data lead's
 * round 3 ruling (b)). A step's fill may be set (steps[].fill); seq-1 and seq-2 take the 1 px context edge. Rows are
 * named at a desk and numbered under 480 px, with the numbered names under the grid; columns are numbered. Groups of
 * parts sit apart by a gap. A row the title names prints bold with a frame in the subject ink.
 * encode: from (code), to (code), value (number), special (number, optional: the count of the cell's links in the class).
 * labels: order ([code], the parts in drawing order), names ({code: name}), groups ([{name, keys}]), steps ([{min, max,
 * label, fill}], in order), special_label (the class's key words), from_label and to_label (words over the row names and
 * the column numbers), axes_short (one line in their place under 480 px), named ([code]), key_title.
 * Maker B, round 3. */
(function (K) {
  'use strict';
  var TINT = ['seq-2', 'seq-3', 'seq-4', 'seq-5'], DARK = { 'seq-4': 1, 'seq-5': 1 }, EDGE = { 'seq-1': 1, 'seq-2': 1 };
  K.register_chart({
    form: 'adjacency-matrix', name: 'Adjacency Matrix', family: 'relationships',
    encode: { from: 'code', to: 'code', value: 'number', special: 'number?' },
    labels: ['order', 'names', 'groups', 'steps', 'special_label', 'from_label', 'to_label', 'axes_short', 'named', 'key_title'],
    phone: 'differs',
    draw: function (c) {
      var P = K.parts, L = c.labels, W = c.width, ph = W < 480;
      var ef = c.field('from'), et = c.field('to'), ev = c.field('value'), esp = c.field('special', false);
      var order = (L.order || []).map(String), names = L.names || {}, named = [].concat(L.named || []).map(String);
      var steps = L.steps || [], lb = c.size('label'), tk = c.size('tick');
      var cell = {};
      c.rows.forEach(function (r) { cell[r[ef] + '|' + r[et]] = r; if (order.indexOf(String(r[ef])) < 0 || order.indexOf(String(r[et])) < 0) c.warn('adjacency-matrix: ' + r[ef] + ' or ' + r[et] + ' is not in labels.order'); });
      var step = function (v) { for (var i = 0; i < steps.length; i++) if (v >= steps[i].min && v <= steps[i].max) return i; return steps.length - 1; };
      var tint = function (i) { return steps[i] && steps[i].fill || TINT[Math.max(0, TINT.length - steps.length + i)]; };
      // the key: each step's tint in order, then the class with no sign
      var y = lb + 2;
      if (L.key_title) { c.text(0, y - lb + tk, L.key_title, { role: 'tick', weight: 600, fill: 'label', max: W }); y += tk + 8; }
      var ks = steps.map(function (s, i) { return { label: s.label, fill: tint(i), edge: EDGE[tint(i)] ? 'context' : undefined, ordered: true, direct: true }; });
      y += P.key(c, ks, 0, y, W) - 6;
      if (L.special_label && esp) y += P.key(c, [{ label: L.special_label, stroke: 'label' }], 0, y, W) - 6;
      y += 10;
      // the group a part sits in, for the gaps between groups
      var gi = {};
      (L.groups || []).forEach(function (g, i) { (g.keys || []).forEach(function (k) { gi[String(k)] = i; }); });
      var n = order.length, gg = 6, ngap = (L.groups || []).length ? (L.groups.length - 1) : 0;
      var num = function (i) { return String(i + 1); };
      // the row names' column: number and name at a desk, the number alone on a phone
      var nw = c.measure(num(n - 1), 'tick', 600, true) + 10, lw = nw;
      if (!ph) order.forEach(function (k) { lw = Math.max(lw, nw + c.measure(names[k] || k, 'label', named.indexOf(k) >= 0 ? 700 : 400)); });
      lw = Math.ceil(lw) + 10;
      var cs = Math.floor(Math.min(ph ? 40 : 46, (W - lw - ngap * gg) / n));
      var pos = function (i) { var g = gi[order[i]] || 0; return i * cs + g * gg; };
      var x0 = lw, head = y;
      if (ph && L.axes_short) y = c.text(0, y + tk * 0.95, L.axes_short, { role: 'tick', weight: 600, fill: 'label', max: W }).bottom + 6;
      else if (L.to_label || L.from_label) {
        if (L.to_label) c.text(x0, y + tk * 0.95, L.to_label, { role: 'tick', weight: 600, fill: 'label' });
        if (L.from_label) c.text(0, y + tk * 0.95, L.from_label, { role: 'tick', weight: 600, fill: 'label' });
        y += tk + 8;
      }
      order.forEach(function (k, j) { c.text(x0 + pos(j) + cs / 2, y + tk * 0.95, num(j), { role: 'tick', weight: 600, anchor: 'middle', fill: 'label', tnum: true }); });
      y += tk + 8;
      var y0 = y;
      order.forEach(function (a, i) {
        var ry = y0 + pos(i), isn = named.indexOf(a) >= 0, cy = ry + cs / 2;
        c.text(0, cy + tk * 0.35, num(i), { role: 'tick', weight: 600, fill: 'label', tnum: true });
        if (!ph) c.text(nw, cy + lb * 0.35, names[a] || a, { role: 'label', weight: isn ? 700 : 400 });
        order.forEach(function (b, j) {
          var r = cell[a + '|' + b], x = x0 + pos(j), v = r ? r[ev] : 0;
          // an empty cell is the ground inside a gridline
          if (!v) { c.rect(x + 1.5, ry + 1.5, cs - 3, cs - 3, { stroke: 'gridline', width: 1, mark: false }); return; }
          var sp = esp && r[esp] > 0, f = tint(step(v));
          if (esp && r[esp] > 0 && r[esp] !== v) c.warn('adjacency-matrix: cell ' + a + ' to ' + b + ' mixes the class with no sign with others');
          if (sp) {
            // the class with no sign: no fill, a 1.5 px edge in the text's ink, its count inside
            c.rect(x + 1, ry + 1, cs - 2, cs - 2, { fill: 'surface', kind: 'cell', data: { key: a + ' to ' + b, field: ev, value: v } });
            c.rect(x + 1.75, ry + 1.75, cs - 3.5, cs - 3.5, { stroke: 'label', width: 1.5, mark: false });
            c.text(x + cs / 2, cy + tk * 0.35, String(v), { role: 'tick', weight: 700, anchor: 'middle', tnum: true, fill: 'label' });
          } else {
            c.rect(x + 1, ry + 1, cs - 2, cs - 2, { fill: f, kind: 'cell', data: { key: a + ' to ' + b, field: ev, value: v } });
            if (EDGE[f]) c.rect(x + 1.5, ry + 1.5, cs - 3, cs - 3, { stroke: 'context', width: 1, mark: false });
            c.text(x + cs / 2, cy + tk * 0.35, String(v), { role: 'tick', weight: 700, anchor: 'middle', fill: DARK[f] ? 'label-on-subject' : 'label', tnum: true });
          }
        });
        if (isn) c.rect(x0 - 1, ry, pos(n - 1) + cs + 2, cs, { stroke: 'subject', width: 2, mark: false });
      });
      y = y0 + pos(n - 1) + cs + 10;
      // on a phone the numbered names sit under the grid
      if (ph) order.forEach(function (k, i) {
        var t = c.text(0, y + lb * 0.95, num(i) + '  ' + (names[k] || k), { role: 'label', weight: named.indexOf(k) >= 0 ? 700 : 400, max: W });
        y = t.bottom + 2;
      });
      c.height(y);
      void head;
    }
  });
})(globalThis.OAChart);
