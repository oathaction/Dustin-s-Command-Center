/* Proportional symbols (coverage plan 3.8, extended; S86). One circle for each row, its area in proportion to its count
 * (the radius by the square root, the largest at the drawing's widest circle), so counts too far apart for a bar's length
 * still compare. At a desk the circles stand side by side on one line, each named under it with its count; on a phone they
 * stand one under another, named beside. The circle the title names takes the subject ink with its words inside where they
 * fit; the rest take the track ink with a 1 px context-ink edge (RF-1). A size key in S16's grammar follows the circles: an
 * eyebrow title, circles at set counts side by side on one line, each count centered under its circle. Rows too small to draw
 * at that scale print as counts in words in the key's band, never as circles: at a desk beside the key, its first line level
 * with the key's title; on a phone under the key.
 * encode: category (text), value (number).
 * labels: names ({stored: printed}), named ([categories]), words_only ([categories] printed in words), word ("{v} {name}",
 * each such row), words ("{list}", the line they print in, the rows joined with "and"), key_steps ([counts], in the order
 * drawn), key_title.
 * formats: value. */
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
      var wo = L.words_only || [], all = c.all_rows || c.rows, named = L.named || [];
      var words = all.filter(function (r) { return wo.indexOf(r[ec]) >= 0; });
      var circ = c.rows.filter(function (r) { return wo.indexOf(r[ec]) < 0; });
      var maxv = Math.max.apply(null, circ.map(function (r) { return +r[ev]; }));
      var isn = function (r) { return named.indexOf(r[ec]) >= 0; }, wt = function (r) { return isn(r) ? 700 : 600; };
      var lab = c.size('label'), lh = Math.round(lab * 1.25), y = 0, gap = 16;
      var list = words.map(function (r) { return String(L.word || '{v} {name}').split('{v}').join(fv(r[ev])).split('{name}').join(nm(r)); });
      var joined = list.length > 1 ? list.slice(0, -1).join(', ') + ' and ' + list[list.length - 1] : list.join('');
      // a named circle's words inside it, where each line fits its chord with 6 px to spare; true when they do
      var inside = function (r, cx, cy, rad) {
        var ls = c.wrap(nm(r), 'label', 2 * rad * 0.8, 700).concat([fv(r[ev])]), hh = lab + (ls.length - 1) * lh, top = cy - hh / 2;
        var ok = ls.every(function (s, j) { var d0 = Math.max(Math.abs(top + j * lh - cy), Math.abs(top + j * lh + lab - cy)); return d0 < rad && c.measure(s, 'label', 700, true) + 12 < 2 * Math.sqrt(rad * rad - d0 * d0); });
        if (ok) ls.forEach(function (s, j) { c.text(cx, top + j * lh + lab * 0.86, s, { role: 'label', weight: 700, anchor: 'middle', tnum: j === ls.length - 1, fill: 'label-on-subject' }); });
        return ok;
      };
      var draw_circle = function (r, cx, cy, R) {
        var rad = Math.sqrt(+r[ev] / maxv) * R;
        c.circle(cx, cy, rad, { fill: isn(r) ? 'subject' : 'track', area_of: { value: +r[ev], max_value: maxv, max_radius: R }, data: { key: r[ec], field: ev, value: r[ev] } });
        if (!isn(r)) c.circle(cx, cy, rad - 0.5, { stroke: 'context', width: 1, mark: false });
        return isn(r) && inside(r, cx, cy, rad);
      };
      var name_w = function (r, max) { var ln = c.wrap(nm(r), 'label', max, wt(r)), w = 0; ln.forEach(function (s) { w = Math.max(w, c.measure(s, 'label', wt(r))); }); return { w: w, n: ln.length }; };
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
          var s = slot(r, R), cx = x + s / 2, rad = Math.sqrt(+r[ev] / maxv) * R;
          if (!draw_circle(r, cx, base - rad, R)) {
            var t = c.text(cx, base + 10 + lab * 0.86, nm(r), { role: 'label', weight: wt(r), anchor: 'middle', max: s + 0.5 });
            var v = c.text(cx, t.bottom - lab * 0.241 + lh, fv(r[ev]), { role: 'label', weight: isn(r) ? 700 : 400, anchor: 'middle', tnum: true });
            low = Math.max(low, v.bottom);
          }
          x += s + g2;
        });
        bottom = low;
      } else {
        // on a phone each circle sits in a column of its own, named beside it
        var tw = 0;
        circ.forEach(function (r) { tw = Math.max(tw, name_w(r, W * 0.48).w, c.measure(fv(r[ev]), 'label', 400, true)); });
        R = Math.max(12, Math.min(84, Math.floor((W - 14 - tw) / 2)));
        // the key shares the scale, so the circles shrink until its steps fit the width side by side
        var kneed = function (Rr) { return (L.key_steps || []).reduce(function (t, st) { return t + Math.max(2 * Math.sqrt(st / maxv) * Rr, c.measure(fv(st), 'tick', 400, true)) + 6; }, -6); };
        while (R > 12 && kneed(R) > W) R -= 1;
        circ.forEach(function (r) {
          var rad = Math.sqrt(+r[ev] / maxv) * R, nw = name_w(r, W - 2 * R - 14), th = nw.n * lh + lh;
          var h = Math.max(2 * rad, th), cy = y + h / 2;
          if (!draw_circle(r, R, cy, R)) {
            var t = c.text(2 * R + 14, cy - th / 2 + lab * 0.86, nm(r), { role: 'label', weight: wt(r), max: W - 2 * R - 14 });
            c.text(2 * R + 14, t.bottom - lab * 0.241 + lh, fv(r[ev]), { role: 'label', weight: isn(r) ? 700 : 400, tnum: true });
          }
          y += h + 12;
        });
        bottom = y - 12;
      }
      // the key, as S16 draws its size key, then the rows too small to draw, in words beside it or under it
      var ks = L.key_steps || [], ky = bottom + 28, kx = 0, kb = ky;
      if (L.key_title) c.text(0, ky, L.key_title, { role: 'eyebrow', weight: 700, fill: 'secondary' });
      var kmax = ks.length ? Math.sqrt(Math.max.apply(null, ks) / maxv) * R : 0;
      kb = ky + 14 + 2 * kmax;
      // each step takes its circle's width or its count's, whichever is wider; the gaps close up to 6 px on a narrow phone
      var kw = ks.map(function (st) { return Math.max(2 * Math.sqrt(st / maxv) * R, c.measure(fv(st), 'tick', 400, true)); });
      var kg = ks.length > 1 ? Math.max(6, Math.min(14, (W - kw.reduce(function (t, w) { return t + w; }, 0)) / (ks.length - 1))) : 0;
      ks.forEach(function (st, i) {
        var r = Math.sqrt(st / maxv) * R, mid = kx + kw[i] / 2;
        c.circle(mid, kb - r, r, { stroke: 'label', width: c.t('bubble-outline'), mark: false });
        c.text(mid, kb + 16, fv(st), { role: 'tick', anchor: 'middle', tnum: true });
        kx = mid + kw[i] / 2 + kg;
      });
      kx -= kg;
      bottom = ks.length ? kb + 20 : bottom;
      if (words.length) {
        var wl = String(L.words || '{list}').split('{list}').join(joined), beside = !c.phone && W - kx - 18 >= 200;
        var wb = c.text(beside ? kx + 18 : 0, beside ? ky : bottom + 18 + lab * 0.86, wl, { role: 'label', weight: 400, max: beside ? W - kx - 18 : W });
        bottom = Math.max(bottom, wb.bottom);
      }
      c.key([{ fill: named.length ? 'subject' : 'track', direct: true }]);
      c.height(bottom + 6);
    }
  });
})(globalThis.OAChart);
