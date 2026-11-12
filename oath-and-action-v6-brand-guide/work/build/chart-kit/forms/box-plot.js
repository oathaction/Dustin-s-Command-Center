/* Box plot (coverage plan 3.5, extended; S51). The spread of one measure in each of a few groups, drawn from a summary
 * (R2-2): one row a group, the group's name and count of units flush left beside its row (over it on a phone), a box from
 * the first to the third quartile with its median as a 2 px line, whiskers to the ends the summary gives (Tukey's fences,
 * as the measure line says), and each unit past them as a small open dot, read from a second dataset of outliers. The
 * median prints over its line. Every box takes the light fill with its median in the subject ink and its whiskers and
 * outliers in the context ink; a group the title names takes the subject ink for its box, whiskers and outliers, with
 * its median in the ink set on the subject (the data lead's ruling (e)). One value axis runs along the bottom, with light
 * gridlines through every row.
 * encode: category (text, the group), low (number, the lower whisker's end), q1, median, q3 (numbers), high (number, the
 * upper whisker's end), count (number, units in the group), key (code, optional).
 * labels: names ({key: printed name}), count ("{count} counties": words under each name), median ("{median}": words over
 * the median line), named (keys of groups in the subject ink, the rest in the light fill), point (the one group in the
 * red point), outliers ({dataset, category, value}: the second dataset's name and its columns for each unit past a
 * whisker), axis (words under the value axis).
 * formats: value (the median's words), tick. scale: x ([lo, hi]). On a phone the same arrangement draws narrower, the
 * name over its box. Maker B, round 2. */
(function (K) {
  'use strict';
  K.register_chart({
    form: 'box-plot',
    name: 'Box Plot',
    family: 'distribution-and-density',
    encode: { category: 'text', low: 'number', q1: 'number', median: 'number', q3: 'number', high: 'number', count: 'number', key: 'code?' },
    labels: ['names', 'count', 'median', 'named', 'point', 'outliers', 'axis'],
    phone: 'same',
    draw: function (c) {
      var P = K.parts, L = c.labels, f = c.spec.formats || {}, W = c.width, ph = c.phone;
      var ec = c.field('category'), elo = c.field('low'), e1 = c.field('q1'), em = c.field('median'), e3 = c.field('q3'), ehi = c.field('high'), en = c.field('count');
      var ek = c.field('key', false) || ec, names = L.names || {};
      var fv = f.value || 'number:1', ft = f.tick || 'integer', tick = c.size('tick'), size = c.size('label');
      var ink = P.named_fill(c, L.named, ek, 'subject', L.point);
      // the units past the whiskers, from the spec's second dataset
      var oc = L.outliers || null, outs = [];
      if (oc) {
        var ds = (c.extra || {})[oc.dataset];
        if (!ds) c.warn('labels.outliers names no second dataset: ' + oc.dataset);
        else outs = ds.filter(function (u) { return typeof u[oc.value] === 'number'; });
      }
      var vals = [];
      c.rows.forEach(function (r) { vals.push(r[elo], r[ehi]); });
      outs.forEach(function (u) { vals.push(u[oc.value]); });
      var sx = (c.spec.scale || {}).x, dom = sx || K.nice(Math.min(0, Math.min.apply(null, vals)), Math.max.apply(null, vals), ph ? 4 : 6);
      var ticks = K.ticks(dom[0], dom[1], ph ? 4 : 6);
      var name = function (r) { var k = String(r[ek]); return names[k] !== undefined ? names[k] : String(r[ec]); };
      var cnt = function (r) { return L.count ? String(L.count).replace('{count}', K.fmt(r[en], 'integer')) : ''; };
      // the names: a column at the left on a desk, over each box on a phone
      var lw = 0;
      c.rows.forEach(function (r) { lw = Math.max(lw, c.measure(name(r), 'label', 700), L.count ? c.measure(cnt(r), 'tick') : 0); });
      var x0 = ph ? 0 : Math.ceil(lw + 24), x1 = W - 8, pad = 4;
      var xs = K.scale.linear([dom[0], dom[1]], [x0 + pad, x1 - pad]);
      var bh = ph ? 26 : 30, head = ph ? (L.count ? size + tick + 12 : size + 8) : 0;
      var pitch = bh + head + (ph ? 22 : 28), top = 6, bottom = top + c.rows.length * pitch - (ph ? 12 : 16);
      ticks.forEach(function (t) { c.line(xs(t), top, xs(t), bottom, { stroke: 'gridline', width: c.t('line-hairline'), mark: false }); });
      c.rows.forEach(function (r, i) {
        var role = ink(r), b = ink.named && ink.is_named(r) || ink.is_point(r), y0 = top + i * pitch + head, cy = y0 + bh / 2, k = r[ek];
        // the group's name and its count of units
        if (ph) {
          c.text(0, top + i * pitch + size, name(r), { role: 'label', weight: b ? 700 : 600 });
          if (L.count) c.text(0, top + i * pitch + size + tick + 4, cnt(r), { role: 'tick' });
        } else {
          c.text(0, cy + (L.count ? -2 : size * 0.35), name(r), { role: 'label', weight: b ? 700 : 600 });
          if (L.count) c.text(0, cy + tick + 2, cnt(r), { role: 'tick' });
        }
        // the named group's box in the subject ink, its median, whiskers and outliers in ink with it; every other box in the
        // light fill with its median as a 2 px line in the subject ink and its whiskers and outliers in the context ink
        // (the data lead's ruling (e))
        var lit = role === 'subject' || role === 'point', wst = lit ? 'subject' : 'context', cap = bh * 0.3;
        [[elo, e1], [e3, ehi]].forEach(function (pr, j) {
          var a = xs(r[pr[0]]), z = xs(r[pr[1]]);
          c.line(a, cy, z, cy, { stroke: wst, width: c.t('line-context'), mark: false });
          var ex = j ? z : a;
          c.line(ex, cy - cap, ex, cy + cap, { stroke: wst, width: c.t('line-context'), data: { key: k, field: j ? ehi : elo, value: r[j ? ehi : elo] } });
        });
        var bx = xs(r[e1]), bw = xs(r[e3]) - bx;
        c.rect(bx, y0, bw, bh, Object.assign({ fill: role, data: { key: k, field: e1, value: r[e1] } }, ink.keyline(r)));
        c.datum(xs(r[e3]), cy, { data: { key: k, field: e3, value: r[e3] } });
        var mx = xs(r[em]), mlw = c.t('line-context');
        c.rect(K.snap(mx, 2) - mlw / 2, y0, mlw, bh, { fill: lit ? 'label-on-subject' : 'subject', data: { key: k, field: em, value: r[em] } });
        if (L.median) {
          var words = String(L.median).replace('{median}', K.fmt(r[em], fv)), mw = c.measure(words, 'tick', b ? 700 : 600);
          c.text(Math.min(Math.max(mx, x0 + mw / 2), W - mw / 2), y0 - 7, words, { role: 'tick', weight: b ? 700 : 600, anchor: 'middle', fill: 'label' });
        }
        // the units past the whiskers, small open dots on the row's line
        if (oc) outs.filter(function (u) { return String(u[oc.category]) === String(r[ec]) || String(u[oc.category]) === String(k); }).forEach(function (u) {
          c.circle(xs(u[oc.value]), cy, 3, { fill: 'surface', data: { key: String(k) + '|' + u[oc.value], field: oc.value, value: u[oc.value] } });
          c.circle(xs(u[oc.value]), cy, 3, { stroke: wst, width: c.t('line-hairline') + 0.5, mark: false });
        });
      });
      // the value axis along the bottom
      var ay = bottom + tick + 8;
      ticks.forEach(function (t) {
        c.line(xs(t), bottom, xs(t), bottom + 4, { stroke: 'baseline', width: c.t('line-hairline'), mark: false });
        c.text(xs(t), ay, K.fmt(t, ft), { role: 'tick', anchor: 'middle' });
      });
      var end = ay + 4;
      if (L.axis) { var ab = c.text(x0, ay + tick + 10, L.axis, { role: 'tick', weight: 600, max: W - x0 }); end = ab.bottom; }
      c.height(end + 2);
    }
  });
})(globalThis.OAChart);
