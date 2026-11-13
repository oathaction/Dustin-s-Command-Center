/* Dot density map (coverage plan 3.14, extended; S83). Dots in the subject ink, each a stated count, placed at random inside
 * each county from a seed the spec records (K.parts.map_dots: one path for every dot, so the page carries no element a
 * dot), over the land ink with state lines in the context ink at 0.5 px and Alaska and Hawaii apart in thin frames. A
 * dot is a count, never an address. One dot stands for a larger count under 480 px, so the dots never cover the land;
 * the key prints the unit at each width (phone: differs).
 * encode: id (id, the county's geoid, in the layer's order), dots (integer: dots at the desk's unit), dots_phone (integer:
 * dots at the phone's unit); both from a derived table, the count over the unit rounded to a whole dot.
 * labels: layer ('counties'), seed (a number), per ([desk, phone]: the count one dot stands for), key ('{n}' fills with
 * the unit), r (the dot's radius, px). */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'dot-density-map', name: 'Dot Density Map', family: 'maps',
    encode: { id: 'id', dots: 'integer', dots_phone: 'integer' },
    labels: ['layer', 'seed', 'per', 'key', 'r'],
    phone: 'differs',
    draw: function (c) {
      var L = c.labels, W = c.width, ei = c.field('id'), ed = c.field(c.phone ? 'dots_phone' : 'dots'), G = K.geo(L.layer || 'counties');
      var per = (L.per || [])[c.phone ? 1 : 0], r = L.r || 0.75;
      // the key: one dot and the count it stands for
      var kt = c.text(14, 14, String(L.key || '').replace('{n}', K.fmt(per, 'integer')), { role: 'tick', max: W - 14 });
      c.circle(4, 14 - c.size('tick') * 0.35, Math.max(r, 1.5), { fill: 'subject', mark: false });
      var T = K.parts.map_fit(c, G, { x: 0, y: kt.bottom + 12, w: W });
      K.parts.map_shapes(c, G, T, G.ids.map(function (id) { return { id: id, fill: 'land' }; }), { merge: true });
      K.parts.map_mesh(c, G, T, { between: function (a, b) { return b !== null && a.slice(0, 2) !== b.slice(0, 2); }, stroke: 'context', width: 0.5 });
      K.parts.map_mesh(c, G, T, { which: 'outline', stroke: 'context', width: 0.5 });
      K.parts.map_insets(c, G, T);
      var counts = {};
      c.rows.forEach(function (row) { var n = row[ed]; if (n !== null && n !== undefined && n !== '' && +n > 0) counts[String(row[ei])] = +n; });
      var res = K.parts.map_dots(c, G, T, counts, { per: 1, seed: L.seed, r: r });
      if (res.skipped.length) c.warn('counties the layer lacks: ' + res.skipped.join(', '));
      c.height(T.y + T.h + 4);
    }
  });
})(globalThis.OAChart);
