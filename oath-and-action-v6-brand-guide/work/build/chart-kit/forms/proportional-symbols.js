/* Proportional symbols (coverage plan 3.8, extended; S86). One circle for each row, its area in proportion to its count
 * (the radius by the square root, the largest at the drawing's widest circle), so counts too far apart for a bar's length
 * still compare. At a desk the circles stand side by side on one line, each named under it with its count; on a phone they
 * stand one under another, named beside. Rows too small to draw at that scale print as counts in words over the circles,
 * never as circles. A key of nested circles at set counts says that area carries the count.
 * encode: category (text), value (number).
 * labels: names ({stored: printed}), named ([categories] in the subject ink; the rest take the light fill with an edge),
 * words_only ([categories] printed in words), word ("{v} {name}", each such row), words ("{list}", the line they print in,
 * the rows joined with "and"), key_steps ([counts]), key_title. formats: value. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'proportional-symbols', name: 'Proportional Symbols', family: 'proportion-and-overlap',
    encode: { category: 'text', value: 'number' },
    labels: ['names', 'named', 'words_only', 'word', 'words', 'key_steps', 'key_title'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, ec = c.field('category'), ev = c.field('value'), f = c.spec.formats || {};
      var nm = function (r) { return (L.names || {})[r[ec]] || r[ec]; }, fv = function (v) { return K.fmt(v, f.value || 'integer'); };
      var wo = L.words_only || [], all = c.all_rows || c.rows;
      var words = all.filter(function (r) { return wo.indexOf(r[ec]) >= 0; });
      var circ = c.rows.filter(function (r) { return wo.indexOf(r[ec]) < 0; });
      var maxv = Math.max.apply(null, circ.map(function (r) { return +r[ev]; }));
      var fill = K.parts.named_fill(c, L.named, ec);
      var lab = c.size('label'), lh = Math.round(lab * 1.25), y = 0, gap = 16;
      var list = words.map(function (r) { return String(L.word || '{v} {name}').split('{v}').join(fv(r[ev])).split('{name}').join(nm(r)); });
      var joined = list.length > 1 ? list.slice(0, -1).join(', ') + ' and ' + list[list.length - 1] : list.join('');
      var draw_circle = function (r, cx, cy, R) {
        var rad = Math.sqrt(+r[ev] / maxv) * R;
        c.circle(cx, cy, rad, Object.assign({ fill: fill(r), area_of: { value: +r[ev], max_value: maxv, max_radius: R }, data: { key: r[ec], field: ev, value: r[ev] } }, fill.edge(r)));
        return rad;
      };
      var wt = function (r) { return fill.named && fill.is_named(r) ? 700 : 600; };
      var name_w = function (r, max) { var ln = c.wrap(nm(r), 'label', max, wt(r)), w = 0; ln.forEach(function (s) { w = Math.max(w, c.measure(s, 'label', wt(r))); }); return { w: w, n: ln.length }; };
      // the rows too small to draw, in words over the circles
      if (words.length) { var wb = c.text(0, lab * 0.86, String(L.words || '{list}').split('{list}').join(joined), { role: 'label', weight: 400, max: W }); y = wb.bottom + 22; }
      var R, bottom;
      if (!c.phone) {
        // each circle's room is its own width or its name's on up to three lines, whichever is wider
        var slot = function (r, Rr) { var d = 2 * Math.sqrt(+r[ev] / maxv) * Rr, w = Math.max(d, 60), n = name_w(r, w); while (n.n > 3) { w += 4; n = name_w(r, w); } return Math.max(d, n.w); };
        var fit = function (Rr) { return circ.reduce(function (t, r) { return t + slot(r, Rr); }, 0) + gap * (circ.length - 1); };
        R = 110;
        while (R > 12 && fit(R) > W) R -= 1;
        // what room is left spreads between the circles, up to 48 px a gap
        var g2 = circ.length > 1 ? Math.min(48, gap + (W - fit(R)) / (circ.length - 1)) : 0, x = 0;
        var base = y + Math.ceil(2 * R), low = base;
        circ.forEach(function (r) {
          var s = slot(r, R), cx = x + s / 2;
          draw_circle(r, cx, base - Math.sqrt(+r[ev] / maxv) * R, R);
          var t = c.text(cx, base + 10 + lab * 0.86, nm(r), { role: 'label', weight: wt(r), anchor: 'middle', max: s + 0.5 });
          var v = c.text(cx, t.bottom + lab * 0.86, fv(r[ev]), { role: 'label', weight: fill.named && fill.is_named(r) ? 700 : 400, anchor: 'middle', tnum: true });
          low = Math.max(low, v.bottom);
          x += s + g2;
        });
        bottom = low;
      } else {
        // on a phone each circle sits in a column of its own, named beside it
        var tw = 0;
        circ.forEach(function (r) { tw = Math.max(tw, name_w(r, W * 0.48).w, c.measure(fv(r[ev]), 'label', 400, true)); });
        R = Math.max(12, Math.min(84, Math.floor((W - 14 - tw) / 2)));
        circ.forEach(function (r) {
          var rad = Math.sqrt(+r[ev] / maxv) * R, nw = name_w(r, W - 2 * R - 14), th = nw.n * lh + lh;
          var h = Math.max(2 * rad, th), cy = y + h / 2;
          draw_circle(r, R, cy, R);
          var t = c.text(2 * R + 14, cy - th / 2 + lab * 0.86, nm(r), { role: 'label', weight: wt(r), max: W - 2 * R - 14 });
          c.text(2 * R + 14, t.bottom + lab * 0.86, fv(r[ev]), { role: 'label', weight: fill.named && fill.is_named(r) ? 700 : 400, tnum: true });
          y += h + 12;
        });
        bottom = y - 12;
      }
      // the key: nested circles on one line, each count beside its circle's top on a leader
      var ks = (L.key_steps || []).slice().sort(function (a, b) { return b - a; });
      if (ks.length) {
        var ky = bottom + 26;
        if (L.key_title) { var kt = c.text(0, ky + c.size('tick') * 0.86, L.key_title, { role: 'tick', weight: 600, max: W }); ky = kt.bottom + 10; }
        var kr = Math.sqrt(ks[0] / maxv) * R, kb = ky + 2 * kr, kx = kr + 1;
        ks.forEach(function (s) { var r = Math.sqrt(s / maxv) * R; c.circle(kx, kb - r, r, { stroke: 'label', width: 1, mark: false }); });
        var used = [];
        ks.forEach(function (s) {
          var r = Math.sqrt(s / maxv) * R, ty = kb - 2 * r, lx = 2 * kr + 10;
          var t = c.text(lx + 4, ty + c.size('tick') * 0.35, fv(s), { role: 'tick', tnum: true });
          c.line(kx, ty, lx, ty, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
          used.push(t);
        });
        bottom = kb;
      }
      c.key([{ fill: fill.named ? 'subject' : 'subject', direct: true }]);
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
