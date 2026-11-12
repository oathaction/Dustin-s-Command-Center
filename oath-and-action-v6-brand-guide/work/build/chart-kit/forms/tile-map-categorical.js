/* Tile-grid map, categorical (coverage plan 3.14, core; S07). One square per state on the shared 12 by 8 grid, every state
 * equal; the category read by fill, outline and a word in the key; a second line in each tile, such as a year.
 * encode: code (code), category (category), sub (any, optional: printed under the code).
 * labels: categories ([{value, label, style}] with style solid, open or light), key_at ([col, row], optional). formats: sub. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'tile-map-categorical', name: 'Tile Grid Map Categorical', family: 'maps',
    encode: { code: 'code', category: 'category', sub: 'any?' },
    labels: ['categories', 'key_at', 'key_cols'],
    phone: 'same',
    draw: function (c) {
      var G = (typeof OAChartGeo !== 'undefined' ? OAChartGeo : globalThis.OAChartGeo);
      if (!G) throw new Error('load geo.js before a map form');
      var rows = c.rows, ec = c.field('code'), ek = c.field('category'), esub = c.field('sub', false), f = c.spec.formats || {};
      var W = c.width, cats = c.labels.categories || [], by = {};
      cats.forEach(function (x) { by[String(x.value)] = x; });
      var tm = K.parts.tiles(c), gap = tm.gap, size = tm.size;
      var pitch = tm.pitch, top = 0, tsize = c.phone ? c.t('type-tile-code-phone') : c.size('tick');
      var drawn = {};
      // a tile too small for its code at the smallest text size draws no code; the table names every state (D3-93)
      var codes = size - 4 >= c.measure('WW', 'tick', 600) * tsize / c.size('tick');
      rows.forEach(function (r) {
        var t = G.tiles[r[ec]];
        if (!t) return;
        drawn[r[ec]] = true;
        var x = t[0] * pitch, y = top + t[1] * pitch, cat = by[String(r[ek])] || {}, st = cat.style || 'light';
        var o = { data: { key: r[ec], field: ek, value: r[ek], category: r[ek] } };
        if (st === 'solid') c.rect(x, y, size, size, Object.assign({ fill: 'subject' }, o));
        else if (st === 'open') { c.rect(x, y, size, size, Object.assign({ fill: 'surface' }, o)); c.rect(x + 1, y + 1, size - 2, size - 2, { stroke: 'subject', width: c.t('tile-frame'), mark: false }); }
        else c.rect(x, y, size, size, Object.assign({ fill: 'track' }, o));
        var ink = st === 'solid' ? 'label-on-subject' : 'label';
        if (codes) c.text(x + Math.min(5, (size - c.measure(r[ec], 'tick', 600) * tsize / c.size('tick')) / 2), y + 5 + tsize * 0.8, r[ec], { role: 'tick', size: tsize, weight: 600, fill: ink });
        if (codes && esub && r[esub] !== null && r[esub] !== '' && size >= 34) c.text(x + 5, y + 8 + tsize * 1.85, K.fmt(r[esub], f.sub || 'text'), { role: 'tick', size: tsize, fill: ink });
      });
      Object.keys(G.tiles).forEach(function (k) { if (!drawn[k]) c.warn('no row for ' + k + '; every state and DC is drawn'); });
      // the key, in the grid's empty upper middle, or under the map on a phone
      var ka = c.labels.key_at || [1, 0], kx = c.phone ? 0 : ka[0] * pitch, ky = c.phone ? top + 8 * pitch + 8 : top + ka[1] * pitch;
      var sw = 13, kmax = c.phone ? W - sw - 8 : (c.labels.key_cols || 4) * pitch - sw - 8;
      // the key goes under the map wherever, in the grid's upper middle, it would touch a tile (D3-93)
      if (!c.phone) {
        var kh = 14;
        cats.forEach(function (x) { kh += K.wrap(x.label, c.size('tick'), kmax, 400).length * Math.round(c.size('tick') * 1.25) + 8; });
        var hit = Object.keys(G.tiles).some(function (k) {
          var t = G.tiles[k], tx0 = t[0] * pitch, ty0 = top + t[1] * pitch;
          return tx0 < kx + sw + 7 + kmax && kx < tx0 + size && ty0 < ky + kh && ky < ty0 + size;
        });
        if (hit) { kx = 0; ky = top + 8 * pitch + 8; kmax = W - sw - 8; }
      }
      var ly = ky + 14;
      cats.forEach(function (x) {
        if (x.style === 'solid') c.rect(kx, ly - 11, sw, sw, { fill: 'subject', mark: false });
        else if (x.style === 'open') { c.rect(kx, ly - 11, sw, sw, { fill: 'surface', mark: false }); c.rect(kx + 1, ly - 10, sw - 2, sw - 2, { stroke: 'subject', width: c.t('tile-frame'), mark: false }); }
        else c.rect(kx, ly - 11, sw, sw, { fill: 'track', mark: false });
        var kb = c.text(kx + sw + 7, ly, x.label, { role: 'tick', max: kmax });
        ly = kb.y + kb.h + 8 + c.size('tick') * 0.77;
      });
      c.key(cats.map(function (x) { return { fill: x.style === 'solid' ? 'subject' : x.style === 'open' ? 'surface' : 'track', pattern: x.style === 'open' }; }));   // an open tile reads by its frame
      if (!codes) {
        var nb = c.text(0, ly + 6, (K.words && K.words.unlabeled_tiles) || 'State codes are in the table at this width.', { role: 'note', max: W, fill: 'secondary' });
        ly = nb.y + nb.h + 4;
      }
      c.height(Math.max(top + 8 * pitch - gap, ly));
    }
  });
})(globalThis.OAChart);
