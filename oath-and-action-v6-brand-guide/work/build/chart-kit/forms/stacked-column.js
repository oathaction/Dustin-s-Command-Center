/* Stacked column (coverage plan 3.4, extended; S45). One column per period from a zero line, split into up to four parts
 * stacked in a fixed order, the first on the zero line; the parts take the categorical inks in DR-236's order (Charcoal,
 * Verdigris, Prussian, then Stone, always hatched) and a key above names them. A column's total may print above it.
 * encode: x (year or category), parts (list of number columns, the first on the zero line).
 * labels: parts ([{field, label}] in the same order), totals_at (x values whose totals print above their columns),
 * total_words ('{v}' words for a printed total), x_ticks (x values to label; the kit thins them otherwise), y_head
 * (words over the value scale). formats: y_tick (the scale), total (a printed total). */
(function (K) {
  'use strict';
  var CAT = ['cat-1', 'cat-2', 'cat-3', 'cat-4'];
  K.register_chart({
    form: 'stacked-column', name: 'Stacked Column', family: 'composition',
    encode: { x: 'category', parts: 'list' },
    labels: ['parts', 'totals_at', 'total_words', 'x_ticks', 'y_head'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, ex = c.field('x'), parts = c.field('parts'), L = c.labels, f = c.spec.formats || {}, W = c.width;
      if (parts.length > 4) c.warn('more than four parts: split into small multiples (DR-234)');
      var defs = {}; (L.parts || []).forEach(function (d) { defs[d.field] = d; });
      var role = function (i) { return CAT[Math.min(i, 3)]; };
      var size = c.size('label'), tick = c.size('tick'), y = 0;
      // the key, in stacking order read from the top of a column down, so it matches what the eye meets first
      c.pattern('hatch', 'cat-4');
      y += size + 2;
      y += P.key(c, parts.map(function (p, i) {
        var hatch = role(i) === 'cat-4';
        return { label: (defs[p] || {}).label || p, fill: hatch ? null : role(i), stroke: hatch ? 'cat-4' : null, pattern: hatch ? 'hatch' : null };
      }), 0, y, W) + 8;
      var st = P.stack(c.rows, parts, { offset: 'zero' });
      var vs = P.value_scale(c, 0, st.hi, c.phone ? 4 : 5);
      if (L.y_head) { c.text(0, y + tick, L.y_head, { role: 'tick', fill: 'secondary' }); y += tick + 8; }
      var top = y + Math.round(tick * 0.6) + (L.totals_at ? size + 6 : 0), plotH = c.t(c.phone ? 'columns-phone-height' : 'columns-height'), bot = top + plotH;
      var gut = P.value_gutter(c, vs.ticks, f.y_tick || 'integer'), x0 = gut + 10, x1 = W;
      var ys = K.scale.linear([vs.lo, vs.hi], [bot, top]), n = st.length, step = (x1 - x0) / n;
      var bw = Math.max(2, Math.min(step - (c.phone ? 2 : 4), step * 0.78));
      P.value_grid(c, ys, vs.ticks, f.y_tick || 'integer', x0, x1, gut);
      var at = [].concat(L.totals_at || []).map(String);
      st.forEach(function (s, i) {
        var r = s.row, cx = x0 + step * i + step / 2;
        s.segs.forEach(function (g, j) {
          if (g.missing || g.end === g.start) return;
          var ya = ys(g.end), yb = ys(g.start), o = { kind: j ? 'segment' : 'bar', axis: 'y', zero: ys(0), data: { key: r[ex], field: g.field, value: g.value } };
          if (role(j) === 'cat-4') {
            c.rect(cx - bw / 2, ya, bw, yb - ya, Object.assign({ pattern: 'hatch' }, o));
            c.rect(cx - bw / 2 + 0.5, ya + 0.5, bw - 1, Math.max(0, yb - ya - 1), { stroke: 'cat-4', mark: false });
          } else c.rect(cx - bw / 2, ya, bw, yb - ya, Object.assign({ fill: role(j) }, o));
        });
        if (at.indexOf(String(r[ex])) >= 0) {
          var tw = String(L.total_words || '{v}').split('{v}').join(K.fmt(s.total, f.total || 'integer'));
          var hw = c.measure(tw, 'label', 700) / 2, tx = Math.max(hw, Math.min(W - hw, cx)), ty = ys(s.total);
          // over every column its words reach across, so a taller neighbor never runs into them
          st.forEach(function (o2, k) { var ox = x0 + step * k + step / 2; if (Math.abs(ox - tx) < hw + bw / 2 + 2) ty = Math.min(ty, ys(o2.total)); });
          c.text(tx, ty - 7, tw, { role: 'label', weight: 700, anchor: 'middle', tnum: true });
        }
      });
      P.zero_line(c, ys, x0, x1);
      // the time axis: the spec's picks, or every year thinned to fit
      var ay = bot + tick + 10, picks = L.x_ticks ? [].concat(L.x_ticks).map(String) : null, wmax = c.measure('0000', 'tick') + 12, every = Math.max(1, Math.ceil(wmax / step));
      while (!picks && every < n && (n - 1) % every && every < 10) every++;
      st.forEach(function (s, i) {
        var v = String(s.row[ex]);
        if (picks ? picks.indexOf(v) < 0 : (n - 1 - i) % every) return;
        var cx = x0 + step * i + step / 2, w = c.measure(v, 'tick'), tx = Math.max(w / 2, Math.min(W - w / 2, cx));
        c.line(cx, bot + 1, cx, bot + 5, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(tx, ay, K.fmt(s.row[ex], 'year'), { role: 'tick', anchor: 'middle' });
      });
      c.height(ay + 4);
    }
  });
})(globalThis.OAChart);
