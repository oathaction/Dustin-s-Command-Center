/* Small-multiple maps (coverage plan 3.14, extended; S84). The same map of the states at several dates, one panel each, in
 * the same classes, inks and key, each panel named with its date and its counts (Rule 14.8), drawn through the
 * choropleth's panel (K.forms.choropleth). Two panels a row from 480 px, one below. No state codes: each panel is small, and
 * the table names every state at every date.
 * encode: code (code), panel (any: the column whose values split the panels, in order), category (category).
 * labels: categories ([{value, label, step}], the key's order, lightest first; step 1 to n of steps), steps (fills),
 * panel_title ('{panel}' fills), panel_counts (words with {c1} to {cn}, each the count in that category), key_title,
 * dc ('DC'). formats: panel. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'small-multiple-maps', name: 'Small Multiple Maps', family: 'maps',
    encode: { code: 'code', panel: 'any', category: 'category' },
    labels: ['categories', 'steps', 'panel_title', 'panel_counts', 'key_title', 'dc'],
    phone: 'same',
    draw: function (c) {
      var B = K.forms.choropleth, L = c.labels, W = c.width, f = c.spec.formats || {}, G = globalThis.OAChartGeo;
      var ec = c.field('code'), ep = c.field('panel'), ek = c.field('category'), cats = L.categories || [];
      var steps = L.steps || ['seq-1', 'seq-3', 'seq-5'], idx = {};
      cats.forEach(function (x, i) { idx[String(x.value)] = i + 1; });
      var keys = [];
      c.rows.forEach(function (r) { var k = String(r[ep]); if (keys.indexOf(k) < 0) keys.push(k); });
      var y = B.key(c, 0, steps, cats.map(function (x) { return x.label; }));
      var cols = W >= 480 ? 2 : 1, gap = 24, pw = (W - gap * (cols - 1)) / cols, rowtop = y + 8, low = rowtop;
      keys.forEach(function (k, i) {
        var col = i % cols, x0 = col * (pw + gap);
        if (col === 0 && i > 0) rowtop = low + 14;
        var rows = c.rows.filter(function (r) { return String(r[ep]) === k; });
        var n = cats.map(function (x) { return rows.filter(function (r) { return String(r[ek]) === String(x.value); }).length; });
        var t1 = c.text(x0, rowtop + 15, String(L.panel_title || '{panel}').replace('{panel}', K.fmt(rows[0][ep], f.panel || 'text')), { role: 'label', weight: 700, max: pw });
        var cw = String(L.panel_counts || '').replace(/\{c(\d)\}/g, function (_, d) { return K.fmt(n[+d - 1] || 0, 'integer'); });
        var t2 = cw ? c.text(x0, t1.bottom + 4 + c.size('tick') * 0.8, cw, { role: 'tick', max: pw }) : t1;
        var items = rows.filter(function (r) { return G.tiles[r[ec]]; }).map(function (r) {
          return { id: G.tiles[r[ec]][2], cls: idx[String(r[ek])] || null, data: { key: r[ec] + ' ' + r[ep], field: ek, value: r[ek] } };
        });
        var res = B.panel(c, { layer: 'states', x: x0, y: t2.bottom + 8, w: pw, items: items, steps: steps, codes: false, dc: L.dc });
        low = Math.max(low, res.bottom);
      });
      c.height(low + 4);
    }
  });
})(globalThis.OAChart);
