/* Treemap (coverage plan 3.4, extended; S47). The positive parts of one whole as rectangles whose areas are their
 * values, laid out largest first in rows that keep each tile near square (squarified). Every tile takes one light fill
 * and the tile the title names takes ink or working red; parts under a share fold into one last tile, and the table
 * lists each of them. Each tile prints its name and its value with its share; the drawing is taller on a phone.
 * encode: category (text), value (number; rows of zero or less are left out and the note says so).
 * labels: names ({category: printed name}), fold_below (a share, 0 to 100, under which a part folds), fold_label (the
 * folded tile's name), value_words ('{v}, {p}' words under each name), named and point (K.parts.named_fill).
 * formats: value, share. */
(function (K) {
  'use strict';
  // squarify: lay values (largest first) into the box x, y, w, h; returns [{i, x, y, w, h}]
  function squarify(vals, x, y, w, h) {
    var out = [], tot = vals.reduce(function (s, v) { return s + v.v; }, 0), scale = w * h / tot, items = vals.map(function (v) { return { i: v.i, a: v.v * scale }; });
    var worst = function (row, side) {
      var s = row.reduce(function (t, r) { return t + r.a; }, 0), mx = 0, mn = Infinity;
      row.forEach(function (r) { mx = Math.max(mx, r.a); mn = Math.min(mn, r.a); });
      return Math.max(side * side * mx / (s * s), s * s / (side * side * mn));
    };
    var lay = function (row, horiz) {
      var s = row.reduce(function (t, r) { return t + r.a; }, 0), thick = s / (horiz ? w : h), p = horiz ? x : y;
      row.forEach(function (r) {
        var len = r.a / thick;
        out.push(horiz ? { i: r.i, x: p, y: y, w: len, h: thick } : { i: r.i, x: x, y: p, w: thick, h: len });
        p += len;
      });
      if (horiz) { y += thick; h -= thick; } else { x += thick; w -= thick; }
    };
    var row = [];
    while (items.length) {
      var horiz = w >= h ? false : true, side = horiz ? w : h, it = items[0];
      if (!row.length || worst(row.concat([it]), side) <= worst(row, side)) { row.push(it); items.shift(); }
      else { lay(row, horiz); row = []; }
    }
    if (row.length) lay(row, w >= h ? false : true);
    return out;
  }
  K.register_chart({
    form: 'treemap', name: 'Treemap', family: 'composition',
    encode: { category: 'text', value: 'number' },
    labels: ['names', 'fold_below', 'fold_label', 'value_words', 'named', 'point'],
    phone: 'same',
    draw: function (c) {
      var ek = c.field('category'), ev = c.field('value'), L = c.labels, f = c.spec.formats || {}, W = c.width;
      var names = L.names || {}, nm = function (k) { return names[k] !== undefined ? names[k] : k; };
      var rows = c.rows.filter(function (r) { return r[ev] > 0; });
      var tot = rows.reduce(function (s, r) { return s + r[ev]; }, 0), cut = (L.fold_below || 0) * tot / 100;
      var keep = rows.filter(function (r) { return r[ev] >= cut; }).sort(function (a, b) { return b[ev] - a[ev]; });
      var fold = rows.filter(function (r) { return r[ev] < cut; });
      var items = keep.map(function (r) { return { key: String(r[ek]), v: r[ev], rows: [r] }; });
      if (fold.length) items.push({ key: null, v: fold.reduce(function (s, r) { return s + r[ev]; }, 0), rows: fold, fold: true });
      var fill = K.parts.named_fill(c, L.named, 'key', null, L.point);
      var H = Math.round(c.phone ? Math.max(W * 1.45, 520) : W * 0.66), gap = c.t('tile-frame');
      var tiles = squarify(items.map(function (it, i) { return { i: i, v: it.v }; }), 0, 0, W, H);
      var pad = 8;
      tiles.forEach(function (t) {
        var it = items[t.i], row = { key: it.key }, role = it.fold ? (c.ground === 'charcoal' ? 'context' : 'light-fill') : fill(row);
        var x = t.x + gap / 2, y = t.y + gap / 2, w = t.w - gap, h = t.h - gap;
        // a folded tile records each part it holds, at its share of the tile, so the checks read every value
        c.rect(x, y, w, h, Object.assign({ fill: role, kind: 'tile', data: it.fold ? { key: 'folded', field: ev, value: it.v } : { key: it.key, field: ev, value: it.v } }, fill.keyline(row)));
        if (it.fold) it.rows.forEach(function (r) { c.datum(x + w / 2, y + h / 2, { data: { key: r[ek], field: ev, value: r[ev] } }); });
        // words: dark on the light fill and on red, light on ink; on Charcoal the light fill is the context ink, so its
        // words take the ground's dark
        var ink = role === 'subject' ? 'label-on-subject' : (c.ground === 'charcoal' && role !== 'subject') ? 'surface' : 'label';
        var name = it.fold ? (L.fold_label || '') : nm(it.key), vw = String(L.value_words || '{v}, {p}')
          .split('{v}').join(K.fmt(it.v, f.value || 'integer')).split('{p}').join(K.fmt(100 * it.v / tot, f.share || 'percent:0'));
        // the name in the label size where it fits, else in the tick size with a narrower margin
        var fit = null;
        [['label', pad], ['tick', 5]].some(function (o) {
          var rl = o[0], pd = o[1], sz = c.size(rl), lh2 = Math.round(sz * 1.2), maxw = w - 2 * pd;
          var nl = c.wrap(name, rl, maxw, 700), vl = c.wrap(vw, 'tick', maxw, 400), tl = Math.round(c.size('tick') * 1.25);
          var widest = Math.max.apply(null, nl.map(function (l) { return c.measure(l, rl, 700); }).concat(vl.map(function (l) { return c.measure(l, 'tick'); })));
          if (nl.length * lh2 + vl.length * tl + 2 * pd + 2 <= h && widest <= maxw + 0.5) { fit = { rl: rl, pd: pd, sz: sz, lh: lh2, maxw: maxw }; return true; }
          return false;
        });
        if (!fit) { c.warn('tile ' + (it.key || 'folded') + ' is too small for its words at ' + W + ' px: raise fold_below'); return; }
        var nb = c.text(x + fit.pd, y + fit.pd + fit.sz * 0.95, name, { role: fit.rl, weight: 700, max: fit.maxw + 1, leading: fit.lh, fill: ink });
        c.text(x + fit.pd, nb.bottom + 3 + c.size('tick') * 0.95, vw, { role: 'tick', max: fit.maxw + 1, fill: ink, weight: 400 });
      });
      c.height(H);
    }
  });
})(globalThis.OAChart);
