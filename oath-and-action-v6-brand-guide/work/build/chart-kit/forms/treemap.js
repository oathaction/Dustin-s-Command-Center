/* Treemap (coverage plan 3.4, extended; S47). The positive parts of one whole as rectangles whose areas are their
 * values, laid out largest first, the folded tile last, in rows that keep each tile near square (squarified). Every
 * tile takes the track ink with a 1 px edge in the context ink, and the tile the title names takes the subject ink
 * (an area form spends no red, Rule 05.1, the data lead's RF-1); parts too small for their words fold into one last
 * tile, and the table lists each of them. Each tile prints its name and its value with its share; the drawing is taller
 * on a phone.
 * encode: category (text), value (number; rows of zero or less are left out and the note says so).
 * labels: names ({category: printed name}), fold ("fit": fold the fewest smallest parts that let every tile hold its
 * words at 256 px), fold_below (or a share, 0 to 100, under which a part folds), fold_label (the folded tile's name,
 * {n} its count of parts), value_words ('{v}, {p}' words under each name), named (the tile the title names).
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
    labels: ['names', 'fold', 'fold_below', 'fold_label', 'value_words', 'named'],
    phone: 'same',
    draw: function (c) {
      var ek = c.field('category'), ev = c.field('value'), L = c.labels, f = c.spec.formats || {}, W = c.width;
      var names = L.names || {}, nm = function (k) { return names[k] !== undefined ? names[k] : k; };
      var rows = c.rows.filter(function (r) { return r[ev] > 0; }).sort(function (a, b) { return b[ev] - a[ev]; });
      var tot = rows.reduce(function (s, r) { return s + r[ev]; }, 0);
      // RF-1 (Rule 05.1): an area form's named tile takes the subject ink outright, never the red point, since its red
      // would follow the data past 5 percent of the view; every other tile takes the track ink with a 1 px edge in the
      // context ink, so the drawing reads light with one dark tile
      var named = [].concat(L.named || []).map(String);
      var gap = c.t('tile-frame'), pad = 8;
      var words = function (it) {
        return { name: it.fold ? String(L.fold_label || '').split('{n}').join(String(it.rows.length)) : nm(it.key), vw: String(L.value_words || '{v}, {p}')
          .split('{v}').join(K.fmt(it.v, f.value || 'integer')).split('{p}').join(K.fmt(100 * it.v / tot, f.share || 'percent:0'))
          .split(', ').map(function (q) { return q.replace(/ /g, ' '); }).join(', ') };   // a figure keeps its unit on its line
      };
      // a tile's words in the label size where they fit, else in the tick size with a narrower margin; null if neither
      var fitting = function (it, w, h) {
        var wd = words(it), fit = null;
        [['label', pad], ['tick', 5], ['tick', 3]].some(function (o) {
          var rl = o[0], pd = o[1], sz = c.size(rl), lh2 = Math.round(sz * 1.2), maxw = w - 2 * pd;
          var nl = c.wrap(wd.name, rl, maxw, 700), vl = c.wrap(wd.vw, 'tick', maxw, 400), tl = Math.round(c.size('tick') * 1.25);
          var widest = Math.max.apply(null, nl.map(function (l) { return c.measure(l, rl, 700); }).concat(vl.map(function (l) { return c.measure(l, 'tick'); })));
          if (nl.length * lh2 + vl.length * tl + 2 * pd + 2 <= h && widest <= maxw + 0.5) { fit = { rl: rl, pd: pd, sz: sz, lh: lh2, maxw: maxw }; return true; }
          return false;
        });
        return fit;
      };
      // the items: the kept parts largest first, then the folded tile last, whatever its size (RF-10)
      var items_for = function (k) {
        var keep = rows.slice(0, rows.length - k), fold = rows.slice(rows.length - k);
        var its = keep.map(function (r) { return { key: String(r[ek]), v: r[ev], rows: [r] }; });
        if (fold.length) its.push({ key: null, v: fold.reduce(function (s, r) { return s + r[ev]; }, 0), rows: fold, fold: true });
        return its;
      };
      // the shortest height, from a set of proportions, at which every tile holds its words; null where none does
      var lay = function (its, w0, phone) {
        var ratios = phone ? [1.45, 1.6, 1.8, 2.0, 2.3] : [0.62, 0.7, 0.8, 0.9], got = null, last = null;
        ratios.some(function (rt) {
          var H0 = Math.round(Math.max(w0 * rt, phone ? 520 : 0)), tl = squarify(its.map(function (it, i) { return { i: i, v: it.v }; }), 0, 0, w0, H0);
          last = { H: H0, tiles: tl };
          if (tl.every(function (t) { return fitting(its[t.i], t.w - gap, t.h - gap); })) { got = last; return true; }
          return false;
        });
        return got || (last && Object.assign(last, { short: true }));
      };
      // the fold: labels.fold "fit" folds the fewest smallest parts (two or more) that let every tile hold its words at
      // the narrowest drawing, 256 px, so every width folds the same parts (entry 14.52's test); else fold_below, a share
      var k = 0;
      if (L.fold === 'fit') {
        for (k = 0; k < rows.length - 1; k++) { if (k === 1) continue; var tl0 = lay(items_for(k), 256, true); if (tl0 && !tl0.short) break; }
      } else if (L.fold_below) k = rows.filter(function (r) { return r[ev] < L.fold_below * tot / 100; }).length;
      var items = items_for(k), got = lay(items, W, c.phone), H = got.H, tiles = got.tiles;
      tiles.forEach(function (t) {
        var it = items[t.i], isn = !it.fold && named.indexOf(it.key) >= 0, role = isn ? 'subject' : 'track';
        var x = t.x + gap / 2, y = t.y + gap / 2, w = t.w - gap, h = t.h - gap;
        // a folded tile records each part it holds, so the checks read every value
        c.rect(x, y, w, h, { fill: role, kind: 'tile', data: it.fold ? { key: 'folded', field: ev, value: it.v } : { key: it.key, field: ev, value: it.v } });
        if (!isn) c.rect(x + 0.5, y + 0.5, w - 1, h - 1, { stroke: 'context', width: 1, mark: false });
        if (it.fold) it.rows.forEach(function (r) { c.datum(x + w / 2, y + h / 2, { data: { key: r[ek], field: ev, value: r[ev] } }); });
        // words: light on the subject ink, the text's ink on the track
        var ink = isn ? 'label-on-subject' : 'label', wd = words(it), fit = fitting(it, w, h);
        if (!fit) { c.warn('tile ' + (it.key || 'folded') + ' is too small for its words at ' + W + ' px: fold more parts'); return; }
        var nb = c.text(x + fit.pd, y + fit.pd + fit.sz * 0.95, wd.name, { role: fit.rl, weight: 700, max: fit.maxw + 1, leading: fit.lh, fill: ink });
        c.text(x + fit.pd, nb.bottom + 3 + c.size('tick') * 0.95, wd.vw, { role: 'tick', max: fit.maxw + 1, fill: ink, weight: 400 });
      });
      c.height(H);
    }
  });
})(globalThis.OAChart);
