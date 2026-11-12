/* Parliament chart (coverage plan 3.4, extended; S48). Every seat in a chamber as a dot on a half circle of rows, the
 * groups laid from left to right in a set order, each row holding its share of each end block so the blocks meet on
 * near-radial lines, one empty place apart, and the blocks between the ends in the innermost row. Every seat
 * takes the one party-mark ink (DR-48, DR-58, Rule 14.7); an empty seat is an open ring in the same ink. Each block is
 * named with its count: the end blocks under the half circle's feet, the blocks between them in its hollow with a
 * hairline to their seats. A tick over the outer row marks where the last block's seats begin, such as a majority.
 * encode: group (category), seats (integer).
 * labels: order (group values from left to right), words ({group: '{n} words'} printed for each block), open (the
 * group value drawn as open rings, such as vacancies), majority ({seats, label}: the tick and its words). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'parliament', name: 'Parliament Chart', family: 'composition',
    encode: { group: 'category', seats: 'integer' },
    labels: ['order', 'words', 'open', 'majority'],
    phone: 'same',
    draw: function (c) {
      var eg = c.field('group'), es = c.field('seats'), L = c.labels, W = c.width, size = c.size('label'), tick = c.size('tick');
      var order = L.order || c.rows.map(function (r) { return String(r[eg]); });
      var by = {}; c.rows.forEach(function (r) { by[String(r[eg])] = r; });
      var groups = order.filter(function (g) { return by[g]; }).map(function (g) { return { g: g, n: by[g][es], row: by[g] }; });
      var N = groups.reduce(function (s, g) { return s + g.n; }, 0), Rr = 11;
      var top = (L.majority ? tick * 2 + 14 : 4), Ro = Math.floor((W / 2 - 1) / 1.03), Ri = Ro * 0.4, cx = W / 2, cy = top + Ro;
      var radii = [], rsum = 0;
      for (var i = 0; i < Rr; i++) { var rr = Ri + (Ro - Ri) * i / (Rr - 1); radii.push(rr); rsum += rr; }
      var per = radii.map(function (rr) { return Math.round(N * rr / rsum); }), diff = N - per.reduce(function (s, n) { return s + n; }, 0);
      for (var j = Rr - 1; diff !== 0; j = (j + Rr - 1) % Rr) { per[j] += diff > 0 ? 1 : -1; diff += diff > 0 ? -1 : 1; }
      // each row holds its share of each end block, so the blocks meet on near-radial lines; the blocks between the ends
      // sit in the innermost row, at the middle
      var ends = [groups[0], groups[groups.length - 1]], mids = groups.slice(1, -1), alloc = per.map(function () { return {}; });
      mids.forEach(function (g) { alloc[0][g.g] = g.n; });
      var room = per.map(function (n, ri) { return n - mids.reduce(function (s, g) { return s + (alloc[ri][g.g] || 0); }, 0); });
      var a = ends[0], b = ends[1], tot = a.n + (a === b ? 0 : b.n), got = 0, fr = [];
      room.forEach(function (m, ri) { var ideal = m * a.n / tot, fl = Math.floor(ideal); alloc[ri][a.g] = fl; got += fl; fr.push({ ri: ri, f: ideal - fl }); });
      fr.sort(function (p, q) { return q.f - p.f || q.ri - p.ri; });
      for (var q = 0; got < a.n; q++, got++) alloc[fr[q % Rr].ri][a.g]++;
      if (a !== b) room.forEach(function (m, ri) { alloc[ri][b.g] = m - alloc[ri][a.g]; });
      // in each row, left to right: the blocks in order, one empty place between two blocks
      var seats = [], gapa = [];
      radii.forEach(function (rr, ri) {
        var blocks = groups.filter(function (g) { return alloc[ri][g.g] > 0; }), slots = per[ri] + blocks.length - 1, k = 0;
        blocks.forEach(function (g, bi) {
          if (bi) { if (g === b) gapa.push({ ri: ri, a: Math.PI - k * Math.PI / (slots - 1) }); k++; }
          for (var m = 0; m < alloc[ri][g.g]; m++, k++) {
            var an = Math.PI - k * Math.PI / (slots - 1);
            seats.push({ g: g, p: { a: an, r: rr, x: cx + rr * Math.cos(an), y: cy - rr * Math.sin(an) } });
          }
        });
      });
      var rad = Math.max(1.5, Math.min((Ro - Ri) / (Rr - 1), Math.PI * Ri / (per[0] + 2)) * 0.42);
      var openg = L.open === undefined ? null : String(L.open);
      seats.forEach(function (s) {
        var d = { key: s.g.g, field: es, value: s.g.n, party: s.g.g };
        if (s.g.g === openg) {
          c.circle(s.p.x, s.p.y, rad - 0.6, { fill: 'surface', kind: 'seat', data: d });
          c.circle(s.p.x, s.p.y, rad - 0.6, { stroke: 'party', width: 1.2, mark: false });
        } else c.circle(s.p.x, s.p.y, rad, { fill: 'party', kind: 'seat', data: d });
      });
      var words = function (g) { return String((L.words || {})[g.g] || g.g + ' {n}').split('{n}').join(K.fmt(g.n, 'integer')); };
      // the end blocks named under the feet, flush with the half circle's two ends
      var fy = cy + rad + 8 + size, n0 = groups[0], n1 = groups[groups.length - 1];
      c.text(cx - Ro, fy, words(n0), { role: 'label', weight: 700 });
      if (groups.length > 1) c.text(cx + Ro, fy, words(n1), { role: 'label', weight: 700, anchor: 'end' });
      // the blocks between, named together in the hollow, their words resting on the feet's line, with one hairline up to
      // their seats in the innermost row
      if (mids.length) {
        var ms = seats.filter(function (s) { return mids.indexOf(s.g) >= 0; }), mx = ms.reduce(function (t, s) { return t + s.p.x; }, 0) / ms.length;
        var my = Math.max.apply(null, ms.map(function (s) { return s.p.y; })), mw2 = 2 * (Ri - rad) - 8, lh2 = Math.round(size * 1.25);
        var mtxt = mids.map(words).join(', '), nl = c.wrap(mtxt, 'label', mw2, 600).length;
        var tb = c.text(cx, cy + rad - (nl - 1) * lh2, mtxt, { role: 'label', weight: 600, anchor: 'middle', max: mw2 + 1, leading: lh2 });
        c.line(mx, my + rad + 3, mx, tb.y - 3, { stroke: 'leader', width: c.t('line-hairline'), mark: false });
      }
      // the majority tick in the text's ink, over the outer row's gap before the last block
      if (L.majority) {
        var ga = gapa.filter(function (gp) { return gp.ri === Rr - 1; })[0], am = ga ? ga.a : Math.PI / 2;
        var tx1 = cx + (Ro + rad + 3) * Math.cos(am), ty1 = cy - (Ro + rad + 3) * Math.sin(am), tx2 = cx + (Ro + rad + 11) * Math.cos(am), ty2 = cy - (Ro + rad + 11) * Math.sin(am);
        c.line(tx1, ty1, tx2, ty2, { stroke: 'label', width: 1.5, mark: false });
        if (L.majority.label) { var mw = c.measure(L.majority.label, 'tick', 600) / 2; c.text(Math.max(mw, Math.min(W - mw, tx2)), ty2 - 6, L.majority.label, { role: 'tick', weight: 600, anchor: 'middle', fill: 'label' }); }
      }
      c.height(fy + 6);
    }
  });
})(globalThis.OAChart);
