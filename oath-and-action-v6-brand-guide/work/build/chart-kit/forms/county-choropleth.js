/* County choropleth (coverage plan 3.14, extended; S81). Every county shaded by its class on the 2024 Census outlines (the
 * kit's 'counties' layer), drawn through the choropleth's panel and key (K.forms.choropleth): no county lines, state lines
 * in the context ink at 0.5 px, a county with no estimate in the land ink with a context edge, the nation beside the map.
 * The drawing reads only each county's class from a derived table (DL-E1, DR-249: one small number a county on the page);
 * the table groups by state and the CSV export lists every county with its value and margin.
 * encode: id (id, the county's geoid, in the layer's order), cls (integer, 1 to n; empty with no estimate).
 * labels: layer ('counties'), steps, class_labels, key_title, none_label, nation_text (the national figure, beside the
 * map). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'county-choropleth', name: 'County Choropleth', family: 'maps',
    encode: { id: 'id', cls: 'integer' },
    labels: ['layer', 'steps', 'class_labels', 'key_title', 'none_label', 'nation_text'],
    phone: 'same',
    draw: function (c) {
      var B = K.forms.choropleth, L = c.labels, ei = c.field('id'), ek = c.field('cls'), steps = L.steps || B.STEPS;
      var items = c.rows.map(function (r) {
        var k = r[ek] === null || r[ek] === undefined || r[ek] === '' ? null : +r[ek];
        return { id: String(r[ei]), cls: k, data: { key: r[ei], field: ek, value: k === null ? '' : k } };
      });
      var y = B.key(c, 0, steps, L.class_labels || [], items.some(function (it) { return !it.cls; }) && L.none_label ? [{ fill: 'land', words: L.none_label }] : null);
      if (L.nation_text) y = c.text(0, y + 12, L.nation_text, { role: 'tick', weight: 700, max: c.width }).bottom + 4;
      var res = B.panel(c, { layer: L.layer || 'counties', x: 0, y: y + 10, w: c.width, items: items, steps: steps, codes: false, merge: true, state_lines: true });
      c.height(res.bottom + 4);
    }
  });
})(globalThis.OAChart);
