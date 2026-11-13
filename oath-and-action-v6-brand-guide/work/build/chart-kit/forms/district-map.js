/* District map (coverage plan 3.14, extended; S80). One state's House districts on their 2024 Census outlines (a fitted
 * layer, such as 'cd119-mi'), drawn twice: one panel for each party, named with the seats it won, a district filled in
 * its winner's panel and a ghost outline in the other, so position carries party and no hue does (DR-58). The margin takes
 * the district tile map's four steps of one sequential ink, every won district with a context edge, from the same derived table, so the two maps share every class and key word;
 * each district's number sits on its shape in its step's label ink, or beside it with a leader. Panels side by side from
 * 560 px, one above the other below it.
 * encode: district (text), party (category), cls (integer, 1 to 4), state (code).
 * labels: layer, fips (the state's two-digit code, joined to the district for the layer's geoid), panels ([{value,
 * label, where}]; {n} the party's seats, {of} the state's; where names the panel in the note, "in the Democrats’ panel"),
 * step_labels, key_title, ghost_label, nation (a line of words beside the panels: the national result set apart),
 * inset ({ids: [districts], title, at: [x0, y0, x1, y1]}: a framed inset of a city's districts in each panel, drawn
 * larger in the same steps, edges and ghosts, in the empty part of the layer's frame at [x0, y0, x1, y1] (frame units),
 * its view framed on the map; BC-S1, round 3 fix pass), unlabeled ("{list}": the note naming districts with no room for
 * their number in their own panel). Each district is numbered in the panel where it is filled (C-S1). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'district-map', name: 'District Map', family: 'maps',
    encode: { district: 'text', party: 'category', cls: 'integer', state: 'code?' },
    labels: ['layer', 'fips', 'panels', 'step_labels', 'key_title', 'ghost_label', 'nation', 'inset', 'unlabeled'],
    phone: 'same',
    draw: function (c) {
      var L = c.labels, W = c.width, ed = c.field('district'), ep = c.field('party'), ek = c.field('cls');
      var G = K.geo(L.layer), id_of = function (r) { return String(L.fips) + (r[ed] === '00' ? '00' : r[ed]); };
      // BC-S4 (round 3 fix pass): on Charcoal the ghost outline takes the band ink, as on the district tile map
      var ghost = c.ground === 'charcoal' ? 'band' : 'ghost';
      var y = 0, sw = 14, kx = 0;
      if (L.key_title) { var kt = c.text(0, 13, L.key_title, { role: 'eyebrow', weight: 700, fill: 'secondary', max: W }); y = kt.bottom + 6; }
      var ky = y + 14, kbot = 0;
      var entries = (L.step_labels || []).map(function (w, i) { return { w: w, s: i + 1 }; });
      if (L.ghost_label) entries.push({ w: L.ghost_label, ghost: true });
      entries.forEach(function (e) {
        var need = sw + 6 + c.measure(e.w, 'tick');
        if (kx > 0 && kx + need > W) { kx = 0; ky += 22; }
        // BC N3 (second pass): the outline's swatch takes a 1 px context edge round a ghost inset, so it reads on Charcoal
        if (e.ghost) { c.rect(kx + 0.5, ky - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false }); c.rect(kx + 3.5, ky - 7.5, sw - 7, sw - 7, { stroke: ghost, width: 1, mark: false }); }
        else {
          c.rect(kx, ky - 11, sw, sw, { fill: 'seq-' + (e.s + 1), mark: false });
          c.rect(kx + 0.5, ky - 10.5, sw - 1, sw - 1, { stroke: 'context', width: 1, mark: false });
        }
        var tb = c.text(kx + sw + 6, ky, e.w, { role: 'tick', max: W - kx - sw - 6 });
        kx = tb.x + tb.w + 18; kbot = Math.max(kbot, tb.bottom);
        if (tb.lines > 1) { kx = 0; ky = tb.bottom + 14; }
      });
      c.key([1, 2, 3, 4].map(function (s) { return { fill: 'seq-' + (s + 1), ordered: true, outline: true }; }));
      y = Math.max(ky, kbot) + 14;
      if (L.nation) { var nb = c.text(0, y + 13, L.nation, { role: 'tick', weight: 700, max: W }); y = nb.bottom + 4; }
      var unplaced = [], panels = L.panels || [], side = W >= 560, gap = 24, pw = side ? (W - gap * (panels.length - 1)) / panels.length : W, low = y;
      var ins = L.inset || null, in_ids = ins ? ins.ids.map(function (d) { return String(L.fips) + d; }) : [];
      panels.forEach(function (pn, pi) {
        var x0 = side ? pi * (pw + gap) : 0, y0 = side ? y + 10 : low + 10;
        var mine = c.rows.filter(function (r) { return String(r[ep]) === String(pn.value); });
        var nb2 = c.text(x0, y0 + 15, String(pn.label).replace('{n}', K.fmt(mine.length, 'integer')).replace('{of}', K.fmt(c.rows.length, 'integer')), { role: 'label', weight: 700, max: pw });
        var T = K.parts.map_fit(c, G, { x: x0, y: nb2.bottom + 10, w: pw, max_h: side ? 420 : 380 });
        var items = c.rows.map(function (r) {
          var won = String(r[ep]) === String(pn.value);
          return { id: id_of(r), fill: won ? 'seq-' + (r[ek] + 1) : 'surface', data: won ? { key: r[ed], field: ek, value: r[ek], party: r[ep] } : undefined };
        });
        K.parts.map_shapes(c, G, T, items);
        // a ghost district takes a 1 px ghost outline; every won district a 1 px context edge (the data lead's C-1)
        var won = {}; c.rows.forEach(function (r) { won[id_of(r)] = String(r[ep]) === String(pn.value) ? r[ek] : 0; });
        K.parts.map_mesh(c, G, T, { which: 'all', between: function (a, b) { return !won[a] && (b === null || !won[b]); }, stroke: ghost, width: 1 });
        K.parts.map_mesh(c, G, T, { which: 'all', between: function (a, b) { return !!won[a] || (b !== null && !!won[b]); }, stroke: 'context', width: 1 });
        // BC N3: the state's own outline in the context ink above the ghosts, so the state keeps its shape on Charcoal
        K.parts.map_mesh(c, G, T, { which: 'outline', stroke: 'context', width: 1 });
        // BC-S1: a framed inset of the city's districts, larger, in the empty part of the frame, its view framed on the map
        var T2 = null;
        if (ins) {
          var a = ins.at, ix = T.ox + a[0] * T.k, iy = T.oy + a[1] * T.k, iw = (a[2] - a[0]) * T.k, ih = (a[3] - a[1]) * T.k;
          var tt = c.text(ix + 6, iy + 6 + c.size('tick') * 0.8, ins.title, { role: 'tick', weight: 600, max: iw - 12 });
          T2 = K.parts.map_fit(c, G, { x: ix + 6, y: tt.bottom + 6, w: iw - 12, max_h: iy + ih - tt.bottom - 12, ids: in_ids });
          // the view on the map, then the inset's own frame
          var vb = [Infinity, Infinity, -Infinity, -Infinity];
          in_ids.forEach(function (id) { G.rings(G.index[id]).forEach(function (rs) { rs[0].forEach(function (q) { var pq = T.pt(q); vb[0] = Math.min(vb[0], pq[0]); vb[1] = Math.min(vb[1], pq[1]); vb[2] = Math.max(vb[2], pq[0]); vb[3] = Math.max(vb[3], pq[1]); }); }); });
          c.rect(vb[0] - 2.5, vb[1] - 2.5, vb[2] - vb[0] + 5, vb[3] - vb[1] + 5, { stroke: 'context', width: 1, mark: false });
          c.rect(ix + 0.5, iy + 0.5, iw - 1, T2.y + T2.h + 6 - iy - 1, { stroke: 'gridline', width: 1, mark: false });
          var items2 = c.rows.filter(function (r) { return in_ids.indexOf(id_of(r)) >= 0; }).map(function (r) {
            var wn = String(r[ep]) === String(pn.value);
            return { id: id_of(r), fill: wn ? 'seq-' + (r[ek] + 1) : 'surface' };
          });
          K.parts.map_shapes(c, G, T2, items2);
          K.parts.map_mesh(c, G, T2, { ids: in_ids, which: 'all', between: function (a2, b2) { return !won[a2] && (b2 === null || !won[b2]); }, stroke: ghost, width: 1 });
          K.parts.map_mesh(c, G, T2, { ids: in_ids, which: 'all', between: function (a2, b2) { return !!won[a2] || (b2 !== null && !!won[b2]); }, stroke: 'context', width: 1 });
          K.parts.map_mesh(c, G, T2, { ids: in_ids, which: 'outline', stroke: 'context', width: 1 });
        }
        // C-S1: each district is numbered in the panel where it is filled, the city's districts in the inset
        var lab = function (rs, TT) {
          return K.parts.map_labels(c, G, TT, rs.sort(function (a2, b2) { return G.labels[G.index[id_of(b2)]][2] - G.labels[G.index[id_of(a2)]][2]; }).map(function (r) {
            var w2 = won[id_of(r)];
            return { id: id_of(r), words: String(+r[ed]), weight: 600, fill: 'on-seq-' + (w2 + 1) };
          }), { role: 'tick', inset: 1, column: false, reach: W < 300 ? [10, 20] : [10, 20, 32] });
        };
        var mine2 = c.rows.filter(function (r) { return !!won[id_of(r)]; });
        var res = lab(mine2.filter(function (r) { return !T2 || in_ids.indexOf(id_of(r)) < 0; }), T);
        if (T2) res.unplaced = res.unplaced.concat(lab(mine2.filter(function (r) { return in_ids.indexOf(id_of(r)) >= 0; }), T2).unplaced);
        res.unplaced.forEach(function (u) { unplaced.push({ n: +u.words, where: pn.where || '' }); });
        var bottom = T.y + T.h;
        c.texts.forEach(function (t) { if (t.x >= x0 - 1 && t.x < x0 + pw) bottom = Math.max(bottom, t.y + t.h); });
        low = Math.max(low, bottom + 18);
      });
      // a district with no room for its number at this width is named under the maps, with its panel; the table names
      // every one
      if (unplaced.length) {
        var groups = [];
        panels.forEach(function (pn) {
          var ns = unplaced.filter(function (u) { return u.where === (pn.where || ''); }).map(function (u) { return u.n; }).sort(function (a2, b2) { return a2 - b2; });
          if (!ns.length) return;
          var w3 = ns.length > 1 ? ns.slice(0, -1).join(', ') + ' and ' + ns[ns.length - 1] : String(ns[0]);
          groups.push((pn.where ? w3 + ' ' + pn.where : w3));
        });
        var words = L.unlabeled ? String(L.unlabeled).replace('{list}', groups.join(', ')) : K.word('unlabeled_marks').replace('{codes}', groups.join(', '));
        low = c.text(0, low + 6, words, { role: 'note', max: W, fill: 'secondary' }).bottom + 6;
      }
      c.height(low);
    }
  });
})(globalThis.OAChart);
