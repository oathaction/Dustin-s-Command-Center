/* District map (coverage plan 3.14, extended; S80). One state's House districts on their 2024 Census outlines (a fitted
 * layer, such as 'cd119-mi'), drawn twice: one panel for each party, named with the seats it won, a district filled in
 * its winner's panel and a ghost outline in the other, so position carries party and no hue does (DR-58). The margin takes
 * the district tile map's four gray steps from the same derived table, so the two maps share every class and key word;
 * each district's number sits on its shape in its step's label ink, or beside it with a leader. Panels side by side from
 * 560 px, one above the other below it.
 * encode: district (text), party (category), cls (integer, 1 to 4), state (code).
 * labels: layer, fips (the state's two-digit code, joined to the district for the layer's geoid), panels ([{value,
 * label}]; {n} the party's seats, {of} the state's), step_labels, key_title, ghost_label, nation (a line of words beside
 * the panels: the national result set apart). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'district-map', name: 'District Map', family: 'maps',
    encode: { district: 'text', party: 'category', cls: 'integer', state: 'code?' },
    labels: ['layer', 'fips', 'panels', 'step_labels', 'key_title', 'ghost_label', 'nation'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, ed = c.field('district'), ep = c.field('party'), ek = c.field('cls');
      var G = K.geo(L.layer), id_of = function (r) { return String(L.fips) + (r[ed] === '00' ? '00' : r[ed]); };
      var y = 0, sw = 14, kx = 0;
      if (L.key_title) { var kt = c.text(0, 13, L.key_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: W }); y = kt.bottom + 6; }
      var ky = y + 14, kbot = 0;
      var entries = (L.step_labels || []).map(function (w, i) { return { w: w, s: i + 1 }; });
      if (L.ghost_label) entries.push({ w: L.ghost_label, ghost: true });
      entries.forEach(function (e) {
        var need = sw + 6 + c.measure(e.w, 'tick');
        if (kx > 0 && kx + need > W) { kx = 0; ky += 22; }
        if (e.ghost) c.rect(kx + 0.5, ky - 10.5, sw - 1, sw - 1, { stroke: 'ghost', width: 1, mark: false });
        else {
          c.rect(kx, ky - 11, sw, sw, { fill: 'mag-' + e.s, mark: false });
          if (e.s === 1) c.rect(kx + 0.5, ky - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false });
        }
        var tb = c.text(kx + sw + 6, ky, e.w, { role: 'tick', max: W - kx - sw - 6 });
        kx = tb.x + tb.w + 18; kbot = Math.max(kbot, tb.bottom);
        if (tb.lines > 1) { kx = 0; ky = tb.bottom + 14; }
      });
      c.key([1, 2, 3, 4].map(function (s) { return { fill: 'mag-' + s, ordered: true, outline: s === 1 }; }));
      y = Math.max(ky, kbot) + 14;
      if (L.nation) { var nb = c.text(0, y + 13, L.nation, { role: 'tick', weight: 700, max: W }); y = nb.bottom + 4; }
      var unplaced = [], panels = L.panels || [], side = W >= 560, gap = 24, pw = side ? (W - gap * (panels.length - 1)) / panels.length : W, low = y;
      panels.forEach(function (pn, pi) {
        var x0 = side ? pi * (pw + gap) : 0, y0 = side ? y + 10 : low + 10;
        var mine = c.rows.filter(function (r) { return String(r[ep]) === String(pn.value); });
        var nb2 = c.text(x0, y0 + 15, String(pn.label).replace('{n}', K.fmt(mine.length, 'integer')).replace('{of}', K.fmt(c.rows.length, 'integer')), { role: 'label', weight: 700, max: pw });
        var T = K.parts.map_fit(c, G, { x: x0, y: nb2.bottom + 10, w: pw, max_h: side ? 420 : 380 });
        var items = c.rows.map(function (r) {
          var won = String(r[ep]) === String(pn.value);
          return { id: id_of(r), fill: won ? 'mag-' + r[ek] : 'surface', data: won ? { key: r[ed], field: ek, value: r[ek], party: r[ep] } : undefined };
        });
        K.parts.map_shapes(c, G, T, items);
        // a ghost district takes a 1 px ghost outline; a lightest step its context edge; borders a 1 px line of the ground
        var won = {}; c.rows.forEach(function (r) { won[id_of(r)] = String(r[ep]) === String(pn.value) ? r[ek] : 0; });
        K.parts.map_mesh(c, G, T, { which: 'all', between: function (a, b) { return !won[a] || (b !== null && !won[b]) || (b === null && !won[a]); }, stroke: 'ghost', width: 1 });
        K.parts.map_mesh(c, G, T, { between: function (a, b) { return !!won[a] && (b === null || !!won[b]); }, stroke: 'surface', width: 1 });
        K.parts.map_mesh(c, G, T, { which: 'all', between: function (a, b) { return won[a] === 1 || (b !== null && won[b] === 1); }, stroke: 'context', width: 1 });
        var res = K.parts.map_labels(c, G, T, c.rows.slice().sort(function (a, b) { return G.labels[G.index[id_of(b)]][2] - G.labels[G.index[id_of(a)]][2]; }).map(function (r) {
          var w2 = won[id_of(r)];
          return { id: id_of(r), words: String(+r[ed]), weight: 600, fill: w2 ? 'on-mag-' + w2 : undefined };
        }), { role: 'tick', inset: 1, column: false, reach: [10, 20, 32] });
        res.unplaced.forEach(function (u) { if (unplaced.indexOf(u.words) < 0) unplaced.push(u.words); });
        var bottom = T.y + T.h;
        c.texts.forEach(function (t) { if (t.x >= x0 - 1 && t.x < x0 + pw) bottom = Math.max(bottom, t.y + t.h); });
        low = Math.max(low, bottom + 18);
      });
      // a district with no room for its number at this width is named under the maps; the table names every one
      if (unplaced.length) low = c.text(0, low + 6, K.word('unlabeled_marks').replace('{codes}', unplaced.sort(function (a, b) { return a - b; }).join(', ')), { role: 'note', max: W, fill: 'secondary' }).bottom + 6;
      c.height(low);
    }
  });
})(globalThis.OAChart);
