/* Bubble timeline (coverage plan 3.3, extended; S34). Events or periods along one time axis, each a circle whose area is in
 * proportion to a count (D2-124), centered on one line. Circles overlap where periods sit close; each takes a light fill and
 * an outline, drawn oldest first, so every edge stays visible. A period with nothing to count takes a short tick on the
 * line; a period still under way takes a dashed outline. A key of round sizes sits above.
 * encode: key (id), x (year, month or date), size (number), complete (boolean, optional: false marks a period under way).
 * labels: key_title (words over the size key), key_values (round sizes for the key), key_unit (words after each key value,
 * with {value}), partial (words in the key for a period under way). formats: size (in the words), x.
 * annotations: [{at: {x}, text, value, place, dx, dy, max, anchor, phone}]: a note with a leader to the top of that
 * circle; "value": true prints the count before the text. Maker B, round 1. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'bubble-timeline',
    name: 'Bubble Timeline',
    family: 'change-over-time',
    encode: { key: 'id', x: 'time', size: 'number', complete: 'boolean?' },
    labels: ['key_title', 'key_values', 'key_unit', 'partial'],
    phone: 'same',
    draw: function (c) {
      // an outline drawn as a path, so it can take a dash
      var ring = function (x, y, r, dash) { c.path('M' + K.round(x - r) + ',' + K.round(y) + 'a' + K.round(r) + ',' + K.round(r) + ' 0 1,0 ' + K.round(2 * r) + ',0a' + K.round(r) + ',' + K.round(r) + ' 0 1,0 ' + K.round(-2 * r) + ',0', { stroke: 'subject', width: c.t('bubble-outline'), dash: dash, mark: false }); };
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width;
      var ek = c.field('key'), ex = c.field('x'), es = c.field('size'), ec = c.field('complete', false);
      var rows = c.rows.slice().sort(function (a, b) { return K.time(a[ex]) - K.time(b[ex]); });
      var vmax = Math.max.apply(null, rows.map(function (r) { return r[es] || 0; }));
      var rmax = c.t(c.phone ? 'bubble-radius-max-phone' : 'bubble-radius-max-mid'), rs = K.scale.sqrt(vmax, rmax);
      var size = c.size('label'), y = 0;
      // the size key: round sizes side by side on one baseline, each with its figure
      var kv = (L.key_values || []).filter(function (v) { return v <= vmax * 1.2; });
      if (L.key_title) { var kt = c.text(0, size, L.key_title, { role: 'label', weight: 600, max: W }); y = kt.bottom + 6; }
      if (kv.length) {
        var kr = Math.max.apply(null, kv.map(function (v) { return Math.sqrt(v / vmax) * rmax; })), kx = 0, base = y + 2 * kr;
        kv.forEach(function (v) {
          var r = Math.sqrt(v / vmax) * rmax;
          c.circle(kx + r, base - r, r, { fill: 'band', mark: false });
          c.circle(kx + r, base - r, r, { stroke: 'subject', width: c.t('bubble-outline'), mark: false });
          var words = String(L.key_unit || '{value}').replace('{value}', K.fmt(v, f.size || 'integer'));
          var tb = c.text(kx + 2 * r + 6, base - 2, words, { role: 'tick' });
          kx = tb.x + tb.w + 18;
        });
        if (L.partial && ec && rows.some(function (r) { return r[ec] === false; })) {
          var pr = Math.min(kr, 9), pw = c.measure(L.partial, 'tick');
          // the partial key goes to its own line where the row has no room left for it
          if (kx + 2 * pr + 6 + pw > W) { kx = 0; base += 2 * pr + 10; }
          ring(kx + pr, base - pr, pr, '3 2');
          var pb = c.text(kx + 2 * pr + 6, base - 2, L.partial, { role: 'tick', max: W - kx - 2 * pr - 6 });
          base = Math.max(base, pb.bottom);
        }
        y = base + 18;
      }
      // the line the circles sit on, and the time axis under it
      var ts = rows.map(function (r) { return K.time(r[ex]); }), tlo = ts[0], thi = ts[ts.length - 1];
      // the ends leave room for the largest circle at either end
      var rfirst = rs(rows[0][es] || 0), rlast = rs(rows[rows.length - 1][es] || 0), rbig = 0;
      rows.forEach(function (r) { rbig = Math.max(rbig, rs(r[es] || 0)); });
      var x0 = Math.max(4, rfirst + 1), x1 = W - Math.max(4, rlast + 1, rbig * 0.5);
      var xs = K.scale.linear([tlo, thi], [x0, x1]);
      rows.forEach(function (r) { var o = xs(K.time(r[ex])) + rs(r[es] || 0) - (W - 1); if (o > 0) x1 -= o; });
      xs = K.scale.linear([tlo, thi], [x0, x1]);
      // notes go above the circles, so the circles' line sits low enough to leave them room
      var cy = y + rmax * 2 + (c.annotations.length ? 2 * size + 24 : 8);
      c.line(0, cy, W, cy, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
      rows.forEach(function (r) {
        var v = r[es] || 0, x = xs(K.time(r[ex])), rad = rs(v);
        if (!v) { c.line(x, cy - 3, x, cy + 3, { stroke: 'context', width: c.t('line-hairline'), data: { key: r[ek], field: es, value: 0 } }); return; }
        var under = ec && r[ec] === false;
        c.circle(x, cy, rad, { fill: under ? 'surface' : 'band', data: { key: r[ek], field: es, value: v }, area_of: { value: v, max_value: vmax, max_radius: rmax } });
        if (under) ring(x, cy, rad, '3 2'); else c.circle(x, cy, rad, { stroke: 'subject', width: c.t('bubble-outline'), mark: false });
      });
      // the axis: a year at each round step, thinned to fit
      var ay = cy + rmax + c.size('tick') + 8, step = 10;
      while (xs(tlo + step) - xs(tlo) < c.measure('0000', 'tick') + 16) step *= 2;
      for (var yr = Math.ceil(tlo / step) * step; yr <= thi; yr += step) {
        var hw = c.measure(String(yr), 'tick') / 2, xx = Math.max(hw, Math.min(W - hw, xs(yr)));
        c.line(xs(yr), cy + rmax + 2, xs(yr), cy + rmax + 6, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(xx, ay, String(yr), { role: 'tick', anchor: 'middle' });
      }
      // notes with leaders to the top of their circles
      c.annotations.forEach(function (a) {
        if (c.phone && a.phone && a.phone.hide) return;
        var r = rows.filter(function (q) { return String(q[ex]) === String(a.at.x); })[0];
        if (!r) { c.warn('annotation at ' + JSON.stringify(a.at) + ' matches no row'); return; }
        var o = Object.assign({}, a, c.phone && a.phone ? a.phone : {});
        var words = a.value ? K.fmt(r[es], f.size || 'integer') + (a.text || '') : a.text;
        P.note(c, xs(K.time(r[ex])), cy - rs(r[es] || 0), words, { place: o.place || 'above', dx: o.dx, dy: o.dy, max: o.max, anchor: o.anchor, weight: a.value ? 700 : 400 });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
